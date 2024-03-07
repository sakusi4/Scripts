import redis

def copy_redis_data(from_host, from_port, from_db, to_host, to_port, to_db):    
    from_redis = redis.Redis(host=from_host, port=from_port, db=from_db, decode_responses=True)
    to_redis = redis.Redis(host=to_host, port=to_port, db=to_db, decode_responses=True)
    
    keys = from_redis.keys('*')
    
    for key in keys:
        key_type = from_redis.type(key)
        
        try :
            if key_type == 'string':
                value = from_redis.get(key)
                to_redis.set(key, value)

            elif key_type == 'hash':
                value = from_redis.hgetall(key)
                to_redis.hmset(key, value)

            elif key_type == 'list':
                value = from_redis.lrange(key, 0, -1)
                to_redis.rpush(key, *value)

            elif key_type == 'set':
                value = from_redis.smembers(key)
                to_redis.sadd(key, *value)

            elif key_type == 'zset':
                value = from_redis.zrange(key, 0, -1, withscores=True)
                to_redis.zadd(key, dict(value))
            
            print(f'succeeded copy key : {key}')            
        except Exception:
            print(f'failed copy key : {key}')


from_host = '127.0.0.1'
from_port = 6379
from_db = 0
to_host = '127.0.0.1'
to_port = 63791
to_db = 0

copy_redis_data(from_host, from_port, from_db, to_host, to_port, to_db)