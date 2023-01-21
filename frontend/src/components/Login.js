import React, { useState } from "react";
import styles from "../styles/login.module.css";
import "../App.css";
import { Navigate, useNavigate } from "react-router-dom";
const Login = () => {
  const [username, setUsername] = useState('');
  const [Password, setPassword] = useState("");
  let navigate = useNavigate()
  
  const usernameHandler = (event) => {
    setUsername(event.target.value)
  }
  const passwordHandler = (event) => {
    setPassword(event.target.value)
  }

  const loginFormSubmit = () => {
    
  }

  return (
    <div className="grid justify-center items-center h-screen">
      <div className="flex-row space-y-4">
        <h1 className="text-2xl text-center">Chat App</h1>
        <div className="flex-row bg-[#343A46] p-10 rounded-md">
          <h3 className="text-2xl text-center mb-6">Login</h3>
          <form className="flex flex-col space-y-6 mb-6" onSubmit={loginFormSubmit}>
            <input type='text' placeholder="Username" value={username} className="bg-transparent border-b focus:outline-none " onChange={usernameHandler} />
            <input type='Password' placeholder="Password" className="bg-transparent border-b focus:outline-none" value={Password} onChange={passwordHandler}/>
            <button type="submit" className={styles['login-btn']}>Login</button>
          </form>
          <a className="cursor-pointer opacity-40" onClick={(event) => {navigate('/signup')}} target="_blank">Don't have an account? Register</a>
        </div>
      </div>
    </div>
  );
};

export default Login;
