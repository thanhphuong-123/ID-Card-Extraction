from flask import Flask, render_template
from flask_cors import CORS, cross_origin
from flask import request

import os
# import my_yolov6
import cv2
import sys
from PIL import Image

from predict import predict

# Khởi tạo Flask Server Backend
app = Flask(__name__)

# Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = "static"

# yolov6_model = my_yolov6.my_yolov6("weights/fire_detect.pt", "cpu", "data/mydataset.yaml", 640, False)


@app.route('/', methods=['POST'])
def predict_yolov7():
    image = request.files['file']
    if image:
        # Lưu file
        path_to_save = os.path.join(
            app.config['UPLOAD_FOLDER'], image.filename)
        # print("Save = ", path_to_save)
        # image.save(path_to_save)

        # frame = cv2.imread(path_to_save)
        # cv2.imwrite(path_to_save, frame)
        
        img = predict('D:/Nam-4/Nam-4/HTTM/Flask/yolov7/weights/best.pt', 'D:/Nam-4/Nam-4/HTTM/Flask/yolov7/data/my_dataset.yaml', path_to_save)
        
        result = Image.fromarray(img)
        result.save(path_to_save)
        
        cv2.imshow('result', img)
        cv2.waitKey(0)
    #     # Nhận diên qua model Yolov6
    #     frame, no_object = yolov6_model.infer(frame)

    #     if no_object > 0:
    #         cv2.imwrite(path_to_save, frame)

    #     del frame
    #     # Trả về đường dẫn tới file ảnh đã bounding box
        return path_to_save  # http://server.com/static/path_to_save

@app.route('/image', methods=['GET'])
def get_image():
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'gt_314.png')
    return render_template("test.html", user_image = image_path)

# Start Backend
if __name__ == '__main__':
    app.run(host='localhost', port='5000', debug=True)
