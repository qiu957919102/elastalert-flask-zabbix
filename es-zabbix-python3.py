#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    : 
# @File    : 
# @Software: PyCharm
import time
import re
import elasticsearch
import logging
import threading
import sh
class EsDump:
    def __init__(self, es_host):
        self.es_host = es_host
        try:
            self.es = elasticsearch.Elasticsearch([es_host, '', ''], http_auth=('*','*'))
        except Exception as e:
            print(e)
    def echo(self, dsl_body):
        try:
            echo_matches = self.es.search(index="_all", body=dsl_body)
        except Exception as e:
            print(e)
        return echo_matches

    def echo_detail(self, dsl_body):
        try:
            detail_matches = self.es.search(index="_all", body=dsl_body)
        except Exception as e:
            print(e)
        return detail_matches

    def list_errorlog_type(self, gte_time):
        dsl_body = {
            "query": {
                "bool": {
                    "filter": {
                        "bool": {
                            "must": [
                                {"range": {"@timestamp": {"gte": gte_time, "lt": "now"}}},
                            ],
                        }
                    }
                }
            },
            "aggs": {
                "target": {
                    "terms": {
                        "field": "type.raw",
                        "size": "200"
                    }
                }

            }
        }
        list_result = self.echo(dsl_body)
        print("错误列表" + list_result)
        return list_result
    def exist_error_record(self, gte_time, errortype):
        dsl_body = {
            "query": {
                "bool": {
                    "filter": {
                        "bool": {
                            "must": [
                                {"range": {"@timestamp": {"gte": gte_time, "lt": "now"}}},
                                {"term": {"_type": errortype}},
                            ]
                        }
                    },
                }
            },
        }
        record_result = self.echo_detail(dsl_body)
        print("错误类型" + record_result)
        return record_result


ZABBIX_IP = '172.16.5.1'
MONITOR_NAME = 'al-bj-op-es'


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


class Zabbix:
    def errorlog_sender(self, interval):
        r = EsDump('172.16.5.6')
        gte_time = "now-" + interval
        result = r.list_errorlog_type(gte_time)
        for errorlog_type in result['aggregations']['target']['buckets']:
            Yewulist = [u'error-search-.*' u'error-web-.*', u'error-pay-.*', u'error-tianxiao-.*', u'error-yunying-.*',
                        u'error-weishi-.*', u'error-gaotu-.*', u'gaotu-tomcat-error-.*', u'error-babyabc-.*',u'uqun-error-.*',u'error-jiaoyan-.*']
            for i in Yewulist:
                rmatch = re.match(i, errorlog_type['key'])
                if rmatch:
                    errortype = rmatch.group()
                    result = r.exist_error_record(gte_time, errortype)
                    key = "error-log[" + errortype + "]"
                    for ret in result['hits']['hits']:
                        value = ret['_source']['host'] + " " + ret['_source']['message']
                        value = value.replace('\n', ' ')
                        thr2 = threading.Thread(target=send_async_zabbix, args=[ZABBIX_IP, MONITOR_NAME, key, value])
                        thr2.start()

if __name__ == "__main__":
    zabbix = Zabbix()

    while True:
        t1 = threading.Thread(zabbix.errorlog_sender('120s'))
        t1.start()
        time.sleep(120)
