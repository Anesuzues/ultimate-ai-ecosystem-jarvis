/**
 * Wake-word + voice-input hook using Picovoice Porcupine ("Jarvis" built-in keyword).
 * The user's accessKey is read from localStorage. If absent, the hook stays disabled.
 */
import { useCallback, useEffect, useRef, useState } from 'react';
import { PorcupineWorker, BuiltInKeyword } from '@picovoice/porcupine-web';
import { WebVoiceProcessor } from '@picovoice/web-voice-processor';

export const PORCUPINE_KEY_STORAGE = 'jarvis_porcupine_key';

export function useWakeWord({ enabled, onWake }) {
  const [status, setStatus] = useState('idle'); // 'idle' | 'starting' | 'listening' | 'error'
  const [error, setError] = useState(null);
  const workerRef = useRef(null);

  const stop = useCallback(async () => {
    try {
      if (workerRef.current) {
        await WebVoiceProcessor.unsubscribe(workerRef.current);
        workerRef.current.terminate();
        workerRef.current = null;
      }
    } catch (e) { /* ignore */ }
    setStatus('idle');
  }, []);

  useEffect(() => {
    let cancelled = false;
    async function start() {
      const key = (localStorage.getItem(PORCUPINE_KEY_STORAGE) || '').trim();
      if (!enabled || !key) { setStatus('idle'); return; }
      setStatus('starting'); setError(null);
      try {
        const worker = await PorcupineWorker.create(
          key,
          [BuiltInKeyword.Jarvis],
          (detection) => { if (detection?.label) onWake?.(detection.label); },
          { publicPath: '/porcupine_params.pv', forceWrite: true },
        );
        if (cancelled) { worker.terminate(); return; }
        workerRef.current = worker;
        await WebVoiceProcessor.subscribe(worker);
        if (!cancelled) setStatus('listening');
      } catch (e) {
        setError(e?.message || String(e));
        setStatus('error');
      }
    }
    start();
    return () => { cancelled = true; stop(); };
  }, [enabled]);

  return { status, error, stop };
}
