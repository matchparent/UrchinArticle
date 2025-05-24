from .Env import config
import redis


def redis_connect():
    return redis.Redis(
        connection_pool=redis.ConnectionPool(host=config.red_host, port=config.red_port, db=config.red_db,
                                             decode_responses=True))
