from common.base.baseMysql import BaseMySQLService
from domains.uploadFile.upload_file_model import UploadFileModel

class UploadFileRepository(BaseMySQLService[UploadFileModel]):
    def __init__(self):
        super().__init__(UploadFileModel)
