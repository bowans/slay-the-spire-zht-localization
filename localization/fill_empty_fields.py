import json
import sys
import os
import io
import pytest
from functools import partial, reduce
from itertools import chain
from validate_localization import read_json, flatten, get_json_files


if sys.version_info.major < (3):
    raise Exception("must use python 3")
else:
    from json.decoder import JSONDecodeError


def fill_with_a(a, b):
    """ Resolves discrepencies between 'a' and 'b' with contents from 'a'. """
    assert type(a) == type(b), "type: a='{}', type='{}' vs b='{}', type='{}'".format(a, type(a), b, type(b))
    if isinstance(a, dict):
        missing_keys = a.keys() - b.keys()
        for key in missing_keys:
            b[key] = a.get(key)
        extra_keys = b.keys() - a.keys()
        if len(extra_keys) > 0:
            raise Exception("Uhoh, I don't know what to do with these extra "
                            "keys: '{}'. Someone might have screwed up?"
                            .format(extra_keys))
        assert len(a.keys()) == len(b.keys())
        return flatten([fill_with_a(x[0][1], x[1][1]) for x in zip(sorted(a.items()), sorted(b.items()))])
    elif isinstance(a, list):
        b.extend(a[len(b):])
        return flatten(map(lambda x:fill_with_a(*x), zip(a, b)))
    else:
        return []


def resolve_discrep(eng_files, other_files):
    eng_files   = sorted(list(eng_files))
    other_files = sorted(list(other_files))
    eng_filenames   = list(map(os.path.basename, eng_files))
    other_filenames = list(map(os.path.basename, other_files))
    assert eng_filenames == other_filenames, "{} --- {}".format(eng_filenames, other_filenames)
    eng_jsons   = list(map(read_json, eng_files))
    other_jsons = list(map(read_json, other_files))
    list(map(lambda x: fill_with_a(*x), zip(eng_jsons, other_jsons)))
    list(map(lambda x: write_json(*x),  zip(other_files, other_jsons)))


def write_json(filename, data):
    with io.open(filename, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    localization_dir = os.path.abspath(os.path.dirname(__file__))
    eng_pack = os.path.join(localization_dir, "eng")
    abs_paths = map(lambda x: os.path.join(localization_dir, x), os.listdir(localization_dir))
    def is_dir_and_not_excluded(x):
        return os.path.isdir(x) and not (x.endswith('eng') or x.endswith('www'))
    lang_packs = filter(is_dir_and_not_excluded, abs_paths)
    eng_json = get_json_files(eng_pack)
    other_jsons = filter(lambda x:x != [], [get_json_files(x) for x in lang_packs])
    resolve_w_eng = partial(resolve_discrep, eng_json)
    errors = list(map(resolve_w_eng, other_jsons))


@pytest.mark.parametrize("a,b,expect", [
                                        ({'c':3, 'z':0}, {'a':1, 'z':0}, {'a':1, 'c':3, 'z':0}),
                                        ([],['a','b','c'],['a','b','c']),
                                        ([1,2],[1,2,3],[1,2,3]),
                                        ([1,2,3],[1,2,3],[1,2,3]),
                                        ([1,2,3,4],[1,2,3],[1,2,3,4]),
                                        ([1,2,3,4,5],[1,2,3],[1,2,3,4,5]),
                                        ])
def test_compare(a, b, expect):
    fill_with_a(a, b)
    assert b == expect
