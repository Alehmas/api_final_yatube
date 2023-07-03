import sys
import os


root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir_content = os.listdir(BASE_DIR)
PROJECT_DIR_NAME = 'yatube_api'
# check that the folder with the project is in the root of the repository
if (
        PROJECT_DIR_NAME not in root_dir_content
        or not os.path.isdir(os.path.join(BASE_DIR, PROJECT_DIR_NAME))
):
    assert False, (
        f'The folder with the project `{PROJECT_DIR_NAME}` was not found in the directory `{BASE_DIR}`. '
        f'Make sure you have the correct project structure.'
    )

MANAGE_PATH = os.path.join(BASE_DIR, PROJECT_DIR_NAME)
project_dir_content = os.listdir(MANAGE_PATH)
FILENAME = 'manage.py'
# make sure the project structure is correct and manage.py is in place
if FILENAME not in project_dir_content:
    assert False, (
        f'File `{FILENAME}` was not found in directory `{MANAGE_PATH}`. '
        f'Make sure you have the correct project structure.'
    )

pytest_plugins = [
    'tests.fixtures.fixture_user',
    'tests.fixtures.fixture_data',
]

# test .md
default_md = '# api_final\napi final\n'
filename = 'README.md'
assert filename in root_dir_content, (
    f'File `{filename}` not found in project root'
)

with open(filename, 'r') as f:
    file = f.read()
    assert file != default_md, (
        f'Don`t forget to style `{filename}`'
    )
