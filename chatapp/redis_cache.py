from .models import User
from redis import Redis

redis = Redis()


def update_online_status(user):
    redis.sadd('online_users', user.username)
    user.is_online = True
    user.save()


def update_offline_status(user):
    redis.srem('online_users', user.username)
    user.is_online = False
    user.save()


def get_online_users():
    return redis.smembers('online_users')
