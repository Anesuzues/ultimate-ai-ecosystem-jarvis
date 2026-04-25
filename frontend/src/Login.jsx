import React from 'react';
import { useLocation } from 'react-router-dom';

// REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
function startLogin() {
  const redirectUrl = window.location.origin + '/';
  window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
}

export default function Login() {
  const location = useLocation();
  const error = location.state?.error;
  return (
    <div className="scanlines min-h-screen bg-obsidian text-[#E2F1F8] flex items-center justify-center px-6">
      <div className="hud-frame border border-cyan-jarvis/25 bg-cyan-jarvis/[0.02] p-8 max-w-md w-full">
        <div className="font-hud uppercase tracking-[0.4em] text-cyan-jarvis text-glow text-3xl text-center mb-1 animate-flicker">
          J.A.R.V.I.S
        </div>
        <div className="font-hud uppercase tracking-[0.25em] text-[10px] text-[#E2F1F8]/50 text-center mb-8">
          Just A Rather Very Intelligent System
        </div>

        <div className="font-hud uppercase tracking-[0.2em] text-xs text-cyan-jarvis/70 mb-3">
          › Identity verification required
        </div>
        <p className="text-[12px] text-[#E2F1F8]/70 leading-relaxed mb-6">
          Authenticate to access the cognitive uplink, persistent memory, and voice synthesis subsystems.
        </p>

        {error && (
          <div data-testid="login-error" className="border border-red-500/40 bg-red-500/5 text-red-300 text-[11px] p-2 mb-4 font-mono">
            {error}
          </div>
        )}

        <button
          data-testid="login-google-btn"
          onClick={startLogin}
          className="w-full font-hud uppercase tracking-[0.25em] text-sm text-obsidian bg-cyan-jarvis hover:bg-white px-4 py-3 transition-colors"
        >
          Authenticate with Google →
        </button>

        <div className="mt-8 font-hud uppercase tracking-[0.2em] text-[10px] text-[#E2F1F8]/30 text-center">
          STARK INDUSTRIES · CLEARANCE LEVEL 9
        </div>
      </div>
    </div>
  );
}
