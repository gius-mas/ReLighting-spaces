# ReLighting spaces - Training daylight access cognition in combinatorial spatial assemblages using Reinforcement Learning  
This repository contains RL models an GH-definitions from the paper "ReLighting spaces - Training daylight access cognition in combinatorial spatial assemblages using Reinforcement Learning" by Giuseppe Massafra, Alessio Erioli presented on the FMA 2024 Conference. This repository contains both source code for Python and GH-definition tu use RL-trained agents involved in combinatorial process to build spatial assemblies with adaptive control over daylight condition.

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
