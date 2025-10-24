# Docker setup for uit-ro-transport-request

## 🐳 Docker Architecture

```
Internet → Port 80 → Nginx → Frontend (React) on /
                          → Backend (FastAPI) on /api/*
```

## 🚀 Quick Start

### Build and run the entire stack:
```bash
docker-compose up --build
```

### Run in background:
```bash
docker-compose up -d --build
```

### Stop the stack:
```bash
docker-compose down
```

### View logs:
```bash
docker-compose logs -f
docker-compose logs backend
docker-compose logs frontend
docker-compose logs nginx
```

## 📋 Services

- **Nginx** (Port 80): Reverse proxy and web server
- **Frontend**: React application (Vite dev server)
- **Backend**: FastAPI application

## 🌐 Access

- **Application**: http://localhost/
- **API**: http://localhost/api/
- **Health Check**: http://localhost/health

## 📁 Volume Mounts

- `./backend/attachments` → `/app/attachments` (uploaded files)
- `./backend/data` → `/app/data` (application data)

## 🛠️ Development

### Make changes to code:
- Backend: Edit files in `./backend/` - changes auto-reload
- Frontend: Edit files in `./frontend/` - changes auto-reload

### View real-time logs:
```bash
docker-compose logs -f backend
```

### Rebuild after major changes:
```bash
docker-compose down
docker-compose up --build
```

## 🔧 Configuration

### Environment Variables
- Backend: Set in `docker-compose.yaml` under `backend.environment`
- Frontend: Set in `docker-compose.yaml` under `frontend.environment`

### Nginx Configuration
- Edit `./nginx/nginx.conf` for reverse proxy settings
- Restart: `docker-compose restart nginx`

## 🔒 Security Notes

- Only port 80 is exposed externally
- Backend and frontend are isolated in internal network
- File uploads limited to 50MB (configurable in nginx.conf)