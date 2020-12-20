from flask import Flask, render_template
import os
import json
import cv2
import src.cameraClass as camCls

app = Flask(__name__)

camera = camCls.Camera(src=0, rot=180, closest_field = 20)
#camera = camCls.Camera(src=2, rot=180, closest_field = 20)
#camera = camCls.Camera(src=4, rot=180, closest_field = 3)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wait_throw')
def get_score():
    camera.dart_motion_dect()
    return json.dumps({'score': camera.dartThrow.score})

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port='8090') #, debug=True
    img = cv2.imread('static/jpg/base_img0.jpg')
    print(camera.board.h)
    imgWarp = cv2.warpPerspective(img,camera.board.h,(1000,1000))
    #img = camera.cap.read() 
    cv2.imwrite('static/jpg/warp.jpg', imgWarp)
