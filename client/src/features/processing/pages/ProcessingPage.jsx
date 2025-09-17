import React, { useEffect, useRef, useState } from 'react'
import IdentifierForm from '../components/IdentifierForm.jsx'
import ResultActions from '../components/ResultActions.jsx'
import Chart from '../components/Chart.jsx'
import Spinner from '../../../shared/components/Spinner.jsx'
import Alert from '../../../shared/components/Alert.jsx'
import { getSnapshot , getInformation} from '../../../app/api.js'
import {
  saveIdentifier, loadIdentifier, clearIdentifier,
  saveAutoRefresh, loadAutoRefresh,
  saveIntervalSec, loadIntervalSec
} from '../../../app/storage.js'

export default function ProcessingPage() {
  const [identifier, setIdentifier] = useState('')
  const [status, setStatus] = useState('idle') // 'idle' | 'connected' | 'error'
  const [data, setData] = useState(null)
  const [lastUpdated, setLastUpdated] = useState(null)
  const [message, setMessage] = useState('')

  const [autoRefreshEnabled, setAutoRefreshEnabled] = useState(false)
  const [intervalSec, setIntervalSec] = useState(5)
  const [isFetching, setIsFetching] = useState(false)

  const timerRef = useRef(null)

  useEffect(() => {
    const id = loadIdentifier()
    const autoR = loadAutoRefresh()
    const inter = loadIntervalSec()
    if (id) {
      setIdentifier(id)
      setStatus('connected')
    }
    setAutoRefreshEnabled(autoR)
    setIntervalSec(inter)
  }, [])

  useEffect(() => {
    if (identifier && status === 'connected' && data == null) {
      refreshNow()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [identifier, status])

  useEffect(() => {
    if (!identifier) return
    if (!autoRefreshEnabled) { clearTimer(); return }
    setTimer()
    return () => clearTimer()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [identifier, autoRefreshEnabled, intervalSec])

  function setTimer() {
    clearTimer()
    timerRef.current = setInterval(() => {
      refreshNow()
    }, intervalSec * 1000)
  }
  function clearTimer() {
    if (timerRef.current) {
      clearInterval(timerRef.current)
      timerRef.current = null
    }
  }

  async function refreshNow() {
    if (!identifier || isFetching) return
    setIsFetching(true)
    setMessage('')
    try {
      const snap = await getInformation(identifier)
      const fresh =
      Array.isArray(snap)
        ? snap.map(item => ({ ...item }))
        : (snap && typeof snap === 'object' ? { ...snap } : snap)

      setData(fresh)  
      // setData(snap)
      setLastUpdated(Date.now())
      setStatus('connected')
      setMessage('עודכן בהצלחה')
    } catch (err) {
      setStatus('error')
      setMessage(err?.message || 'שגיאה ברענון')
    } finally {
      setIsFetching(false)
    }
  }

  async function onConnection() {
    if (!identifier || isFetching) return
    setIsFetching(true)
    setMessage('')
    try {
      await getSnapshot(identifier)
      setData(null)
      setStatus('connected')
      setMessage('חובר בהצלחה')
    } catch (err) {
      setStatus('error')
      setMessage(err?.message || 'שגיאה בחיבור')
    } finally {
      setIsFetching(false)
    }
  }

  function handleConnect(id) {
    saveIdentifier(id)
    setIdentifier(id)
    setStatus('connected')
    setData(null)
    setLastUpdated(null)
    onConnection()
  }

  function handleDisconnect() {
    clearIdentifier()
    setIdentifier('')
    setStatus('idle')
    setData(null)
    setLastUpdated(null)
    setMessage('')
    clearTimer()
  }

  function onToggleAutoRefresh(val) {
    setAutoRefreshEnabled(val)
    saveAutoRefresh(val)
  }
  function onChangeInterval(n) {
    setIntervalSec(n)
    saveIntervalSec(n)
  }

  const metrics = data?.results?.metrics || []

  return (
    <div className="grid">
      {status === 'idle' && (
        <IdentifierForm onConnect={handleConnect} disabled={isFetching} />
      )}

      {status !== 'idle' && (
        <div className="card">
          <div className="spacer" />

          <ResultActions
            identifier={identifier}
            lastUpdated={lastUpdated}
            onRefresh={refreshNow}
            onDisconnect={handleDisconnect}
            autoRefreshEnabled={autoRefreshEnabled}
            onToggleAutoRefresh={onToggleAutoRefresh}
            intervalSec={intervalSec}
            onChangeInterval={onChangeInterval}
            isFetching={isFetching}
          />

          {isFetching && <Spinner label="טוען נתונים..." />}

          {message && (
            <div style={{marginTop:10}}>
              <Alert type={status === 'error' ? 'error' : 'info'}>{message}</Alert>
            </div>
          )}
        </div>
      )}

      <div>
        {status === 'connected' && <Chart metrics={metrics} />}
      </div>

      {/* <div>
        {status === 'connected' && <ChartSwitcher data={[metrics]} defaultType="bar" rtl height={340} />}
      </div>
      <div style={{ width: 360 }}>
        {status === 'connected' && <PieChart metrics={metrics} donut={false} />}
      </div> */}
    </div>
  )
}
