from pydantic import BaseModel, Field

class SendMessageDTO(BaseModel):
    to_phone: str = Field(..., description="Phone number to send the message to (e.g., 628123456789)")
    message: str = Field(..., description="Text message to send")
