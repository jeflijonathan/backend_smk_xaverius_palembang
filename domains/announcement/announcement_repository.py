from sqlalchemy.orm import joinedload
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from common.base.baseMysql import BaseMySQLService
from domains.announcement.announcement_model import AnnouncementModel, AnnouncementUserLogModel


class AnnouncementRepository(BaseMySQLService[AnnouncementModel]):
    def __init__(self):
        super().__init__(AnnouncementModel)

    def find_all(
        self, 
        db: Session, 
        where: Optional[Dict[str, Any]] = None, 
        paginator: Optional[Dict[str, int]] = None
    ) -> List[AnnouncementModel]:
        filter_data = {"query": where or {}}
        options = [joinedload(AnnouncementModel.user_logs)]
        return self.find(db, filter_data, paginator, options)

    def count_all(self, db: Session) -> int:
        # PERBAIKAN: Tambahkan parameter {} agar sesuai dengan BaseMySQLService.count()
        return self.count(db, {})

    def find_by_id(self, db: Session, id_announcement: str) -> Optional[AnnouncementModel]:
        options = [joinedload(AnnouncementModel.user_logs)]
        return self.find_one(db, {"id_announcement": id_announcement}, options)