import os
import argparse
import random

def get_background_pictures(file_dir):
    file_names = []
    for name in os.listdir(file_dir):
        if name.split('.')[-1] == "jpg":        # background must be jpg;
            file_names.append(file_dir + "/" + name)
    print("Background No:", len(file_names), " from: ", file_dir)
    return file_names


def get_foreground_pictures(file_dir):
    file_names = []
    for name in os.listdir(file_dir):
        if name.split('.')[-1] == "png":
            file_names.append(file_dir + "/" + name)
    print("Foreground No:", len(file_names), " from: ", file_dir)
    return file_names



# 1. save all lines in on file
# 2. modify the 1 line by bg_picture.jpg
# 3. modify the 2 - end lines by fg_picture.png
# 4. save to a new file

def modify_config(config_path, config_path_out, bg_pictures, fg_pictures):
    print("Modifying names......")
    for name in os.listdir(config_path):
        # only deal with *autoscene.txt, config2d.txt no change. Put all in /tmp/ is okay
        if(name.split("_")[-1].split(".")[0] == "autoscene"):   
            print(name)
            new_lines = []
            with open(config_path + "/" + name, "r") as f:
                old_lines = []
                for line in f:
                    old_lines.append(line)
                new_lines.append(old_lines[0])          # line 0
                l1 = old_lines[1].split(" ")
                l1[0] = random.choice(bg_pictures)      # line 1
                l1 = " ".join(l1)
                new_lines.append(l1)
                for i in range(2, len(old_lines)):
                    l = old_lines[i].split(" ")
                    l[0] = random.choice(fg_pictures)
                    new_lines.append(" ".join(l))
            with open(config_path_out + "/" + name, "w") as f:
                for l in new_lines:
                    f.writelines(l)
    



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='change picture names')
    parser.add_argument('--background_path', type=str, help='Path to background pictures',
                                        default="/home/larrydong/dataset/esim_generator/coco")
    parser.add_argument('--foreground_path', type=str, help='Path to forground pictures',
                                        default="/home/larrydong/dataset/esim_generator/foreground_objects")
    parser.add_argument('--config_path', type=str, help='Path to config files',
                                        default="/home/larrydong/dataset/esim_generator/configs")
    parser.add_argument('--config_path_out', type=str, help='Path to save config files',
                                        default="/home/larrydong/dataset/esim_generator/configs/new")

    args = parser.parse_args()

    bg_pictures = get_background_pictures(args.background_path)
    fg_pictures = get_foreground_pictures(args.foreground_path)

    modify_config(
        config_path = args.config_path,
        config_path_out = args.config_path_out,
        fg_pictures = fg_pictures,
        bg_pictures = bg_pictures
    )
