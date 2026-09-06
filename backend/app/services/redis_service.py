from typing import Tuple, Dict, Any
import redis
from app.core.config import settings


class RedisService:

    @staticmethod
    def get_client() -> redis.Redis:
        return redis.Redis.from_url(settings.get_redis_url(), socket_timeout=3)

    @classmethod
    def check_readiness(cls) -> Tuple[bool, Dict[str, Any]]:
        """
        Verifies Redis server connectivity without exposing secrets.
        """
        try:
            client = cls.get_client()
            response = client.ping()
            if response:
                return True, {"status": "connected"}
            return False, {"status": "unresponsive"}
        except Exception as e:
            return False, {"status": "error", "detail": str(e)}
