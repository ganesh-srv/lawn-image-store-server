from flask import Flask, jsonify, request
# import xarray as xr
# import numpy as np
# from cachetools import cached, TTLCache
from pprint import pprint
import os
import base64
from datetime import datetime
from flask_jwt_extended import JWTManager, jwt_required

lawnImageServerApp = Flask(__name__)
data_folder = os.path.join(os.path.dirname(os.getcwd()), 'Images/')



# Set up Flask-JWT-Extended
lawnImageServerApp.config['JWT_SECRET_KEY'] = 'hrrr-weather-lawn'
jwt = JWTManager(lawnImageServerApp)


# Test request
@lawnImageServerApp.route('/health')
def hello():
    return jsonify({'staus': 'Ok'})


@lawnImageServerApp.route('/lawn/image/save', methods=['POST'])
# @jwt_required()
def upload():
    try:   
        data = request.get_json()
        base64_image = data.get('image')
        date_time = data.get('datetime')
        dt = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        time  =dt.time().strftime('%H-%M-%S')
        directory = os.path.join(data_folder, f'{dt.date()}')
        if not os.path.exists(directory):
            os.makedirs(directory)
        image_data = base64.b64decode(base64_image)
        filename = os.path.join(directory, f'{time}.jpeg')
        with open(filename, 'wb') as f:
            f.write(image_data)
        return jsonify({'message': 'Image saved successfully'}), 200
    except KeyError:
        return jsonify({'error': 'Invalid JSON. Please provide both "image" and "datetime".'}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred: ' + str(e)}), 500


if __name__=='__main__':
    lawnImageServerApp.run(host="0.0.0.0", port=6000, debug=True)
