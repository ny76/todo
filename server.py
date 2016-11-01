#!/usr/bin/env python3

import os
import random
import string

import cherrypy
from jinja2 import Environment, FileSystemLoader, Template
import json
from bson import BSON
from bson.json_util import dumps

from app_data import AppData
from task_dal import TaskDAL
from utils import *

env = AppData.ENV
web_root = AppData.ROOT


class Server(object):
    
  @cherrypy.expose
  def index(self):
    redir('home')

  @cherrypy.expose
  def dev(self):
    res = self.dev.__name__
    return str(res)
    
  @cherrypy.expose
  def home(self, **data):
    act = 'home'
    
    if not data: data = {}
    data['act'] = act
    data['rows'] = TaskDAL().GetAll()

    #if not rows: redir('/')
    
    t = env.get_template(act + '.html')    

    return t.render(disp(data))
    
    
  @cherrypy.expose
  def add(self, **data):
    act = 'add'
    
    if not data: data = {}
    data['act'] = act
    
    t = env.get_template(act + '.html')    

    return t.render(disp(data))
    
  @cherrypy.expose
  def edit(self, id, **data):
    act = 'edit'
    
    row = TaskDAL().GetItem(id)
    
    if not row: redir('/')
    
    data = row
    
    if not data: data = {}
    data['act'] = act
    data['id'] = id
    
    t = env.get_template(act + '.html')    

    return t.render(disp(data))
    
  @cherrypy.expose
  def delete(self, id):
    act = 'delete'

    row = TaskDAL().GetItem(id)
    
    if not row: redir('/')
    
    data = row
        
    if not data: data = {}
    data['act'] = act
    data['id'] = id
    
    t = env.get_template(act + '.html')    

    return t.render(disp(data))

  @cherrypy.expose
  def conn(self):
    return TaskDAL().CheckConn()

  @cherrypy.expose
  def shutdown(self):  
    cherrypy.engine.exit()
    
    
@cherrypy.expose
class DataService(object):

  @cherrypy.tools.accept(media='text/plain')
  def GET(self):
    pass

  def POST(self, **data):
    #print(data)
    act = data['act']
    
    
    if act == 'add':
      if null(data): respond(act, 'missing')
        #redir('add', {'missing': div('Missing data!')})
      else: 
        res = TaskDAL().Add(**data)
        
        if res == True: redir('/')
      
      redir(act)
    elif act == 'edit': self.PUT(**data)      
    elif act == 'delete': return self.DELETE(**data)      

    
  
# {'priority': '4', 'task': 'nnnn', 'cmd_add': 'ADD'}

  def PUT(self, **data):
    act = data['act']
    if null(data): respond(act, 'missing')
      #redir('add', {'missing': div('Missing data!')})
    else: 
      res = TaskDAL().Update(**data)
      
      if res == True: redir('/')
    
    redir(act)
  
  def DELETE(self, **data):
    #return str(data['id'])
    #'''
    res = TaskDAL().Delete(data['id'])
      
    if res == True: redir('/')
    
    redir('delete')
    #'''  

if __name__ == '__main__':
  conf = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.abspath(web_root) # os.getcwd()
    },
    '/data': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [('Content-Type', 'text/plain')],
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'public'
    }
  }

  webapp = Server()
  webapp.data = DataService()
  cherrypy.quickstart(webapp, '/', conf)
