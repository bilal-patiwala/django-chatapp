import React, { useContext } from "react";
import ChatContext from "../context/ChatContext";
import styles from "../styles/lobby.module.css";
import "../App.css";
import { ReactComponent as User } from "../assets/user.svg";
import { ReactComponent as Chat } from "../assets/chat.svg";
const Room = () => {
  let { receiver } = useContext(ChatContext);
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
        <input type="text" className="w-4/5 bg-[#16181D] p-2 rounded-md ml-2 mr-2 focus:outline-none font-AlbertSans" placeholder="type your message here"/>
        <button className="w-1/5 mr-2 bg-[#16181D] p-2 rounded-md ">send</button>
      </div>
    </div>
  ) : (
    <div className={styles['chat']} >
      <Chat />
    </div>
  );
};

export default Room;
