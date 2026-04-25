# JARVIS — Windows Local Setup

Run JARVIS entirely on your Windows machine. Phone (or any other device on your Wi-Fi) can connect to it as a PWA.

## TL;DR — first-time install

1. Open **PowerShell as Administrator**
2. Run:
   ```powershell
   cd <wherever-you-cloned-this>\windows-local
   .\setup.ps1
   ```
   This installs Python, Node.js, MongoDB, and (optionally) Ollama using `winget`. It then installs all Python + Node dependencies.
3. Open `backend.env` and set your `EMERGENT_LLM_KEY` (or leave blank if you only want to use Ollama). Save as `..\backend\.env`.
4. Double-click **`start.bat`** — three windows pop open (Mongo, FastAPI backend, React frontend). Wait until you see "Compiled successfully" in the React window.
5. Browser auto-opens at <http://localhost:3000>.

## Use it from your phone

1. On your Windows PC, run `ipconfig` and copy your **IPv4 address** (e.g. `192.168.1.42`).
2. On your phone, connect to the **same Wi-Fi network**.
3. Open Chrome / Safari and visit `http://192.168.1.42:3000`.
4. Tap browser menu → **Add to Home Screen** / **Install app** — JARVIS becomes a standalone app icon.
5. Tap **Settings** (gear icon, top right) → paste a **Picovoice access key** ([free at console.picovoice.ai](https://console.picovoice.ai)) → enable wake-word → Save & Reload. Now say *"Jarvis…"* to start dictating.

> **First-time setup only**: you must run the React frontend with the right backend URL. If your Windows PC's IP is `192.168.1.42`, edit `..\frontend\.env` and set:
> ```
> REACT_APP_BACKEND_URL=http://192.168.1.42:8001
> ```
> The `setup.ps1` script writes this for you automatically.

## Use Ollama (fully local, no API costs)

```powershell
ollama pull llama3.1     # ~5 GB — one-time
ollama serve             # leave this running
```
Then in JARVIS → Settings → "Local (Ollama)" → save. All chat now runs on your GPU/CPU, never leaves your machine.

## Files in this folder

| File | Purpose |
|------|---------|
| `setup.ps1`        | One-shot installer — runs winget, pip install, yarn install, writes `.env` files |
| `start.bat`        | Launches MongoDB + backend + frontend in three windows |
| `start.ps1`        | Same as `start.bat` but PowerShell-native (handy if you've disabled `.bat`) |
| `stop.bat`         | Kills the three processes |
| `backend.env.example` | Template for `..\backend\.env` |
| `frontend.env.example`| Template for `..\frontend\.env` |

## Troubleshooting

* **"winget: command not found"** → you're on Windows 10 < 1809. Install [App Installer](https://apps.microsoft.com/detail/9NBLGGH4NNS1) from the Microsoft Store, then re-run `setup.ps1`.
* **MongoDB doesn't start** → run `mongod --dbpath C:\data\db` once manually so it creates its data folder.
* **Phone can't reach `192.168.1.42:3000`** → Windows Firewall is blocking. Allow inbound on TCP 3000 and 8001:
  ```powershell
  New-NetFirewallRule -Name JARVIS-frontend -DisplayName "JARVIS frontend" -Protocol TCP -LocalPort 3000 -Action Allow
  New-NetFirewallRule -Name JARVIS-backend  -DisplayName "JARVIS backend"  -Protocol TCP -LocalPort 8001 -Action Allow
  ```
  `setup.ps1` runs these automatically.
* **"Wake-word error" badge in JARVIS** → verify your Picovoice key, and make sure you allowed microphone access in the browser.
* **Ollama "unreachable"** → start `ollama serve` and pull the model first (`ollama pull llama3.1`).
