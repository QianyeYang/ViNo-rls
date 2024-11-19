import os, vino
from glob import glob
from vino.logic import utils
from collections import defaultdict
from loguru import logger
import argparse


def fix_resource_path(py_file: str) -> None:
    '''
    Replace import resource -> import plai.resources_rc

    :param py_file: str
    :type py_file: path to the python file

    :return: None
    '''
    assert os.path.isfile(py_file), f"{py_file} does not exist"

    with open(py_file, 'r') as f:
        lines = f.readlines()

    with open(py_file, 'w') as f:
        for line in lines:
            if 'import resource' in line:
                line = line.replace('import resources_rc', 'import vino.resources_rc')
            f.write(line)


def main() -> None:
    '''
    Compile the *.ui files.
    '''
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--force", action="store_true", help="Force update all UI files")
    args = argparser.parse_args()

    # Load existing hash file
    ui_record_filepath = vino.FILE_UI_HASH_RECORD
    logger.info("Load Hashing ")

    if args.force or not os.path.exists(ui_record_filepath):
        logger.info("Force update all UI files")
        previous_hash_dict = defaultdict(str)
    else:
        previous_hash_dict = utils.load_json(ui_record_filepath)


    # compute latest hashing
    UI_files = glob(os.path.join(vino.DIR_UI_FILES, '*.ui'))
    latest_hash_dict = {}

    logger.info(f"Found {len(UI_files)} UI files")
    logger.info(f"Compute hashing ......")

    for uif in UI_files:
        latest_hash_dict[os.path.basename(uif)] = utils.compute_file_hash(uif)

    logger.info(f"Hashing completed!")


    # compare and update
    for idx, uif in enumerate(UI_files):
        py_file = os.path.join(
            vino.DIR_GUI, 
            os.path.basename(uif.replace('.ui', '.py'))
        )
        
        ui_key = os.path.basename(uif)

        if ui_key not in previous_hash_dict:
            pass
        elif latest_hash_dict[ui_key] == previous_hash_dict[ui_key]:
            logger.info(f"[{idx+1}/{len(UI_files)}] {uif} is up-to-date")
            continue

        command = f"PySide6-uic {uif} -o {py_file}"
        os.system(command) 
        logger.info(f"[{idx+1}/{len(UI_files)}] converted {uif}")

        if os.path.isfile(py_file):
            fix_resource_path(py_file)


    utils.save_json(latest_hash_dict, ui_record_filepath)


    # update qrc files
    logger.info("compile resource files...")
    os.system(
        f"pyside6-rcc {vino.FILE_RESOURCE} -o {os.path.join(vino.DIR_PACKAGE, 'resources_rc.py')}"
    )
    logger.info("Done!")
    
    