import React, { useEffect, useState, useCallback } from 'react';
import { BrowserRouter, Routes, Route, useLocation, useNavigate, Navigate } from 'react-router-dom';
import Jarvis from './Jarvis';
import Login from './Login';
import AuthCallback from './AuthCallback';
import { fetchMe } from './api';

function AppRouter() {
  const [user, setUser] = useState(null);
  const [authState, setAuthState] = useState('checking'); // 'checking' | 'auth' | 'anon'
  const location = useLocation();

  const checkAuth = useCallback(async () => {
    try {
      const { data } = await fetchMe();
      setUser(data);
      setAuthState('auth');
    } catch {
      setUser(null);
      setAuthState('anon');
    }
  }, []);

  useEffect(() => {
    // CRITICAL: If returning from OAuth callback, skip /me check; AuthCallback will handle.
    if (window.location.hash?.includes('session_id=')) {
      setAuthState('checking');
      return;
    }
    checkAuth();
  }, [checkAuth]);

  if (authState === 'checking' && !location.hash?.includes('session_id=')) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-obsidian text-cyan-jarvis font-hud uppercase tracking-[0.3em] animate-pulse-soft">
        Boot sequence…
      </div>
    );
  }

  // synchronous detection of session_id in URL fragment
  if (location.hash?.includes('session_id=')) {
    return <AuthCallback onAuthed={(u) => { setUser(u); setAuthState('auth'); }} />;
  }

  return (
    <Routes>
      <Route path="/login"
             element={authState === 'auth' ? <Navigate to="/" replace /> : <Login />} />
      <Route path="/"
             element={authState === 'auth'
               ? <Jarvis user={user} onLogout={() => { setUser(null); setAuthState('anon'); }} />
               : <Navigate to="/login" replace />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppRouter />
    </BrowserRouter>
  );
}
