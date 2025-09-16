const API_BASE = import.meta.env.VITE_API_BASE || ''

export async function getInformation(identifier) {
  const res = await fetch(`${API_BASE}/api/information`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: identifier })
  })
  console.log(res)
  if (!res.ok) {
    let msg = 'Snapshot request failed'
    try { const j = await res.json(); msg = j.message || msg } catch {}
    throw new Error(msg)
  }
  return res.json()
}
export async function getSnapshot(identifier) {
  const res = await fetch(`${API_BASE}/api/snapshot`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: identifier })
  })
  console.log(res)
  if (!res.ok) {
    let msg = 'Snapshot request failed'
    try { const j = await res.json(); msg = j.message || msg } catch {}
    throw new Error(msg)
  }
  return res.json()
}
