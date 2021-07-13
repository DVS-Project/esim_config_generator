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




# def modify_config(config_path, picture_path, picture_names):
#     file_names = []
#     for name in os.listdir(config_path):
#         id, n = name.split("_")
#         if(n == "autoscene.txt"):
#             L = []
#             with open(config_path + "/" + name, "r") as f:
#                 for line in f:
#                     L.append(line)      # save all lines
#                 line_number = len(L)
#                 for i in range(1, len(L)):
#                     first_part = L[i].split(" ")[0]
#                     first_part_new = picture_path + "/" + random.choice(picture_names)
#                     print("old: ", first_part, "-> new: ", first_part_new)
#                 print(11111)


def modify_config(config_path, config_path_out, bg_pictures, fg_pictures):
    for name in os.listdir(config_path):
        if(name.split("_")[-1].split(".")[0] == "autoscene"):
            with open(config_path + "/" + name, "r") as f:
                L = []
                for line in f:
                    L.append(line)
                # modify the lines
    # TODO: modify the files...



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
