import React from 'react'
import { Link } from 'react-router-dom'

function NotFoundPage() {
  return (
    <>
      <h1>404 Error!</h1>
      <h4>Page Not Found :(</h4>
      <Link to="/">Go back to home</Link>
    </>
  )
}

export default NotFoundPage