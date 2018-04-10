#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import threading
import os
import sys
from time import sleep
from wsgiref.simple_server import make_server
import json
import ConfigParser
import httplib
module_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(module_path+'/plugin')

'''
在使用python2 configparser读取配置文件的时候，发现没法保留配置文件大小写，进行重写optionxform
'''
class myconf(ConfigParser.ConfigParser):  
    def __init__(self,defaults=None):  
        ConfigParser.ConfigParser.__init__(self,defaults=None)  
    def optionxform(self, optionstr):  
        return optionstr

class confParse(object):  
    def __init__(self,conf_path):  
        self.conf_path = conf_path  
        self.conf_parser = myconf()  
        self.conf_parser.read(conf_path)  
  
    def get_sections(self):
        return self.conf_parser.sections()  
  
    def get_options(self,section):  
        return self.conf_parser.options(section)  
  
    def get_items(self,section):  
        return self.conf_parser.items(section)  
  
    def get_val(self,section,option,is_bool = False,is_int = False):  
        if is_bool and not is_int:  
            #bool类型配置  
            val = self.conf_parser.getboolean(section,option)  
            return val  
        elif not is_bool and is_int:  
            val = self.conf_parser.getint(section,option)  
            return val  
  
        val = self.conf_parser.get(section,option)  
        return val
    def add_section(self,section):
        self.conf_parser.add_section(section)
        self.conf_parser.write(open(self.conf_path,"w"))
    def set_option(self,section,option,value):
        self.conf_parser.set(section, option, value)
        self.conf_parser.write(open(self.conf_path,"w"))


class AgentService(object):
    def __init__(self,port,config):
        self.port = port 
        self.config = config
        self.configobj = None
        self.status = ""
        self.interval = ""
        self.host = None
        self.serverHost = None
        self.serverPort = None
        self.serverContext = None
        self.items = {}

    def init_env(self):
        self.configobj = confParse(self.config)
        self.status = self.configobj.get_val('status','status')
        self.host = self.configobj.get_val('host','host')
        self.serverHost = self.configobj.get_val('server_api','host')
        self.serverPort = self.configobj.get_val('server_api','port')
        self.serverContext = self.configobj.get_val('server_api','context')
        self.interval = self.configobj.get_val('interval','interval',is_int = True)
        items_option = self.configobj.get_options('items')
        for key in items_option:
            self.items[key]=self.configobj.get_val('items',key)
        print ' '

    def set_env(self,data):
        for key,value in data.items():
            if key == 'items':
                for optionkey,optionvalue in value.items():
                    self.configobj.set_option(key,optionkey,optionvalue)
            else:
                self.configobj.set_option(key,key,value) 
            setattr(self,key,value)



    def handle_request(self,environment,start_response):
        start_response('200 OK',[('Content-Type','text/plain')])
        try:
            request_body_size = int(environment.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        else:
            data_json = eval(environment['wsgi.input'].read(request_body_size))
            self.set_env(data_json)
        return 'ok'

    def run_server(self):
	try:
            httpd = make_server('',self.port,self.handle_request)
            httpd.serve_forever()
	except Exception as e:
            print e
	    os._exit(1)

    def start_server(self):
        t = threading.Thread(target=self.run_server,args=())
        t.start()

    def run_agent(self):
        while True:
            if self.status == 'enabled':
                self.start_monitor()
                sleep(self.interval)
            else:
                print 'disabled',self.status
                sleep(self.interval)

    def start_monitor(self):
        monitor_items = {}
        monitor_data = {}
        for key,value in self.items.items():
            if isinstance(value,list):
                length = len(value)
            else:
                try:
                    value = eval(value)
                    length = len(value)
                except:
                    length = 0
            if length > 0:
                monitor_items[key]=value
        for key,value in monitor_items.items():
            try:
                modulename = __import__(key)
            except ImportError as e:
                print e
            else:
                monitor_data[key]={}
                excute = getattr(modulename,key)
                if key == 'network' or key == 'disk':
                    for card in value:
                        monitor_data[key][card] = excute(card)
                else:
                    monitor_data[key]= excute()
        monitor_data['host']=self.host
        print monitor_data
        self.post_data(json.dumps(monitor_data))

    def post_data(self,data):
        headers = {"Content-type":"application/json"}
        conn = httplib.HTTPConnection(self.serverHost,self.serverPort)
        conn.request("POST", self.serverContext, data, headers)
        try:
            httpres = conn.getresponse()
        except Exception as e:
            print e
        print httpres.status


    def start_agent(self):
        t = threading.Thread(target=self.run_agent,args=())
        t.start()

def main():
    try:
        pid = os.fork()
        if pid > 0:
            os._exit(0)
    except OSError,error:
        print 'fork #1 failed: %d (%s)' % (error.errno, error.strerror)
        os._exit(1)
    os.chdir('/')
    os.setsid()
    os.umask(0)
    try:
        pid = os.fork()
        if pid > 0:
            os._exit(0)
    except OSError,error:
        print 'fork #2 failed: %d (%s)' % (error.errno, error.strerror)
        os._exit(1)
    agentconf = '/root/monitor/agent/agent.conf'
    agent_instance = AgentService(7000,agentconf)
    agent_instance.init_env()
    logfile = confParse(agentconf).get_val('log','logfile')
    stream = open(logfile,'a')
    os.dup2(stream.fileno(),1)
    os.dup2(stream.fileno(),2)
    stream.close()
    agent_instance.start_server()
    agent_instance.start_agent()


if __name__ == "__main__":
    main()
