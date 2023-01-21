import React, { useContext } from 'react'
import AuthContext from '../context/AuthContext'
import '../App.css'

const Home = () => {
  let {user, logout} = useContext(AuthContext)
  return (
    <div>Home {user.username}
      <p className='cursor-pointer text-2xl' onClick={logout}>logout</p>
    </div>
  )
}

export default Home