import os
import cherrypy
from app_data import AppData
from utils import *
from user_dal import UserDAL

class Auth():
  
  def __init__(self):
    val = cherrypy.session.get(AppData.LOGIN_KEY, None)

    self.first = val is None
    self.logged = not not val
    self.login_name = val or self.anonymous()
    
    print('first: %s' % str(self.first))
    print('logged: %s' % str(self.logged))
    print('login_name: %s' % str(self.login_name))

  def anonymous(self):
      return ''
 
  def login(self, username = None, password = None):
    msg = '' 
    
    if cherrypy.request.method == 'POST':
      if null(username, password): msg = 'missing data!'
      else:
        user = UserDAL().GetItemByKey('username', username) 
      
        if user and user['password'] == password:
          self.on_login(username)
        else: msg = 'invalid data!'
        
    self.login_scr(username, msg)

  def logout(self):
    del_sess(AppData.LOGIN_KEY)
    raise cherrypy.HTTPRedirect("/")    
 
  def register(self, username = None, password = None, name = None):
    ok = False
    msg = ''
    user_exist = False
    
    if cherrypy.request.method == 'POST':
      if null(username, password, name): msg = 'missing data!'
      else:
        mgr = UserDAL()
        
        if mgr.HasItemByKey('username', username): user_exist = True
        else:
          res = mgr.Add(username, password, name)
        
          if res == True:
            ok = True
            self.on_register(username)
          else: msg = 'invalid data!'
        
    self.register_scr(username, msg, user_exist)

  def on_login(self, username):
    cherrypy.session[AppData.LOGIN_KEY] = username
    raise cherrypy.HTTPRedirect("/")  

  def on_register(self, username):
    cherrypy.session[AppData.LOGIN_KEY] = username
    raise cherrypy.HTTPRedirect("/")  

  def on_logout(self, username):
      pass
        
  def login_scr(self, username = None, msg = None):
    cherrypy.response.body = str("""<html><body>
      <form method="post" action="login">
          Login: <input type="text" name="username"
          value="%s" size="10" />
          <br />
          Password: <input type="password" name="password" size="10" />
          <br /> 
          <div style='color: brown; font-size: 80%%;'>%s</div>
          <input type="submit" value='LOGIN'/>
      </form>
      </body></html>""" % ((username or ''), (msg or ''))).encode('utf-8')
        
  def register_scr(self, username = None, msg = None, user_exist = False):
    user_exist_disp = cond(user_exist, 'block', 'none')
    
    if user_exist: msg = ''
     
    cherrypy.response.body = str("""<html><body>
      <form method="post" action="register">
          Login: <input type="text" name="username"
          value="%s" size="10" />
          <div style='color: brown; font-size: 80%%; display: %s;'>Username already exists!</div>
          <br />
          Password: <input type="password" name="password" size="10" />
          <br />
          Name: <input type="text" name="name" size="20" />
          <br /> 
          <div style='color: brown; font-size: 80%%;'>%s</div>
          <input type="submit" value='REGISTER'/>
      </form>
      </body></html>""" % ((username or ''), user_exist_disp, (msg or ''))).encode('utf-8')
