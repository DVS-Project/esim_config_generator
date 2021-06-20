中文版注释

## 基本介绍

此代码通过ESIM生成飞椅数据集形式的数据序列。生成的数据用来训练 Reducing the Sim-to-Real Gap for Event Cameras 一文中的方法。


# Comments from larrydong:

1. 运行环境是python2.7（否则会在运行时有error），conda虚拟环境需要的依赖项有：
conda install matplotlib defusedxml opencv
conda install -c conda-forge netifaces
pip install rospkg

2. 数据准备：需要准备ESIM的背景数据（例如COCO），以及前景数据（COCO或作者使用的图片）。背景数据至少有1张jpg，前景数据可以配置有多个路径，均至少有max_num张png图片；作者提供了jpg转png代码。详见“从已有配置文件生成数据集”相应链接。

3. 运行步骤：第一步根据json配置文件生成ESIM的配置文件，第二步按照ESIM的配置文件生成ros的bag数据。也可以用提供的脚本批量生成。

4. 如果bag数据用于后续其他操作，例如e2vid，需要转成HDF5格式。转换方法参考：[github.com/TimoStoff/events_contrast_maximization](github.com/TimoStoff/events_contrast_maximization)

5. And, 请将/tmp中生成的文件及时保存出来，否则电脑reboot之后就！没！了！

6. 完整代码过程
``` bash 
python scripts/generate_esim2d_scenes.py generator_config/slow_motions.json --scene_id=0 --contrast_threshold_mean=0.1 --contrast_threshold_sigma=0.1

source ~/esim_ws/devel/setup.bash (ss_esim)

conda activate py27

roscore

python scripts/2d_launch_esim.py --launch_file_path="/tmp/esim.launch"
```

## 运行条件

