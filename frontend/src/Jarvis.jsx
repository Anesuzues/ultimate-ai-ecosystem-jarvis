import React, { useEffect, useRef, useState, useCallback } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import 'highlight.js/styles/github-dark.css';
import {
  Send, Trash2, Plus, Cpu, Database, BookOpen, Mic, Wifi, MicOff,
  Volume2, VolumeX, Download, LogOut,
} from 'lucide-react';
import {
  fetchStatus, fetchSessions, fetchMessages, deleteSession,
  exportSessionUrl, transcribe, ttsUrl, streamChat, logout,
} from './api';

const CATEGORY_LABELS = {
  research: 'RESEARCH', coding: 'CODING', build: 'BUILD',
  content: 'CONTENT', general: 'GENERAL',
};
const SYSTEM_ICONS = {
  router: Cpu, memory: Database, knowledge: BookOpen, voice: Mic, network: Wifi,
};

function StatusCard({ system }) {
  const Icon = SYSTEM_ICONS[system.name] || Cpu;
  const dotClass =
    system.status === 'online' ? 'dot-online animate-pulse-soft' :
    system.status === 'standby' ? 'dot-standby' : 'dot-offline';
  return (
    <div data-testid={`status-card-${system.name}`}
         className="hud-frame border border-cyan-jarvis/15 bg-cyan-jarvis/[0.02] hover:bg-cyan-jarvis/[0.06] hover:border-cyan-jarvis/40 p-3 transition-colors">
      <div className="flex items-center justify-between mb-2">
        <Icon size={14} className="text-cyan-jarvis" />
        <span className={`dot ${dotClass}`} />
      </div>
      <div className="font-hud uppercase tracking-[0.2em] text-[10px] text-cyan-jarvis/60">{system.name}</div>
      <div className="font-hud uppercase tracking-wider text-sm text-[#E2F1F8] mt-0.5">{system.label}</div>
      <div className="text-[10px] text-[#E2F1F8]/50 mt-1.5 leading-tight">{system.detail}</div>
      <div className="text-[10px] font-hud uppercase tracking-widest mt-2"
           style={{ color: system.status === 'online' ? '#00E676' : system.status === 'standby' ? '#FF9100' : '#FF3B30' }}>
        {system.status}
      </div>
    </div>
  );
}

function CategoryBadge({ category }) {
  if (!category) return null;
  return (
    <span data-testid={`category-badge-${category}`}
          className="inline-block border border-cyan-jarvis/50 px-2 py-0.5 font-hud text-[10px] uppercase tracking-[0.25em] text-cyan-jarvis">
      [{CATEGORY_LABELS[category] || category}]
    </span>
  );
}

function MessageBubble({ msg, isStreaming }) {
  const isUser = msg.role === 'user';
  return (
    <div data-testid={`message-${msg.role}-${msg.id}`}
         className={`animate-boot mb-5 ${isUser ? 'pl-12' : 'pr-12'}`}>
      <div className="flex items-center gap-2 mb-1.5">
        {!isUser && <CategoryBadge category={msg.category} />}
        <span className="font-hud uppercase tracking-[0.2em] text-[10px] text-[#E2F1F8]/40">
          {isUser ? 'OPERATOR' : 'JARVIS'} · {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>
      <div className={`p-4 jarvis-content text-[13px] leading-relaxed ${
        isUser ? 'border-r-2 border-r-[#E2F1F8]/30 bg-white/[0.02] text-[#E2F1F8]/90'
               : 'border-l-2 border-l-cyan-jarvis bg-cyan-jarvis/[0.03] text-[#E2F1F8]'}`}>
        {isUser ? (
          msg.content
        ) : (
          <div className="markdown-body">
            <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]}>
              {msg.content || ''}
            </ReactMarkdown>
            {isStreaming && <span className="inline-block w-2 h-4 bg-cyan-jarvis ml-1 animate-pulse-soft align-middle" />}
          </div>
        )}
      </div>
    </div>
  );
}

