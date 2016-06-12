# coding=utf-8
from flask import jsonify
from app.exceptions import ValidationError
from . import api


def bad_request(message):
    response = jsonify({'error': '错误的请求', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'error': '未经授权', 'message': message})
    response.status_code = 500
    return response


def forbidden(message):
    response = jsonify({'error': '禁止进入', 'message': message})
    response.status_code = 403
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
