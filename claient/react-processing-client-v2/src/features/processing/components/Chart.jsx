import React from 'react'

export default function Chart({ metrics }) {
  if (!metrics || metrics.length === 0) {
    return <div className="card"><div className="muted">אין נתונים להצגה</div></div>
  }

  const padding = { top: 16, right: 16, bottom: 36, left: 36 }
  const width = 800
  const height = 280
  const innerW = width - padding.left - padding.right
  const innerH = height - padding.top - padding.bottom

  const maxVal = Math.max(...metrics.map(m => Number(m.value) || 0))
  const barW = (innerW / metrics.length) * 0.7
  const gap = (innerW / metrics.length) * 0.3

  const bars = metrics.map((m, idx) => {
    const v = Number(m.value) || 0
    const h = maxVal === 0 ? 0 : (v / maxVal) * innerH
    const x = padding.left + idx * (barW + gap)
    const y = padding.top + (innerH - h)
    return (
      <g key={idx}>
        <rect x={x} y={y} width={barW} height={h} rx="6" ry="6" fill="#3b82f6" />
        <text x={x + barW / 2} y={height - 10} textAnchor="middle" fontSize="12" fill="#8aa0b3">
          {m.name}
        </text>
        <text x={x + barW / 2} y={y - 6} textAnchor="middle" fontSize="12" fill="#e6edf3">
          {v}
        </text>
      </g>
    )
  })

  const ticks = 4
  const tickEls = []
  for (let i = 0; i <= ticks; i++) {
    const v = (maxVal / ticks) * i
    const y = padding.top + (innerH - (innerH / ticks) * i)
    tickEls.push(
      <g key={i}>
        <line x1={padding.left - 6} y1={y} x2={width - padding.right} y2={y} stroke="#223043" strokeDasharray="3,3" />
        <text x={padding.left - 10} y={y + 4} textAnchor="end" fontSize="11" fill="#8aa0b3">
          {v.toFixed(0)}
        </text>
      </g>
    )
  }

  return (
    <div className="card chart-wrap">
      <svg width="100%" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Bar chart">
        <rect x="0" y="0" width={width} height={height} fill="transparent" />
        {tickEls}
        {bars}
      </svg>
    </div>
  )
}


