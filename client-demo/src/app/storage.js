const KEY = 'processing.requestId'

export function saveRequestId(id) {
  try { localStorage.setItem(KEY, id) } catch {}
}
export function loadRequestId() {
  try { return localStorage.getItem(KEY) || '' } catch { return '' }
}
export function clearRequestId() {
  try { localStorage.removeItem(KEY) } catch {}
}