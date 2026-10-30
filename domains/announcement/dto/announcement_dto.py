from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class AnnouncementBaseDTO(BaseModel):
    title: str
    description: Optional[str] = None
    url_drive: Optional[str] = None

class AnnouncementCreateDTO(AnnouncementBaseDTO):
    id_user: str

class AnnouncementUpdateDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    url_drive: Optional[str] = None
    id_user: Optional[str] = None

class AnnouncementUserLogResponseDTO(BaseModel):
    id_log: str
    action: str
    created_at: datetime
    # We can include basic user info if needed
    id_user: str
    
    model_config = ConfigDict(from_attributes=True)

class AnnouncementResponseDTO(AnnouncementBaseDTO):
    id_announcement: str
    created_at: datetime
    updated_at: datetime
    user_logs: list[AnnouncementUserLogResponseDTO] = []
    
    model_config = ConfigDict(from_attributes=True)
