## JacobianIK3D <- IterateIK3D

JacobianIK3D calculates rotations for all joints simultaneously, producing natural and smooth movement. It is particularly suited for biological animations. The resulting twist around the forward vector will always be kept from the previous pose. **Note:** It converges more slowly than other IK solvers, leading to gentler and less immediate tracking of targets.

