# IsaacLabExtendedTasks
This repository is based on IsaacLab and is designed to add new tasks that are not available in `omni.isaac.lab_tasks`.

## Structure
The repository, IsaacLabExtendedTasks, consists of two main components:
- `omni.isaac.extended_assets`
- `omni.isaac.extended_tasks`

Both components are built on top of `omni.isaac.lab_assets` and `omni.isaac.lab_tasks`.

## Installation
To install this repository, follow these steps:

1. Clone the repository.
```
git clone https://github.com/makolon/IsaacLabExtendedTasks.git
```

2. Build docker container.
```
cp .env.sample .env
docker compose build
# Or build separately
docker compose build isaac-lab-base
docker compose build isaac-lab-extasks
```
3. Enter `extasks` container.
```
docker compose run isaac-lab-base
docker compose run isaac-lab-extasks
```
4. Run the following command in each directory to install the necessary components:
```
cd exts/
cd omni.isaac.extended_assets/
pip install -e .

cd omni.isaac.extended_tasks/
pip install -e .
```

:construction: Update the DISPLAY environment in the .env file using free display. (The display free if it is not in the /tmp/.X11-unix/ folder of the host machine) Also, change the WEBPORT to enable the first free port (Get it by calculating DISPLAY + 6080).

```
# If there is no file /tmp/.X11-unix/X20
DISPLAY=:20
WEBPORT=6100
```


## Example
You can simulate the `Isaac-Siemens-Gearbox-Assembly-Franka-v0` environment by running the following command.
```
cd ./scripts
python create_scene.py --task Isaac-Siemens-Gearbox-Assembly-Franka-v0 --enable_cameras
```


## Available Tasks
The following tasks are currently available in this repository:
- **Block World**
  - Sort
    - `Isaac-Block-Sort-Franka-v0`
    - `Isaac-Block-Sort-UR5e-v0`
    - `Isaac-Block-Sort-UR10e-v0`
    - `Isaac-Block-Sort-XArm7-v0`
    - `Isaac-Block-Sort-LBRIIWA7-v0`
    - `Isaac-Block-Sort-Gen3n7-v0`
    - `Isaac-Block-Sort-Jaco7N-v0`
    - `Isaac-Block-Sort-Jaco7S-v0`
  - Stack
    - `Isaac-Block-Stack-Franka-v0`
    - `Isaac-Block-Stack-UR5e-v0`
    - `Isaac-Block-Stack-UR10e-v0`
    - `Isaac-Block-Stack-XArm7-v0`
    - `Isaac-Block-Stack-LBRIIWA7-v0`
    - `Isaac-Block-Stack-Gen3n7-v0`
    - `Isaac-Block-Stack-Jaco7N-v0`
    - `Isaac-Block-Stack-Jaco7S-v0`
- **Factory**
  - Siemens Gearbox Assembly
    - `Isaac-Siemens-Gearbox-Assembly-Franka-v0`
    - `Isaac-Siemens-Gearbox-Assembly-UR5e-v0`
    - `Isaac-Siemens-Gearbox-Assembly-UR10e-v0`
    - `Isaac-Siemens-Gearbox-Assembly-XArm7-v0`
  - FMB Single Assembly
    - `Isaac-FMB-Single-Assembly-Franka-v0`
    - `Isaac-FMB-Single-Assembly-UR5e-v0`
    - `Isaac-FMB-Single-Assembly-UR10e-v0`
    - `Isaac-FMB-Single-Assembly-XArm7-v0`
  - IndustReal Gear Assembly
    - `Isaac-Industreal-Gear-Assembly-Franka-v0`
    - `Isaac-Industreal-Gear-Assembly-UR5e-v0`
    - `Isaac-Industreal-Gear-Assembly-UR10e-v0`
    - `Isaac-Industreal-Gear-Assembly-XArm7-v0`
  - Fusion360 Joint Assembly
    - `Isaac-Fusion360-Joint-Assembly-Franka-v0`
    - `Isaac-Fusion360-Joint-Assembly-UR5e-v0`
    - `Isaac-Fusion360-Joint-Assembly-UR10e-v0`
    - `Isaac-Fusion360-Joint-Assembly-XArm7-v0`
- **Kitchen**
  - Bowl Stack
    - `Isaac-Bowl-Stack-Franka-v0`
    - `Isaac-Bowl-Stack-UR5e-v0`
    - `Isaac-Bowl-Stack-UR10e-v0`
    - `Isaac-Bowl-Stack-XArm7-v0`
  - Coffee Make
    - `Isaac-Coffee-Make-Franka-v0`
    - `Isaac-Coffee-Make-UR5e-v0`
    - `Isaac-Coffee-Make-UR10e-v0`
    - `Isaac-Coffee-Make-XArm7-v0`


## Extension
This repository is intended for use with IsaacTAMP and IsaacLab. It can be installed via the following command:
```
pip install git+https://github.com/makolon/IsaacLabExtendedTasks.git/#subdirectory=omni.isaac.extended_assets
pip install git+https://github.com/makolon/IsaacLabExtendedAssets.git/#subdirectory=omni.isaac.extended_tasks
```

For detailed usage instructions, please refer to the README files located in each directory.
