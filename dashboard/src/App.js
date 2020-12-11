import React, {useEffect,useState} from "react";
import {Table, Space, Button} from 'antd'
import axios from 'axios'
import "./App.less";
import YouTube from 'react-youtube';



const App = () => {
  const columns = [
    {
      title: 'Preview',
      dataIndex: 'yt_id',
      key: 'yt_id',
      render: value =>(
        <YouTube videoId={value}/>
        )
    },
    {
      title: 'Title',
      dataIndex: 'title',
      key: 'title',
      sorter: (a, b) => a.title.localeCompare(b.title),
        sortDirections: ['descend', 'ascend']
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
    }
    ,
    {
      title: 'Published At',
      dataIndex: 'published_at',
      key: 'published_at',
      sorter: (a, b) => a.published_at.localeCompare(b.published_at),
      sortDirections: ['descend', 'ascend']
    }
  ];

  const [isLoading, setIsLoading] = useState(true)
  const [nextPage, setNextPage] = useState(null)
  const [prevPage, setPrevPage] = useState(null)
  const [data, setData] = useState({})

  const fetchData = (url)=>{

    setIsLoading(true)
    axios.get(url).then((res)=>{
      setData(res.data)
      if(res.data.next)
        setNextPage(res.data.next)
      if(res.data.previous)
        setPrevPage(res.data.previous)
    })
    .then(()=>{
      setIsLoading(false)
    })
  }

  useEffect(()=>{
    fetchData('http://127.0.0.1:8000')
  },[] )

  return(
    <div>
      <Space className='app' align="center">
        {/* <Button onClick={()=>fetchData(nextPage)} disabled={prevPage===null} type='primary' size='large'>Previous Page</Button>  
        <Button onClick={()=>fetchData(prevPage)} disabled={nextPage===null} type='primary' size='large'>Next Page</Button>   */}
        
      </Space>
      <Table columns={columns} dataSource={data.results} loading={isLoading}/>
    </div>  
  )

}

export default App;
