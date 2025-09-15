import React, { useState } from 'react'
import Alert from '../../../shared/components/Alert.jsx'

export default function IdentifierForm({ onConnect, disabled }) {
  const [id, setId] = useState('')
  const [error, setError] = useState('')

  function submit(e) {
    e.preventDefault()
    setError('')
    const v = id.trim()
    if (!v) { setError('המזהה חובה'); return }
    onConnect(v)
  }

  return (
    <form className="card" onSubmit={submit}>
      <div className="row cols-2">
        <div>
          <label>מזהה (יכול להיות URL או שם קבוצה)</label>
          <input
            type="text"
            value={id}
            onChange={e => setId(e.target.value)}
            placeholder="לדוגמה: https://example.com/path או TeamAlpha"
          />
        </div>
        <div style={{display:'flex', alignItems:'end'}}>
          <button className="btn primary" type="submit" disabled={disabled}>
            התחבר
          </button>
        </div>
      </div>

      {error && <div className="spacer" />}
      {error && <Alert type="error">{error}</Alert>}
    </form>
  )
}
