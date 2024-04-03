
import datetime
import os
import time
import uuid
from flask import current_app, request
from flask_jwt_extended import current_user
from . import file
from ..auth import models, dto
from . import models, enums
from .. import user
from ..common import const, dto, jwt_wrapper
from .. import db

@file.route('/list', methods=['GET'])
@jwt_wrapper.jwt_required_ext(optional=False)
def listFiles():
    """
    summary:list files or directories
    consumes:
      - application/json
    security:
      - bearerAuth: []
    parameters:
      - in: query
        name: per_page
        schema:
          type: integer
          default: 10
      - in: query
        name: page
        schema:
          type: integer
          default: 1
    responses:
      200:
        description: return file list of the user
      content:
        application/json:
          scehma:
            type: array
            items:
            $ref: '#/components/schemas/FileInfo'
      401:
        description: Unauthorized

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
  schemas:
    FileInfo: 
      type: object
      properties:
        
    """
    curUser = user.models.User.query.filter_by(id=current_user.id).one_or_none()
    if not curUser:
        return dto.make_auth_401()
    
    perPage = request.args.get('per_page', type=int, default=10)  
    page = request.args.get('page', type=int, default=1)  

    pagination = models.FileInfo.query.filter_by(user_id=current_user.id, deleted=0, parent_id=0).paginate(page=page, per_page=perPage, error_out=False)
    fileInfoList = [fileInfo.to_dict() for fileInfo in pagination.items]  
    return dto.make_success_resp(1, fileInfoList)


@file.route('', methods=['POST'])
@jwt_wrapper.jwt_required_ext(optional=False)
def uploadFile():
    save_path = request.form['save_path']
    parent_id = request.form['parent_id']
    created_time = request.form['created_time']
    modified_time = request.form['modified_time']
    content_type = request.form['content_type']
    file_type = request.form['file_type']
    original_filename = f.filename
    f = request.files['file']

    filename = uuid.uuid1()
    abs_path = f'{save_path}/{filename}'
    f.save(abs_path)

    fileinfo = models.FileInfo(
        user_id = current_user.id,
        parent_id = parent_id,
        orgi_filename  = original_filename,
        filename = filename,
        file_type = file_type,
        content_type = content_type,
        deleted = const.NO_DELETED,
        file_created_time = created_time,
        file_modified_time = modified_time,
        created_time = datetime.now(),
    )

    db.session.add(fileinfo)

    return dto.make_success_resp(2, None)

@file.route('/dir', methods=['POST'])
@jwt_wrapper.jwt_required_ext(optional=False)
def create_directory():
    parent_id = request.json.get('parent_id')
    dir_name = request.json.get('dir_name')
    user_id = current_user.id

    parent_dir = models.FileInfo.query.filter_by(id, deleted=const.NO_DELETED).one_or_none()
    if not parent_dir:
        return dto.make_response(2, 'parent direcotry is not existing ')


    # check parent_id and direcotry exists
    # it's better to add a distributed lock here
    dir = models.FileInfo.query.filter_by(user_id=user_id, 
                                    parent_id=parent_id, 
                                    file_type=enums.FileType.DIRECTORY, 
                                    content_type=enums.ContentType.DIRECTORY, 
                                    deleted=const.NO_DELETED).one_or_none()
    if dir:
        return dto.make_response(2, f'direcotry has already existed in {parent_dir.orgi_filename}')
    
    dir_path = current_app.config['NAS_STORE_PATH']

    os.mkdir(dir_path + '/' + dir_name)
    fileinfo = models.FileInfo(
        user_id = current_user.id,
        parent_id = parent_id,
        orgi_filename  = dir_name,
        filename = uuid.uuid1(),
        file_type = enums.FileType.DIRECTORY,
        content_type = enums.ContentType.DIRECTORY,
        deleted = const.NO_DELETED,
        file_created_time = datetime.now(),
        file_modified_time = datetime.now(),
        created_time = datetime.now(),
    )

    db.session.add(fileinfo)

    return dto.make_success_resp(2, {id: fileinfo.id})

