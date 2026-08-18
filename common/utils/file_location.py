import os
import re
import shutil
import uuid
from datetime import datetime
from typing import Optional


BASE_UPLOAD_DIR = "uploads"
TEMP_DIR = os.path.join(BASE_UPLOAD_DIR, "temp")


def _sanitize_filename(filename: str) -> str:
    """
    Remove or replace characters that are unsafe for file systems.
    Keeps alphanumeric, dots, hyphens, and underscores.
    """
    name, ext = os.path.splitext(filename)
    name = re.sub(r'[^\w\-.]', '_', name)      # replace unsafe chars
    name = re.sub(r'_+', '_', name).strip('_')  # collapse multiple underscores
    return f"{name}{ext.lower()}"


def generate_stored_filename(original_name: str) -> str:
    """
    Generate a unique, human-readable filename for storage.
    Format: YYYYMMDD_HHmmss_<short-uuid>_<sanitized-original-name>
    Example: 20260707_115500_a1b2c3d4_foto_profil.jpg
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    short_id = uuid.uuid4().hex[:8]
    safe_name = _sanitize_filename(original_name)
    return f"{timestamp}_{short_id}_{safe_name}"


def move_temp_to_location(
    temp_filename: str,
    destination: str,
    new_filename: Optional[str] = None,
) -> dict:
    """
    Move an uploaded file from temp to a structured destination folder.

    Args:
        temp_filename: The filename inside uploads/temp (returned by upload endpoint).
        destination:   Sub-path under uploads/ where the file should live.
                       Examples: "users/avatars", "classroom/documents", "presensi/photos"
        new_filename:  Optional custom filename. If omitted, the temp_filename is kept.

    Returns:
        dict with 'file_url' (forward-slash relative path) and 'filename'.

    Raises:
        FileNotFoundError: If the temp file doesn't exist.
        ValueError:        If the destination resolves outside the uploads directory.
    """
    temp_path = os.path.join(TEMP_DIR, temp_filename)

    if not os.path.exists(temp_path):
        raise FileNotFoundError(f"Temp file '{temp_filename}' not found.")

    # Prevent path traversal attacks
    dest_dir = os.path.join(BASE_UPLOAD_DIR, destination)
    dest_dir_abs = os.path.abspath(dest_dir)
    base_abs = os.path.abspath(BASE_UPLOAD_DIR)

    if not dest_dir_abs.startswith(base_abs):
        raise ValueError("Invalid destination: path traversal detected.")

    os.makedirs(dest_dir, exist_ok=True)

    final_filename = new_filename if new_filename else temp_filename
    dest_path = os.path.join(dest_dir, final_filename)

    shutil.move(temp_path, dest_path)

    file_url = dest_path.replace("\\", "/")

    return {
        "file_url": file_url,
        "filename": final_filename,
    }
