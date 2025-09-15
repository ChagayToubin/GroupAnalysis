import React from 'react'
import ProcessingPage from './features/processing/pages/ProcessingPage.jsx'

export default function App() {
  return (
    <div className="container">
      <header className="header">
        <h1>מערכת עיבוד — צד לקוח</h1>
        <p className="subtitle">בלי אימות • שליחה ידנית • הצגת סטטוס/תוצאות</p>
      </header>
      <ProcessingPage />
      <footer className="footer">
        <small>© 2025</small>
      </footer>
    </div>
  )
}