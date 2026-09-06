from typing import Tuple, Dict, Any
from minio import Minio
from app.core.config import settings


class StorageService:

    @staticmethod
    def get_client() -> Minio:
        return Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )

    @classmethod
    def check_readiness(cls) -> Tuple[bool, Dict[str, Any]]:
        """
        Verifies MinIO storage connectivity without exposing credentials.
        """
        try:
            client = cls.get_client()
            bucket_exists = client.bucket_exists(settings.MINIO_BUCKET)
            if not bucket_exists:
                client.make_bucket(settings.MINIO_BUCKET)
            return True, {"status": "connected", "bucket": settings.MINIO_BUCKET}
        except Exception as e:
            return False, {"status": "error", "detail": str(e)}
