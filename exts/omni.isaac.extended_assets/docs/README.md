# Isaac Lab Extended Assets: Assets for Additional Tasks

This extension contains configurations for various assets and sensors. The configuration instances are
used to spawn and configure the instances in the simulation. They are passed to their corresponding
classes during construction.

## Organizing custom assets

For Isaac Lab, we primarily store assets on the Omniverse Nucleus server. However, at times, it may be
needed to store the assets locally (for debugging purposes). In such cases, the extension's `data`
directory can be used for temporary hosting of assets.

Inside the `data` directory, we recommend following the same structure as our Nucleus directory
`Isaac/IsaacLab`. This helps us later to move these assets to the Nucleus server seamlessly.

The recommended directory structure inside `data` is as follows:

* **`Robots/<Company-Name>/<Robot-Name>`**: The USD files should be inside `<Robot-Name>` directory with the name of the robot.
* **`Scenes/<Scene-Name>`**: The USD files should be inside `<Scene-Name>` directory with the name of the scene.
* **`Props/<Prop-Type>/<Prop-Name>`**: The USD files should be inside `<Prop-Name>` directory with the name of the prop. This includes mounts, objects and markers.
* **`Policies/<Task-Name>`**: The policy should be JIT/ONNX compiled with the name `policy.pt`. It should also contain the parameters used for training the checkpoint. This is to ensure reproducibility.

## Referring to the assets in your code

You can use the following snippet to refer to the assets:

```
from omni.isaac.extended_assets import ISAACEXTENDED_ASSETS_DATA_DIR

# Gen3n7
GEN3N7_C_USD_PATH = f"{ISAACEXTENDED_ASSETS_DATA_DIR}/Robots/Kinova/gen3n7.usd"
# XArm7
XAMR7_USD_PATH = f"{ISAACEXTENDED_ASSETS_DATA_DIR}/Robots/UFactory/xarm7.usd"
```

## Maintained model
- Default
  - [x] Franka w/ panda hand
  - [ ] UR5e w/ robotiq2f 85
  - [ ] UR5e w/ robotiq2f 140
  - [ ] UR10e w/ robotiq2f 85
  - [ ] UR10e w/ robotiq2f 140
  - [ ] Gen3 w/ robotiq2f 85
  - [x] xArm7 w/ xarm gripper
  - [ ] iiwa7 w/ allegro hand
  - [ ] iiwa7 w/ schunk wsg50
  - [ ] Jaco7N
  - [ ] Jaco7S
- Instanceable
  - [x] Franka w/ panda hand
  - [ ] UR5e w/ robotiq2f 85
  - [ ] UR5e w/ robotiq2f 140
  - [ ] UR10e w/ robotiq2f 85
  - [ ] UR10e w/ robotiq2f 140
  - [ ] Gen3 w/ robotiq2f 85
  - [x] xArm7 w/ xarm gripper
  - [ ] iiwa7 w/ allegro hand
  - [ ] iiwa7 w/ schunk wsg50
  - [ ] Jaco7N
  - [ ] Jaco7S
