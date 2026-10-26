# Runtime trace: count calls to RateLimiter.check_rate_limit while requests run
# through the app in-process. Wraps the method; no source files are modified.
import sys
sys.path.insert(0, ".")
import safety.rate_limiter as rl
from fastapi.testclient import TestClient

calls = []
original = rl.RateLimiter.check_rate_limit
def traced(self, *args, **kwargs):
    calls.append((args, kwargs))
    return original(self, *args, **kwargs)
rl.RateLimiter.check_rate_limit = traced

from api.main import app
print("middleware stack:", [m.cls.__name__ for m in app.user_middleware])
routes = sorted({getattr(r, "path", "?") for r in app.routes})
print("route count:", len(routes))
client = TestClient(app)
statuses = {}
for path in ["/", "/health"]:
    for _ in range(20):
        r = client.get(path)
        statuses.setdefault(path, {}).setdefault(r.status_code, 0)
        statuses[path][r.status_code] += 1
print("statuses:", statuses)
print("sample headers GET /:", {k: v for k, v in client.get("/").headers.items() if "ratelimit" in k.lower() or k.lower() in ("x-request-id",)})
print("check_rate_limit calls observed:", len(calls))
