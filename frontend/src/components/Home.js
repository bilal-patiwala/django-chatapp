import React, { useContext } from "react";
import AuthContext from "../context/AuthContext";
import "../App.css";
import { ChatProvider } from "../context/ChatContext";
import Lobby from "./Lobby";
import Room from "./Room";

const Home = () => {
  let { user, logout } = useContext(AuthContext);
  return (
    <ChatProvider>
      <div className="flex ">
        <Lobby/>
        <Room />
      </div>
    </ChatProvider>

    // <div>Home {user.username}
    // <p className='cursor-pointer text-2xl' onClick={logout}>logout</p>
    // </div>
  );
};

export default Home;
