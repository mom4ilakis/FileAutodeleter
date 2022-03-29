from os import path, listdir, remove, environ
from datetime import datetime, timedelta

import click

DEFAULT_OFFSET = {'weeks': 1}
DEFAULT_DIR = environ.get('AUTODELETER_DEF_DIR', 'H:\\Photos\\Import\\Sigma\\Converted\\')


def get_files_older_than(dir_path, offset=None, date=None):
    print(f'Reading files from: {dir_path}')
    timestamp = date or datetime.today() - timedelta(**offset or DEFAULT_OFFSET)
    files = [(dir_path + filename, path.getmtime(dir_path + filename)) for filename in listdir(dir_path)]
    older_files = [file[0] for file in files if datetime.fromtimestamp(file[1]) < timestamp]

    return older_files


def delete_old_files(dir_path, offset=None, date=None):
    dir_path = dir_path or DEFAULT_DIR

    if not dir_path.endswith('\\'):
        dir_path += '\\'

    print(f'Checking for old files in {dir_path}')

    files_to_delete = get_files_older_than(dir_path, offset, date)

    if files_to_delete:
        print(f'Found {len(files_to_delete)} files to delete!')

        for file in files_to_delete:
            print(f'Deleting {file}')
            remove(file)

        print('Delete is DONE')
    else:
        print('No files for deleting :(')


@click.command()
@click.option('--dir', prompt='Directory to scan', help='Directory to scan')
@click.option('--offset', default=None, help='Type of offset: 1-weeks, 4-days etc')
@click.option('--date', default=None, help='Date that is used to determine which files are old in isoformat')
def delete_old_files_command(dir, offset, date):
    if offset:
        amount, type = offset.split('-')
        delete_old_files(dir, {type: amount})
    elif date:
        date = datetime.fromisoformat(date)
        delete_old_files(dir, date=date)
    else:
        delete_old_files(dir)


if __name__ == '__main__':
    delete_old_files_command()
