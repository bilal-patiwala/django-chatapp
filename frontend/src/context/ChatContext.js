import { createContext, useContext, useState } from "react";
import AuthContext from "./AuthContext";

const ChatContext = createContext()

export const ChatProvider = ({children}) => {
    let {user, authToken} = useContext(AuthContext)
    let [receiver, setReceiver] = useState('')
    const selectedUser = async (event) => {
        event.preventDefault()
        setReceiver(event.target.value)
        console.log(authToken.access);
        let response = await fetch(`http://127.0.0.1:8000/getThread/${event.target.value}/`, {
            method:"GET",
            headers:{
                'AUTHORIZATION':`Bearer ${authToken.access}}`,
            }
        })
        let data = await response.json()
        console.log(data);
    }
    let contextData = {
        receiver:receiver,
        selectedUser:selectedUser
    }
    return(
        <ChatContext.Provider value={contextData}>
            {children}
        </ChatContext.Provider>
    )
}

export default ChatContext