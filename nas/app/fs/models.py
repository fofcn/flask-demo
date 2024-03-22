from sqlalchemy import Column, DateTime, Integer, SmallInteger, String
from .. import db
from ..common import dict_mixin

class FileInfo(db.Model, dict_mixin.DictMixIn):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'file_info'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='primary key')
    user_id = Column(Integer, nullable=False, comment='user id')
    parent_id = Column(Integer, nullable=False, comment='parent directory id, 0 for top level directory, others for a specific directory')
    orgi_filename  = Column(String, nullable=False, default='', comment='original filename')
    filename = Column(String, nullable=False, default='', comment='storage filename')
    file_type = Column(SmallInteger, nullable=False, default=1, comment='file type: 1 for file, 2 for directory')
    content_type = Column(SmallInteger, nullable=False, default=0, comment='content type, 0 for dir, 1 for photos, 2 for videos, ...')
    deleted = Column(Integer, nullable=False, default=0, comment='is deleted or not, 0 for no, 1 for yes')
    file_created_time = Column(DateTime, nullable=False, comment='file created time')
    file_modified_time = Column(DateTime, nullable=False, comment='file modified time')
    created_time = Column(DateTime, nullable=False, comment='record created time')
    modified_time = Column(DateTime, nullable=True, comment='record modified time')
