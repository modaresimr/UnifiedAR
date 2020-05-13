import hashlib
import logging
logger = logging.getLogger(__file__)
def hashkey(key):
   hash_object = hashlib.sha1(key.encode('utf-8'))
   return  hash_object.hexdigest()


cachefolder="cache"
import general.utils as utils
import os.path
def get(key,valf):
   hkey=hashkey(key)
   try:
      val=utils.loadState(cachefolder,hkey)
      logger.debug(f'cached file found {key} {hkey}')
   except Exception as e:
      
      if not(os.path.exists(f'save_data/{hkey}')):
        logger.debug(f'cached file not found {key} {hkey}')
      else:
          logger.error(f'error in cached {e}',exc_info=True)
      
      val=valf()
      utils.saveState(val,cachefolder,hkey)
      with open(f'{hkey}.txt', 'w') as f:
         print(key,file=f)
         f.close()

      
   return val


def removeCache():
   import shutil
   shutil.rmtree('save_data/'+cachefolder)
