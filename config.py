import yaml, os, sys
from shutil import copyfile

# ensure .agile-tracker folder exists and create if not
home = os.path.expanduser("~")
localfolder = os.path.join(home, '.bikescraper-cl')
if not os.path.exists(localfolder):
    print("Creating directory %s." % localfolder)
    os.makedirs(localfolder)

def get(configpath):
    if configpath is None:
        configpath = os.path.join(localfolder, 'config.yaml')
        if not os.path.exists(configpath):
            print("Copying in default config.")
            dir = os.path.dirname(os.path.abspath(__file__))
            file = 'config.yaml'
            defaultconfig = os.path.join(dir, file)
            copyfile(defaultconfig, configpath)
    try:
        with open(configpath, 'r') as f:
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError as err:
                print("Problem parsing config YAML file:")
                print(err)
    except FileNotFoundError:
        print("File %s not found." % configpath)
        sys.exit(1)