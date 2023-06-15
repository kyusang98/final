from bottle import post, route, run, request, template, response

from crawl import dictionary

import time
from camera import VideoCamera

import boto3
from boto3.dynamodb.conditions import Key, Attr


import telegram
import asyncio

#telegram code
bot_token = '6082136191:AAG35lMMeZnAxVUT9V-OrFn_aTILFvfGxys'
bot = telegram.Bot(token = bot_token)

async def get_updates():
    updates = await bot.getUpdates()
    return updates

async def send_message(my_chat_id, message):
    await bot.sendMessage(chat_id = my_chat_id, text=message)

updates = asyncio.run(get_updates())

if dictionary is not None:
    my_chat_id = updates[-1].message['from']['id']
    asyncio.run(send_message(my_chat_id, str(dictionary)))



#dynamo code
def write_data(user, date, value, dynamodb):
    table = dynamodb.Table('Attend')
    item = {'User':user, 
            'Date':date, 
            'Value':str(dictionary)}
    table.put_item(Item=item)
    print('item', user, 'added!')
    print('-------')

Access_Key = 'AKIAYBRKZA2B45R472XE'
Secret_Key = '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'

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=Access_Key,
                          aws_secret_access_key=Secret_Key,
                          region_name='us-east-2',
                          endpoint_url='https://dynamodb.us-east-2.amazonaws.com')




@route('/')
@route('/login')
def login():
    return  '''
            <form action='/login' method='post'>
                Username: <input name='username' type='text' />
                Password: <input name='password' type='password' />
                <input value='Login' type='submit' />
            </form> 
            '''

def check_login(username, password):
    if username == '2018732006' and password == 'raspberry':
        return True
    else:
        return False

@post('/login') # or @route('/login', method='POST')
def login_auth():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        date = time.strftime('%Y.%m.%d - %H:%M:%S') #https://bio-info.tistory.com/118
        user = username
        value = str(dictionary)
        write_data(user, date, value, dynamodb)
        return '''
               <p>User %s has been successfully logged in!</p>
               <p>Crawled Data: %s</p>
               <html>
                  <head>
                       <title>Video Streaming Demonstration</title>
                  </head>
                  <body>
                       <h1>Video Streaming Demonstration</h1>
                       <img id="bg" class="img-thumbnail" src="/video_feed"> 
                  </body>
               </html>
               ''' % (username,dictionary)
    else:
        return '<p>Login failed!</p>'

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@route('/video_feed')
def video_feed():
    response.content_type = 'multipart/x-mixed-replace; boundary=frame'
    return gen(VideoCamera())


run(host='172.20.10.3', post=8000, reloader=True)
