echo 'setting up conda'
# setup conda
if [ $# -eq 0 ]
  then
    source ~/anaconda3/etc/profile.d/conda.sh
else
  source $1
fi

conda create --prefix ./envs python=3.6
echo 'installing bob.bio.spear'
conda activate ./envs
conda install \
-c https://www.idiap.ch/software/bob/conda \
-c defaults \
-c https://www.idiap.ch/software/bob/conda/label/archive \
bob=4.0.0 bob.bio.spear

pip install pydub
conda install ffmpeg
pip install ffprobe
pip install ffmpeg


#conda env create --prefix ./envs --file environment_droplet.yml
