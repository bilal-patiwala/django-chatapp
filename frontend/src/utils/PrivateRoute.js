import React from 'react'
import { Navigate, Outlet } from 'react-router-dom'

export const PrivateRoute = () => {
  return (
        false ? <Outlet/> : <Navigate to='login'/>
    )
}
