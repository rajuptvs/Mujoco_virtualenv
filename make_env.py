"""
Generates a mujoco envrionment spec with N_ROBOTS spheros in random positions on a MAP_SIZE map.
"""
import random as rnd

MODEL_XML = """<?xml version="1.0" ?>
<mujoco>
    <option timestep="0.005" />
    <worldbody>
        <camera euler="0 0 0" fovy="40" name="rgb" pos="0 0 2.5"></camera>
        SPHEROS_
        <body name="floor" pos="FLOOR_ 0.025">
            <geom condim="3" size="FLOORSIZE_ 0.02" rgba="0.8 0.8 0.8 0.2" type="box"/>
        </body>
    </worldbody>
</mujoco>
"""

MAP_SIZE = (10, 10)
N_ROBOTS = 3


def build_env(sphero_poss, colors=None):
    env_str = MODEL_XML
    spheros_str = ""
    if colors:
        assert len(colors) == len(sphero_poss)
    for si, pos in enumerate(sphero_poss):
        rgba = " ".join([str(i) for i in colors[si]]) if colors else "0.5 0.5 0.5 0.75"
        sphero_str = f"""
    <body name="s{si}" pos="{pos[0]} {pos[1]} 0.3">
        <joint type="free" stiffness="0" damping="0" frictionloss="0.1" armature="0"/>
        <geom mass="1.0" friction="1 1 1" pos="0 0 0" rgba="{rgba}" size="0.15" type="sphere"/>
    </body>"""
        spheros_str += sphero_str
    env_str = env_str.replace("SPHEROS_", spheros_str)
    floor_coords_str = "0 0"
    env_str = env_str.replace("FLOOR_", floor_coords_str)
    env_str = env_str.replace("FLOORSIZE_", f"{MAP_SIZE[0]} {MAP_SIZE[1]}")
    return env_str


def make_random_env():
    sphero_positions = []
    # generate a robot for each player to have enough to play
    colors = []
    # stones that are on the board
    for i in range(N_ROBOTS):
        x = rnd.random() * MAP_SIZE[0]
        y = rnd.random() * MAP_SIZE[1]
        # randomly assign color
        rgba = (1, 1, 1, 1) if rnd.random() < 0.5 else (0, 0, 0, 1)
        colors.append(rgba)
        sphero_positions.append((x, y))
    env = build_env(sphero_positions, colors)
    return env


def make_empty_env():
    return make_random_env(0)


if __name__=="__main__":
    env = make_empty_env()
    with open("board.xml", "w") as f:
        f.write(env)