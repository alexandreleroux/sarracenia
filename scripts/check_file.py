#!/usr/bin/python3

import os,stat,time
from hashlib import md5

class Transformer(object): 
      def __init__(self):
          pass

      def perform(self,parent):
          logger = parent.logger
          msg    = parent.msg

          logger.info("local file %s " % msg.local_file)
          logger.info("partflg    %s " % msg.partflg)
          logger.info("sumflg     %s " % msg.sumflg )
          logger.info("filesize   %s " % msg.filesize)
          logger.info("offset     %d " % msg.offset)
          logger.info("length     %d " % msg.length)

          if msg.partflg != '1' or msg.sumflg != 'd'  :
             logger.warning("ignore parts or not md5sum on data")
             os.unlink(msg.local_file)
             return False

          lstat  = os.stat(msg.local_file)
          fsiz   = lstat[stat.ST_SIZE]

          if fsiz != msg.filesize :
             logger.error("filesize differ (corrupted ?)  lf %d  msg %d" % fsiz,msg.filesize)
             os.unlink(msg.local_file)
             return False

          f = open(msg.local_file,'rb')
          if msg.offset != 0 : f.seek(msg.offset,0)
          if msg.length != 0 : data = f.read(msg.length)
          else:                data = f.read()
          f.close()
          fsum =  md5(data).hexdigest()

          if fsum != msg.checksum :
             logger.error("checksum differ (corrupted ?)  lf %s  msg %s" % fsum,msg.checksum)

          os.unlink(msg.local_file)
          return False

transformer = Transformer()
self.on_file = transformer.perform

