from fastapi import FastAPI, UploadFile
# from typing import Optional
# from pydantic import BaseModel
from subprocess import Popen #check_output
# from starlette.responses import 
# from dotenv import load_dotenv
import os

app = FastAPI()

@app.get('/')
def index():
    return 'My Personal Server'


# @app.get('/apple-touch-icon-120x120-precomposed.png')
# def image_png():
#     with open('./FastAPI/app/apple-touch-icon-120x120-precomposed.png', 'r') as file:
#         img = file.read()
#     return UploadFile(filename="apple-touch-icon-120x120-precomposed.png", file=img, content_type="image/png")

@app.get('/start_kodi')
def start_kodi():
    # load_dotenv()
    # return check_output(['sshpass', '-p', os.environ['SSHPASS'], 'ssh', '-p', '1990', 'jetson@192.168.0.170', 'kd'])
    try:
        Popen(["startx", "kodi"])
        return {'successfully launched kodi'}
    except:
        return {'failed to launch kodi'}


@app.get('/start_chrome')
def start_chrome():
    # load_dotenv()
    # return check_output(['sshpass', '-p', os.environ['SSHPASS'], 'ssh', '-p', '1990', 'jetson@192.168.0.170', 'kd'])
    try:
        Popen(["startx", "chromium-browser"])
        return {'successfully launched chrome'}
    except:
        return {'failed to launch chrome'}
