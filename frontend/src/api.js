import axios from 'axios';

export const API_BASE = `${process.env.REACT_APP_BACKEND_URL}/api`;

export const api = axios.create({
  baseURL: API_BASE,
  withCredentials: true,
});

// ---- auth
export const exchangeSession = (sessionId) =>
  api.post('/auth/session', null, { headers: { 'X-Session-ID': sessionId } });
export const fetchMe = () => api.get('/auth/me');
export const logout = () => api.post('/auth/logout');

// ---- core
export const fetchStatus = () => api.get('/status');
export const fetchSessions = () => api.get('/sessions');
export const fetchMessages = (sid) => api.get(`/sessions/${sid}/messages`);
export const deleteSession = (sid) => api.delete(`/sessions/${sid}`);
export const exportSessionUrl = (sid, format = 'md') =>
  `${API_BASE}/sessions/${sid}/export?format=${format}`;

// ---- voice
export const transcribe = (blob) => {
  const fd = new FormData();
  fd.append('audio', blob, 'voice.webm');
  return api.post('/voice/transcribe', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
};
export const ttsUrl = `${API_BASE}/voice/tts`;

// ---- streaming chat (fetch-based, since EventSource doesn't support POST)
export async function* streamChat({ session_id, message }) {
  const res = await fetch(`${API_BASE}/chat/stream`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id, message }),
  });
  if (!res.ok || !res.body) {
    throw new Error(`stream failed: ${res.status}`);
  }
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    // Parse complete SSE blocks delimited by blank line
    let idx;
    while ((idx = buffer.indexOf('\n\n')) !== -1) {
      const block = buffer.slice(0, idx);
      buffer = buffer.slice(idx + 2);
      const ev = parseSseBlock(block);
      if (ev) yield ev;
    }
  }
}

function parseSseBlock(block) {
  let event = 'message';
  let dataLines = [];
  for (const line of block.split('\n')) {
    if (line.startsWith('event:')) event = line.slice(6).trim();
    else if (line.startsWith('data:')) dataLines.push(line.slice(5).trim());
  }
  if (!dataLines.length) return null;
  try {
    return { event, data: JSON.parse(dataLines.join('\n')) };
  } catch {
    return { event, data: dataLines.join('\n') };
  }
}
