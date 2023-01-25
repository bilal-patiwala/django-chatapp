import { createContext, useState } from "react";

const ChatContext = createContext()

export const ChatProvider = ({children}) => {
    let [receiver, setReceiver] = useState('')
    const selectedUser = (event) => {
        event.preventDefault()
        setReceiver(event.target.value)
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