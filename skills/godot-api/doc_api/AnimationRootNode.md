## AnimationRootNode <- AnimationNode

AnimationRootNode is a base class for AnimationNodes that hold a complete animation. A complete animation refers to the output of an AnimationNodeOutput in an AnimationNodeBlendTree or the output of another AnimationRootNode. Used for `AnimationTree.tree_root` or in other AnimationRootNodes. Examples of built-in root nodes include AnimationNodeBlendTree (allows blending nodes between each other using various modes), AnimationNodeStateMachine (allows to configure blending and transitions between nodes using a state machine pattern), AnimationNodeBlendSpace2D (allows linear blending between **three** AnimationNodes), AnimationNodeBlendSpace1D (allows linear blending only between **two** AnimationNodes).

