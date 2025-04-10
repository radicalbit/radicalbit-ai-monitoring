import hashlib


def hash_key(key: str) -> str:
    return hashlib.sha3_256(key.encode('utf-8')).hexdigest()
