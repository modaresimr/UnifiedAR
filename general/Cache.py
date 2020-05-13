import hashlib
import logging
logger = logging.getLogger(__file__)
def hashkey(key):
   hash_object = hashlib.sha1(key.encode('utf-8'))
   return  hash_object.hexdigest()


cachefolder="cache"
import general.utils as utils
def get(key,valf):
   try:
      val=utils.loadState(cachefolder,hashkey(key))
      logger.debug(f'cached file found {key}')
   except:
      logger.debug(f'cached file not found {key}')
      val=valf()
      utils.saveState(val,cachefolder,hashkey(key))
   return val


def removeCache():
   import shutil
   shutil.rmtree('save_data/'+cachefolder)
