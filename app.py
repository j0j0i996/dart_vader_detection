import os
import json
import sys
import src.cameraClass as camCls
import src.camMngClass as camMng
import atexit
import asyncio
import websockets
import cv2
import time
from flask import Flask, request, send_from_directory, send_file, safe_join
from flask_socketio import SocketIO, send, emit

SOCKET_SERVER_URL = '192.168.0.10'
PORT = 3000

cam_manager = camMng.camManager()

app = Flask(__name__)
app.config["IMAGES"] = "static/jpg"
#app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app)

def exit_handler():
    cam_manager.stop_cams()

@sio.on('connect')
def connect():
    print('connected')

@sio.on('echo')
def echo(message):
    print(message)
    emit('echoresponse', {'data': message['data']})

@sio.on('start_dect')
def start_dect(msg):
    if cam_manager.dect_loop_active == False:
        sio.start_background_task(target = cam_manager.dect_loop(sio))

@sio.on('end_dect')
def end_dect(msg):
    cam_manager.dect_loop_active = False

@sio.on('disconnect')
def disconnect():
    print('disconnected')

@app.route('/echo/<msg>', methods=['GET'])
def echo(msg):
    print(msg)
    return json.dumps( msg )

@app.route('/calibration', methods=['PATCH'])
def calibraton():
    closest_field = request.args.get('closest_field')
    cam_idx = request.args.get('cam_idx')
    success = cam_manager.cam_list[int(cam_idx)].auto_calibration(int(closest_field))
    return str(success)

@app.route('/get-cal-img/<int:cam_idx>', methods=['GET'])
def get_cal_img(cam_idx):
    src = cam_manager.cam_list[cam_idx].src
    filename = 'calibration_warp_{}.jpg'.format(src)
    safe_path = safe_join(app.config["IMAGES"], filename)

    try: 
        return send_file(safe_path, as_attachment=False)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':

    atexit.register(exit_handler)

    cam_manager.start_cams()

    sio.run(app, host=SOCKET_SERVER_URL, port=PORT)

    #cam_manager.take_pic()

    #cam_manager.cam_list[0].auto_calibration(18)
    #cam_manager.cam_list[1].auto_calibration(11)
    #cam_manager.cam_list[2].auto_calibration(2)
    #cam_manager.manual_calibration()

    cam_manager.stop_cams()
