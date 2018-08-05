import os
import zipfile
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json
import glob

# https://docs.zhconvert.org/api/convert/
ZHT_CONVERT_URL = 'https://api.zhconvert.org/convert'


class NotExistException(Exception):
    pass


def update_localization(path, target_dir=None):
    """
    Copy localization from desktop-1.0.jar from SlayTheSpire folder.

    :param path: The path of SlayTheSpire folder
    :param target_dir: Target folder to put copied localization
    :raises NotExistException: raises if desktop-1.0.jar does not exist
    """
    jar_path = os.path.join(path, 'desktop-1.0.jar')

    if not os.path.exists(jar_path):
        raise NotExistException('{} does not exist.'.format(jar_path))

    with zipfile.ZipFile(jar_path, 'r') as z:
        target_names = (
            'localization/eng/',
            'localization/zhs/',
            'localization/zht/',
            'localization/REFERENCES.txt',
            'localization/TRANSLATOR_README.txt',
            'localization/UPDATES.txt',
            'localization/validate_localization.py',
        )
        for name in z.namelist():
            if name.startswith(target_names):
                if target_dir is None:
                    z.extract(name)
                else:
                    z.extract(name, target_dir)


def zht_convert(text):
    """
    Convert zhs text to zht text via https://docs.zhconvert.org/api/convert/

    :param text: text for converting
    :return: converted text or None if error
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    post_fields = {'text': text, 'converter': 'Taiwan'}
    request = Request(
        ZHT_CONVERT_URL, urlencode(post_fields).encode(), headers=headers)
    try:
        response = urlopen(request).read()
    except HTTPError as e:
        print('Post API fail, {}'.format(e))
        return None
    else:
        resp_dict = json.loads(response.decode())
        return resp_dict.get('data', {}).get('text')


def update_zhs2zht(target_dir):
    """
    Convert localization/zhs into zhs2zht.

    :param target_dir: Target folder which contains localization
    """
    for zhs_file in glob.iglob(os.path.join(target_dir, 'localization/zhs/*')):
        file_name = os.path.basename(zhs_file)
        zhs2zht_file = os.path.join(target_dir, 'zhs2zht', file_name)
        print('Converting localization/zhs/{}'.format(file_name))
        with open(zhs_file, 'r', encoding='utf8') as f_source:
            converted_data = zht_convert(f_source.read())
            if converted_data is None:
                print('Fail.')
            else:
                with open(zhs2zht_file, 'w', encoding='utf8') as f_dest:
                    print('Writing zhs2zht/{}'.format(file_name))
                    f_dest.write(converted_data)
                    print('Done.')


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument(
        'path', help='Folder path of SlayTheSpire', nargs='?', default=None)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-a',
        '--all',
        help=
        'update localization and convert zhs into zhs2zht (Require path of SlayTheSpire)',
        action='store_true')
    group.add_argument(
        '-l',
        '--localization-only',
        help='update localization only (Require path of SlayTheSpire)',
        action='store_true')
    group.add_argument(
        '-c',
        '--convert-only',
        help='convert zhs into zhs2zht only',
        action='store_true')
    args = parser.parse_args()

    do_localization = args.all or args.localization_only
    do_convert = args.all or args.convert_only
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if do_localization:
        if args.path is None:
            parser.error('updating localization requires path')
        else:
            game_path = args.path
            try:
                update_localization(game_path, target_dir=base_dir)
            except NotExistException as e:
                print('Fail to update localization,', e)
                exit(1)

    if do_convert:
        update_zhs2zht(base_dir)
