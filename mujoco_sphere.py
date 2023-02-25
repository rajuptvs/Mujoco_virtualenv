"""
started code for controlling multiple sphere robots
using external force
"""

import glfw
from mujoco_py import load_model_from_path, MjSim, MjViewer
import math
import numpy as np
import paho.mqtt.client as mqtt

# n time steps to apply force, x-force, y-force, z-force, x-torque, y-torque, z-torque
ROBOT_RAD = 0.15
N_ROBOTS = 1


class Sphero:
    def __init__(self, xy, angle, robot_id, model, sim):
        print('Spawning robot at', xy, angle)
        self.y, self.x = xy
        self.angle = angle
        self.r = ROBOT_RAD
        self.color = 0
        self.robot_id = robot_id
        self.centered = False
        self.model = model
        self.sim = sim
        self.vel_integ = np.zeros(3)
        # PID constant
        self.vel_integ_gamma = 0.8

    def getPos(self):
        return self.sim.data.body_xpos[self.robot_id]

    def center(self):
        """apply external torque to center the robot in a target cell
        proportional to velocity and distance to target
        """
        # get the current position
        pos = self.getPos()
        # TODO: get the target position
        target_x = None
        target_y = None
        # get the velocity
        vel = self.sim.data.body_xvelp[self.robot_id]
        self.vel_integ = self.vel_integ_gamma * (self.vel_integ + vel)
        # get the distance to target
        dist = math.sqrt((pos[0] - target_x)**2 + (pos[1] - target_y)**2)
        # check if target is reached
        if dist < 0.02 and abs(vel[0]) < 0.02 and abs(vel[1]) < 0.02:
            self.centered = True
            # stop applying force to zero
            self.sim.data.xfrc_applied[self.robot_id] = np.zeros_like(
                self.sim.data.xfrc_applied[self.robot_id])
        else:
            self.centered = False
            # get the direction to target
            # todo: use the robot angle to determine the direction
            torque_x = None
            torque_y = None
            # apply the force
            self.sim.data.xfrc_applied[self.robot_id] = [
                0, 0, 0,
                -torque_y,
                torque_x,
                0]

    def setColor(self, color):
        self.color = color
        # set robot color if moving to a board
        if color == -1:
            self.model.geom_rgba[self.robot_id - 1] = (1, 1, 1, 1)
        elif color == 1:
            self.model.geom_rgba[self.robot_id - 1] = (0, 0, 0, 1)
        else:
            self.model.geom_rgba[self.robot_id - 1] = (0.5, 0.5, 0.5, 0.75)


class VirtualGoBoardMQTT:
    def __init__(self):
        client = mqtt.Client()
        client.on_message = self.handleMove
        client.connect("localhost", 1883)
        # subscribe to relevant topics
        client.subscribe("/control")
        client.loop_start()
        self.client = client

        self.MODEL_XML = "board.xml"
        self.robots = None
        self.robot_to_id = None
        self.model = None
        self.sim = None
        self.viewer = None
        self.running = None

    def start(self):
        self.model = load_model_from_path(self.MODEL_XML)
        self.sim = MjSim(self.model)
        self.viewer = MjViewer(self.sim)
        self.robots = []
        self.robot_to_id = {}
        # initialize robots
        # note: this has to be consistent with the board.xml file
        for n in range(N_ROBOTS):
            self.robot_to_id[n] = self.model.body_name2id(f's{n}')
            y = None
            x = None
            angle = None
            self.robots.append(Sphero((y, x), angle, self.robot_to_id[n], self.model, self.sim))
        self.running = True
        self.run()

    def run(self):
        # indicate that the board is ready
        while self.running:
            # center the robots and get their true positions
            for robot in self.robots:
                robot.center()
                rx, ry, _ = robot.getPos()
                # do somthing with the robot
            self.sim.step()
            self.viewer.render()
        glfw.destroy_window(self.viewer.window)

    def handleMove(self, cli, _, tm):
        """mqtt message handler"""
        topic = tm.topic
        cmd = topic.split("/")
        if cmd[1] == "control":
            pass
        elif cmd[1] == "reset":
            self.running = False


if __name__ == "__main__":
    vgb = VirtualGoBoardMQTT()
    while True:
        vgb.start()