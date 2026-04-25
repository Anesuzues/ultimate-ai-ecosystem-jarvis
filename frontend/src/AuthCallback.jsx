import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { exchangeSession } from './api';

export default function AuthCallback({ onAuthed }) {
  const navigate = useNavigate();
  const location = useLocation();
  const ran = React.useRef(false);

  useEffect(() => {
    if (ran.current) return;
    ran.current = true;
    const hash = location.hash || '';
    const m = hash.match(/session_id=([^&]+)/);
    if (!m) {
      navigate('/login', { replace: true });
      return;
    }
    const sid = decodeURIComponent(m[1]);
    (async () => {
      try {
        const { data } = await exchangeSession(sid);
        onAuthed && onAuthed(data);
        // strip hash and go to dashboard
        window.history.replaceState({}, '', '/');
        navigate('/', { replace: true, state: { user: data } });
      } catch (e) {
        navigate('/login', { replace: true, state: { error: 'Login failed' } });
      }
    })();
  }, [location, navigate, onAuthed]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-obsidian text-cyan-jarvis font-hud uppercase tracking-[0.3em] text-xl animate-pulse-soft">
      Authenticating handshake…
    </div>
  );
}
