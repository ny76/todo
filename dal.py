from app_data import *
import pymongo
from pymongo import MongoClient, InsertOne, DeleteOne, ReplaceOne, UpdateOne
from pymongo.errors import BulkWriteError
from datetime import datetime
from bson.objectid import ObjectId


_id = '_id'

class DAL(object):
  
  def __init__(self, coll_name):
    self.coll_name = coll_name
    self.coll = self.GetColl(coll_name)
  
  def CheckConn(self):
    client = None
    
    try:
      client = MongoClient()
      info = client.server_info()
    except pymongo.errors.ServerSelectionTimeoutError:
      pass
    else:
      if info['ok']:
        client.close()
        
        return 'Conn OK'
    
    return 'No Conn!'
  
  def GetDb(self):
    try:
      client = MongoClient()
      info = client.server_info()
    except pymongo.errors.ServerSelectionTimeoutError:
      #raise Exception('No Connection!')
      return None
    else:
      if info['ok']:
        db = client[AppData.DB_NAME]
        
        return db
    
    return None
  
  def GetColl(self, coll = AppData.COLL_NAME):
    db = self.GetDb()
    
    if db: return db[coll]
    return None
  
  def GetAll(self):
    coll = self.coll
    
    if coll:
      rows = coll.find().sort('date', -1)
      #json_obj = [{date: '2016-10-10T10:10:10', task: 'Com\'n, make my day!', priority: 1}]
      return rows

    return None

  def GetItem(self, id):
    coll = self.coll
    
    if coll:
      row = coll.find_one({_id: ObjectId(id)})
      
    return row

  def HasItemByKey(self, key, val):
    coll = self.coll
    
    if coll:
      row = coll.find_one({key: val})
      
    return row

  def GetItemByKey(self, key, val):
    coll = self.coll
    
    if coll:
      row = coll.find_one({key: val})
      
    return row
  
  def Add(self, **data):
    coll = self.coll
    
    if coll:
      data['date'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
      data.pop('act', None)
      
      req = InsertOne(data)
      ok = True
      
      try:
        res = coll.bulk_write([req])
      except BulkWriteError as bwe:
        ok = False
        res = bwe.details  
       
      '''
    valid op res:
    
  
    bulk_api_result

        The raw bulk API result.
        {'nUpserted': 0, 'nModified': 0, 'writeConcernErrors': [], 'upserted': [], 'nInserted': 1, 'nRemoved': 0, 'nMatched': 0, 'writeErrors': []}

    deleted_count

        The number of documents deleted.

    inserted_count

        The number of documents inserted.

    matched_count

        The number of documents matched for an update.

    modified_count

        The number of documents modified.

        Note

        modified_count is only reported by MongoDB 2.6 and later. When connected to an earlier server version, or in certain mixed version sharding configurations, this attribute will be set to None.

    upserted_count

        The number of documents upserted.

    upserted_ids

        A map of operation index to the _id of the upserted document.
        

    ________________________________________
        
    invalid op:
    
    {'nUpserted': 0, 'nModified': 0, 'upserted': [], 'writeErrors': [{'code': 11000, 'op': {'date': '2016-10-25T08:56:32', 'username': 'test', 'login_id': 1761932, 'password': 'pass', '_id': ObjectId('580ef4101ad5d50e1bf185c0'), 'name': 'name'}, 'index': 0, 'errmsg': 'E11000 duplicate key error collection: todo.user index: login_id_1 dup key: { : 1761932 }'}], 'writeConcernErrors': [], 'nMatched': 0, 'nInserted': 0, 'nRemoved': 0}

      '''
      # InsertOne({'_id': ObjectId('5807243e1ad5d521eb7fe1b8'), 'date': '2016-10-19T10:43:58', 'task': 'TEST', 'priority': 1})
 
      if ok:
        inserted_id = req._doc.get(_id, None)    
      
        return not not str(inserted_id)
      else:
        return res
    
    return False
  
  def Update(self, **data):
    coll = self.coll
    data.pop('act', None)
    
    if coll:
      req = UpdateOne(
        {_id: ObjectId(data.pop('id'))},
        {'$set': data},
        False
      )
      
      res = coll.bulk_write([req])
      
      #found = int(res.bulk_api_result['nMatched']) > 0
      found = res.matched_count > 0
      modified = res.modified_count > 0
      
      return found
    
    return False
  
  def Delete(self, id):
    coll = self.coll
    
    if coll:
      req = DeleteOne({_id: ObjectId(id)})
      
      res = coll.bulk_write([req])
      
      found = int(res.bulk_api_result['nRemoved']) > 0
      deleted = res.deleted_count > 0
      
      return found
    
    return False






