from fastapi import Request, HTTPException
from .logger import logger
from starlette.middleware.base import BaseHTTPMiddleware
import time

class Middleware(BaseHTTPMiddleware):
    def __init__(self, app, throttle_rate: int = 60):
        super().__init__(app)
        self.throttle_rate = throttle_rate
        self.request_log = {}  # Track timestamps per IP

    async def dispatch(self, request: Request, call_next):
        # Rate limiting logic
        client_ip = request.client.host
        now = time.time()
        self.request_log = {
            ip: [ts for ts in times if ts > now - 60]
            for ip, times in self.request_log.items()
        }
        ip_history = self.request_log.get(client_ip, [])
        if len(ip_history) >= self.throttle_rate:
            raise HTTPException(status_code=429, detail="Too many requests")
        ip_history.append(now)
        self.request_log[client_ip] = ip_history

        # Logging logic
        start = time.time()
        response = await call_next(request)
        process_time = time.time() - start
        log_dict = {
            'url': request.url.path,
            'method': request.method,
            'process_time': process_time
        }
        logger.info(log_dict, extra=log_dict)
        return response