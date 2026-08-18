from typing import Optional
from common.base.baseDTO import BaseDTO

class UploadFileResponseDTO(BaseDTO):
    id: str  # Override because our ID is UUID string
    original_name: str
    file_url: str
    mime_type: str
    file_size: int
    
    class Config:
        from_attributes = True
