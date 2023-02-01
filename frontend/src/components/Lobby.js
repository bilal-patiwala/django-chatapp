import React, { useContext, useEffect, useState } from "react";
import styles from "../styles/lobby.module.css";
import { ReactComponent as User } from "../assets/user.svg";
import {ReactComponent as Search} from '../assets/search.svg'
import ChatContext from "../context/ChatContext";
import AuthContext from "../context/AuthContext";
const Lobby = () => {
    let {user, authToken} = useContext(AuthContext)
    let [search, setSearch] = useState('');
    let [searchedUser, setSearchedUser] = useState([])
    let {selectedUser} = useContext(ChatContext)
    useEffect(() => {
        
        if(search !== ''){
            searching()
        }
        else{
            setSearchedUser([])
        }
    },[search])

    const searching = async () => {
        let response = await fetch(`http://127.0.0.1:8000/searchUser/${search}`,{
            method:'GET',
            headers:{
              'Authorization':`Bearer ${localStorage.getItem('authToken')}`,
            }
        })

        let data = await response.json()
        setSearchedUser(data)
        console.log(searchedUser);
    }

    const handleSearch = (event) => {
        setSearch(event.target.value)
    }

    const selectButton = (event) => {
      selectedUser(event)
      setSearch("")
      setSearchedUser([])
    }

  return (
    <div className="w-1/4 border-r-2 h-screen border-[#374151] ">
      {/* header */}
      <div className={styles["header"]}>
        <div className="flex items-center">
          <User className={styles["user-image"]} />
          <h1 className="text-center w-3/4 text-2xl font-AlbertSans">
            Chat App
          </h1>
        </div>
      </div>

      {/* searchbar */}

      <div className="m-4">
        <div className="flex p-2 space-x-2 rounded-md bg-[#16181D] items-center searchbar">
            <Search className={styles['search-icon']}/>
            <input type='text' className="bg-transparent w-full focus:outline-none" value={search} placeholder="Search" onChange={handleSearch}/>
        </div>
      </div>

      <div className={styles['for-search']}>
        {searchedUser.map((user,index) => (
            <button value={user.username} key={index} className='border-b-2 border-[#374151] text-xl p-2' onClick={selectButton}>{user.username}</button>
        ))}
      </div>

      {/* Chats */}
      <div className="m-4">
        <h1 className="text-xl ml-2">Chats</h1>
      </div>
    </div>
  );
};

export default Lobby;
