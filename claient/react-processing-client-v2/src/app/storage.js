const KEY_ID = 'processing.identifier'
const KEY_AUTO = 'processing.autoRefresh'
const KEY_INTERVAL = 'processing.refreshIntervalSec'

export function saveIdentifier(id) { try { localStorage.setItem(KEY_ID, id) } catch {} }
export function loadIdentifier()    { try { return localStorage.getItem(KEY_ID) || '' } catch { return '' } }
export function clearIdentifier()   { try { localStorage.removeItem(KEY_ID) } catch {} }

export function saveAutoRefresh(enabled) { try { localStorage.setItem(KEY_AUTO, enabled ? '1' : '0') } catch {} }
export function loadAutoRefresh()        { try { return (localStorage.getItem(KEY_AUTO) || '0') === '1' } catch { return false } }

export function saveIntervalSec(n) { try { localStorage.setItem(KEY_INTERVAL, String(n)) } catch {} }
export function loadIntervalSec() {
  try {
    const v = parseInt(localStorage.getItem(KEY_INTERVAL) || '5', 10)
    return Number.isFinite(v) ? v : 5
  } catch { return 5 }
}
