from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get('personal_index')
def index():
    return 'My Personal Server'