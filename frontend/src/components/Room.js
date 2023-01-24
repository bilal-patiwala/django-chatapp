import React, { useContext } from 'react'
import ChatContext from '../context/ChatContext'

const Room = () => {
    let {receiver} = useContext(ChatContext)
  return (
    <div className='w-3/4'>
        <h1>{receiver}</h1>
    </div>
  )
}

export default Room