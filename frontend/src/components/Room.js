import React, { useContext, useEffect, useRef, useState } from "react";
import ChatContext from "../context/ChatContext";
import styles from "../styles/lobby.module.css";
import "../App.css";
import { ReactComponent as User } from "../assets/user.svg";
import { ReactComponent as Chat } from "../assets/chat.svg";
import AuthContext from "../context/AuthContext";

const Room = () => {


  let { receiver, sender, thread_id } = useContext(ChatContext);
  let {user, authToken} = useContext(AuthContext)
  console.log(user);
  let [message, setMessage] = useState('')
  let [allMessages, setAllMessages] = useState([])
  let [currentMessage, setCurrentMessages] = useState([])
  let messageScroller = useRef(null)

  const scrollBottom = () => {
    messageScroller.current?.scrollIntoView({ bottom:'scrollHeight',behavior: "smooth" })
  }

  const messageHandler = (event) => {
    setMessage(event.target.value)
  }

  let ws = null
  let chatSocket = null
  if(receiver){
    ws = `ws://127.0.0.1:8000/ws/chat/${receiver}/?token=${authToken.refresh}`
    chatSocket = new WebSocket(ws);
    chatSocket.onopen = async (event) => {
      console.log("Connection open", event);
    };
    chatSocket.onmessage = async (event) => {
      console.log("Message", event);
      let data = await JSON.parse(event.data)
      let response = await JSON.parse(data.text)
      let message1 = response
      // document.querySelector('#chat-log').value += ('[' + message.sender + ']:' + message.message + '\n');
      console.log(message1.sender + " " + message1.message);
      console.log(message1);
      setCurrentMessages(message1)
      scrollBottom()
    };
  }
  
  useEffect( () => {
    if(receiver){
      getMessage()
      
    }
  },[receiver,currentMessage])
  
  const getMessage = async () => {
    let response = await fetch("http://127.0.0.1:8000/getMessages/", {
      method:"GET",
      headers:{
        'Authorization':`Bearer ${authToken.refresh}`,
      }
    })
    let ddata = await response.json()
    console.log(ddata);
    setAllMessages(ddata)
  }

  // if(chatSocket === null){
  //   chatSocket.onclose = async (event) => {
  //     console.log("close", event);
  //   };
  // }
  
  console.log(user.username + " " + currentMessage.sender);
  const messageSubmit = (event) => {
    let data = {
      message: message, 
      'sender':sender,
      'receiver':receiver,
      'thread_id':thread_id
    };
    data = JSON.stringify(data);
    chatSocket.send(data);
    setMessage('')
    scrollBottom()
  }
  return receiver ? (
    <div className="relative w-3/4">
      {/* header */}
      <div className={styles["header"]}>
        <div className="flex items-center">
          <User className={styles["user-image"]} />
          <h1 className="ml-2 w-3/4 text-2xl font-AlbertSans">{receiver}</h1>
        </div>
      </div>

      {/* chat log */}
      
      <div className={styles['chat-log']}>
        {
          allMessages.map((message, index) => (
            message.user === user.user_id ? (
              <p key={index} className={styles['sender-logs']}>
                {message.message} 
              </p>
            ) : (
              <p key={index} className={styles['receive-logs']}>{message.message}</p>
            )
          ))
        }
        <div ref={messageScroller}></div>
      </div>

      {/* footer */}
      <div className={styles['footer']}>
        <input type="text" className="w-4/5 bg-[#16181D] p-2 rounded-md ml-2 mr-2 focus:outline-none font-AlbertSans" placeholder="type your message here" value={message} onChange={messageHandler} />
        <button className="w-1/5 mr-2 bg-[#16181D] p-2 rounded-md " onClick={messageSubmit}>send</button>
      </div>

    </div>
    ) : (
      <div className={styles['chat']} >
        <Chat />
      </div>
    );
};

export default Room;
