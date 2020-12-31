from flask import Flask, render_template
import os
import json
import cv2
import sys
import src.cameraClass as camCls
import src.camMngClass as camMng
import atexit
import time

app = Flask(__name__)

#camera = camCls.Camera(src=4, rot=180)
#camera.calibrate_board(3)
camManager = camMng.camManager()

def exit_handler():
    camManager.stop_cams()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wait_throw')
def get_score():
    score, event, std_pos = camManager.detection()
    return json.dumps({'score': score, 'event': event, 'pos_x': int(std_pos[0]), 'pos_y': int(std_pos[1])})

if __name__ == '__main__':
    atexit.register(exit_handler)
    camManager.start_cams()
    app.run(host='0.0.0.0', port='8090') #, debug=True


    #for cam in camManager.cam_list:
    #   cam.manual_calibration()

    #camManager.cam_list[0].calibrate_board(12)
    #camManager.cam_list[1].calibrate_board(3)
    #camManager.cam_list[2].calibrate_board(4)

    #camManager.start_cams()
    #while True:
        #camManager.motion_detection()

    #time.sleep(1)
    #camManager.stop_cams()
    #print('end')
    #img = cv2.imread('static/jpg/test_0.jpg')
    #print(camera.board.h)
    #imgWarp = cv2.warpPerspective(img,camManager.cam_list[0].board.h,(800,800))
    #img = camera.cap.read() 
    #cv2.imwrite('static/jpg/warp.jpg', imgWarp)
