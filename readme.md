# Rodent attention quantifier for analysis of rodent behaviour. 
* Early beta testing (not stable!)
* Currently only tested with rats

## Depentencies:
See attention_quantifier.yaml


## Installation:
* Install miniconda 64-bit version
* Change directory to project root
* conda env create --file attention_quantifier.yaml

## Run program:
conda activate attention_quantifier

for windows:
ipython GUI.py

for mac:
pythonw GUI.py

## Important:
Current beta version only supports CPU processing (slow).   
keep data inside the data folder!

## Pipeline:
* Select video to process ->
* crop (GUI) ->
* confine observer (GUI)
* frames with light will be extracted as well as normalized, grayscale filtered and compressed ->
* analysis of video with multi animal deeplabcut (beta) ->
* create tracklets (points) ->
* read trackelts -> 
* fix identities -> 
* calculate angle from "observer" to "performer" ->
* plot angles and vectors used to calculate angles on top of video ->
* pipeline done!
