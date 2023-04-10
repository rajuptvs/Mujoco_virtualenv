import threading
import queue
from fastapi import FastAPI
from queue import Queue, Empty
import mujoco as mj 
from mujoco import viewer
import numpy as np
import os
import time

app = FastAPI()

model = mj.MjModel.from_xml_path('ball.xml')  # MuJoCo model
data = mj.MjData(model)                       # MuJoCo data
cam = mj.MjvCamera()                          # Abstract camera
opt = mj.MjvOption()                          # visualization options
renderer = mj.Renderer(model)

# enable joint visualization option:
scene_option = mj.MjvOption()
scene_option.flags[mj.mjtVisFlag.mjVIS_JOINT] = True
viwer = viewer.launch_passive(model= model, data= data)
def my_infinite_loop(q):
    while True:
        try:
            print("looping")
            mj.mj_step(model, data)
            print("current location", round(data.body("sphero1").xpos[0], 6))
            # wait for a message to arrive in the queue with a timeout of 1 second
            msg = q.get(timeout=0.0000000000000001)
            
            print("running simulation")
            # check the message type and act accordingly
            if msg['type'] == 'update_state':
                # update the state of the loop
                print("updating state")
                pass
            elif msg['type'] == 'do_something':
                # perform some action
                data.body('sphero1').xfrc_applied[0] = 1
                print("performing action")
                pass
            elif msg['type'] == 'stop':
                # stop the loop
                print("stopping loop")
                break
        except Empty:
            # continue looping if no new messages arrived within the timeout
            pass

queue = queue.Queue()
thread = threading.Thread(target=my_infinite_loop, args=(queue,))
thread.start()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/update_state/{data}")
async def update_state(data: int):
    queue.put({'type': 'update_state', 'data': data})
    return {"message": "state updated"}

@app.get("/do_something")
async def do_something():
    queue.put({'type': 'do_something'})
    return {"message": "action performed"}


@app.get("/stop")
async def stop():
    queue.put({'type': 'stop'})
    return {"message": "loop stopped"}