## SkeletonProfileHumanoid <- SkeletonProfile

A SkeletonProfile as a preset that is optimized for the human form. This exists for standardization, so all parameters are read-only. A humanoid skeleton profile contains 56 bones divided into 4 groups: `"Body"`, `"Face"`, `"LeftHand"`, and `"RightHand"`. It is structured as follows: [codeblock lang=text] Root └─ Hips ├─ LeftUpperLeg │ └─ LeftLowerLeg │ └─ LeftFoot │ └─ LeftToes ├─ RightUpperLeg │ └─ RightLowerLeg │ └─ RightFoot │ └─ RightToes └─ Spine └─ Chest └─ UpperChest ├─ Neck │ └─ Head │ ├─ Jaw │ ├─ LeftEye │ └─ RightEye ├─ LeftShoulder │ └─ LeftUpperArm │ └─ LeftLowerArm │ └─ LeftHand │ ├─ LeftThumbMetacarpal │ │ └─ LeftThumbProximal │ │ └─ LeftThumbDistal │ ├─ LeftIndexProximal │ │ └─ LeftIndexIntermediate │ │ └─ LeftIndexDistal │ ├─ LeftMiddleProximal │ │ └─ LeftMiddleIntermediate │ │ └─ LeftMiddleDistal │ ├─ LeftRingProximal │ │ └─ LeftRingIntermediate │ │ └─ LeftRingDistal │ └─ LeftLittleProximal │ └─ LeftLittleIntermediate │ └─ LeftLittleDistal └─ RightShoulder └─ RightUpperArm └─ RightLowerArm └─ RightHand ├─ RightThumbMetacarpal │ └─ RightThumbProximal │ └─ RightThumbDistal ├─ RightIndexProximal │ └─ RightIndexIntermediate │ └─ RightIndexDistal ├─ RightMiddleProximal │ └─ RightMiddleIntermediate │ └─ RightMiddleDistal ├─ RightRingProximal │ └─ RightRingIntermediate │ └─ RightRingDistal └─ RightLittleProximal └─ RightLittleIntermediate └─ RightLittleDistal [/codeblock]

**Props:**
- bone_size: int = 56
- group_size: int = 4
- root_bone: StringName = &"Root"
- scale_base_bone: StringName = &"Hips"


