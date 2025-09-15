import React, { useState } from 'react'
import Alert from '../../../shared/components/Alert.jsx'

export default function InputForm({ onSubmit, disabled }) {
  const [textA, setTextA] = useState('')
  const [multi, setMulti] = useState('')
  const [error, setError] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    setError('')
    const a = textA.trim()
    const arr = multi.split(/\r?\n|,/).map(s => s.trim()).filter(Boolean)
    if (!a) { setError('שדה א חייב להיות מלא'); return }
    if (arr.length === 0) { setError('שדה ב חייב לכלול לפחות טקסט אחד'); return }
    onSubmit({ text: a, texts: arr })
  }

  return (
    <form className="card" onSubmit={handleSubmit}>
      <div className="row cols-2">
        <div>
          <label>שדה טקסט (A)</label>
          <input type="text" value={textA} onChange={e => setTextA(e.target.value)} placeholder="טקסט בודד..." />
        </div>
        <div>
          <label>שדה עם כמה טקסטים (B) — שורה לכל טקסט או פסיק</label>
          <textarea value={multi} onChange={e => setMulti(e.target.value)} placeholder="טקסט 1\nטקסט 2\nטקסט 3"></textarea>
        </div>
      </div>
      <div className="spacer"></div>
      {error && <Alert type="error">{error}</Alert>}
      <div style={{display:'flex', gap: 8, justifyContent:'flex-start', marginTop: 10}}>
        <button className="btn primary" type="submit" disabled={disabled}>שלח לעיבוד</button>
      </div>
    </form>
  )
}