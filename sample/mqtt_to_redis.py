import asyncio

import redis
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1
from pip import logger

conn = redis.StrictRedis(port=32768, decode_responses=True)

# TOPIC = '#'
TOPIC = [('+/TSE/+', QOS_1), ('+/OTC/+', QOS_1),('+/TFE/+', QOS_1),('+/OPT/+', QOS_1)]
count = 0


async def count_avg(future):
    global count
    while 1:
        if future.done():
            break
        print('Count - {}'.format(count))
        count = 0
        await asyncio.sleep(1)


async def uptime_coro(future):
    C = MQTTClient()
    await C.connect('mqtt://vpn.alvin.tw/', )
    await C.subscribe(TOPIC)
    try:
        i = 1
        while 1:
            message = await C.deliver_message()
            i += 1
            packet = message.publish_packet
            global count
            count += 1
            msg = packet.payload.data.decode('utf8')
            stock_id = packet.variable_header.topic_name.split('/')[-1]
            content = msg
            #print(stock_id)
            conn.rpush(stock_id, content)
        await C.unsubscribe([TOPIC])
        await C.disconnect()

    except ClientException as ce:
        logger.error("Client exception: %s" % ce)

    future.set_result('Finish')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    asyncio.ensure_future(uptime_coro(future))
    asyncio.ensure_future(count_avg(future))
    loop.run_until_complete(future)
