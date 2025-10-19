# Wattpad Downloader - Debugging Guide

## Common Issues and Solutions

### Bad Gateway Error (502)

**Symptoms:**
- Website returns "Bad Gateway" error
- Application appears to be running but not accessible
- Traefik logs show routing errors

**Root Cause:**
- Traefik routing configuration mismatch
- Container configured for wrong port

**Solution:**
1. Check container port configuration:
   ```bash
   docker inspect <container_name> | grep -A 20 -B 5 Labels
   ```

2. Verify application port:
   - Check Dockerfile: `EXPOSE 80`
   - Check main.py: `uvicorn.run("main:app", host="0.0.0.0", port=80)`

3. Fix Traefik labels:
   ```bash
   # Stop misconfigured container
   docker stop <container_name>
   
   # Create new container with correct port
   docker run -d --name <new_name> --network coolify \
     -l traefik.enable=true \
     -l traefik.http.routers.<router_name>.rule='Host(`your-domain.com`) && PathPrefix(`/`)' \
     -l traefik.http.routers.<router_name>.entrypoints=http \
     -l traefik.http.routers.<router_name>.service=<service_name> \
     -l traefik.http.services.<service_name>.loadbalancer.server.port=80 \
     -l traefik.http.middlewares.gzip.compress=true \
     -l traefik.http.routers.<router_name>.middlewares=gzip \
     <image_name>
   ```

4. Test the fix:
   ```bash
   curl -v http://your-domain.com/
   ```

5. Clean up old container:
   ```bash
   docker rm <old_container_name>
   ```

### Container Not Starting

**Check logs:**
```bash
docker logs <container_name>
```

**Common issues:**
- Port conflicts
- Missing environment variables
- Network connectivity issues

### Traefik Configuration Issues

**Check Traefik logs:**
```bash
docker logs coolify-proxy
```

**Common errors:**
- `EntryPoint doesn't exist` - Check entry point configuration
- `No valid entryPoint for this router` - Router configuration issue
- `unable to find the IP address for the container` - Container networking issue

## Server Management Commands

### Check running containers
```bash
docker ps -a
```

### Check container logs
```bash
docker logs <container_name> --tail 50
```

### Check Traefik configuration
```bash
docker exec coolify-proxy cat /traefik/dynamic/default_redirect_503.yaml
```

### Test connectivity
```bash
# Test local connectivity
curl -v http://localhost:80

# Test external connectivity
curl -v http://your-domain.com/
```

## Deployment Checklist

1. ✅ Container is running
2. ✅ Application is listening on correct port (80)
3. ✅ Traefik labels are correctly configured
4. ✅ Port mapping matches application port
5. ✅ Network connectivity is working
6. ✅ Domain resolution is working
7. ✅ SSL/TLS is configured (if using HTTPS)

## Troubleshooting Steps

1. **Check container status**: `docker ps -a`
2. **Check application logs**: `docker logs <container_name>`
3. **Check Traefik logs**: `docker logs coolify-proxy`
4. **Verify port configuration**: Check Dockerfile and main.py
5. **Test local connectivity**: `curl localhost:80`
6. **Test external connectivity**: `curl your-domain.com`
7. **Check Traefik labels**: `docker inspect <container_name> | grep -i traefik`

## Important Notes

- The application runs on port 80 inside the container
- Traefik must be configured to route to port 80, not 3000
- Always test both local and external connectivity
- Keep old containers for rollback if needed
- Document any custom configurations

## Last Updated
- Date: 2025-01-19
- Issue: Bad Gateway Error (502)
- Solution: Fixed Traefik port configuration from 3000 to 80