function SessionItem({ session, active, onClick, onDelete, onExport }) {
  return (
    <div data-testid={`session-item-${session.id}`} onClick={onClick}
         className={`group cursor-pointer border p-2.5 mb-2 transition-colors ${
           active ? 'border-cyan-jarvis bg-cyan-jarvis/[0.06]'
                  : 'border-cyan-jarvis/10 hover:border-cyan-jarvis/40 hover:bg-cyan-jarvis/[0.03]'}`}>
      <div className="flex items-start justify-between gap-2">
        <div className="font-hud uppercase tracking-wider text-[12px] text-[#E2F1F8] truncate">
          {session.title || 'Untitled'}
        </div>
        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition">
          <button data-testid={`export-session-${session.id}`}
                  onClick={(e) => { e.stopPropagation(); onExport(session.id); }}
                  className="text-[#E2F1F8]/40 hover:text-cyan-jarvis" aria-label="Export">
            <Download size={12} />
          </button>
          <button data-testid={`delete-session-${session.id}`}
                  onClick={(e) => { e.stopPropagation(); onDelete(session.id); }}
                  className="text-[#E2F1F8]/40 hover:text-amber-warn" aria-label="Delete">
            <Trash2 size={12} />
          </button>
        </div>
      </div>
      <div className="text-[10px] text-[#E2F1F8]/40 mt-1 font-mono">
        {session.message_count} msgs · {new Date(session.updated_at).toLocaleDateString()}
      </div>
    </div>
  );
}

