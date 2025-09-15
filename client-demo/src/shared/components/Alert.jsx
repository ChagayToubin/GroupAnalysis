import React from 'react'

export default function Alert({ type='info', children }) {
  const color = type === 'error' ? '#ef4444' : (type === 'success' ? '#22c55e' : '#3b82f6')
  return (
    <div style={{
      border: `1px solid ${color}55`,
      background: `${color}18`,
      color,
      padding: '10px 12px',
      borderRadius: 12
    }}>
      {children}
    </div>
  )
}