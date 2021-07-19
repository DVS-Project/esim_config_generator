#!/bin/bash

# move one config file to /tmp and run code.
# avoid roslaunch.shutdown error of original code.

conda activate py27
source ~/sim_ws/devel/setup.bash

config_dir=/home/larrydong/dataset/esim_generator/configs
autoscene_files=(`ls $config_dir | grep "autoscene" | sort -d`)   # make an array
config2d_files=(`ls $config_dir | grep "config2d" | sort -d`)

bag_save_dir=/home/larrydong/dataset/esim_generator/rosbag


idx=0
while [ $idx -le 280 ]
do
    autoscene=${autoscene_files[$idx]}
    config2d=${config2d_files[$idx]}
    echo "idx: $idx, f1: $autoscene, f2: $config2d"

    # cp to /tmp and run
    `cp $config_dir/$autoscene $config_dir/$config2d /tmp`
    # echo "list /tmp: `ls /tmp | grep .txt`"


    # run generate codes...
    python ../scripts/generate_preset.py /tmp
    echo "Generate done. No. $idx"
    `rm /tmp/$autoscene /tmp/$config2d`
    
    idx=$[$idx + 1]
done

`mv /tmp/*.bag $bag_save_dir`
echo "Move all bags to file: $bag_save_dir"