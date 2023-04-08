import mujoco as mj
from mujoco.glfw import glfw
import numpy as np
import os
import time

xml_path = 'ball.xml' #xml file (assumes this is in the same folder as this file)
simend = 100 #simulation time
print_camera_config = 0 #set to 1 to print camera config
                        #this is useful for initializing view of the model)

# global variables
button_left = False
button_middle = False
button_right = False
lastx = 0
lasty = 0
current_ball=0
x_pos=0
y_pos=0
x_vel_index=0
y_vel_index=1
counter=0
import math
def move_and_rotate(current_coords, angle, forward):
    forward+=angle
    angle= angle
    x, y, z = current_coords
    x_prime = math.cos(angle)
    y_prime = math.sin(angle)
    z_prime = 0
    return  forward, [x_prime, y_prime, z_prime]
## Dictionary to store indexes of x and y velocites of each ball
vel_indexes_dict = {0: [0, 1], 1: [6, 7], 2: [12, 13], 3: [18, 19]}

### Dictionary to store indexes of x and y positions of each ball
pos_indexes_dict = {0: [0, 1], 1: [7, 8], 2: [14, 15], 3: [21, 22]}

### Dictionary to store model names based on index
model_geom_names_dict = {0: 'sphero1', 1: 'sphero2', 2: 'sphero3', 3: 'sphero4'}

### Dictionary to store geom
_overlay = {}
def add_overlay(gridpos, text1, text2):

    if gridpos not in _overlay:
        _overlay[gridpos] = ["", ""]
    _overlay[gridpos][0] += text1 + "\n"
    _overlay[gridpos][1] += text2 + "\n"

def get_position_data(indexes):
    x_pos=indexes[0]
    y_pos=indexes[1]
    x_pos=round(data.qpos[x_pos],4)
    y_pos=round(data.qpos[y_pos],4)
    return x_pos,y_pos
def get_indexes_data(indexes):
    x_pos=indexes[0]
    y_pos=indexes[1]
    return x_pos,y_pos
    
    print("indexes",indexes)

#HINT1: add the overlay here
def create_overlay(model,data):
    global times
    topleft = mj.mjtGridPos.mjGRID_TOPLEFT
    topright = mj.mjtGridPos.mjGRID_TOPRIGHT
    bottomleft = mj.mjtGridPos.mjGRID_BOTTOMLEFT
    bottomright = mj.mjtGridPos.mjGRID_BOTTOMRIGHT
    
    
    add_overlay(
            bottomleft,
            "Key Bindings",' ' ,
            )
    add_overlay(
        bottomleft,
        "Restart",'Backspace' ,
         )
    add_overlay(
        bottomleft,
        "Quit",'Esc' ,
    )
    add_overlay(
        bottomleft,
        "Previous Robot",'F1' ,
         )

    add_overlay(
        bottomleft,
        "Next Robot",'F2' ,
         )
    add_overlay(
        bottomright,
        "Current Ball",str(current_ball) ,
    )
    add_overlay(
        bottomright,
        "Current Position"," X coordinates: "+str(x_pos) + " Y Coordinates: " + str(y_pos) ,
    )
    add_overlay(
        topleft,
        "time",str(data.time) ,
    )

def init_controller(model,data):
    #initialize the controller here. This function is called once, in the beginning
    pass

def controller(model, data):
    #put the controller here. This function is called inside the simulation.
    pass
def reset_forces():
    global current_ball
    data.body(model_geom_names_dict[current_ball]).xfrc_applied[0:2] = [0, 0]
    print("resetting forces")

