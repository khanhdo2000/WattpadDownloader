# Wattpad Downloader - Deployment Guide

## Server Information
- **Server IP**: 31.97.70.110
- **Domain**: qc0k4ck0oooscwkskws8gg4o.31.97.70.110.sslip.io
- **SSH Access**: `ssh root@31.97.70.110`

## Architecture
- **Reverse Proxy**: Traefik (coolify-proxy container)
- **Application**: FastAPI (Python) running on port 80
- **Container Management**: Docker with Coolify
- **Network**: coolify network

## Container Configuration

### Current Working Container
```bash
Container Name: qc0k4ck0oooscwkskws8gg4o-fixed
Image: qc0k4ck0oooscwkskws8gg4o:549be9616234056fe4048806938bf305653956ad
Network: coolify
Port: 80 (internal)
```

### Traefik Labels (Working Configuration)
```yaml
traefik.enable: "true"
traefik.http.routers.http-0-qc0k4ck0oooscwkskws8gg4o.rule: "Host(`qc0k4ck0oooscwkskws8gg4o.31.97.70.110.sslip.io`) && PathPrefix(`/`)"
traefik.http.routers.http-0-qc0k4ck0oooscwkskws8gg4o.entrypoints: "http"
traefik.http.routers.http-0-qc0k4ck0oooscwkskws8gg4o.service: "http-0-qc0k4ck0oooscwkskws8gg4o"
traefik.http.services.http-0-qc0k4ck0oooscwkskws8gg4o.loadbalancer.server.port: "80"
traefik.http.middlewares.gzip.compress: "true"
traefik.http.routers.http-0-qc0k4ck0oooscwkskws8gg4o.middlewares: "gzip"
```

## Deployment Commands

### Deploy New Container
```bash
# Build and push image (if needed)
docker build -t qc0k4ck0oooscwkskws8gg4o:latest .
docker push qc0k4ck0oooscwkskws8gg4o:latest

# Deploy to server
ssh root@31.97.70.110 "docker run -d --name qc0k4ck0oooscwkskws8gg4o-new --network coolify \
  -l traefik.enable=true \
  -l traefik.http.routers.http-0-qc0k4ck0oooscwkskws8gg4o.rule='Host(\`qc0k4ck0oooscwkskws8gg4o.31.97.70.110.sslip.io\`) && PathPrefix(\`/\`)' \
  -l traefik.http.routers.http-0-qc0k4ck0oooscwkskws8gg4o.entrypoints=http \
  -l traefik.http.routers.http-0-qc0k4ck0oooscwkskws8gg4o.service=http-0-qc0k4ck0oooscwkskws8gg4o \
  -l traefik.http.services.http-0-qc0k4ck0oooscwkskws8gg4o.loadbalancer.server.port=80 \
  -l traefik.http.middlewares.gzip.compress=true \
  -l traefik.http.routers.http-0-qc0k4ck0oooscwkskws8gg4o.middlewares=gzip \
  qc0k4ck0oooscwkskws8gg4o:latest"
```

### Update Existing Container
```bash
# Stop old container
ssh root@31.97.70.110 "docker stop qc0k4ck0oooscwkskws8gg4o-fixed"

# Start new container
ssh root@31.97.70.110 "docker run -d --name qc0k4ck0oooscwkskws8gg4o-updated --network coolify \
  -l traefik.enable=true \
  -l traefik.http.routers.http-0-qc0k4ck0oooscwkskws8gg4o.rule='Host(\`qc0k4ck0oooscwkskws8gg4o.31.97.70.110.sslip.io\`) && PathPrefix(\`/\`)' \
  -l traefik.http.routers.http-0-qc0k4ck0oooscwkskws8gg4o.entrypoints=http \
  -l traefik.http.routers.http-0-qc0k4ck0oooscwkskws8gg4o.service=http-0-qc0k4ck0oooscwkskws8gg4o \
  -l traefik.http.services.http-0-qc0k4ck0oooscwkskws8gg4o.loadbalancer.server.port=80 \
  -l traefik.http.middlewares.gzip.compress=true \
  -l traefik.http.routers.http-0-qc0k4ck0oooscwkskws8gg4o.middlewares=gzip \
  qc0k4ck0oooscwkskws8gg4o:latest"

# Remove old container
ssh root@31.97.70.110 "docker rm qc0k4ck0oooscwkskws8gg4o-fixed"
```

## Health Checks

### Check Application Status
```bash
# Check if container is running
ssh root@31.97.70.110 "docker ps | grep qc0k4ck0oooscwkskws8gg4o"

# Check application logs
ssh root@31.97.70.110 "docker logs qc0k4ck0oooscwkskws8gg4o-fixed --tail 20"

# Test local connectivity
ssh root@31.97.70.110 "curl -v http://localhost:80"
```

### Check External Access
```bash
# Test from local machine
curl -v http://qc0k4ck0oooscwkskws8gg4o.31.97.70.110.sslip.io/

# Check response headers
curl -I http://qc0k4ck0oooscwkskws8gg4o.31.97.70.110.sslip.io/
```

## Monitoring

### Check Traefik Status
```bash
# Check Traefik logs
ssh root@31.97.70.110 "docker logs coolify-proxy --tail 20"

# Check Traefik configuration
ssh root@31.97.70.110 "docker exec coolify-proxy cat /traefik/dynamic/default_redirect_503.yaml"
```

### Check System Resources
```bash
# Check Docker status
ssh root@31.97.70.110 "systemctl status docker"

# Check container resource usage
ssh root@31.97.70.110 "docker stats --no-stream"
```

## Rollback Procedure

If deployment fails:
```bash
# Stop new container
ssh root@31.97.70.110 "docker stop qc0k4ck0oooscwkskws8gg4o-new"

# Start previous working container
ssh root@31.97.70.110 "docker start qc0k4ck0oooscwkskws8gg4o-fixed"
```

## Important Notes

1. **Port Configuration**: Always ensure Traefik routes to port 80, not 3000
2. **Network**: Container must be on the `coolify` network
3. **Labels**: Traefik labels must match the domain and service configuration
4. **Testing**: Always test both local and external connectivity
5. **Backup**: Keep previous working containers for quick rollback

## Troubleshooting

See [DEBUGGING.md](./DEBUGGING.md) for detailed troubleshooting steps.

## Last Updated
- Date: 2025-01-19
- Status: Working
- Container: qc0k4ck0oooscwkskws8gg4o-fixed
- Issue Fixed: Bad Gateway Error (502)
