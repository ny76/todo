import random

import cherrypy
from utils import *
from dal import DAL

class TaskDAL(DAL):
    
  coll_name = 'task'
  
  def __init__(self):
    super().__init__(self.coll_name)

   
    
    