import unittest
from json_parser import JsonParser
from sys import argv, path


inputs = {
    'nulls': '''{"test": {"null": "something", "key": [1, 2]}, "test1": [4, 5], "null_obj": null, "ke'y1": "null"}''',
    'one_value': '''25''',
    'incorrect_syntax': '''{"list_obj": [4, 5], ''',
    "EXAMPLE": '''{"tags": ["dress", "black", "xxl"]}''',
    'int': '''2'''
}

inputo = {
    'nulls': {"test": {"null": "something", "key": [1, 2]}, "test1": [4, 5], "null_obj": None, "ke'y1": "null"},
    'one_value': '25',
    'EXAMPLE': {"tags": ["dress", "black", "xxl"]},
    'tuple_obj': {"tuple_obj": (1, 2)},
    'set_obj': {"set_obj": {2, 5}},
    'bool': True,
    'int': 2
}

specific_values = {
    'tuple_obj': '''{"tuple_obj": [1, 2]}''',
    'set_obj': '''{"set_obj": [2, 5]}''',
    'bool': '''true'''
}


class TestJsonParser(unittest.TestCase):

    def test_dumps(self):
        print('{line}TESTING dumps{line}'.format(line="-"*50))
        for k, v in inputo.items():
            try:
                val = JsonParser.dumps(v)
                if k in specific_values.keys():
                    self.assertEqual(val, specific_values[k])
                else:
                    self.assertEqual(val, inputs[k])
                print(f'SUCCESS Tested value - {v} RESULT VALUE - {val.__repr__()}')
            except SyntaxError as e:
                print(f'FAILED with value - {v}', f'WITH ERROR - {e.msg}')

    def test_loads(self):
        print('{line}TESTING loads{line}'.format(line="-"*50))
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
