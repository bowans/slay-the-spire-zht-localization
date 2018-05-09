import json
import sys
import os
from functools import partial, reduce
from itertools import chain

# a list of files to be ignored.
ignored_files = []

if sys.version_info.major < (3):
    raise Exception("must use python 3")
else:
    from json.decoder import JSONDecodeError

class LintError(Exception):
    def __str__(self):  # Override to include exception name in exception string
        return "{}: {}".format(self.__class__.__name__, self.args[0])

class TypeMismatch(LintError):
    pass

class UnsharedDictKeys(LintError):
    pass

class ArraySizeMismatch(LintError):
    pass

class DuplicateKeyError(LintError):
    pass


def jsonify(j):
    return json.dumps(j, ensure_ascii=True)


def truncate_list(l):
    assert isinstance(l, list)
    return l if l == [] else "{}".format(l[0][:20])  # truncate


def compare(a, b, path):
    cmp = partial(compare, path=path)
    if type(a) != type(b):
        return [(path, TypeMismatch("'{}' and '{}'".format(a, b)))]
    elif isinstance(a, dict):
        a_keys = set(a.keys())
        b_keys = set(b.keys())
        set_diff = a_keys.symmetric_difference(b_keys)
        if set_diff != set():
            return [(path, UnsharedDictKeys("'{}'".format(set_diff)))]
        else:
            return flatten([cmp(x[0][1], x[1][1]) for x in zip(sorted(a.items()), sorted(b.items()))])
    elif isinstance(a, list):
        if len(a) != len(b):
            lang_pack = os.path.basename(os.path.dirname(path))
            return [(path, ArraySizeMismatch("(eng={} vs {}={}): search by '{}' or '{}' for eng or {} respectively".format(len(a), lang_pack, len(b), truncate_list(a), truncate_list(b), lang_pack)))]
        else:
            return flatten(map(lambda x:cmp(*x), zip(b, a)))
    else:
        return []


def get_json_files(lang_dir):
    return [os.path.join(lang_dir, f) for f in os.listdir(lang_dir) if f.endswith('.json')]


def compare_lang_pack(eng_files, other_files):
    eng_filenames = sorted(map(os.path.basename, eng_files))
    other_filenames = sorted(map(os.path.basename, other_files))
    assert eng_filenames == other_filenames, "{} --- {}".format(eng_filenames, other_filenames)
    eng_jsons = map(read_json, sorted(eng_files))
    other_jsons = map(read_json, sorted(other_files))
    cmp_funcs = map(lambda p:partial(compare, path=p), sorted(other_files))
    return reduce(chain, map(lambda c,x:c(*x), cmp_funcs, zip(eng_jsons, other_jsons)))


def dict_raise_on_duplicates(ordered_pairs):
    """Reject duplicate keys."""
    d = {}
    for k, v in ordered_pairs:
        if k in d:
           raise DuplicateKeyError("%r" % (k,))
        else:
           d[k] = v
    return d


def read_json(json_file):
    with open(json_file, encoding=('UTF-8-sig')) as f:
        try:
            return json.load(f, object_pairs_hook=dict_raise_on_duplicates)
        except JSONDecodeError as e:
            print("WARNING! Invalid Json detected. Problem in file: `{}` at line `{}`, column `{}`"
                  .format(json_file, e.lineno, e.colno))
            print(e)
            sys.exit(1)
        except DuplicateKeyError as e:
            print("In file: " + json_file)
            print(e)
            sys.exit(1)


def flatten(list_of_lists):
    return [y for x in list_of_lists for y in x]


if __name__ == "__main__":
    localization_dir = os.path.abspath(os.path.dirname(__file__))
    eng_pack = os.path.join(localization_dir, "eng")
    abs_paths = map(lambda x: os.path.join(localization_dir, x), os.listdir(localization_dir))
    def is_dir_and_not_excluded(x):
        return os.path.isdir(x) and len(os.path.basename(x)) == 3 and not (x.endswith('eng') or x.endswith('www'))
    lang_packs = filter(is_dir_and_not_excluded, abs_paths)
    eng_json = get_json_files(eng_pack)
    other_jsons = [get_json_files(x) for x in lang_packs]
    compare_against_eng = partial(compare_lang_pack, eng_json)
    errors = flatten(map(compare_against_eng, other_jsons))

    # Filter out errors in file ignore list. The more complicated rules are hardcoded to save time.
    errors = [e for e in errors if not (os.path.basename(e[0]) in ignored_files)]
    errors = [e for e in errors if not (os.path.basename(e[0]) in "keywords.json" and isinstance(e[1], ArraySizeMismatch))]
    errors = [e for e in errors if not (os.path.basename(e[0]) in "credits.json" and isinstance(e[1], ArraySizeMismatch))]
    errors = [e for e in errors if not (os.path.basename(e[0]) == "cards.json" and isinstance(e[1], UnsharedDictKeys) and 'UPGRADE_DESCRIPTION' in str(e[1]))]

    if len(errors) == 0:
        print("SUCCESS. No errors found.")
        sys.exit(0)
    else:
        error_count = len(errors)
        error_limit = 5
        if error_count > error_limit:
            trunc_msg = "(showing the first `{}`)".format(error_limit)
        else:
            trunc_msg = ""
        plurality = 's' if error_count > 1 else ''
        print("WARNING! `{}` error{} detected in localization json files {}:".format(error_count, plurality, trunc_msg))
        def error_format(errors, limit):
            return list(map(lambda e:"In file: {}\n{}".format(e[0],e[1]), errors[:limit]))
        msg = "```{}```".format("\n\n".join(error_format(errors, limit=error_limit)))
        print(msg)
        with open('validation_results.txt', 'w') as f:
            f.write("\n\n".join(error_format(errors, limit=sys.maxsize)))
        sys.exit(1)
