import os
import shutil
import uuid
from typing import Tuple

# Define magic numbers for allowed types
MAGIC_NUMBERS = {
    "ffd8ffe0": "image/jpeg",
    "ffd8ffe1": "image/jpeg",
    "ffd8ffe2": "image/jpeg",
    "ffd8ffee": "image/jpeg",
    "ffd8ffdb": "image/jpeg",
    "89504e47": "image/png",
    "25504446": "application/pdf"
}

def validate_magic_number(file_path: str) -> Tuple[bool, str]:
    """
    Reads the first few bytes of the file and compares them against known signatures.
    Returns (is_valid, mime_type).
    """
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4)
            hex_bytes = header.hex()
            
            # Check for matches in our dictionary
            for magic, mime in MAGIC_NUMBERS.items():
                if hex_bytes.startswith(magic):
                    return True, mime
            return False, "Unknown or invalid magic number"
    except Exception as e:
        return False, str(e)

def move_to_permanent_storage(temp_path: str, original_name: str, permanent_dir: str = "uploads/permanent") -> str:
    """
    Moves file from temp to permanent directory with a UUID4 name to avoid collisions.
    Returns the new relative path/URL.
    """
    os.makedirs(permanent_dir, exist_ok=True)
    ext = os.path.splitext(original_name)[1]
    new_filename = f"{uuid.uuid4()}{ext}"
    permanent_path = os.path.join(permanent_dir, new_filename)
    
    shutil.move(temp_path, permanent_path)
    return permanent_path.replace("\\", "/")

def cleanup_temp_file(temp_path: str) -> None:
    """
    Safely removes the temporary file.
    """
    try:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    except Exception:
        pass  # Fail-safe, do not raise internal errors

def move_temp_to_primary(temp_filename: str, location_name: str, base_upload_dir: str = "uploads") -> str:
    """
    Moves a file from temp directory to a primary directory based on location_name.
    Example: move_temp_to_primary("saidjaidsa.jpg", "users") -> moves to "uploads/users/saidjaidsa.jpg"
    Returns the new relative path/URL.
    """
    temp_path = os.path.join(base_upload_dir, "temp", temp_filename)
    if not os.path.exists(temp_path):
        raise FileNotFoundError(f"Temp file {temp_filename} not found.")

    primary_dir = os.path.join(base_upload_dir, location_name)
    os.makedirs(primary_dir, exist_ok=True)
    
    primary_path = os.path.join(primary_dir, temp_filename)
    shutil.move(temp_path, primary_path)
    return primary_path.replace("\\", "/")
