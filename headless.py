import mujoco as mj
from mujoco.glfw import glfw
import numpy as np
import os
import time

xml_path = 'goal_ball.xml' #xml file (assumes this is in the same folder as this file)

#get the full path
dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname + "\\" + xml_path)
xml_path = abspath
print(xml_path)
# MuJoCo data structures
model = mj.MjModel.from_xml_path('ball.xml')  # MuJoCo model
data = mj.MjData(model)                # MuJoCo data
cam = mj.MjvCamera()                        # Abstract camera
opt = mj.MjvOption()                        # visualization options


def xfrc():
    #debug function to check if the force is being applied and the position of the ball
    # data.body('sphero1').xfrc_applied[0] = 1
    data.qvel[0]=0.6
    print(round(data.qpos[0],3),round(data.qpos[1],3))

for i in range(10000000000):
    mj.mj_step(model, data)

    ### can comment out the below if you don't want to see the ball moving or debug
    if i % 1000 == 0 and i <= 10000:
        xfrc()

    print(f"Current Loc:{round(data.qpos[0],3)}")