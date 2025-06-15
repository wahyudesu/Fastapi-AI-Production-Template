import time
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, throttle_rate: int = 60):
        super().__init__(app)
        self.throttle_rate = throttle_rate
        self.request_log = {}  # Track timestamps per IP

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()

        # Clean up old request logs older than 60 seconds
        self.request_log = {
            ip: [ts for ts in times if ts > now - 60]
            for ip, times in self.request_log.items()
        }

        ip_history = self.request_log.get(client_ip, [])

        if len(ip_history) >= self.throttle_rate:
            raise HTTPException(status_code=429, detail="Too many requests")

        ip_history.append(now)
        self.request_log[client_ip] = ip_history

        return await call_next(request)