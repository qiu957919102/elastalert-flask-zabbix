#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    :
# @File    :
# @Software: PyCharm
from flask import Flask,jsonify, request
from flask_mail import Mail, Message
import threading
app = Flask(__name__)


"""邮件服务配置"""
app.config['MAIL_SERVER'] = 'smtpproxy.baijiahulian.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'op@baijiahulian.com'
mail = Mail(app)
"""异步发送邮件"""
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/uqunhttpstatus', methods=['POST'])
def uqunhttpstatus():
    data = request.json
    path = data['path']
    status = data['path']
    requestV1 = data['request']
    num_matches = data['num_matches']
    num_hits = data['num_hits']
    referrer = data['referrer']
    agent = data['referrer']
    rule_level = data['rule_level']
    """异步邮件"""
    msg = Message("U群HttpStatus", recipients=["op-notice@baijiahulian.com"])
    msg.add_recipient("liyuan@baijiahulian.com")
    msg.body = "级别: " + rule_level + "\n" + "状态码: " + str(status) + "\n" + "numhits: " + str(num_hits) + "\n" + "path: " + path + "\n" + "request: " + requestV1 + "\n" + "nummatchs：" \
               + str(num_matches) + "\n" + "referrer: " + referrer + "\n" + "agent：" + agent
    thr = threading.Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return jsonify({"code": 200})



@app.route('/haokehttpstatus', methods=['POST'])
def haokehttpstatus():
    data = request.json
    path = data['path']
    status = data['path']
    requestV1 = data['request']
    num_matches = data['num_matches']
    num_hits = data['num_hits']
    referrer = data['referrer']
    agent = data['referrer']
    rule_level = data['rule_level']
    """异步邮件"""
    msg = Message("好课HttpStatus", recipients=["op-notice@baijiahulian.com"])
    msg.add_recipient("zhuxingtao@baijiahulian.com")
    msg.body = "级别: " + rule_level + "\n" + "状态码: " + str(status) + "\n" + "numhits: " + str(
        num_hits) + "\n" + "path: " + path + "\n" + "request: " + requestV1 + "\n" + "nummatchs：" \
               + str(num_matches) + "\n" + "referrer: " + referrer + "\n" + "agent：" + agent
    """异步发邮件"""
    thr = threading.Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return jsonify({"code": 200})

@app.route('/gaotuhttpstatus', methods=['POST'])
def gaotuttpstatus():
    data = request.json
    path = data['path']
    status = data['path']
    requestV1 = data['request']
    num_matches = data['num_matches']
    num_hits = data['num_hits']
    referrer = data['referrer']
    agent = data['referrer']
    rule_level = data['rule_level']
    """异步邮件"""
    msg = Message("高途HttpStatus", recipients=["op-notice@baijiahulian.com"])
    msg.add_recipient("chenbixia@baijiahulian.com")
    msg.body = "级别: " + rule_level + "\n" + "状态码: " + str(status) + "\n" + "numhits: " + str(
        num_hits) + "\n" + "path: " + path + "\n" + "request: " + requestV1 + "\n" + "nummatchs：" \
               + str(num_matches) + "\n" + "referrer: " + referrer + "\n" + "agent：" + agent
    """异步发邮件"""
    thr = threading.Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return jsonify({"code": 200})


if __name__ == '__main__':
    app.run(debug=True, port=8888, host='0.0.0.0')
