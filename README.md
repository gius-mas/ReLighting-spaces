# ReLighting spaces - Training daylight access cognition in combinatorial spatial assemblages using Reinforcement Learning  
This repository contains RL models an GH-definitions from the paper "ReLighting spaces - Training daylight access cognition in combinatorial spatial assemblages using Reinforcement Learning" by Giuseppe Massafra, Alessio Erioli presented on the FMA 2024 Conference. This repository contains both source code for Python and GH-definition tu use RL-trained agents involved in combinatorial process to build spatial assemblies with adaptive control over daylight access conditions.

# Abstract
This research aims to enhance a combinatorial process for the generation of spatial assemblages with adaptive control over climate-related factors, such as daylight access, by means of Reinforcement Learning (RL). 
In combinatorial design, a finite set of parts and rules for their coupling and iterative aggregation, generates larger assemblies whose properties, performances, and functions, at different system scales, differ  from those of the constituent parts; the whole is composed of multitudes, engendered by the mutually occurring interactions. A key role in establishing the potential for the emergence of holistic qualities lies in the design of both parts and rules as well as in the policy that regulates rule selection in relation to the design goals.
Combinatorial design is defined by Sanchez as an inherently open process, where no kind of optimization is achievable. However, it is possible to operate within this context to create systems whose holistic properties, related to quantitative aspects of the architectural space, follow predetermined design criteria. In their combinatorial research, both Sanchez, Alexander (in “A Pattern Language”), and Stiny (in his study on “Shape Grammars”) use fixed criteria (either stochastic or heuristics-based) for the choice of aggregation; a different strategy is using a reward-oriented policy to derive the aggregation rule to apply at each iteration.   
From this perspective, Makoto Sei Watanabe in his Induction Cities series experimented with "inductive" models: a wide range of viable spatial configurations generated via a stochastic process coupled with selective target conditions based on climatic factors such as direct sunlight access (Sun God City).
Building on Watanabe's work, this study aims to bind combinatorial logic with topological considerations and environmental-climatic feedback, for the context-adaptive generation of spatial units assemblages with control over daylight hours access on exposed surfaces. The approach uses RL-trained agents instead of random choice/heuristics iterative algorithms to adapt to lighting conditions in the process of selection and aggregation of parts. The agents move and place parts (voxels) within a voxelized space, aiming to ensure topological consistency and a target daylight hours access on exposed surfaces in the final assembly.  
The research introduces condition-based adaptivity into a combinatorial process by means of RL training, moving beyond both random choice and predetermined heuristics sets; although both can relate to boundary conditions, they are respectively non-controllable and tied to a specific environmental scenario. Through the agent’s trained policy, the system learns a state-action-reward relationship in a process of continuous feedback between space, environment and climate data that applies to any environmental configuration that can be coded in the system’s terms.
The study is implemented coupling state-of-the-art Python RL libraries (Stable Baselines 3, Gymnasium) and the Rhino+Grasshopper environment for modelling, daylight factor calculation, and visualization, building a custom infrastructure for bidirectional data communication between computing environments during the training and inference phases.

# Installation 
Install Anaconda.
Create Python 3.8 environment and install `stable-baselines3` and `gymnasium` by running the following commands
```bash
    conda create --name py38 python=3.8
    conda activate py38
    pip install stable-baselines3
    pip install gymnasium
````
In order to use gym environments, also install shimmy and swig
```bash
  pip install 'shimmy>=0.2.1'
  pip install swig
````
You need also to install these GH plug-in:
- Hoopsnake for recoursive loops in GH
- Ladybug Tools for solar analysis

# Usage
Run a istance of the Anaconda Powershell, and do the following
```bash
    conda activate py38
````
Go to the folder where your scripts are: copy the address from the address bar in Windows Explorer and type in both Anaconda Powershell cd followed by the pasted address (enter to execute). Example:
```bash
  cd C:\Users\myUserName\Documents\ReLIghting-spaces
````
Open PPO model 2.0.gh in Grasshopper and reset the Hoopsanke component. Then run load_model.py
```bash
  python load_model.py
````
Go back to GH and loop the Hoopsnake component.
After this the agent will start to build-up an assembly
