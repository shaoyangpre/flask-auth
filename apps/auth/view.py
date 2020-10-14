from flask import request, jsonify

from ..models import User, UserRole, UserPermission, Permission, RolePermission
from . import auth

@auth.route('/allauth', methods=['GET'])
def all_auth():
    id = request.json['id']
    endpoint = request.endpoint
    user = User.query.filter_by(id=id).first()
    if user:
        if user.is_active == 0:
            rep = {'用户已被禁用'}
        else:
            user_ids = UserRole.query.filter_by(user_id=id).with_entities(UserRole.role_id).all()
            ids = [id[0] for id in user_ids]
            permission_end = Permission.query.join(RolePermission).filter(RolePermission.role_id.in_(ids)).with_entities(Permission.endpoint).all()
            user_per_end = Permission.query.join(UserPermission).filter(UserPermission.user_id==id).with_entities(Permission.endpoint).all()
            all_per = [per[0] for per in set(permission_end + user_per_end)]
            if endpoint in all_per:
                rep = {'message': True}
            else:
                rep = {"message": '权限不足'}
    else:
        rep = {'message': '用户不存在'}

    return jsonify(rep)
