const API_BASE = import.meta.env.VITE_API_BASE || ''

export async function startProcess({ text, texts }) {
  const res = await fetch(`${API_BASE}/api/process/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, texts })
  })
  if (!res.ok) {
    let msg = 'Request failed'
    try {
      const j = await res.json()
      msg = j.message || msg
    } catch {}
    throw new Error(msg)
  }
  return res.json()
}

export async function getStatus(requestId) {
  const url = new URL(`${API_BASE}/api/process/status`)
  url.searchParams.set('requestId', requestId)
  const res = await fetch(url.toString())
  if (!res.ok) {
    let msg = 'Status failed'
    try {
      const j = await res.json()
      msg = j.message || msg
    } catch {}
    throw new Error(msg)
  }
  return res.json()
}