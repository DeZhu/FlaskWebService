# -*- coding: utf-8 -*-
"""
Env: python3.6
Created on 2017-10-10 16:20:13
@author: zhude
使用 Python 和 Flask 框架来创建一个 RESTful 的 web service
WEB开发调试工具：HTTPie

HTTP 标准的方法有如下:
HTTP 方法   行为                   示例
==========  =====================  ==================================
GET         获取资源的信息         http://example.com/api/orders
GET         获取某个特定资源的信息 http://example.com/api/orders/123
POST        创建新资源             http://example.com/api/orders
PUT         更新资源               http://example.com/api/orders/123
DELETE      删除资源               http://example.com/api/orders/123


"""
from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth
from numpy import unicode

app = Flask(__name__)
# 使用的是内存数据库，一个真正的 web service 需要一个真实的数据库进行支撑
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

# 用户认证
auth = HTTPBasicAuth()


@auth.get_password  # 回调函数，验证用户名和密码
def get_password(username):
    if username == 'use1':
        return 'password'  # 密码
    return None


@auth.error_handler  # 回调函数是用于给客户端发送未授权错误代码
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@app.route('/todo/api/v1.0/tasks', methods=['GET'])  # http http://127.0.0.1:5000/todo/api/v1.0/tasks
@auth.login_required  # 需要认证的函数添加 @auth.login_required 装饰器， 调用需要：http --auth use1:password  http://127.0.0.1:5000/todo/api/v1.0/tasks
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])  # http http://127.0.0.1:5000/todo/api/v1.0/tasks/1
def get_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


@app.errorhandler(404)  # 从定义404错误
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo/api/v1.0/tasks', methods=['POST'])  # http post http://127.0.0.1:5000/todo/api/v1.0/tasks title=ceshi
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>',
           methods=['PUT'])  # http put http://127.0.0.1:5000/todo/api/v1.0/tasks/3 title=ceshi2
def update_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>',
           methods=['DELETE'])  # http delete http://127.0.0.1:5000/todo/api/v1.0/tasks/3
def delete_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)
