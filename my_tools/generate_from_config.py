import os
import argparse
import subprocess

def get_config_name(config_path):
    autoscene_files = []
    config2d_files = []
    for name in os.listdir(config_path):
        file_type = name.split("_")[-1].split(".")[0]
        if(file_type == "autoscene"):   
            # autoscene_files.append(config_path + "/" + name)
            autoscene_files.append(name)
        elif(file_type == "config2d"):
            # config2d_files.append(config_path + "/" + name)
            config2d_files.append(name)
    autoscene_files.sort()
    config2d_files.sort()
    return autoscene_files, config2d_files



def bash_process(config_path, autocene_files, config2d_files):
    for i in range(len(autocene_files)):
        f1 = autocene_files[i]
        f2 = config2d_files[i]
        print(f1)
        subprocess.call(['123       '])
        # os.system('esim_generate')
        # os.system('rm /tmp/f1 /tmp/f2')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='change picture names')
    parser.add_argument('--config_path', type=str, help='Path to config files',
                                        default="/home/larrydong/dataset/esim_generator/configs")
    args = parser.parse_args()
    
    autocene_files, config2d_files = get_config_name(args.config_path)

    bash_process(args.config_path, autocene_files, config2d_files)


