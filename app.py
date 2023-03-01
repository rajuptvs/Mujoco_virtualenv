from flask import Flask, request
from mujoco_py import load_model_from_path, MjSim
from mujoco_py.mjviewer import MjViewer
from multiprocessing import Process, Value

app = Flask(__name__)

class MujocoSimulation:
    def __init__(self):
        model = load_model_from_path('ball.xml')
        self.sim = MjSim(model)
        self.viewer = MjViewer(self.sim)


    def move_right(self):
        print("right right")
        ball_id = self.sim.model.body_name2id('ball')
        self.sim.data.xfrc_applied[ball_id,0] = 1.0
        return 'RIGHT FORCE APPLIED'

    def move_left(self):
        ball_id = self.sim.model.body_name2id('ball')
        self.sim.data.xfrc_applied[ball_id,0] = -1.0
        return 'OK'

    def move_up(self):
        ball_id = self.sim.model.body_name2id('ball')
        self.sim.data.xfrc_applied[ball_id,1] = 1.0
        return 'OK'

    def move_down(self):
        ball_id = self.sim.model.body_name2id('ball')
        self.sim.data.xfrc_applied[ball_id,1] = -1.0
        return 'OK'

    def run_simulation(self, sim_running):
        # Load the Mujoco model and create a simulation


        while sim_running.value:
            self.sim.step()
            self.viewer.render()

simulation = MujocoSimulation()

@app.route('/move_right', methods=['POST'])
def move_right():
    return simulation.move_right()

@app.route('/move_left', methods=['POST'])
def move_left():
    return simulation.move_left()

@app.route('/move_up', methods=['POST'])
def move_up():
    return simulation.move_up()

@app.route('/move_down', methods=['POST'])
def move_down():
    return simulation.move_down()

if __name__ == '__main__':
    sim_running = Value('b', True)
    simulation_process = Process(target=simulation.run_simulation, args=(sim_running,))
    simulation_process.start()

    app.run(debug=True)

    sim_running.value = False
    simulation_process.join()
