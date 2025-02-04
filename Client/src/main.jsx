// !important imports
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'

//pages
import Homepage from './pages/Homepage'
import NotFoundPage from './pages/NotFoundPage'
import GalleryPage from './pages/GalleryPage'
import MainDemoPage from './pages/MainDemoPage'


const router = createBrowserRouter([
  {path: '/', element: <Homepage />, errorElement: <NotFoundPage />}, 
  {path: '/gallery', element: <GalleryPage />}, 
  {path: '/demo', element: <MainDemoPage />}
])


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
