#!/bin/sh

source ~/574/anaconda3/etc/profile.d/conda/sh

conda activate ../envs

verify.py experiment.py

conda deactivate
