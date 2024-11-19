import os
from loguru import logger
import subprocess


def get_git_branches() -> list:
    '''
    Get all the branches in the git repository.

    :return: A list of branches in the git repository.
    :rtype: list
    '''
    result = subprocess.run(['git', 'branch', '-a'], stdout=subprocess.PIPE, text=True)
    branches = result.stdout.strip().split('\n')
    cleaned_branches = [branch.strip().replace('* ', '') for branch in branches]
    cleaned_branches = [branch.replace("remotes/origin/", "") for branch in cleaned_branches]
    return list(set(cleaned_branches))


def is_version_number_valid(version_number: str) -> bool:
    '''
    Check if the version number is valid.

    :param version_number: The version number to check.
    :type version_number: str

    :return: True if the version number is valid, False otherwise.
    :rtype: bool
    '''
    numbers = version_number.split('.')
    if len(numbers) != 3:
        return False
    for n in numbers:
        if not n.isdigit():
            return False
    return True


def main() -> None:
    '''
    Auto update the software to the release version input by the user.
    
    If the user input a version number that is not in the release list,
    the software will not be updated.
    '''
    logger.info('>>> Checking latest version...')
    os.system('git fetch --all')
    all_brances = get_git_branches()
    release_branches = [branch for branch in all_brances if branch.startswith('release-')]

    logger.info('>>> Please input the target release version:')
    target_release_version = input('>>> ')

    while(not is_version_number_valid(target_release_version)):
        logger.error('Invalid version number, please input again.')
        target_release_version = input('>>> ')

    if f'release-v{target_release_version}' not in release_branches:
        logger.error(f'The release version {target_release_version} is not in the release list.')
        logger.info(f'The software will not be updated.')
        logger.info(f'Please contact the developer for more information.')
        return
        
    logger.info(f'>>> Checkout to release-v{target_release_version}...')
    os.system(f'git checkout release-v{target_release_version}')
    logger.info(f'>>> Pulling latest changes...')
    os.system('git pull')
    os.system('pip install -e .')
    logger.info(f'>>> The software has been updated to release-v{target_release_version}.')
    