export default function Jarvis({ user, onLogout }) {
  const [systems, setSystems] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [streamingId, setStreamingId] = useState(null);
  const [bootDone, setBootDone] = useState(false);
  const [recording, setRecording] = useState(false);
  const [transcribing, setTranscribing] = useState(false);
  const [voiceOut, setVoiceOut] = useState(false);
  const messagesEndRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioPlayerRef = useRef(null);

  const refreshStatus = useCallback(async () => {
    try { const { data } = await fetchStatus(); setSystems(data); } catch {}
  }, []);
  const refreshSessions = useCallback(async () => {
    try { const { data } = await fetchSessions(); setSessions(data); } catch {}
  }, []);
  const loadMessages = useCallback(async (sid) => {
    if (!sid) { setMessages([]); return; }
    try { const { data } = await fetchMessages(sid); setMessages(data); } catch {}
  }, []);

  useEffect(() => {
    refreshStatus(); refreshSessions();
    const t = setTimeout(() => setBootDone(true), 600);
    const id = setInterval(refreshStatus, 30000);
    return () => { clearTimeout(t); clearInterval(id); };
  }, [refreshStatus, refreshSessions]);

  useEffect(() => { loadMessages(activeSessionId); }, [activeSessionId, loadMessages]);
  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages, sending]);

  // ---- TTS playback
  const playTts = async (text) => {
    if (!text) return;
    try {
      const res = await fetch(ttsUrl, {
        method: 'POST', credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, voice: 'nova' }),
      });
      if (!res.ok) return;
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      if (audioPlayerRef.current) {
        audioPlayerRef.current.pause();
        URL.revokeObjectURL(audioPlayerRef.current.src);
      }
      const audio = new Audio(url);
      audioPlayerRef.current = audio;
      audio.play().catch(() => {});
    } catch {}
  };

  // ---- mic
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mr = new MediaRecorder(stream, { mimeType: 'audio/webm' });
      audioChunksRef.current = [];
      mr.ondataavailable = (e) => { if (e.data.size) audioChunksRef.current.push(e.data); };
      mr.onstop = async () => {
        stream.getTracks().forEach((t) => t.stop());
        const blob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        setTranscribing(true);
        try {
          const { data } = await transcribe(blob);
          if (data?.text) setInput((prev) => (prev ? prev + ' ' : '') + data.text);
        } catch {}
        finally { setTranscribing(false); }
      };
      mediaRecorderRef.current = mr;
      mr.start();
      setRecording(true);
    } catch (e) {
      alert('Microphone access required');
    }
  };
  const stopRecording = () => {
    if (mediaRecorderRef.current && recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  };

  // ---- streaming send
  const handleSend = async () => {
    const text = input.trim();
    if (!text || sending) return;
    setSending(true);
    setInput('');

    const tempUserId = `tmp-u-${Date.now()}`;
    const tempJarvisId = `tmp-j-${Date.now()}`;
    setMessages((m) => [
      ...m,
      { id: tempUserId, role: 'user', content: text, created_at: new Date().toISOString() },
      { id: tempJarvisId, role: 'jarvis', content: '', category: null, created_at: new Date().toISOString() },
    ]);
    setStreamingId(tempJarvisId);

    let metaCategory = null;
    let accumulated = '';
    let finalJarvis = null;
    let serverSessionId = activeSessionId;

    try {
      for await (const ev of streamChat({ session_id: activeSessionId, message: text })) {
        if (ev.event === 'meta') {
          metaCategory = ev.data.category;
          serverSessionId = ev.data.session_id;
          setMessages((m) => m.map((x) => {
            if (x.id === tempUserId) return ev.data.user_message;
            if (x.id === tempJarvisId) return { ...x, category: metaCategory };
            return x;
          }));
        } else if (ev.event === 'chunk') {
          accumulated += ev.data.text || '';
          setMessages((m) => m.map((x) => x.id === tempJarvisId ? { ...x, content: accumulated } : x));
        } else if (ev.event === 'done') {
          finalJarvis = ev.data.jarvis_message;
          setMessages((m) => m.map((x) => x.id === tempJarvisId ? finalJarvis : x));
        } else if (ev.event === 'error') {
          throw new Error(ev.data?.detail || 'stream error');
        }
      }
      if (serverSessionId && serverSessionId !== activeSessionId) {
        setActiveSessionId(serverSessionId);
      }
      refreshSessions();
      if (voiceOut && finalJarvis?.content) playTts(finalJarvis.content);
    } catch (e) {
      setMessages((m) => m.map((x) => x.id === tempJarvisId
        ? { ...x, content: 'Apologies — a fault has occurred in the cognitive uplink.', category: 'general' }
        : x));
    } finally {
      setSending(false);
      setStreamingId(null);
    }
  };

  const handleNewChat = () => { setActiveSessionId(null); setMessages([]); };

  const handleDeleteSession = async (sid) => {
    try { await deleteSession(sid); if (sid === activeSessionId) handleNewChat(); refreshSessions(); } catch {}
  };

  const handleExport = (sid) => {
    const a = document.createElement('a');
    a.href = exportSessionUrl(sid, 'md');
    a.download = '';
    document.body.appendChild(a); a.click(); a.remove();
  };

  const handleLogout = async () => {
    try { await logout(); } catch {}
    onLogout && onLogout();
  };

  return (
    <div className="scanlines min-h-screen bg-obsidian text-[#E2F1F8] flex flex-col">
      {/* HEADER */}
      <header className="border-b border-cyan-jarvis/20 px-6 py-3 flex items-center justify-between bg-obsidian/95 backdrop-blur-sm relative z-10">
        <div className="flex items-center gap-4">
          <div className="font-hud text-2xl uppercase tracking-[0.3em] font-bold text-cyan-jarvis text-glow animate-flicker">
            J.A.R.V.I.S
          </div>
          <span className="font-hud text-[10px] uppercase tracking-[0.3em] text-[#E2F1F8]/40 hidden sm:inline">
            Just A Rather Very Intelligent System
          </span>
        </div>
        <div className="flex items-center gap-4">
          <span className="dot dot-online animate-pulse-soft" />
          <span className="font-hud uppercase tracking-[0.2em] text-[11px] text-[#E2F1F8]/60 hidden sm:inline">
            CORE ONLINE · v2.0.0
          </span>
          {user && (
            <div className="flex items-center gap-2 border-l border-cyan-jarvis/20 pl-4">
              {user.picture && <img alt="" src={user.picture} className="w-6 h-6 border border-cyan-jarvis/30" />}
              <span data-testid="user-name" className="font-hud uppercase tracking-[0.2em] text-[11px] text-[#E2F1F8]/80 hidden sm:inline">
                {user.name}
              </span>
              <button data-testid="logout-btn" onClick={handleLogout}
                      className="text-[#E2F1F8]/50 hover:text-amber-warn transition" aria-label="Logout">
                <LogOut size={14} />
              </button>
            </div>
          )}
        </div>
      </header>

      {/* STATUS GRID */}
      <section data-testid="status-grid"
               className={`px-6 pt-5 pb-2 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 ${bootDone ? 'animate-boot' : 'opacity-0'}`}>
        {systems.map((s) => <StatusCard key={s.name} system={s} />)}
      </section>

      {/* MAIN */}
      <main className="flex-1 grid grid-cols-1 md:grid-cols-[280px_1fr] gap-4 px-6 pt-4 pb-6 overflow-hidden">
        {/* SIDEBAR */}
        <aside className="hud-frame border border-cyan-jarvis/15 p-3 flex flex-col bg-cyan-jarvis/[0.015] overflow-hidden">
          <div className="flex items-center justify-between mb-3">
            <div className="font-hud uppercase tracking-[0.25em] text-[11px] text-cyan-jarvis">Sessions</div>
            <button data-testid="new-chat-btn" onClick={handleNewChat}
                    className="font-hud uppercase tracking-[0.2em] text-[10px] text-cyan-jarvis border border-cyan-jarvis/40 hover:border-cyan-jarvis hover:bg-cyan-jarvis/10 px-2 py-1 flex items-center gap-1 transition">
              <Plus size={11} /> New
            </button>
          </div>
          <div className="flex-1 overflow-y-auto pr-1" data-testid="sessions-list">
            {sessions.length === 0 ? (
              <div className="text-[11px] text-[#E2F1F8]/40 font-mono p-2">
                No prior sessions. Issue a command to begin.
              </div>
            ) : sessions.map((s) => (
              <SessionItem key={s.id} session={s} active={s.id === activeSessionId}
                           onClick={() => setActiveSessionId(s.id)}
                           onDelete={handleDeleteSession} onExport={handleExport} />
            ))}
          </div>
        </aside>

        {/* CHAT */}
        <section className="hud-frame border border-cyan-jarvis/15 flex flex-col bg-cyan-jarvis/[0.01] overflow-hidden">
          <div className="border-b border-cyan-jarvis/15 px-4 py-2.5 flex items-center justify-between">
            <div className="font-hud uppercase tracking-[0.25em] text-[11px] text-cyan-jarvis">Conversation</div>
            <div className="flex items-center gap-3">
              <button data-testid="voice-out-toggle" onClick={() => setVoiceOut((v) => !v)}
                      title={voiceOut ? 'Voice replies on' : 'Voice replies off'}
                      className={`flex items-center gap-1.5 font-hud uppercase tracking-[0.2em] text-[10px] px-2 py-1 border transition ${
                        voiceOut ? 'border-cyan-jarvis bg-cyan-jarvis/10 text-cyan-jarvis' : 'border-cyan-jarvis/20 text-[#E2F1F8]/40 hover:text-cyan-jarvis'}`}>
                {voiceOut ? <Volume2 size={11} /> : <VolumeX size={11} />} TTS
              </button>
              <div className="font-hud uppercase tracking-[0.2em] text-[10px] text-[#E2F1F8]/40">
                {activeSessionId ? `SESSION ${activeSessionId.slice(0, 8)}` : 'NEW SESSION'}
              </div>
            </div>
          </div>

          <div data-testid="chat-messages" className="flex-1 overflow-y-auto px-4 py-5">
            {messages.length === 0 && !sending && (
              <div className="h-full flex flex-col items-center justify-center text-center px-4">
                <div className="font-hud uppercase tracking-[0.4em] text-cyan-jarvis text-glow text-2xl mb-3">
                  At your service
                </div>
                <div className="text-[#E2F1F8]/50 text-[12px] max-w-md leading-relaxed">
                  Issue any command. I shall route it, format the reply, and persist the exchange.
                </div>
                <div className="mt-6 grid grid-cols-2 sm:grid-cols-3 gap-2 w-full max-w-2xl">
                  {[
                    'Build a notes app with tags',
                    'Research best vector DBs in 2026',
                    'Write a Python rate limiter',
                    'Draft a launch tweet thread',
                    'Explain CRDTs simply',
                  ].map((p) => (
                    <button key={p} data-testid={`prompt-suggestion-${p.slice(0,10).replace(/\s/g,'-')}`}
                            onClick={() => setInput(p)}
                            className="text-left text-[11px] font-mono text-[#E2F1F8]/70 border border-cyan-jarvis/15 hover:border-cyan-jarvis/50 hover:bg-cyan-jarvis/5 p-2 transition">
                      › {p}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {messages.map((m) => (
              <MessageBubble key={m.id} msg={m} isStreaming={m.id === streamingId} />
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* INPUT */}
          <div className="border-t border-cyan-jarvis/15 p-3 flex gap-2 items-center">
            <span className="font-hud text-cyan-jarvis text-glow text-lg select-none">›</span>
            <input data-testid="chat-input" type="text" value={input}
                   onChange={(e) => setInput(e.target.value)}
                   onKeyDown={(e) => { if (e.key === 'Enter') handleSend(); }}
                   placeholder={transcribing ? 'Transcribing voice…' : recording ? 'Listening…' : 'Issue a command...'}
                   disabled={sending || transcribing}
                   className="flex-1 bg-transparent border-b border-cyan-jarvis/20 focus:border-cyan-jarvis outline-none px-1 py-2 font-mono text-[13px] text-[#E2F1F8] placeholder-[#E2F1F8]/30 transition-colors disabled:opacity-50" />
            <button data-testid={recording ? 'mic-stop-btn' : 'mic-start-btn'}
                    onClick={recording ? stopRecording : startRecording}
                    disabled={sending || transcribing}
                    className={`font-hud uppercase tracking-[0.2em] text-[10px] px-3 py-2 border transition flex items-center gap-1 ${
                      recording ? 'border-amber-warn text-amber-warn animate-pulse-soft'
                                : 'border-cyan-jarvis/30 text-cyan-jarvis/80 hover:border-cyan-jarvis hover:text-cyan-jarvis'}`}
                    title={recording ? 'Stop recording' : 'Start voice input'}>
              {recording ? <MicOff size={12} /> : <Mic size={12} />}
            </button>
            <button data-testid="send-btn" onClick={handleSend} disabled={!input.trim() || sending}
                    className="font-hud uppercase tracking-[0.25em] text-[11px] text-obsidian bg-cyan-jarvis hover:bg-white disabled:bg-cyan-jarvis/30 disabled:cursor-not-allowed px-4 py-2 flex items-center gap-2 transition-colors">
              <Send size={12} /> Transmit
            </button>
          </div>
        </section>
      </main>

      <footer className="border-t border-cyan-jarvis/15 px-6 py-2 flex items-center justify-between text-[10px] font-hud uppercase tracking-[0.25em] text-[#E2F1F8]/40">
        <span>STARK INDUSTRIES · CLEARANCE LEVEL 9</span>
        <span data-testid="footer-time">{new Date().toLocaleDateString()} · ALL SYSTEMS NOMINAL</span>
      </footer>
    </div>
  );
}
