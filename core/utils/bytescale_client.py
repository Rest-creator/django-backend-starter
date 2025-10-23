import requests
from django.conf import settings


class BytescaleClient:
    BASE_URL = f"https://api.bytescale.com/v2/accounts/{settings.BYTESCALE_ACCOUNT_ID}/uploads/form_data"
    HEADERS = {"Authorization": f"Bearer {settings.BYTESCALE_API_KEY}"}

    @classmethod
    def upload_file(cls, file_name: str, file_content: bytes, content_type: str) -> str:
        files = {"file": (file_name, file_content, content_type)}
        resp = requests.post(cls.BASE_URL, headers=cls.HEADERS, files=files, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if not data or "files" not in data or not data["files"]:
            raise RuntimeError("Bytescale response missing 'files'")
        url = data["files"][0].get("fileUrl")
        if not url:
            raise RuntimeError("Bytescale missing fileUrl")
        return url
