
import datetime
import uuid
from flask import request
from flask_jwt_extended import current_user, jwt_required
from . import file
from ..auth import models, dto
from . import models
from .. import user
from ..common import dto
from ..common import jwt_wrapper
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
        deleted = 0,
        file_created_time = created_time,
        file_modified_time = modified_time,
        created_time = datetime.now(),
    )

    db.session.add(fileinfo)

    return dto.make_success_resp(2, None)

    



