import React, { useContext, useState } from "react";
import ChatContext from "../context/ChatContext";
import styles from "../styles/lobby.module.css";
import "../App.css";
import { ReactComponent as User } from "../assets/user.svg";
import { ReactComponent as Chat } from "../assets/chat.svg";
import AuthContext from "../context/AuthContext";

const Room = () => {
  let { receiver } = useContext(ChatContext);
  let {user} = useContext(AuthContext)
  let [message, setMessage] = useState('')

  const messageHandler = (event) => {
    setMessage(event.target.value)
  }
  

  const messageSubmit = (event) => {
    let chatSocket = new WebSocket(
      "ws://" + "127.0.0.1:8000" + "/ws/chat/" + receiver + "/"
    );
    
    chatSocket.onopen = async (event) => {
      console.log("Connection open", event);
    };
  
    chatSocket.onmessage = async (event) => {
      console.log("Message", event);
      let data = JSON.parse(event.data)
      let response = JSON.parse(data.text)
      let message = response
      // document.querySelector('#chat-log').value += ('[' + message.sender + ']:' + message.message + '\n');
    };
  
    chatSocket.onclose = async (event) => {
      console.log("close", event);
    };
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

      {/* footer */}
      <div className="w-full flex absolute bottom-0 mb-2">
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
