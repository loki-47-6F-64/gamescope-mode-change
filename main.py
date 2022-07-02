import os

import pathlib
import logging
import sys

import json

# Get the home directory based on the current working directory
def homedir() -> pathlib.Path:
    cwd = pathlib.Path(os.getcwd()).parts
    if(len(cwd) >= 3):
        return pathlib.Path(f"{cwd[0]}{'/'.join(cwd[1:3])}")
    else:
        return pathlib.Path.home()

VERSION = "0.1.0"
HOME_DIR = str(homedir())
PLUGIN_DIR = pathlib.Path(os.getcwd()).parent.resolve() / "plugins"
DEFAULT_SETTINGS_LOCATION = f"{HOME_DIR}/.config/GamescopeModeChange/settings.json"
LOG_LOCATION = "/tmp/GamescopeModeChange.log"

logging.basicConfig(
    filename = LOG_LOCATION,
    format = '%(asctime)s %(levelname)s %(message)s',
    filemode = 'w',
    force = True)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.info(f"PluginLoader GamescopeModeChange v{VERSION} https://github.com/Loki-47-6F-64/gamescope-mode-change")
logging.debug(f"Current Working Directory: {os.getcwd()}")
logging.debug(f"Plugin Dir: {PLUGIN_DIR}")
logging.debug(f"Home Directory:{HOME_DIR}")

sys.path.append(str(PLUGIN_DIR / "gamescope-mode-change"))
logging.info(sys.path)

sys.path = sys.path[:-1]

class Plugin:
    SETTINGS_PATH = pathlib.Path(DEFAULT_SETTINGS_LOCATION)

    async def get_version(self) -> str:
        return VERSION

    async def mode_change_script_path(self) -> str:
        logging.debug("mode_change_script_path")
        return str(PLUGIN_DIR / "gamescope-mode-change/gamescope-mode-change.py")

    async def read_settings(self) -> str:
        logging.debug("read-settings")
        # If the config file doesn't exist yet, send an empty list back
        if(not Plugin.SETTINGS_PATH.exists()):
            return "[]"

        with open(DEFAULT_SETTINGS_LOCATION, mode="r") as f:
            return f.read()

    async def write_settings(self, contents : str):
        logging.debug(contents)
        if(not Plugin.SETTINGS_PATH.exists()):
            Plugin.SETTINGS_PATH.parent.resolve().mkdir(parents=True, exist_ok=True)

        t = json.loads(contents)

        with open(DEFAULT_SETTINGS_LOCATION, "w") as f:
            f.write(json.dumps(t, indent=4))