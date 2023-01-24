import { createContext, useEffect, useState } from "react";
import jwt_decode from 'jwt-decode'
import { useNavigate } from "react-router-dom";
const AuthContext = createContext("")

export default AuthContext

export const AuthProvider = ({children}) => {
    let [authToken, setAuthToken] = useState(()=> localStorage.getItem('authToken') ? JSON.parse(localStorage.getItem('authToken')) : null)
    let  [user, setUser] = useState(()=> localStorage.getItem('authToken') ? jwt_decode(localStorage.getItem('authToken')) : null)
    let navigate = useNavigate()
    let [loading, setLoading] = useState(true)

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
          const cookies = document.cookie.split(";");
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=") {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      }
    
      const csrftoken = getCookie("csrftoken");

    let loginUser = async (event) => {
        event.preventDefault()
        let response = await fetch("http://127.0.0.1:8000/token/",{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken
            },
            body: JSON.stringify({'username':event.target.username.value, 'password':event.target.password.value})
        })

        let data = await response.json()
        if (response.status === 200){
            setAuthToken(data)
            setUser(jwt_decode(data.access))
            localStorage.setItem('authToken', JSON.stringify(data))
            navigate('/')
        }
        else{
            alert("something went wrong")
        }
    }

    const signupUser = async (event) => {
        event.preventDefault()
        await fetch('http://127.0.0.1:8000/register/', {
            method:"POST",
            headers: {
                'X-CSRFToken':csrftoken,
                'Content-Type':"application/json",
            },
            body: JSON.stringify({username:event.target.username.value, email:event.target.email.value, password:event.target.password.value})
        })
        console.log("user signuped");
        let response = await fetch("http://127.0.0.1:8000/token/",{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken
            },
            body: JSON.stringify({username:event.target.username.value, password:event.target.password.value})
        })
        let data = await response.json()
        if(response.status === 200){
            setAuthToken(data)
            // to run or to access below jwt function you have to npm install jwt-decode
            setUser(jwt_decode(data.access))
            localStorage.setItem('authToken', JSON.stringify(data))
            navigate("/");
        }
        else{
            alert('Something went wrong!')
        }
    }

    let logout = () =>{
        setAuthToken(null)
        setUser(null)
        localStorage.removeItem('authToken')
        navigate('/login')
    }

    let updateToken = async () => {

        let response = await fetch('http://127.0.0.1:8000/token/refresh/', {
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify({'refresh':authToken?.refresh})
        })

        let data = await response.json()
        if(response.status === 200){
            setAuthToken(data)
            setUser(jwt_decode(data.access))
            localStorage.setItem('authToken', JSON.stringify(data))
        }
        else{
            console.log("something gone wrong");
            logout()
        }

        if(loading){
            setLoading(false)
        }
    }

    useEffect(() => {
        let fourminutes = 1000*60*4
        let interval = setInterval(() => {
            if(authToken){
                updateToken()
            }
        },fourminutes)
        return ()=> clearInterval(interval)
    },[authToken, loading])

    let contextData= {
        user:user,
        loginUser:loginUser,
        logout:logout,
        signupUser:signupUser
    }
    return(
        <AuthContext.Provider value={contextData}>
             {children}
        </AuthContext.Provider>
    )
}