def keyboard(window, key, scancode, act, mods):
    global current_ball
    global pos_indexes_dict
    global x_pos
    global y_pos
    global x_vel_index
    global y_vel_index
    if act == glfw.PRESS and key == glfw.KEY_BACKSPACE:
        mj.mj_resetData(model, data)
        mj.mj_forward(model, data)
    elif act == glfw.PRESS and key == glfw.KEY_ESCAPE:
        print("Terminating the simulation")
        glfw.set_window_should_close(window, True)
    elif act != glfw.RELEASE and key == glfw.KEY_RIGHT:
        data.qvel[x_vel_index]=0.6
    elif act != glfw.RELEASE and key == glfw.KEY_UP:
        data.qvel[y_vel_index]=0.6
    elif act != glfw.RELEASE and key == glfw.KEY_LEFT:
        data.qvel[x_vel_index]=-0.6
    elif act != glfw.RELEASE and key == glfw.KEY_DOWN:
        data.qvel[y_vel_index]=-0.6
    elif act != glfw.RELEASE and key == glfw.KEY_SPACE:
        ball_pos = data.qpos
        test=[]
        for i in ball_pos:
            i=round(i, 6)
            test.append(i)
        print(len(test))
    elif act != glfw.RELEASE and key == glfw.KEY_F1:
        model.geom(model_geom_names_dict[current_ball]).rgba=[1,1,1,1]
        if current_ball==0:
            current_ball=3
        else:
            current_ball-=1
        indexes=pos_indexes_dict[current_ball]
        vel_indexes=vel_indexes_dict[current_ball]
        x_vel_index,y_vel_index= get_indexes_data(vel_indexes)
        x_pos,y_pos=get_position_data(indexes)
        print(model.geom(model_geom_names_dict[current_ball]).rgba)
        model.geom(model_geom_names_dict[current_ball]).rgba=[1,0,0,1]
        # print(x_pos,y_pos)   
        
    elif act != glfw.RELEASE and key == glfw.KEY_F2:
        model.geom(model_geom_names_dict[current_ball]).rgba=[1,1,1,1]
        if current_ball<3:
            current_ball+=1                                                                            
        else:
            current_ball=0
        indexes=pos_indexes_dict[current_ball]
        vel_indexes=vel_indexes_dict[current_ball]
        x_vel_index,y_vel_index= get_indexes_data(vel_indexes)
        print(indexes)
        x_pos,y_pos=get_position_data(indexes)
        model.geom(model_geom_names_dict[current_ball]).rgba=[1,0,0,1]
        # print(x_pos,y_pos)
        
    elif act != glfw.RELEASE and key == glfw.KEY_0:
        ### Use this key to debug functions and code as you experiment
        print('Debugging Key')
        # data.xfrc_applied[6][0]=1
        print(model.body('sphero1'))
        # print(data.body('sphero1').xpos)
        
        # data.body(model_geom_names_dict[current_ball]).xfrc_applied[0]=1
    elif act!=glfw.RELEASE and key==glfw.KEY_DELETE:
        reset_forces()

        
        
