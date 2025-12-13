# secure_json.py
import json
import base64

# 🔑 key cố định – giữ nguyên cho mọi platform
SECRET_KEY = b"bkcloud-secret-key"

def _xor(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

def secure_json_dump(data, path):
    try:
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        encrypted = _xor(raw, SECRET_KEY)
        encoded = base64.b64encode(encrypted)
        with open(path, "wb") as f:
            f.write(encoded)
    except Exception as e:
        print(f"[!] Failed to write {path}: {e}")

def secure_json_load(path):
    try:
        with open(path, "rb") as f:
            encoded = f.read()
        encrypted = base64.b64decode(encoded)
        raw = _xor(encrypted, SECRET_KEY)
        return json.loads(raw.decode("utf-8"))
    except Exception as e:
        print(f"[!] Failed to read {path}: {e}")
        return {}
