from redis import Redis


def get_redis_connection():
    return Redis(
        host='localhost',
        port=6379,
        db=0,
        decode_responses=True,
        socket_connect_timeout=5
    )
