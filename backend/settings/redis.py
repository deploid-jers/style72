from redis.asyncio import Redis
from backend.settings.paths import REDIS_URL

redis = Redis.from_url(
    REDIS_URL,
    encoding="utf-8",
    decode_responses=True,
)
