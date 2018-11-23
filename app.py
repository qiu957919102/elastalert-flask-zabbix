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
import sh
app = Flask(__name__)

"""hits表示规则命中条数；matches表示规则命中条数，并且匹配规则触发告警数"""


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


"""异步发送zabbix_sender"""
def send_async_zabbix(ZABBIX_IP,MONITOR_NAME,key,value):
    try:
        sh.zabbix_sender("-z", ZABBIX_IP, "-s", MONITOR_NAME, "-k", key, "-o", value)
    except Exception:
        #######出现字符串太长就切片，只要前5000个
        strvalue = value[0:5000]
        try:
            sh.zabbix_sender("-z", ZABBIX_IP, "-s", MONITOR_NAME, "-k", key, "-o", strvalue)
        except Exception:
            pass

ZABBIX_IP = '172.16.5.1'
MONITOR_NAME = 'al-bj-op-es'





@app.route('/uqunhttpstatus', methods=['POST'])
def uqunhttpstatus():
    data = request.json
    try:
        path = data['path']
    except Exception:
        path = "none"
    try:
        status = data['status']
    except Exception:
        status = "none"
    try:
        requestV1 = data['request']
    except Exception:
        requestV1 = "none"
    try:
        num_matches = data['num_matches']
    except Exception:
        num_matches = "none"
    try:
        num_hits = data['num_hits']
    except Exception:
        num_hits = "none"
    try:
        referrer = data['referrer']
    except Exception:
        referrer = "none"
    try:
        agent = data['agent']
    except Exception:
        agent = "none"
    try:
        rule_level = data['rule_level']
    except Exception:
        rule_level = "none"
    """异步邮件"""
    if rule_level == "Average":
        msg = Message("U群HttpStatus", recipients=["op-notice@baijiahulian.com"])
        msg.add_recipient("zhangliyuan01@baijiahulian.com")
        msg.body = "级别: " + rule_level + "\n" + "状态码: " + str(status) + "\n" + "numhits: " + str(
            num_hits) + "\n" + "path: " + path + "\n" + "request: " + requestV1 + "\n" + "nummatchs：" \
                   + str(num_matches) + "\n" + "referrer: " + referrer + "\n" + "agent：" + agent
        """异步发邮件"""
        thr = threading.Thread(target=send_async_email, args=[app, msg])
        thr.start()
        return jsonify({"code": 200})
    elif rule_level == "High":
        """异步发zabbix_sender"""
        key = "uqunHTTPstatus"
        value = "级别: " + rule_level + "状态码: " + str(status) + "numhits: " + str(
            num_hits) + "path: " + path + "request: " + requestV1 + "nummatchs：" \
                   + str(num_matches) + "referrer: " + referrer + "agent：" + agent
        thr2 = threading.Thread(target=send_async_zabbix, args=[ZABBIX_IP, MONITOR_NAME, key, value])
        thr2.start()
        msg = Message("U群HttpStatus", recipients=["op-notice@baijiahulian.com"])
        msg.add_recipient("zhangliyuan01@baijiahulian.com")
        msg.body = "级别: " + rule_level + "\n" + "状态码: " + str(status) + "\n" + "numhits: " + str(
            num_hits) + "\n" + "path: " + path + "\n" + "request: " + requestV1 + "\n" + "nummatchs：" \
                   + str(num_matches) + "\n" + "referrer: " + referrer + "\n" + "agent：" + agent
        """异步发邮件"""
        thr = threading.Thread(target=send_async_email, args=[app, msg])
        thr.start()
        return jsonify({"code": 200})



@app.route('/haokehttpstatus', methods=['POST'])
def haokehttpstatus():
    data = request.json
    try:
        path = data['path']
    except Exception:
        path = "none"
    try:
        status = data['status']
    except Exception:
        status = "none"
    try:
        requestV1 = data['request']
    except Exception:
        requestV1 = "none"
    try:
        num_matches = data['num_matches']
    except Exception:
        num_matches = "none"
    try:
        num_hits = data['num_hits']
    except Exception:
        num_hits = "none"
    try:
        referrer = data['referrer']
    except Exception:
        referrer = "none"
    try:
        agent = data['agent']
    except Exception:
        agent = "none"
    try:
        rule_level = data['rule_level']
    except Exception:
        rule_level = "none"
    """异步邮件"""
    if rule_level == "Average":
        msg = Message("好课HttpStatus", recipients=["op-notice@baijiahulian.com"])
        msg.add_recipient("zhuxingtao@baijiahulian.com")
        msg.body = "级别: " + rule_level + "\n" + "状态码: " + str(status) + "\n" + "numhits: " + str(
            num_hits) + "\n" + "path: " + path + "\n" + "request: " + requestV1 + "\n" + "nummatchs：" \
                   + str(num_matches) + "\n" + "referrer: " + referrer + "\n" + "agent：" + agent
        """异步发邮件"""
        thr = threading.Thread(target=send_async_email, args=[app, msg])
        thr.start()
        return jsonify({"code": 200})
    elif rule_level == "High":
        """异步发zabbix_sender"""
        key = "uqunHTTPstatus"
        value = "级别: " + rule_level + "状态码: " + str(status) + "numhits: " + str(
            num_hits) + "path: " + path + "request: " + requestV1 + "nummatchs：" \
                   + str(num_matches) + "referrer: " + referrer + "agent：" + agent
        thr2 = threading.Thread(target=send_async_zabbix, args=[ZABBIX_IP, MONITOR_NAME, key, value])
        thr2.start()
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
    try:
        path = data['path']
    except Exception:
        path = "none"
    try:
        status = data['status']
    except Exception:
        status = "none"
    try:
        requestV1 = data['request']
    except Exception:
        requestV1 = "none"
    try:
        num_matches = data['num_matches']
    except Exception:
        num_matches = "none"
    try:
        num_hits = data['num_hits']
    except Exception:
        num_hits = "none"
    try:
        referrer = data['referrer']
    except Exception:
        referrer = "none"
    try:
        agent = data['agent']
    except Exception:
        agent = "none"
    try:
        rule_level = data['rule_level']
    except Exception:
        rule_level = "none"
    """异步邮件"""
    if rule_level == "Average":
        msg = Message("高途HttpStatus", recipients=["op-notice@baijiahulian.com"])
        msg.add_recipient("chenbixia@baijiahulian.com")
        msg.body = "级别: " + rule_level + "\n" + "状态码: " + str(status) + "\n" + "numhits: " + str(
            num_hits) + "\n" + "path: " + path + "\n" + "request: " + requestV1 + "\n" + "nummatchs：" \
                   + str(num_matches) + "\n" + "referrer: " + referrer + "\n" + "agent：" + agent
        """异步发邮件"""
        thr = threading.Thread(target=send_async_email, args=[app, msg])
        thr.start()
        return jsonify({"code": 200})
    elif rule_level == "High":
        """异步发zabbix_sender"""
        key = "uqunHTTPstatus"
        value = "级别: " + rule_level + "状态码: " + str(status) + "numhits: " + str(
            num_hits) + "path: " + path + "request: " + requestV1 + "nummatchs：" \
                   + str(num_matches) + "referrer: " + referrer + "agent：" + agent
        thr2 = threading.Thread(target=send_async_zabbix, args=[ZABBIX_IP, MONITOR_NAME, key, value])
        thr2.start()
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
