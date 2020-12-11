from datetime import datetime, timedelta

import redis
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from core.models import APIKey
from video.models import Video

logger = get_task_logger(__name__)


def yt_search(api_key, query, max_results, published_after, next_token):
    """
    fetch videos from youtube api
    """
    youtube = build(settings.YOUTUBE_API_SERVICE_NAME,
                    settings.YOUTUBE_API_VERSION,
                    developerKey=api_key,
                    cache_discovery=False, )

    try:
        search_response = youtube.search().list(
            q=query,
            type='video',
            order='date',
            part='snippet',
            publishedAfter=published_after,
            maxResults=max_results,
            pageToken=next_token,
        ).execute()
        return search_response
    except HttpError as e:
        raise e


def save_video(results):
    """
    save the response from the API to the database
    """
    for res in results['items']:

        # if video already exist then continue
        check = Video.objects.filter(yt_id=res['id']['videoId'])
        if check.exists():
            continue

        Video.objects.create(
            yt_id=res['id']['videoId'],
            title=res['snippet']['title'],
            description=res['snippet']['description'],
            thumbnail_url=res['snippet']['thumbnails']['high']['url'],
            published_at=res['snippet']['publishedAt']
        )


@shared_task()
def sync_with_youtube():
    """
    Periodic Task that will fetch new videos from the youtube and will save
    them in the database
    """
    r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

    # if there are no videos in db, then the service will start fetching videos
    # 10 minutes before the current time
    published_after = datetime.utcnow() - timedelta(minutes=10)

    max_results = 50
    next_token = None

    # fetching all API keys from the database
    api_keys = APIKey.objects.all()

    # if no api keys are present exit
    if not api_keys.exists():
        logger.error("No API Key present in the database")
        return

    # checking if the value exists in redis, else set it
    if not r.exists('current_api_key_no'):
        r.set('current_api_key_no', str(0))

    current_api_key = api_keys[int(r.get('current_api_key_no'))].key

    videos = Video.objects.all().order_by('-published_at')

    # if there are videos in database,
    # then service will fetch videos after that time
    if videos.exists():
        published_after = videos.first().published_at.replace(tzinfo=None)

    published_after_rfc399 = published_after.isoformat("T") + "Z"

    # Iterate through all the pages of the Youtube API and save videos in db
    while True:
        try:
            results = yt_search(
                current_api_key,
                'football',
                max_results,
                published_after_rfc399,
                next_token
            )

            if len(results['items']) == 0:
                return

            # see if we have nextToken
            if 'nextPageToken' in results:
                next_token = results['nextPageToken']
            else:
                break
            # save the results into the database
            save_video(results)
        except HttpError as e:
            if e.resp['status'] == '403':
                logger.warning('Current API key expired, try next API key')
                # try next api key0
                total_keys = api_keys.count()
                current_api_key_no = int(r.get('current_api_key_no'))
                r.set('current_api_key_no',
                      str((current_api_key_no + 1) % total_keys))
                current_api_key = api_keys[current_api_key_no + 1].key
                return
            # if any other error
            logger.error('Unknown Error Occurred')
