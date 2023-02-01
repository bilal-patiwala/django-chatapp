import { createContext, useContext, useState } from "react";
import AuthContext from "./AuthContext";

const ChatContext = createContext()

export const ChatProvider = ({children}) => {
    let {user, authToken} = useContext(AuthContext)
    let [receiver, setReceiver] = useState('')
    let [sender, setSender] = useState('')
    let [thread_id, setThreadid] = useState("")
    const selectedUser = async (event) => {
        event.preventDefault()
        setReceiver(event.target.value)
        console.log(authToken.access);
        let response = await fetch(`http://127.0.0.1:8000/getThread/${event.target.value}/`, {
            method:"GET",
            headers:{
                'Authorization':`Bearer ${authToken.refresh}`,
            }
        })
        let data = await response.json()
        console.log(data);
        setSender(data.sender)
        setThreadid(data.id)
        console.log(data.sender + " " + data.receiver + " " + data.id);
    }
    let contextData = {
        sender:sender,
        thread_id:thread_id,
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