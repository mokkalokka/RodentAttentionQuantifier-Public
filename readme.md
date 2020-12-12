# Rodent attention quantifier for analysis of rodent behaviour.

* Currently only tested with rats

## Depentencies:

See RAQ-CPU.yaml (for cpu) or RAQ-GPU.yaml (for gpu)

## Installation for CPU only:

* Install miniconda 64-bit version
* Change directory to project root
* conda env create -f RAQ-CPU.yaml

## Installation for GPU (requires CUDA compatible GPU):

* Install miniconda 64-bit version
* Change directory to project root
* conda env create -f RAQ-GPU.yaml

## Run program:

conda activate RAQ-CPU or RAQ-GPU

for windows:
ipython GUI.py

for mac:
pythonw GUI.py


## Pipeline:
* Select video(s) to process ->
* Select analysis options ->
* Start analysis ->
* crop (GUI) ->
* confine observer (GUI)
* frames with light will be extracted as well as normalized, grayscale filtered and compressed ->
* analysis of video with multi animal deeplabcut (beta) ->
* create tracklets (points) ->
* read trackelts ->
* fix identities ->
* calculate angle from chose point to chosen point ->
* plot angles and vectors used to calculate angles on top of video ->
* pipeline done!
