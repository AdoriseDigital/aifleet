# VPS & Cloudflare Master Topology

This document establishes the system configuration, reverse proxy routing, CORS handling protocols, and local file storage paths for the **Adorise Digital** application suite deployed on the Netcup VPS (`185.194.142.32`).

---

## 1. Active Application Ports
The following internal microservices are running on the VPS local loopback interface:

| Port | Service Name | Purpose / Function | Systemd Daemon |
| :--- | :--- | :--- | :--- |
| **4000** | Adorise Social Scheduler | Express backend engine handling social queue posting and Buffer API publishing. | `social-scheduler.service` |
| **6000** | Adorise Scout API | Fastify backend scraper controller triggering Playwright search jobs. | `scout.service` |
| **5678** | n8n Core Engine | Node-based n8n webhook and workflow execution framework. | Docker container |
| **3001** | ClipCalm Ingestor | ClipCalm video editing pipeline (Ingestion API). | `clipcalm.service` |
| **8000** | DearMee Agent Engine | Hermes conversational core AI agent using MiniMax M2/M3 API. | `dearmee-agent.service` |

---

## 2. Nginx Reverse Proxy Routing Topology
Nginx is listening on Ports `80` (HTTP) and `443` (HTTPS) under the virtual host `api.adorisedigital.com` (proxied securely through Cloudflare in SSL **Full (Strict)** mode).

### Active Proxy Configurations:
Path: `/etc/nginx/sites-available/social.adorisedigital.com`

- **Scout Scraper API Routing:**
  - **Rule:** `location /api/v1/`
  - **Proxy Target:** `http://127.0.0.1:6000;`
- **Scout Hunter Webhook Route:**
  - **Rule:** `location = /webhook/scout-hunter`
  - **Proxy Target:** `http://127.0.0.1:5678/webhook/5c0a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c/webhooktrigger/scout-hunter;` (maps directly to active n8n workflow).
- **n8n General Webhooks:**
  - **Rule:** `location /webhook/`
  - **Proxy Target:** `http://127.0.0.1:5678;`
- **DearMee Agent Gateway:**
  - **Rule:** `location /api/agent/`
  - **Proxy Target:** `http://127.0.0.1:5678;` (routed temporarily to n8n workflow node, or `http://127.0.0.1:8000` Hermes).
- **ClipCalm Processor:**
  - **Rule:** `location /api/process-clip`
  - **Proxy Target:** `http://127.0.0.1:3001;`
- **Social Scheduler Catch-All:**
  - **Rule:** `location /`
  - **Proxy Target:** `http://127.0.0.1:4000;`

---

## 3. CORS Handling & Security Protocol
To avoid duplicate CORS header rejections or origin mismatches in browsers (e.g. Chrome/Firefox blockages):

- **Application-Level CORS Disabled:** Local CORS plugins/headers inside the Fastify API (`scout/src/api/server.js`) and Express app (`social-scheduler/scheduler.js`) files have been commented out or restricted.
- **Dynamic Nginx CORS Policy:** CORS headers are injected dynamically at the Nginx location blocks for preflight handshakes:
  ```nginx
  add_header 'Access-Control-Allow-Origin' '$http_origin' always;
  add_header 'Access-Control-Allow-Credentials' 'true' always;
  add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE' always;
  add_header 'Access-Control-Allow-Headers' 'X-Requested-With,Content-Type,Authorization' always;

  if ($request_method = 'OPTIONS') {
      return 204;
  }
  ```

---

## 4. VPS File System Storage Paths
Vertical video binaries deployed through the Social Scheduler queue interface are saved directly to the local storage disk:

- **Absolute Queue Folder Path:** `/opt/mega-stack/social-scheduler/queue/`
- **Manifest DB Mapping File:** `/opt/mega-stack/social-scheduler/manifest.json`

- Node 1-2: Social Radar & Ingestion Bridge
- Node 3-4: pSEO Generation & Indexing
- Node 5-6: Frontend UI Audit (Completed: interactive outreach dispatcher, 13-book preview modal, HTTPS API route normalization, and ClipCalm port reference fix)
