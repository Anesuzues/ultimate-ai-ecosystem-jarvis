import React, { useEffect, useRef, useState, useCallback } from 'react';
import axios from 'axios';
import { Send, Trash2, Plus, Cpu, Database, BookOpen, Mic, Wifi, Zap } from 'lucide-react';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const CATEGORY_LABELS = {
  research: 'RESEARCH',
  coding: 'CODING',
  build: 'BUILD',
  content: 'CONTENT',
  general: 'GENERAL',
};

const SYSTEM_ICONS = {
  router: Cpu,
  memory: Database,
  knowledge: BookOpen,
  voice: Mic,
  network: Wifi,
};

function StatusCard({ system }) {
  const Icon = SYSTEM_ICONS[system.name] || Zap;
  const dotClass =
    system.status === 'online' ? 'dot-online animate-pulse-soft' :
    system.status === 'standby' ? 'dot-standby' : 'dot-offline';
  return (
    <div
      data-testid={`status-card-${system.name}`}
      className="hud-frame border border-cyan-jarvis/15 bg-cyan-jarvis/[0.02] hover:bg-cyan-jarvis/[0.06] hover:border-cyan-jarvis/40 p-3 transition-colors"
    >
      <div className="flex items-center justify-between mb-2">
        <Icon size={14} className="text-cyan-jarvis" />
        <span className={`dot ${dotClass}`} />
      </div>
      <div className="font-hud uppercase tracking-[0.2em] text-[10px] text-cyan-jarvis/60">
        {system.name}
      </div>
      <div className="font-hud uppercase tracking-wider text-sm text-[#E2F1F8] mt-0.5">
        {system.label}
      </div>
      <div className="text-[10px] text-[#E2F1F8]/50 mt-1.5 leading-tight">
        {system.detail}
      </div>
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
    <span
      data-testid={`category-badge-${category}`}
      className="inline-block border border-cyan-jarvis/50 px-2 py-0.5 font-hud text-[10px] uppercase tracking-[0.25em] text-cyan-jarvis"
    >
      [{CATEGORY_LABELS[category] || category}]
    </span>
  );
}

