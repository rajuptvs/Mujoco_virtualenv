import mujoco_py as mj
from mujoco_py import load_model_from_path, MjSim
from mujoco_py.mjviewer import MjViewer
import glfw

ball_list=["ball1","ball2","ball3","ball4"]
ball_ids=ball_list[0]
time_limit = 0
timer = None  

def reset_forces():
    ball_id = sim.model.body_name2id('ball')
    
    sim.data.xfrc_applied[ball_id,0] = 0.0
    sim.data.xfrc_applied[ball_id,1] = 0.0
    global timer
    timer = None  

def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_RIGHT and action != glfw.RELEASE:
        ball_id = sim.model.body_name2id('ball')
        sim.data.xfrc_applied[ball_id,0] = 1.0
        print("right key pressed and registered")
    elif key == glfw.KEY_LEFT and action != glfw.RELEASE:
        ball_id = sim.model.body_name2id('ball')
        sim.data.xfrc_applied[ball_id,0] = -1.0
        print("left key pressed and registered")
    elif key == glfw.KEY_UP and action != glfw.RELEASE:
        ball_id = sim.model.body_name2id('ball')
        sim.data.xfrc_applied[ball_id,1] = 1.0
        print("up key pressed and registered")
    elif key == glfw.KEY_DOWN and action != glfw.RELEASE:
        ball_id = sim.model.body_name2id('ball')
        sim.data.xfrc_applied[ball_id,1] = -1.0
        print("down key pressed and registered")
    elif key == glfw.KEY_E and action != glfw.RELEASE:
        ball_id = sim.model.body_name2id('ball')
        sim.data.xfrc_applied[ball_id,0] = 1.0
        sim.data.xfrc_applied[ball_id,1] = 1.0
        print("E key and registered")
    elif key == glfw.KEY_SPACE and action != glfw.RELEASE:
        reset_forces() 


model = load_model_from_path('ball.xml')
sim = MjSim(model)
viewer = MjViewer(sim)
# Set the key callback function
glfw.set_key_callback(viewer.window, key_callback)

import time
# Run the simulation
while True:
    print("timer is",timer)
    #### Hacky way to reset forces after a second 
    ## have to figure out how to do this properly when a key is released
    if timer is None:  
        timer = time.time()
    elif time.time() - timer > 1.0:  
        reset_forces()
    sim.step()
    viewer.render()