必须首先安装了ESIM。请看[这里](https://github.com/uzh-rpg/rpg_esim/wiki/Installation)。并且运行前激活了esim的环境。

之后修改配置文件：在`generator_config`文件夹中 修改对应的json文件。

`foreground_images`路径包含的文件将在ESIM仿真器中高速“飞行”以产生数据。这些图片 _必须_ 是4通道的png图像（注释：即rgba），否则ESIM会报错。作者使用`tools/jpg_to_png`代码将jpgs图片格式转成pngs。

`background_images` _必须_ 为jpg图片，否则ESIM会报错（作者在这里吐槽了一下ESIM）。

当然，需要保证在`foreground_images`中的每个路径下至少包括`max_num`个图片（注释：foreground_images包含多个路径，每个路径都必须有max_num个图，代码随机选择[`min_num`, `max_num`]一个数字作为前景图片的数量），`background_images`下至少有1张图片（注释：代码从背景图片路径中随机选择1张）。


## 使用方法

主要工作由 `scripts/generate_esim2d_scenes.py` 实现。运行时需要一个配置文件（generator_config中的某个），或使用命令行参数覆盖配置文件中的参数，生成：
  1. 一个场景文件（包括相机轨迹、图像、图像大小和序列时间）
  2. ESIM的配置文件（包括对比度阈值、偏置等）
  3. 一个ROS的launch文件

默认生成路径： `/tmp/000000000_autoscene.txt`, `/tmp/000000000_config2d.txt` 和 `/tmp/esim.launch` 

之后，可以运行 `/scripts/2d_launch_esim.py` 启动ROS，需要传入launch文件路径，例如：
```python scripts/2d_launch_esim.py --launch_file_path="/tmp/esim.launch"```

以上所有步骤可以通过运行 `2d_simulator_generator.sh` 实现。这个脚本包含了上面完整的过程。


## 从已有配置文件生成数据集

可以通过已有的配置文件和场景生成数据集。

例如生成"Reducing the Sim-to-Real Gap for Event Cameras"一文中的训练数据，你需要首先下载COCO数据集，并[从这里下载]](https://drive.google.com/drive/folders/1F6fNgZFmMvGkw6sAwDFE7j8Q7EH3TMve?usp=sharing) 用到的前景图片。

之后[从这里下载](https://drive.google.com/drive/folders/1ILoFnR5BHR17F0VGEzR0JIBfisw1nkc4?usp=sharing) 场景和配置文件。

默认情况下，场景和配置文件中的路径是作者自己的（xxx_autoscene.txt）。你需要修改所有文件中的相关路径。可以采用高[sed](https://stackoverflow.com/questions/11392478/how-to-replace-a-string-in-multiple-files-in-linux-command-line)

最后，直接运行 ```python scripts/generate_preset.py /path/to/config/files``` 即可。主义需要激活ROS环境。

（百度网盘搬运：链接: https://pan.baidu.com/s/1RRZ_her1lpR1TK4UvFFkXQ 提取码: ztti）



# ------   以下为原文   ------

## About
This code allows generating flying chairs style sequences for the Multi-Object-2D simulator from [ESIM](https://github.com/uzh-rpg/rpg_esim). This code was used to generate sequences for [How to Train Your Event Camera Neural Network](https://timostoff.github.io/20ecnn), please cite this work if you use this in an academic context.
```
@Article{Stoffregen20eccv,
  author        = {T. Stoffregen, C. Scheerlinck, D. Scaramuzza, T. Drummond, N. Barnes, L. Kleeman, R. Mahoney},
  title         = {Reducing the Sim-to-Real Gap for Event Cameras},
  journal       = eccv,
  year          = 2020,
  month         = aug
}
```

## Prerequisites
You must have esim for this to work, please follow the instructions [here](https://github.com/uzh-rpg/rpg_esim/wiki/Installation). You must have esim sourced (command `ssim`, if you followed the install instructions).

Next, take a look at the config files in `generator_config` and adapt the paths to suit your needs. The image paths in `foreground_images` are the objects that will be flying around wildly in the simulator. These images _must_ all be 4 channel png images, or you will get cryptic errors from ESIM. _Unfortunately_ imagemagick is a real pain about actually putting in the alpha channel when it feels it doesn't need to. I ended up using a Python script to convert jpgs to pngs, I know, it seems crazy but it's true. You can find it in `tools/jpg_to_png`. 

The image paths in `background_images` _must_ be jpg images, again for mysterious ESIM reasons. Obviously, you must have at least one path with at least `max_num` images in the foreground rubric and at least one path with at least one image for the background rubric.

## Usage
The main work is done in `scripts/generate_esim2d_scenes.py`. This file takes a configuration file (examples can be found in `generator_config`) and some command line arguments that augment/modify the config settings if desired and generates a scene file (this contains the trajectories, the corresponding images, the image size and the sequence duration), an esim config file (this contains contrast thresholds, biases etc) and a ROS launch file.
The default location where these files will be created is `/tmp/000000000_autoscene.txt`, `/tmp/000000000_config2d.txt` and `/tmp/esim.launch` respectively. As an example, you could execute:
```
python scripts/generate_esim2d_scenes.py generator_config/slow_motions.json --scene_id=0 --contrast_threshold_mean=0.3 --contrast_threshold_sigma=0.1
```
Note that the CLI arguments for the contrast thresholds are optional and in this case overrule the values in the config file.

Once this is done, you can use `/scripts/2d_launch_esim.py` to launch ROS itself. The required arguments are the location of the launch file, eg: 
```python scripts/2d_launch_esim.py --launch_file_path="/tmp/esim.launch"```

All of this is also in a bash script, so you could also just run `2d_simulator_generator.sh`.


## Generating datasets from existing configs
You can also generate datasets from existing scene and config files.
For example, to generate the dataset from "Reducing the Sim-to-Real Gap for Event Cameras", you can first download COCO dataset as well as a few custom foreground images you can get from [here](https://drive.google.com/drive/folders/1F6fNgZFmMvGkw6sAwDFE7j8Q7EH3TMve?usp=sharing)
Then, you need to download the config and scene files for the dataset from [here](https://drive.google.com/drive/folders/1ILoFnR5BHR17F0VGEzR0JIBfisw1nkc4?usp=sharing)
By default, these go into /tmp (see inside the autoscene files to see the paths), but you can easily change this using [sed](https://stackoverflow.com/questions/11392478/how-to-replace-a-string-in-multiple-files-in-linux-command-line).
Then, just run `scripts/generate_preset.py` eg:
```python scripts/generate_preset.py /path/to/config/files```
Note that you will need ROS installed and sourced.
