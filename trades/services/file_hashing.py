import hashlib


def compute_file_hash(file_obj) -> str:
    """
    Compute SHA256 hash of uploaded file content.
    File pointer will be reset after reading.
    """
    hasher = hashlib.sha256()

    for chunk in file_obj.chunks():
        hasher.update(chunk)

    file_obj.seek(0)
    return hasher.hexdigest()
