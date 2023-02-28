from mujoco_py import load_model_from_path, MjSim
from mujoco_py.mjviewer import MjViewer
import numpy as np
# Load the MuJoCo XML model and create a simulator
model = load_model_from_path('ball.xml')
sim = MjSim(model)
viewer = MjViewer(sim)

# Set the initial position and velocity of the ball
sim.data.qpos[0:3] = [0, 0,1]
sim.data.qvel[0:3] = [0, 0,0]

# Define the desired circular path as a series of waypoints
gravity=np.array([0,0,-9.81])
num_waypoints = 20
radius = 10
waypoints = np.zeros((num_waypoints, 2))
for i in range(num_waypoints):
    angle = i * 2 * np.pi / num_waypoints
    waypoints[i, :] = [radius*np.cos(angle), radius*np.sin(angle)]

# Define the PID controller gains
kp = 20
ki = 0
kd = 20

# Define the time step and simulation duration
dt = 0.01
duration = 30

# Initialize the error and integral error terms
error = 0
int_error = 0
ball_id = sim.model.body_name2id('ball')

# Run the simulation
for i in range(int(duration/dt)):
    # Compute the current position of the ball
    pos = sim.data.qpos[0:2]

    # Compute the error between the current position and the current waypoint
    current_waypoint = waypoints[i % num_waypoints]
    error = current_waypoint - pos

    # Compute the integral error term
    int_error += error*dt

    # Compute the derivative error term
    if i > 0:
        der_error = (error - prev_error)/dt
    else:
        der_error = 0

    # Compute the control input using the PID formula
    ctrl = kp*error + ki*int_error + kd*der_error
    print(ctrl)

    # Apply the control input as a force to the ball
    sim.data.xfrc_applied[ball_id,0:2] = ctrl

    # Step the simulator forward by one time step
    sim.step()
    viewer.render()

    # Save the current error for use in the next iteration
    prev_error = error