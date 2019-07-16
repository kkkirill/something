import unittest
from json_parser import JsonParser
from json import (loads as l, dumps as d)
from sys import argv, path


inputs = {
    'nulls': '''{"test": {"null": "something", "key": [1, 2]}, "test1": [4, 5], "null_obj": null, "ke'y1": "null"}''',
    'with_other_iterables': '''{"tuple_obj": (4, 5), "set_obj": {2, 5}, "null_obj": "null"}''',
    'one_value': '''25''',
    'incorrect_syntax': '''{"list_obj": [4, 5], '''
}

inputo = {
    'nulls': {"test": {"null": "something", "key": [1, 2]}, "test1": [4, 5], "null_obj": None, "ke'y1": "null"},
    'with_other_iterables': {"tuple_obj": (4, 5), "set_obj": {2, 5}, "null_obj": "null"},
    'one_value': '25'
}


class TestJsonParser(unittest.TestCase):

    # def test_dumps(self):
    #     print(f'{"-"*50}TESTING dumps{"-"*50}')
    #     for k, v in inputo.items():
    #         val = JsonParser.dumps(v)
    #         self.assertEqual(val, inputs[k], f'Tested pair - {k} : {v}')

    def test_loads(self):
        print(f'{"-"*50}TESTING loads{"-"*50}')
        argv.append('-s')
        for k, v in inputs.items():
            if len(argv) == 2:
                argv.append(v)
            else:
                argv[2] = v
            try:
                val = JsonParser.loads(v)
                self.assertEqual(val, inputo[k])
                print(f'SUCCESS Tested value - {v}')
            except SyntaxError as e:
                print(f'FAILED with value - {v}', f'WITH ERROR - {e.msg}')


if __name__ == '__main__':
    unittest.main()
