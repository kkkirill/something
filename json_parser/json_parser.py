import pcre
from pathlib import Path
from requests import get
from ast import literal_eval as leval
from sys import argv

DOCSTRING = '''
Script expects minimum 2 arguments (if you don't want get help).
Possible flags:
    -h|--help - for showing instructions
    -s|--str - to get json as string from arguments
    -f|--file - to read json string from file
    -e|--encoding - to read from file in correct encoding (default: utf-8)
    -u|--url - to get json from url

Usage examples:
    python json_parser.py -h
    python json_parser.py -s 'json_string'
    python json_parser.py -f path_to_file [-e ASCII]
    python json_parser.py -u url_to_json
'''

FLAGS = {"h": ('--help', '-h'), "s": ('--str', '-s'), "f": ('--file', '-f'), "e": ('--encoding', '-e'),
         "u": ('--url', '-u')}


class JsonParser:
    __pattern = pcre.compile(r'(?(DEFINE)'
                             r'(?<json>(?>\s*(?&object)\s*|\s*(?&array)\s*))'
                             r'(?<object>(?>\{\s*(?>(?&pair)(?>\s*,\s*(?&pair))*)?\s*\}))'
                             r'(?<pair>(?>(?&STRING)\s*:\s*(?&value)))'
                             r'(?<array>(?>\[\s*(?>(?&value)(?>\s*,\s*(?&value))*)?\s*\]))'
                             r'(?<value>(?>true|false|null|(?&STRING)|(?&NUMBER)|(?&object)|(?&array)))'
                             r'(?<STRING>(?>"(?>\\(?>["\\\/bfnrt]|u[a-fA-F0-9]{4})|[^"\\\0-\x1F\x7F]+)*"))'
                             r'(?<NUMBER>(?>-?(?>0|[1-9][0-9]*)(?>\.[0-9]+)?(?>[eE][+-]?[0-9]+)?))'
                             r')'
                             r'\A(?&json)\z')

    @classmethod
    def loads(cls, input_str: str):
        null = None
        pcre.enable_re_template_mode()
        json = pcre.match(cls.__pattern, input_str)
        if input_str.isdigit() or (input_str.startswith('-') and input_str[1:].isdigit()):
            return input_str
        if json is None:
            if input_str.startswith('"') and input_str.endswith('"'):
                return leval(input_str)
            raise SyntaxError('Invalid json format')
        else:
            json = json.group(0)
            res: dict = eval(json, {}, {'null': null})
        return res

    @staticmethod
    def dumps(iter_obj) -> str:
        class null:
            def __repr__(self):
                return self.__class__.__name__

        class mstr(str):
            def __repr__(self):
                return ''.join(('"', super().__repr__()[1:-1], '"'))

        my_null = null()

        def serialize(iter_obj):
            if iter_obj is None:
                return my_null
            elif isinstance(iter_obj, str):
                return mstr(iter_obj)
            elif isinstance(iter_obj, bool):
                return mstr(iter_obj).lower()
            elif isinstance(iter_obj, (int, float)):
                return iter_obj
            elif isinstance(iter_obj, (tuple, set, list)):
                return [serialize(el) for el in iter_obj]
            elif isinstance(iter_obj, dict):
                return {mstr(k): serialize(v) for k, v in iter_obj.items()}
            else:
                raise SyntaxError(f'Object is not JSON serializable. Incorrect object type: {type(iter_obj)}')

        return mstr(serialize(iter_obj))


def empty_args(func):
    def wrapper(*args):
        if not args:
            return
        return func(*args)
    return wrapper


@empty_args
def get_json_from_file(values):
    if Path(values[0]).is_file() and values[0] != __file__:
        with open(values[0], 'r', encoding=values[1] if len(values) > 1 else 'utf-8') as f:
            return ''.join(f.readlines()).strip()
    else:
        raise ValueError('Incorrect path to file')


@empty_args
def get_json_from_url(values):
    response = get(values[0])
    if response.status_code == 200:
        if isinstance(response.json(), dict):  # throws ValueError
            return response.content.decode()
    else:
        raise ValueError('Not valid url')


@empty_args
def get_json_from_str(values):
    return values[0]


def replace_long_flags(usr_flags):
    for v in FLAGS.values():
        usr_flags = usr_flags.replace(v[0], v[1])
    return usr_flags


def main():
    flags = replace_long_flags(' '.join(argv[1::2]).strip().lower())
    if any(v in flags for v in FLAGS['h']):
        print(DOCSTRING)
        return
    values = argv[::2][1:]
    json_getters = {'-s': get_json_from_str, '-f': get_json_from_file, '-f -e': get_json_from_file,
                    '-u': get_json_from_url}
    print(flags, values, sep='\n')
    try:
        json_str = json_getters[flags](values) if flags in json_getters.keys() else None
    except ValueError as e:
        print(e)
        return
    if not json_str:
        print('Wrong arguments')
        return
    try:
        obj = JsonParser.loads(json_str)
        print('Result: ', type(obj), obj, sep='\n')
    except SyntaxError as e:
        print(e.msg)


if __name__ == '__main__':
    main()