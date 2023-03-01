from mujoco_py import load_model_from_path, MjSim
from mujoco_py.mjviewer import MjViewer
import glfw

# Define the key callback function
def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_RIGHT and action == glfw.PRESS:
        ball_id = sim.model.body_name2id('ball')
        sim.data.xfrc_applied[ball_id,0] = 1.0
        print("right key pressed and registered")
    if key == glfw.KEY_LEFT and action == glfw.PRESS:
        ball_id = sim.model.body_name2id('ball')
        sim.data.xfrc_applied[ball_id,0] = -1.0
        print("left key pressed and registered")
    if key == glfw.KEY_UP and action == glfw.PRESS:
        # Apply a force to the ball when the spacebar is pressed
        ball_id = sim.model.body_name2id('ball')
        sim.data.xfrc_applied[ball_id,1] = 1.0
        # sim.data.xfrc_applied[ball_id,0] = -0.8 
        print("up key pressed and registered")
    if key == glfw.KEY_DOWN and action == glfw.PRESS:
        # Apply a force to the ball when the spacebar is pressed
        ball_id = sim.model.body_name2id('ball')
        sim.data.xfrc_applied[ball_id,1] = -1.0 
        print("down key pressed and registered")
        
# Load the Mujoco model and create a simulation
model = load_model_from_path('ball.xml')
sim = MjSim(model)
viewer = MjViewer(sim)
# Set the key callback function
glfw.set_key_callback(viewer.window, key_callback)

# Run the simulation
while True:
    sim.step()
    viewer.render()
