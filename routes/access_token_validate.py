from flask import Blueprint, jsonify
from token_services import token_control

access_token_validate_bp=Blueprint('access_token_validate',__name__)

@access_token_validate_bp.route('/access_token_validate', methods=['POST'])
def access_token_validate():
    result=token_control()
    if result['error_code']=='VALID_TOKEN':
        return jsonify({'valid': True, 'message': 'Token geçerli',
            'user_type':result['user_type'], 'token': result['token']}), 200
    return jsonify({'valid': False, 'message':result['error_code']}), result['code']
