from google.cloud import storage
from app.config import GCS_BUCKET


def get_bucket():
    if not GCS_BUCKET:
        raise ValueError("GCS_BUCKET environment variable is not set")
    client = storage.Client()
    return client.bucket(GCS_BUCKET)


def upload_file(
    blob_name: str,
    data: bytes,
    content_type: str | None = None,
) -> str:
    bucket = get_bucket()
    blob = bucket.blob(blob_name)
    blob.upload_from_string(data, content_type=content_type)
    return f"gs://{GCS_BUCKET}/{blob_name}"


def download_file(blob_name: str) -> bytes:
    bucket = get_bucket()
    blob = bucket.blob(blob_name)
    return blob.download_as_bytes()


def delete_file(blob_name: str) -> None:
    bucket = get_bucket()
    blob = bucket.blob(blob_name)
    blob.delete()
