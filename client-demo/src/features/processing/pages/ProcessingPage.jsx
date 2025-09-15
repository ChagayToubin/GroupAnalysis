import React, { useEffect, useState } from 'react'
import InputForm from '../components/InputForm.jsx'
import ResultActions from '../components/ResultActions.jsx'
import Chart from '../components/Chart.jsx'
import Spinner from '../../../shared/components/Spinner.jsx'
import Alert from '../../../shared/components/Alert.jsx'
import { startProcess, getStatus } from '../../../app/api.js'
import { saveRequestId, loadRequestId, clearRequestId } from '../../../app/storage.js'

export default function ProcessingPage() {
  const [requestId, setRequestId] = useState('')
  const [status, setStatus] = useState('idle') // idle | submitted | processing | ready | error
  const [progress, setProgress] = useState(null)
  const [results, setResults] = useState(null)
  const [message, setMessage] = useState('')

  useEffect(() => {
    const existing = loadRequestId()
    if (existing) {
      setRequestId(existing)
      setStatus('submitted')
    }
  }, [])

  async function handleSubmit(payload) {
    setMessage('')
    setResults(null)
    setProgress(null)
    setStatus('submitted')
    try {
      const data = await startProcess(payload)
      // Expecting: { requestId, status: 'queued' | 'processing' }
      setRequestId(data.requestId)
      saveRequestId(data.requestId)
      setStatus(data.status === 'processing' ? 'processing' : 'submitted')
      setMessage('הבקשה התקבלה ומעובדת')
    } catch (err) {
      setStatus('error')
      setMessage(err?.message || 'שגיאה בשליחה')
    }
  }

  async function handleCheck() {
    if (!requestId) return
    setMessage('')
    try {
      const data = await getStatus(requestId)
      // processing
      if (data.status === 'processing' || data.status === 'queued') {
        setStatus('processing')
        setProgress(typeof data.progress === 'number' ? data.progress : null)
        setResults(null)
        setMessage('עדיין בעיבוד...')
        return
      }
      // ready
      if (data.status === 'ready') {
        setStatus('ready')
        setProgress(null)
        setResults(data.results || null)
        setMessage('מוכן!')
        return
      }
      // error
      if (data.status === 'error') {
        setStatus('error')
        setProgress(null)
        setResults(null)
        setMessage(data.message || 'העיבוד נכשל')
        return
      }
      // unknown
      setStatus('error')
      setMessage('סטטוס לא מוכר מהשרת')
    } catch (err) {
      setStatus('error')
      setMessage(err?.message || 'שגיאה בבדיקת הסטטוס')
    }
  }

  function handleReset() {
    clearRequestId()
    setRequestId('')
    setStatus('idle')
    setProgress(null)
    setResults(null)
    setMessage('')
  }

  return (
    <div className="grid">
      <InputForm onSubmit={handleSubmit} disabled={status==='processing'} />

      <div className="card">
        <div style={{display:'flex', gap:8, alignItems:'center', justifyContent:'space-between', flexWrap:'wrap'}}>
          <div>
            <strong>API Base:</strong> <span className="muted">{import.meta.env.VITE_API_BASE || '(same origin)'}</span>
          </div>
          <div style={{display:'flex', gap:8}}>
            <button className="btn" onClick={handleCheck} disabled={!requestId}>הצג תוצאות</button>
            <button className="btn danger" onClick={handleReset}>איפוס מזהה</button>
          </div>
        </div>
        <div className="spacer"></div>
        <ResultActions onCheck={handleCheck} requestId={requestId} status={status} />
        {status === 'processing' && <Spinner label={progress != null ? `מחשב... ${progress}%` : 'מחשב...'} />}
        {message && <div style={{marginTop:10}}><Alert type={status==='error'?'error':(status==='ready'?'success':'info')}>{message}</Alert></div>}
      </div>

      <div>
        {status === 'ready' && results?.metrics && <Chart metrics={results.metrics} />}
      </div>
    </div>
  )
}