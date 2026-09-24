from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from common.base.baseMysql import BaseMySQLService
from domains.teacherSubject.teacher_subject_model import TeacherSubjectModel


class TeacherSubjectRepository(BaseMySQLService[TeacherSubjectModel]):
    def __init__(self):
        super().__init__(TeacherSubjectModel)

    def find_all(self, db: Session, where: Dict[str, Any] = None) -> List[TeacherSubjectModel]:
        filter_data = {"query": where or {}}
        return self.find(db, filter_data)

    def find_by_id(self, db: Session, id_teacher_subject: str) -> Optional[TeacherSubjectModel]:
        return self.find_one(db, {"id_teacher_subject": id_teacher_subject})
