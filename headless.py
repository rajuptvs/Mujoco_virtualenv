import mujoco as mj
import numpy as np
import os
import time
from fastapi import FastAPI
import uvicorn
import multiprocessing

app = FastAPI()

model = mj.MjModel.from_xml_path('ball.xml')  # MuJoCo model
data = mj.MjData(model)                       # MuJoCo data
cam = mj.MjvCamera()                          # Abstract camera
opt = mj.MjvOption()                          # visualization options


def xfrc():
    # debug function to check if the force is being applied and the position of the ball
    data.body('sphero1').xfrc_applied[0] = 1
    # data.qvel[0] = 0.6
    print(round(data.qpos[0], 3), round(data.qpos[1], 3))
    # return round(data.qpos[0], 3)


def run():
    # run the simulation
    while 1:
        mj.mj_step(model, data)
        # print("current location", round(data.qpos[0], 3))


@app.get('/simulate')
async def runsim():
    p = multiprocessing.Process(target=run)
    p.start()


@app.get('/xfrc')
async def runxfrc():
    return xfrc()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
