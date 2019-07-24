import pcre
from sys import argv as a

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
                return eval(input_str, {}, {})
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


def main():
    argv = a[1:]
    json_str = ''
    length = len(argv)
    if length and argv[0] in FLAGS['h']:
        print(DOCSTRING)
        return
    if length > 4 or length < 2:
        print('Incorrect arguments')
        print(DOCSTRING)
        return
    elif length in (2, 3) and argv[0] in FLAGS['f'] and (argv[2] in FLAGS['e'] if length == 3 else True):
        from pathlib import Path
        if Path(argv[1]).is_file() and argv[1] != __file__:
            with open(argv[1], 'r', encoding=argv[2] if length == 3 else 'utf-8') as f:
                json_str = f.readline()
        else:
            print('Incorrect path to file')
            return
    elif length == 2:
        if argv[0] in FLAGS['s']:
            json_str = argv[1]
        elif argv[0] in FLAGS['u']:
            from requests import get
            response = get(argv[1])
            if response.status_code == 200:
                try:
                    if isinstance(response.json(), dict):
                        json_str = response.content.decode()
                except ValueError:
                    print('Not valid json by url')
            else:
                print('Not valid url')
                return
        else:
            print('Incorrect arguments')
            return
    try:
        obj = JsonParser.loads(json_str)
        print('Result: ', type(obj), obj, sep='\n')
    except SyntaxError as e:
        print(e.msg)


if __name__ == '__main__':
    main()