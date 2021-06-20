#!/bin/bash

# config_name=(
#    "slow_motions",
#    "fast_motions",
#    "medium_motions",
#    "variety_motions",
# )

number=20
ct_number=10
for n in $(eval echo {0..$number}); do
   for i in $(eval echo {0..$ct_number}); do
      id=`expr $n \* 100 + $i`
      # # echo "========================================================\n"
      # # echo "This is the $i th image\n"
      # # echo "========================================================\n"
      source ~/sim_ws/devel/setup.bash
      ct_mean=$(bc <<< "(0.1*$i)+0.1")
      python scripts/generate_esim2d_scenes.py generator_config/slow_motions.json --scene_id=$id --contrast_threshold_mean=$ct_mean --contrast_threshold_sigma=0.1
      python scripts/2d_launch_esim.py --launch_file_path="/tmp/esim.launch"
   done
done


# for i in {0..10}
# do
#    for j in {0..}
#    echo "========================================================\n"
#    echo "This is the $i th image\n"
#    echo "========================================================\n"
#    source ~/sim_ws/devel/setup.bash
#    ct_mean=$(bc <<< "(0.1*$i)+0.1")
#    python scripts/generate_esim2d_scenes.py generator_config/slow_motions.json --scene_id=$i --contrast_threshold_mean=$ct_mean --contrast_threshold_sigma=0.1
#    python scripts/2d_launch_esim.py --launch_file_path="/tmp/esim.launch"
# done

