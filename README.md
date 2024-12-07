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
cd omni.isaac.extended_assets
pip install -e .

cd omni.isaac.extended_tasks
pip install -e .
```

:construction: Update the DISPLAY environment in the .env file using free display. (The display free if it is not in the /tmp/.X11-unix/ folder of the host machine)

:construction: Also, change the WEBPORT to enable the first free port (Get it by calculating DISPLAY + 6080).

```
# If there is no file /tmp/.X11-unix/X20
DISPLAY=:20
WEBPORT=6100
```


## Usage
You can simulate the Isaac-Assembly-Franka-v0 environment by running the following command.
```
cd ./scripts
python create_scene.py --task Isaac-Assembly-Franka-v0 --enable_cameras
```

## Extension
This repository is intended for use with IsaacTAMP and IsaacLab. It can be installed via the following command:
```
pip install git+https://github.com/makolon/IsaacLabExtendedTasks.git/#subdirectory=omni.isaac.extended_assets
pip install git+https://github.com/makolon/IsaacLabExtendedAssets.git/#subdirectory=omni.isaac.extended_tasks
```

For detailed usage instructions, please refer to the README files located in each directory.
