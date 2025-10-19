# Wattpad Downloader

A web application that allows users to download Wattpad stories as PDF or EPUB files.

## Features

- Download Wattpad stories as PDF or EPUB
- Support for both free and paid stories (with authentication)
- Image downloading support
- RTL language support (Arabic, etc.)
- Send to Kindle support
- Discord bot integration
- High-speed PDF downloads for donators

## Architecture

- **Frontend**: SvelteKit
- **Backend**: FastAPI (Python)
- **PDF Generation**: WeasyPrint
- **EPUB Generation**: ebooklib
- **Deployment**: Docker with Traefik reverse proxy

## Quick Start

### Local Development

1. **Frontend**:
   ```bash
   cd src/frontend
   npm install
   npm run dev
   ```

2. **Backend**:
   ```bash
   cd src/api
   pip install -r requirements.txt
   python src/main.py
   ```

### Docker Deployment

```bash
# Build the image
docker build -t wattpad-downloader .

# Run locally
docker run -p 80:80 wattpad-downloader
```

## Production Deployment

The application is deployed on:
- **Server**: 31.97.70.110
- **Domain**: qc0k4ck0oooscwkskws8gg4o.31.97.70.110.sslip.io
- **SSH**: `ssh root@31.97.70.110`

### Deployment Options

1. **Coolify (Recommended)**: See [COOLIFY-DEPLOYMENT.md](./COOLIFY-DEPLOYMENT.md)
2. **Manual Docker**: See [DEPLOYMENT.md](./DEPLOYMENT.md)
3. **Docker Compose**: Use the included `docker-compose.yml`

## Troubleshooting

If you encounter issues, see [DEBUGGING.md](./DEBUGGING.md) for common problems and solutions.

## Recent Fixes

- **2025-01-19**: Fixed Bad Gateway Error (502) - Traefik port configuration issue
- **2024-12-24**: Less Errors, Throttled Downloads
- **2024-11-24**: Paste Links support
- **2024-11-24**: Send to Kindle Support
- **2024-11-24**: Fixed Image Downloads
- **2024-10-24**: Discord Bot integration
- **2024-07-24**: RTL Language support
- **2024-06-24**: Authenticated Downloads
- **2024-06-24**: Image Downloading

## Support

- **Discord**: [Join our Discord](https://discord.gg/P9RHC4KCwd)
- **Donate**: [Buy me a Coffee](https://buymeacoffee.com/theonlywayup)

## License

Copyright © 2025 - All rights reserved by [Dhanush R](https://rambhat.la)