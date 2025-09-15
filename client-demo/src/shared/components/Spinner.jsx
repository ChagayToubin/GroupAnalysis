import React from 'react'

export default function Spinner({ label = 'טוען...' }) {
  return (
    <div aria-live="polite" className="muted" role="status">
      <span className="spinner" style={{marginInlineEnd: 8}}>⏳</span>
      {label}
    </div>
  )
}