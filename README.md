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
./docker/container.py start base
./docker/container.py start extasks
```
3. Enter `extasks` container.
```
./docker/container.py enter extasks
```
3. Run the following command in each directory to install the necessary components:
```
cd omni.isaac.extended_assets
pip install -e .

cd omni.isaac.extended_tasks
pip install -e .
```
:construction: You have to add `DISPLAY=:0` as environment variable.


## Usage
You can simulate the Isaac-Franka-Assembly-v0 environment by running the following command.
```
cd ./scripts
python create_scene.py --task Isaac-Franka-Assembly-v0 --enable_cameras
```

## Extension
This repository is intended for use with IsaacTAMP and IsaacLab. It can be installed via the following command:
```
pip install git+https://github.com/makolon/IsaacLabExtendedTasks.git/#subdirectory=omni.isaac.extended_assets
pip install git+https://github.com/makolon/IsaacLabExtendedAssets.git/#subdirectory=omni.isaac.extended_tasks
```

For detailed usage instructions, please refer to the README files located in each directory.