function MessageBubble({ msg }) {
  const isUser = msg.role === 'user';
  return (
    <div
      data-testid={`message-${msg.role}-${msg.id}`}
      className={`animate-boot mb-5 ${isUser ? 'pl-12' : 'pr-12'}`}
    >
      <div className="flex items-center gap-2 mb-1.5">
        {!isUser && <CategoryBadge category={msg.category} />}
        <span className="font-hud uppercase tracking-[0.2em] text-[10px] text-[#E2F1F8]/40">
          {isUser ? 'OPERATOR' : 'JARVIS'} · {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>
      <div
        className={`p-4 jarvis-content text-[13px] leading-relaxed ${
          isUser
            ? 'border-r-2 border-r-[#E2F1F8]/30 bg-white/[0.02] text-[#E2F1F8]/90'
            : 'border-l-2 border-l-cyan-jarvis bg-cyan-jarvis/[0.03] text-[#E2F1F8]'
        }`}
      >
        {msg.content}
      </div>
    </div>
  );
}

function SessionItem({ session, active, onClick, onDelete }) {
  return (
    <div
      data-testid={`session-item-${session.id}`}
      onClick={onClick}
      className={`group cursor-pointer border p-2.5 mb-2 transition-colors ${
        active
          ? 'border-cyan-jarvis bg-cyan-jarvis/[0.06]'
          : 'border-cyan-jarvis/10 hover:border-cyan-jarvis/40 hover:bg-cyan-jarvis/[0.03]'
      }`}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="font-hud uppercase tracking-wider text-[12px] text-[#E2F1F8] truncate">
          {session.title || 'Untitled'}
        </div>
        <button
          data-testid={`delete-session-${session.id}`}
          onClick={(e) => { e.stopPropagation(); onDelete(session.id); }}
          className="opacity-0 group-hover:opacity-100 text-[#E2F1F8]/40 hover:text-amber-warn transition"
          aria-label="Delete session"
        >
          <Trash2 size={12} />
        </button>
      </div>
      <div className="text-[10px] text-[#E2F1F8]/40 mt-1 font-mono">
        {session.message_count} msgs · {new Date(session.updated_at).toLocaleDateString()}
      </div>
    </div>
  );
}

export default function App() {
  const [systems, setSystems] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [bootDone, setBootDone] = useState(false);
  const messagesEndRef = useRef(null);

  const refreshStatus = useCallback(async () => {
    try {
      const { data } = await axios.get(`${API}/status`);
      setSystems(data);
    } catch (e) { /* leave as is */ }
  }, []);

  const refreshSessions = useCallback(async () => {
    try {
      const { data } = await axios.get(`${API}/sessions`);
      setSessions(data);
    } catch (e) {}
  }, []);

  const loadMessages = useCallback(async (sid) => {
    if (!sid) { setMessages([]); return; }
    try {
      const { data } = await axios.get(`${API}/sessions/${sid}/messages`);
      setMessages(data);
    } catch (e) {}
  }, []);

  useEffect(() => {
    refreshStatus();
    refreshSessions();
    const t = setTimeout(() => setBootDone(true), 700);
    const id = setInterval(refreshStatus, 30000);
    return () => { clearTimeout(t); clearInterval(id); };
  }, [refreshStatus, refreshSessions]);

  useEffect(() => { loadMessages(activeSessionId); }, [activeSessionId, loadMessages]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, sending]);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || sending) return;
    setSending(true);

    const optimistic = {
      id: `tmp-${Date.now()}`,
      role: 'user',
      content: text,
      created_at: new Date().toISOString(),
    };
    setMessages((m) => [...m, optimistic]);
    setInput('');

    try {
      const { data } = await axios.post(`${API}/chat`, {
        session_id: activeSessionId,
        message: text,
      });
      setActiveSessionId(data.session_id);
      setMessages((m) => {
        const filtered = m.filter((x) => x.id !== optimistic.id);
        return [...filtered, data.user_message, data.jarvis_message];
      });
      refreshSessions();
    } catch (e) {
      setMessages((m) => [
        ...m,
        {
          id: `err-${Date.now()}`,
          role: 'jarvis',
          content: 'Apologies — a fault has occurred in the cognitive uplink. Please try again.',
          category: 'general',
          created_at: new Date().toISOString(),
        },
      ]);
    } finally {
      setSending(false);
    }
  };

  const handleNewChat = () => {
    setActiveSessionId(null);
    setMessages([]);
  };

  const handleDeleteSession = async (sid) => {
    try {
      await axios.delete(`${API}/sessions/${sid}`);
      if (sid === activeSessionId) handleNewChat();
      refreshSessions();
    } catch (e) {}
  };

  return (
    <div className="scanlines min-h-screen bg-obsidian text-[#E2F1F8] flex flex-col">
      {/* TOP BANNER */}
      <header className="border-b border-cyan-jarvis/20 px-6 py-3 flex items-center justify-between bg-obsidian/95 backdrop-blur-sm relative z-10">
        <div className="flex items-center gap-4">
          <div className="font-hud text-2xl uppercase tracking-[0.3em] font-bold text-cyan-jarvis text-glow animate-flicker">
            J.A.R.V.I.S
          </div>
          <span className="font-hud text-[10px] uppercase tracking-[0.3em] text-[#E2F1F8]/40 hidden sm:inline">
            Just A Rather Very Intelligent System
          </span>
        </div>
        <div className="flex items-center gap-3">
          <span className="dot dot-online animate-pulse-soft" />
          <span className="font-hud uppercase tracking-[0.2em] text-[11px] text-[#E2F1F8]/60">
            CORE ONLINE · v1.0.0
          </span>
        </div>
      </header>

      {/* STATUS DASHBOARD */}
      <section
        data-testid="status-grid"
        className={`px-6 pt-5 pb-2 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 ${bootDone ? 'animate-boot' : 'opacity-0'}`}
      >
        {systems.map((s) => <StatusCard key={s.name} system={s} />)}
      </section>

      {/* MAIN GRID */}
      <main className="flex-1 grid grid-cols-1 md:grid-cols-[280px_1fr] gap-4 px-6 pt-4 pb-6 overflow-hidden">
        {/* SIDEBAR */}
        <aside className="hud-frame border border-cyan-jarvis/15 p-3 flex flex-col bg-cyan-jarvis/[0.015] overflow-hidden">
          <div className="flex items-center justify-between mb-3">
            <div className="font-hud uppercase tracking-[0.25em] text-[11px] text-cyan-jarvis">
              Sessions
            </div>
            <button
              data-testid="new-chat-btn"
              onClick={handleNewChat}
              className="font-hud uppercase tracking-[0.2em] text-[10px] text-cyan-jarvis border border-cyan-jarvis/40 hover:border-cyan-jarvis hover:bg-cyan-jarvis/10 px-2 py-1 flex items-center gap-1 transition"
            >
              <Plus size={11} /> New
            </button>
          </div>
          <div className="flex-1 overflow-y-auto pr-1" data-testid="sessions-list">
            {sessions.length === 0 ? (
              <div className="text-[11px] text-[#E2F1F8]/40 font-mono p-2">
                No prior sessions. Issue a command to begin.
              </div>
            ) : (
              sessions.map((s) => (
                <SessionItem
                  key={s.id}
                  session={s}
                  active={s.id === activeSessionId}
                  onClick={() => setActiveSessionId(s.id)}
                  onDelete={handleDeleteSession}
                />
              ))
            )}
          </div>
        </aside>

        {/* CHAT */}
        <section className="hud-frame border border-cyan-jarvis/15 flex flex-col bg-cyan-jarvis/[0.01] overflow-hidden">
          <div className="border-b border-cyan-jarvis/15 px-4 py-2.5 flex items-center justify-between">
            <div className="font-hud uppercase tracking-[0.25em] text-[11px] text-cyan-jarvis">
              Conversation
            </div>
            <div className="font-hud uppercase tracking-[0.2em] text-[10px] text-[#E2F1F8]/40">
              {activeSessionId ? `SESSION ${activeSessionId.slice(0, 8)}` : 'NEW SESSION'}
            </div>
          </div>

          <div
            data-testid="chat-messages"
            className="flex-1 overflow-y-auto px-4 py-5"
          >
            {messages.length === 0 && !sending && (
              <div className="h-full flex flex-col items-center justify-center text-center px-4">
                <div className="font-hud uppercase tracking-[0.4em] text-cyan-jarvis text-glow text-2xl mb-3">
                  At your service
                </div>
                <div className="text-[#E2F1F8]/50 text-[12px] max-w-md leading-relaxed">
                  Issue any command and I shall route it to the appropriate subsystem.
                  Try: "Research the AI agent market", "Refactor my Python script", or
                  "Build a chat app with auth".
                </div>
                <div className="mt-6 grid grid-cols-2 sm:grid-cols-3 gap-2 w-full max-w-2xl">
                  {[
                    'Build a notes app with tags',
                    'Research best vector DBs in 2026',
                    'Write a Python rate limiter',
                    'Draft a launch tweet thread',
                    'Explain CRDTs simply',
                  ].map((p) => (
                    <button
                      key={p}
                      data-testid={`prompt-suggestion-${p.slice(0,10).replace(/\s/g,'-')}`}
                      onClick={() => setInput(p)}
                      className="text-left text-[11px] font-mono text-[#E2F1F8]/70 border border-cyan-jarvis/15 hover:border-cyan-jarvis/50 hover:bg-cyan-jarvis/5 p-2 transition"
                    >
                      › {p}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {messages.map((m) => <MessageBubble key={m.id} msg={m} />)}

            {sending && (
              <div data-testid="thinking-indicator" className="pr-12 mb-5">
                <div className="font-hud uppercase tracking-[0.2em] text-[10px] text-cyan-jarvis/70 mb-1.5">
                  JARVIS · processing
                </div>
                <div className="border-l-2 border-l-cyan-jarvis bg-cyan-jarvis/[0.03] p-4">
                  <div className="flex gap-1.5">
                    <span className="dot dot-online animate-pulse-soft" />
                    <span className="dot dot-online animate-pulse-soft" style={{ animationDelay: '0.3s' }} />
                    <span className="dot dot-online animate-pulse-soft" style={{ animationDelay: '0.6s' }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* INPUT */}
          <div className="border-t border-cyan-jarvis/15 p-3 flex gap-2 items-center">
            <span className="font-hud text-cyan-jarvis text-glow text-lg select-none">›</span>
            <input
              data-testid="chat-input"
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') handleSend(); }}
              placeholder="Issue a command..."
              disabled={sending}
              className="flex-1 bg-transparent border-b border-cyan-jarvis/20 focus:border-cyan-jarvis outline-none px-1 py-2 font-mono text-[13px] text-[#E2F1F8] placeholder-[#E2F1F8]/30 transition-colors disabled:opacity-50"
            />
            <button
              data-testid="send-btn"
              onClick={handleSend}
              disabled={!input.trim() || sending}
              className="font-hud uppercase tracking-[0.25em] text-[11px] text-obsidian bg-cyan-jarvis hover:bg-white disabled:bg-cyan-jarvis/30 disabled:cursor-not-allowed px-4 py-2 flex items-center gap-2 transition-colors"
            >
              <Send size={12} /> Transmit
            </button>
          </div>
        </section>
      </main>

      {/* FOOTER */}
      <footer className="border-t border-cyan-jarvis/15 px-6 py-2 flex items-center justify-between text-[10px] font-hud uppercase tracking-[0.25em] text-[#E2F1F8]/40">
        <span>STARK INDUSTRIES · CLEARANCE LEVEL 9</span>
        <span data-testid="footer-time">{new Date().toLocaleDateString()} · ALL SYSTEMS NOMINAL</span>
      </footer>
    </div>
  );
}
