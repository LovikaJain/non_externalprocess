import asyncio
from aiohttp import web
import socketio
import aioredis
 
mgr = socketio.AsyncRedisManager('redis://127.0.0.1:6379/0')
sio = socketio.AsyncServer(client_manager=mgr)
# external_sio = socketio.AsyncRedisManager('redis://127.0.0.1:6379/0')
# redis = aioredis.create_redis_pool('redis://127.0.0.1:6379')

namspace_live_meeting = '/live_meeting_stream'
app = web.Application()
sio.attach(app)

async def background_task():
    count = 0
    global streaming_status
    streaming_status = True
    while streaming_status:
        await sio.sleep(10)
        count += 1
        await sio.emit('event response', {'data': 'Keep alive event'}, namespace=namspace_live_meeting)

async def client(request):
    with open('test.html') as file:
        return web.Response(text=file.read(), content_type='text/html')

@sio.event(namespace=namspace_live_meeting)
async def connect(sid, environ):
    print("Connecting to server using session Id:", sid, "using environment:", environ)
    print("connecting to default room:", 'test')
    # sio.save_session()
    await sio.emit('event response', {'data': 'Connected', 'count': 0}, room='test',  namespace=namspace_live_meeting)

@sio.event(namespace=namspace_live_meeting)
async def disconnect_request(sid):
    print("Disconnecting session")
    global streaming_status
    streaming_status = False
    await sio.disconnect(sid, namespace=namspace_live_meeting)


@sio.event(namespace=namspace_live_meeting)
async def disconnect(sid):
    print("Client disconnected!")


@sio.event(namespace=namspace_live_meeting)
async def test_event(sid, message):
    print("Getting external event")
    await sio.emit('event response', {'data': message['data']}, room=message['room'],  namespace=namspace_live_meeting)
    # await listen_queue(message)
    # print("Message::", channel.get())

# @asyncio.coroutine
# async def listen_queue(message):
#     print("Message:", message)
#     channel = await redis.subscribe('socketio')
#     await channel.get()
#     print(channel)
    
# @sio.on('customized event name')

@sio.event(namespace=namspace_live_meeting)
async def join_room(sid, message):
    sio.enter_room(sid, message['room'], namespace=namspace_live_meeting)
    print("External sio event::", )
    await sio.emit('event response', {'data': 'Entered External Room:' + message['room']}, room=message['room'], namespace=namspace_live_meeting)
    print("Entered in room:", message['room'])


app.router.add_static('/static', 'static')
app.router.add_get('/', client)


if __name__ == '__main__':
    sio.start_background_task(background_task)
    web.run_app(app)

