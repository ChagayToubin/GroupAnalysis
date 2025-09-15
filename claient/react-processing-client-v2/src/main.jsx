import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './styles.css'


// יצירת ה"אוביקט" להשתיל את כל הדף
const root = createRoot(document.getElementById('root'))

// השתלה של APP
root.render(<App />)
