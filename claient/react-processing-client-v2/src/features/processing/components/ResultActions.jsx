import React from 'react'

export default function ResultActions({
  identifier,
  lastUpdated,
  onRefresh,
  onDisconnect,
  autoRefreshEnabled,
  onToggleAutoRefresh,
  intervalSec,
  onChangeInterval,
  isFetching
}) {
  const updated = lastUpdated ? new Date(lastUpdated) : null
  const updatedText = updated ? updated.toLocaleTimeString() : '—'

  return (
    <div className="card">
      <div className="row cols-3">
        <div>
          <label>מזהה פעיל</label>
          <div className="status" title={identifier}>{identifier || '—'}</div>
        </div>
        <div>
          <label>עודכן לאחרונה</label>
          <div className="status">{updatedText}</div>
        </div>
        <div style={{display:'flex', alignItems:'end', gap:8}}>
          <button className="btn success" onClick={onRefresh} disabled={!identifier || isFetching}>
            רענן עכשיו
          </button>
          <button className="btn danger" onClick={onDisconnect} disabled={isFetching}>
            נתק
          </button>
        </div>
      </div>

      <div className="spacer"></div>

      <div className="row cols-3">
        <div>
          <label>Auto-Refresh</label>
          <div style={{display:'flex', alignItems:'center', gap:8}}>
            <input
              id="autoRef"
              type="checkbox"
              checked={autoRefreshEnabled}
              onChange={e => onToggleAutoRefresh(e.target.checked)}
            />
            <label htmlFor="autoRef" className="muted">השבת רענון אוטומטי</label>
          </div>
        </div>
        <div>
          <label>מרווח (שניות)</label>
          <select value={intervalSec} onChange={e => onChangeInterval(parseInt(e.target.value, 10))}>
            <option value={3}>3</option>
            <option value={5}>5</option>
            <option value={10}>10</option>
          </select>
        </div>
        <div>
          <label>API Base</label>
          <div className="status">{import.meta.env.VITE_API_BASE || '(same origin)'}</div>
        </div>
      </div>
    </div>
  )
}
