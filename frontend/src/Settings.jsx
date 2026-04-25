import React, { useEffect, useState } from 'react';
import { X, ExternalLink, Download } from 'lucide-react';
import { PORCUPINE_KEY_STORAGE } from './wakeWord';
import { api } from './api';

export const LLM_PROVIDER_STORAGE = 'jarvis_llm_provider';      // 'emergent' | 'ollama'
export const OLLAMA_URL_STORAGE = 'jarvis_ollama_url';
export const OLLAMA_MODEL_STORAGE = 'jarvis_ollama_model';
export const WAKE_ENABLED_STORAGE = 'jarvis_wake_enabled';

export default function SettingsModal({ open, onClose, deferredInstall, onInstall }) {
  const [pvKey, setPvKey] = useState('');
  const [provider, setProvider] = useState('emergent');
  const [ollamaUrl, setOllamaUrl] = useState('http://localhost:11434');
  const [ollamaModel, setOllamaModel] = useState('llama3.1');
  const [wakeEnabled, setWakeEnabled] = useState(false);
  const [savingProvider, setSavingProvider] = useState(false);
  const [providerStatus, setProviderStatus] = useState(null);

  useEffect(() => {
    if (!open) return;
    setPvKey(localStorage.getItem(PORCUPINE_KEY_STORAGE) || '');
    setProvider(localStorage.getItem(LLM_PROVIDER_STORAGE) || 'emergent');
    setOllamaUrl(localStorage.getItem(OLLAMA_URL_STORAGE) || 'http://localhost:11434');
    setOllamaModel(localStorage.getItem(OLLAMA_MODEL_STORAGE) || 'llama3.1');
    setWakeEnabled(localStorage.getItem(WAKE_ENABLED_STORAGE) === '1');
    api.get('/llm/provider').then(({ data }) => setProviderStatus(data)).catch(() => {});
  }, [open]);

  const saveAll = async () => {
    localStorage.setItem(PORCUPINE_KEY_STORAGE, pvKey.trim());
    localStorage.setItem(LLM_PROVIDER_STORAGE, provider);
    localStorage.setItem(OLLAMA_URL_STORAGE, ollamaUrl.trim());
    localStorage.setItem(OLLAMA_MODEL_STORAGE, ollamaModel.trim());
    localStorage.setItem(WAKE_ENABLED_STORAGE, wakeEnabled ? '1' : '0');

    setSavingProvider(true);
    try {
      await api.post('/llm/provider', {
        provider,
        ollama_url: ollamaUrl.trim(),
        ollama_model: ollamaModel.trim(),
      });
      const { data } = await api.get('/llm/provider');
      setProviderStatus(data);
    } catch (e) {
      setProviderStatus({ error: e?.response?.data?.detail || 'failed to update' });
    } finally {
      setSavingProvider(false);
    }

    // Reload the page so wake-word + provider settings re-init cleanly
    setTimeout(() => window.location.reload(), 400);
  };

  if (!open) return null;
  return (
    <div data-testid="settings-modal" className="fixed inset-0 z-50 flex items-center justify-center bg-obsidian/80 backdrop-blur-sm px-4">
      <div className="hud-frame border border-cyan-jarvis/30 bg-obsidian max-w-xl w-full p-6 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-5">
          <div className="font-hud uppercase tracking-[0.3em] text-cyan-jarvis text-glow text-lg">
            System Settings
          </div>
          <button data-testid="settings-close" onClick={onClose} className="text-[#E2F1F8]/50 hover:text-cyan-jarvis">
            <X size={18} />
          </button>
        </div>

        {/* Wake-word section */}
        <section className="mb-6">
          <div className="font-hud uppercase tracking-[0.2em] text-[11px] text-cyan-jarvis/80 mb-2">
            › Wake Word — “Hey JARVIS”
          </div>
          <p className="text-[11px] text-[#E2F1F8]/60 mb-3 leading-relaxed">
            Powered by Picovoice Porcupine — runs offline in your browser, no audio leaves your device.
            Get a <strong>free personal access key</strong> at{' '}
            <a href="https://console.picovoice.ai/" target="_blank" rel="noreferrer"
               className="text-cyan-jarvis underline">console.picovoice.ai <ExternalLink size={10} className="inline" /></a>.
          </p>
          <input
            data-testid="picovoice-key-input"
            type="password"
            value={pvKey}
            onChange={(e) => setPvKey(e.target.value)}
            placeholder="Picovoice access key (paste here)"
            className="w-full bg-obsidian border border-cyan-jarvis/25 focus:border-cyan-jarvis outline-none px-3 py-2 font-mono text-[12px] text-[#E2F1F8] mb-2"
          />
          <label className="flex items-center gap-2 text-[12px] text-[#E2F1F8]/80 cursor-pointer">
            <input
              data-testid="wake-enabled-toggle"
              type="checkbox"
              checked={wakeEnabled}
              onChange={(e) => setWakeEnabled(e.target.checked)}
              className="accent-cyan-jarvis"
            />
            Enable wake-word listening
          </label>
        </section>

        {/* LLM provider */}
        <section className="mb-6">
          <div className="font-hud uppercase tracking-[0.2em] text-[11px] text-cyan-jarvis/80 mb-2">
            › Cognitive Engine
          </div>
          <div className="flex gap-2 mb-3">
            <button
              data-testid="provider-emergent"
              onClick={() => setProvider('emergent')}
              className={`flex-1 font-hud uppercase tracking-[0.2em] text-[10px] px-3 py-2 border transition ${
                provider === 'emergent' ? 'border-cyan-jarvis bg-cyan-jarvis/10 text-cyan-jarvis' : 'border-cyan-jarvis/20 text-[#E2F1F8]/60'}`}>
              Cloud (Emergent)
            </button>
            <button
              data-testid="provider-ollama"
              onClick={() => setProvider('ollama')}
              className={`flex-1 font-hud uppercase tracking-[0.2em] text-[10px] px-3 py-2 border transition ${
                provider === 'ollama' ? 'border-cyan-jarvis bg-cyan-jarvis/10 text-cyan-jarvis' : 'border-cyan-jarvis/20 text-[#E2F1F8]/60'}`}>
              Local (Ollama)
            </button>
          </div>

          {provider === 'ollama' && (
            <div className="space-y-2">
              <input
                data-testid="ollama-url-input"
                value={ollamaUrl}
                onChange={(e) => setOllamaUrl(e.target.value)}
                placeholder="Ollama URL (default http://localhost:11434)"
                className="w-full bg-obsidian border border-cyan-jarvis/25 focus:border-cyan-jarvis outline-none px-3 py-2 font-mono text-[12px] text-[#E2F1F8]"
              />
              <input
                data-testid="ollama-model-input"
                value={ollamaModel}
                onChange={(e) => setOllamaModel(e.target.value)}
                placeholder="Model (e.g. llama3.1, qwen2.5, mistral)"
                className="w-full bg-obsidian border border-cyan-jarvis/25 focus:border-cyan-jarvis outline-none px-3 py-2 font-mono text-[12px] text-[#E2F1F8]"
              />
              <p className="text-[10px] text-[#E2F1F8]/40 leading-relaxed">
                Make sure <code className="text-cyan-jarvis">ollama serve</code> is running and the model is pulled
                (<code className="text-cyan-jarvis">ollama pull {ollamaModel || 'llama3.1'}</code>).
              </p>
            </div>
          )}

          {providerStatus && !providerStatus.error && (
            <div data-testid="provider-status" className="mt-2 text-[10px] font-hud uppercase tracking-[0.2em] text-[#E2F1F8]/50">
              Active: {providerStatus.provider} · {providerStatus.model || ''} {providerStatus.healthy ? '· ✓ healthy' : '· ⚠ unreachable'}
            </div>
          )}
          {providerStatus?.error && (
            <div className="mt-2 text-[10px] text-amber-warn">{providerStatus.error}</div>
          )}
        </section>

        {/* PWA install */}
        <section className="mb-6">
          <div className="font-hud uppercase tracking-[0.2em] text-[11px] text-cyan-jarvis/80 mb-2">
            › Install as App
          </div>
          {deferredInstall ? (
            <button
              data-testid="install-pwa-btn"
              onClick={onInstall}
              className="w-full font-hud uppercase tracking-[0.25em] text-[11px] text-obsidian bg-cyan-jarvis hover:bg-white px-4 py-2 flex items-center justify-center gap-2 transition">
              <Download size={12} /> Install JARVIS to home screen / desktop
            </button>
          ) : (
            <p className="text-[11px] text-[#E2F1F8]/50 leading-relaxed">
              On Android Chrome / Edge: tap the menu → "Install app". On iOS Safari: tap Share → "Add to Home Screen".
              On desktop: look for the install icon in your address bar.
            </p>
          )}
        </section>

        <div className="flex gap-2 justify-end pt-3 border-t border-cyan-jarvis/15">
          <button data-testid="settings-cancel" onClick={onClose}
                  className="font-hud uppercase tracking-[0.2em] text-[10px] px-4 py-2 border border-cyan-jarvis/30 text-[#E2F1F8]/70 hover:text-cyan-jarvis">
            Cancel
          </button>
          <button data-testid="settings-save" onClick={saveAll} disabled={savingProvider}
                  className="font-hud uppercase tracking-[0.25em] text-[11px] text-obsidian bg-cyan-jarvis hover:bg-white px-4 py-2 disabled:opacity-50">
            {savingProvider ? 'Saving…' : 'Save & Reload'}
          </button>
        </div>
      </div>
    </div>
  );
}
