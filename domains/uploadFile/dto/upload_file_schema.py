from typing import Optional, List
from pydantic import BaseModel
from common.base.baseDTO import BaseDTO

class BulkDeleteDTO(BaseModel):
    ids: List[str]

class UploadFileResponseDTO(BaseDTO):
    id: str  # Override because our ID is UUID string
    original_name: str
    file_url: str
    mime_type: str
    file_size: int

    class Config:
        from_attributes = True

# Alias for convenience
UploadFileResponse = UploadFileResponseDTO

