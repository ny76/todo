import os
from jinja2 import Environment, FileSystemLoader

class AppData:
  ROOT = os.path.dirname(__file__) + '/'
  TPL_PATH = os.path.join(ROOT, 'template')
  ENV = Environment(loader=FileSystemLoader(TPL_PATH))
  DB_NAME = 'todo'
  COLL_NAME = 'task'
  CHECK_KEY = 'CHECK_KEY'
  CHECK_VAL = '58004b5a1ad5d50fe6f40464'
  