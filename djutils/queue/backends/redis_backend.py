import re
import redis

from djutils.queue.backends.base import BaseQueue


class RedisQueue(BaseQueue):
    """
    A simple Queue that uses the redis to store messages
    """
    def __init__(self, name, connection):
        """
        QUEUE_CONNECTION = 'host:port:database' or defaults to localhost:6379:0
        """
        super(RedisQueue, self).__init__(name, connection)
        
        if not connection:
            connection = 'localhost:6379:0'
        
        self.queue_name = 'djutils.redis.%s' % re.sub('[^a-z0-9]', '', name)
        self.conn = redis.Redis(
            *connection.split(':')
        )
    
    def write(self, data):
        self.conn.lpush(self.queue_name, data)
    
    def read(self):
        return self.conn.rpop(self.queue_name)
    
    def flush(self):
        self.conn.delete(self.queue_name)
    
    def __len__(self):
        return self.conn.llen(self.queue_name)
