import cherrypy
import structs

nl = '<br>'

def echo(data):
  return data

def act(data):
  host = data['key']
  return host

def typ(obj):
  return str(type(obj)).replace('<', '').replace('>', '')

def local():
  return cherrypy.request.local.name == '127.0.0.1'

def get_sess(key):
    return cherrypy.session.get(key, None)

def header(key):
  return cherrypy.request.headers.get(key, 'NULL')

def dict_str(dict):
  res = ''
  for key in dict: res += key + ': ' + str(dict.get(key, None)) + nl
  
  return res

def has_val(obj):
  return not not obj

def del_sess(key):
  return cherrypy.session.pop(key, None)
  
def null(data): 
  if not data: return False
  if type(data) == type({}): data = list(data.values())
  
  for item in data:
    if not item or str(item).isspace(): return True
    
  return False
    
def cond(cond, val_yes, val_no):
  if cond: return val_yes
  return val_no

def to_qs(data, quest = True):
  if not data: return ''
  
  res = cond(quest, '?', '')
  first = True
  
  for k, v in data.items():
    if first: first = False
    else: res += '&'
     
    res += k + '=' + str(v)

  return res

def redir(url, data = None):
  raise cherrypy.HTTPRedirect(url + to_qs(data))

def respond(act, key):
  data = {}
  data[key] = 'show'
  raise cherrypy.HTTPRedirect(act + to_qs(data))
  #raise cherrypy.InternalRedirect(act, to_qs(data, False))

def disp(data):
  for item in data: 
    val = str(data[item])
    if val == 'show': data[item] = div(structs.messages[item])
    elif val == 'hide': data[item] = 'nodis'
  
  return data
  
def div(msg): return "<div style='font-size: 80%;'>" + msg + '</div>'


  


