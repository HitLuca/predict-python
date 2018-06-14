import json

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from logs.serializers import LogSerializer

redis_publisher = RedisPublisher(facility='default', broadcast=True)


def publish(object):
    """
    Publish an object to websocket listeners
    :param object: A Django model
    :return: {type: object class name, data: OBJECT}
    """
    message = RedisMessage(_serializer(object))
    redis_publisher.publish_message(message)


def _serializer(object):
    """Assumed to be Django models"""
    name = object.__class__.__name__
    if name == 'Log':
        data = LogSerializer(object).data
    else:
        raise NotImplementedError("Websocket not implemented for class {}".format(name))
    return json.dumps({'type': name, 'data': data})
