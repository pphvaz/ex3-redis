#python3 -m pip install redis
#------------------------------------------------------------------
import redis

conR = redis.Redis(host='redis-10339.c245.us-east-1-3.ec2.cloud.redislabs.com',
                  port=10339,
                  password='123456')

conR.set('user:name','vinicius')

print(conR.get('user:name'))


