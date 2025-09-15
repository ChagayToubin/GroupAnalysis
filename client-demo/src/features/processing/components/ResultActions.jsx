import React from 'react'

export default function ResultActions({ onCheck, requestId, status }) {
  return (
    <div className="card">
      <div className="row cols-3">
        <div>
          <label>מזהה בקשה</label>
          <div className="status">{requestId ? requestId : '—'}</div>
        </div>
        <div>
          <label>סטטוס</label>
          <div className="status">{status}</div>
        </div>
        <div style={{display:'flex', alignItems:'end', justifyContent:'flex-start'}}>
          <button className="btn success" onClick={onCheck} disabled={!requestId}>
            הצג תוצאות
          </button>
        </div>
      </div>
    </div>
  )
}