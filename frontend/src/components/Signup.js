import React, { useContext, useState } from 'react'
import styles from "../styles/signup.module.css";
import "../App.css";
import { Navigate, useNavigate } from "react-router-dom";
import AuthContext from '../context/AuthContext';
const Signup = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    let navigate = useNavigate()
    let {signupUser,user} = useContext(AuthContext)
    
    const usernameHandler = (event) => {
        setUsername(event.target.value)
    }
    const passwordHandler = (event) => {
        setPassword(event.target.value)
    }
    const emailHandler = (event) => {
        setEmail(event.target.value)
    }
    const confirmPasswordHandler = (event) => {
        setConfirmPassword(event.target.value)
    }

    const signupFormHandler = (event) => {
        if(username != '' && email!='' && password != '' && confirmPassword != ''){
            if(password === confirmPassword){
                signupUser(event)
            }
            else{
                alert("password not matched")
            }
        }
        else{
            alert("Enter credetials")
        }
    }

  return (
    user ? <Navigate to="/"/> :
    <div className='grid justify-center items-center h-screen'>
        <div className='flex-row space-y-4'>
            <h1 className='text-center text-3xl'>Chat App</h1>
            <div className='flex-row bg-[#343A46] p-10 w-96 rounded-md'>
                <h3 className='text-center text-2xl mb-6'>Sign Up</h3>
                <form className='flex flex-col space-y-6 mb-6' onSubmit={signupFormHandler}>
                    <input type='text' placeholder="Username" name='username' value={username} className="bg-transparent border-b focus:outline-none " onChange={usernameHandler} />
                    <input type='Email' placeholder="Email" name="email" value={email} className="bg-transparent border-b focus:outline-none " onChange={emailHandler} />
                    <input type='password' placeholder="Password" name='password' value={password} className="bg-transparent border-b focus:outline-none " onChange={passwordHandler} />
                    <input type='password' placeholder="Confirm Password" name='confirmpassword' className="bg-transparent border-b focus:outline-none" value={confirmPassword} onChange={confirmPasswordHandler}/>
                    <button type="submit" className={styles['signup-btn']}>Sign-Up</button>
                </form>
                <a className="text-center cursor-pointer opacity-40" onClick={(event) => {navigate('/login')}} target="_blank">have an account? Login</a>
            </div>
        </div>
    </div>
  )
}

export default Signup