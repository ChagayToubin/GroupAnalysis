import React from 'react'
import ProcessingPage from './features/processing/pages/ProcessingPage.jsx'

export default function App() {
  return (
    <div className="container">
      <header className="header">
        <h1>מערכת עיבוד — צד לקוח (V2)</h1>
        <p className="subtitle">בהמשך אני אוסיף פה הסבר בלא בלא בלא</p>
      </header>

      <ProcessingPage />

      <footer className="footer">
        <small>winners group © 2025</small>
      </footer>
    </div>
  )
}
