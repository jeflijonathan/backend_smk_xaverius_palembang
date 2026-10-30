from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from domains.announcement.announcement_repository import AnnouncementRepository
from domains.announcement.announcement_model import AnnouncementModel
from domains.announcement.dto.announcement_dto import AnnouncementCreateDTO, AnnouncementUpdateDTO

from domains.announcement.announcement_model import AnnouncementUserLogModel

class AnnouncementService:
    def __init__(self):
        self.repository = AnnouncementRepository()

    def get_all(self, db: Session, paginator: Optional[Dict[str, int]] = None) -> List[AnnouncementModel]:
        return self.repository.find_all(db, paginator=paginator)

    def count_all(self, db: Session) -> int:
        return self.repository.count_all(db)

    def get_by_id(self, db: Session, id_announcement: str) -> Optional[AnnouncementModel]:
        return self.repository.find_by_id(db, id_announcement)

    def create(self, db: Session, data: AnnouncementCreateDTO) -> AnnouncementModel:
        record_data = data.model_dump(exclude={"id_user"})
        record = self.repository.create(db, record_data)
        
        # Log the creation action
        if data.id_user:
            log_entry = AnnouncementUserLogModel(
                id_announcement=record.id_announcement,
                id_user=data.id_user,
                action="created"
            )
            db.add(log_entry)
            db.commit()
            
        return record

    def update(self, db: Session, id_announcement: str, data: AnnouncementUpdateDTO) -> Optional[AnnouncementModel]:
        record = self.repository.find_by_id(db, id_announcement)
        if not record:
            return None
            
        update_data = data.model_dump(exclude_unset=True)
        id_user = update_data.pop("id_user", None)
        
        updated_record = self.repository.update(db, {"id_announcement": id_announcement}, update_data)
        
        # Log the update action
        if id_user:
            log_entry = AnnouncementUserLogModel(
                id_announcement=id_announcement,
                id_user=id_user,
                action="updated"
            )
            db.add(log_entry)
            db.commit()
            
        return updated_record

    def delete(self, db: Session, id_announcement: str) -> Optional[AnnouncementModel]:
        record = self.repository.find_by_id(db, id_announcement)
        if not record:
            return None
            
        self.repository.delete(db, {"id_announcement": id_announcement})
        return record
