# Mujoco_virtualenv

## ToDo's 
* [X] Create simple microservices for the movement (API endpoints are working (Postman) but having issues interacting with mujoco)[code in microservices branch] 
* [ ] Migrate current code to dm_control instead of Mujoco_py to test other rendering options

## Current Challenges
* [ ] There is a weird issue happening when working with threads/multiprocess with microservices (in a separate branch) 
* [ ] Planning to migrate the code to dmcontrol (as it supports multiple rendering option)

### Installation instructions : 
pip install -r requirements.txt 

install mujoco-py. for further instructions check [here](https://blog.guptanitish.com/blog/install-mujoco/)<br/>

### Demo of the keyboard input in mujoco <br/>
![](https://github.com/rajuptvs/Mujoco_virtualenv/blob/main/demos/keyboard_demo.gif)