def mouse_button(window, button, act, mods):
    # update button state
    global button_left
    global button_middle
    global button_right

    button_left = (glfw.get_mouse_button(
        window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS)
    button_middle = (glfw.get_mouse_button(
        window, glfw.MOUSE_BUTTON_MIDDLE) == glfw.PRESS)
    button_right = (glfw.get_mouse_button(
        window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS)

    # update mouse position
    glfw.get_cursor_pos(window)

def mouse_move(window, xpos, ypos):
    # compute mouse displacement, save
    global lastx
    global lasty
    global button_left
    global button_middle
    global button_right

    dx = xpos - lastx
    dy = ypos - lasty
    lastx = xpos
    lasty = ypos

    # no buttons down: nothing to do
    if (not button_left) and (not button_middle) and (not button_right):
        return

    # get current window size
    width, height = glfw.get_window_size(window)

    # get shift key state
    PRESS_LEFT_SHIFT = glfw.get_key(
        window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS
    PRESS_RIGHT_SHIFT = glfw.get_key(
        window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS
    mod_shift = (PRESS_LEFT_SHIFT or PRESS_RIGHT_SHIFT)

    # determine action based on mouse button
    if button_right:
        if mod_shift:
            action = mj.mjtMouse.mjMOUSE_MOVE_H
        else:
            action = mj.mjtMouse.mjMOUSE_MOVE_V
    elif button_left:
        if mod_shift:
            action = mj.mjtMouse.mjMOUSE_ROTATE_H
        else:                                                                                                         
            action = mj.mjtMouse.mjMOUSE_ROTATE_V
    else:
        action = mj.mjtMouse.mjMOUSE_ZOOM

    mj.mjv_moveCamera(model, action, dx/height,
                      dy/height, scene, cam)

def scroll(window, xoffset, yoffset):
    action = mj.mjtMouse.mjMOUSE_ZOOM
    mj.mjv_moveCamera(model, action, 0.0, -0.05 *
                      yoffset, scene, cam)

#get the full path
dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname + "/" + xml_path)
xml_path = abspath

# MuJoCo data structures
model = mj.MjModel.from_xml_path(xml_path)  # MuJoCo model
data = mj.MjData(model)                # MuJoCo data
cam = mj.MjvCamera()                        # Abstract camera
opt = mj.MjvOption()                        # visualization options
model.geom(model_geom_names_dict[current_ball]).rgba=[1,0,0,1]
# Init GLFW, create window, make OpenGL context current, request v-sync
glfw.init()
window = glfw.create_window(1920, 1080, "Demo", None, None)
glfw.make_context_current(window)
glfw.swap_interval(1)
times=data.time+2
# initialize visualization data structures
mj.mjv_defaultCamera(cam)
mj.mjv_defaultOption(opt)
scene = mj.MjvScene(model, maxgeom=10000)
context = mj.MjrContext(model, mj.mjtFontScale.mjFONTSCALE_150.value)

# install GLFW mouse and keyboard callbacks
glfw.set_key_callback(window, keyboard)
glfw.set_cursor_pos_callback(window, mouse_move)
glfw.set_mouse_button_callback(window, mouse_button)
glfw.set_scroll_callback(window, scroll)

# Example on how to set camera configuration
cam.azimuth = 89.39999999999995
cam.elevation = -22.40000000000012
cam.distance = 23.42488559492616
cam.lookat = np.array([ 0.47564614429835234 , -0.004981136964072872 , 2.6295723292545947 ])

#initialize the controller
init_controller(model,data)

#set the controller
mj.set_mjcb_control(controller)
def simulation_loop():
    global current_ball
    global pos_indexes_dict
    global x_pos
    global y_pos
    global x_vel_index
    global y_vel_index
    global times
    global counter
    while not glfw.window_should_close(window):
        counter+=1
        time_prev = data.time

        while (data.time - time_prev < 1.0/60.0):
            x_pos=round(data.qpos[0],6)
            y_pos=round(data.qpos[1],6)
            mj.mj_step(model, data)
            post_xpos=round(data.qpos[0],6)
            post_ypos=round(data.qpos[1],6)
            indexes=pos_indexes_dict[current_ball]
            vel_indexes=vel_indexes_dict[current_ball]
            x_vel_index,y_vel_index= get_indexes_data(vel_indexes)
            x_pos,y_pos=get_position_data(indexes)
            
    


            

        while not True:
            break;

        # get framebuffer viewport
        viewport_width, viewport_height = glfw.get_framebuffer_size(
            window)
        viewport = mj.MjrRect(0, 0, viewport_width, viewport_height)
        create_overlay(model,data)


        #print camera configuration (help to initialize the view)
        if (print_camera_config==1):
            print('cam.azimuth =',cam.azimuth,';','cam.elevation =',cam.elevation,';','cam.distance = ',cam.distance)
            print('cam.lookat =np.array([',cam.lookat[0],',',cam.lookat[1],',',cam.lookat[2],'])')

        # Update scene and render
        mj.mjv_updateScene(model, data, opt, None, cam,
                        mj.mjtCatBit.mjCAT_ALL.value, scene)
        mj.mjr_render(viewport, scene, context)
        for gridpos, [t1, t2] in _overlay.items():

            mj.mjr_overlay(
                mj.mjtFontScale.mjFONTSCALE_150,
                gridpos,
                viewport,
                t1,
                t2,
                context)

        # clear overlay
        _overlay.clear()
        # swap OpenGL buffers (blocking call due to v-sync)
        glfw.swap_buffers(window)

        # process pending GUI events, call GLFW callbacks
        glfw.poll_events()

    glfw.terminate()

simulation_loop()