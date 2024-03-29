import unittest
from json_parser import JsonParser
from sys import argv, path


inputs = {
    'nulls': '''{"test": {"null": "something", "key": ["1", ["opa", 2]]}, "test1": [4, 5], "null_obj": null, "ke'y1": "null"}''',
    'one_value': '''25''',
    'incorrect_syntax': '''{"list_obj": [4, 5], ''',
    "EXAMPLE": '''{"tags": ["dress", "black", "xxl"]}''',
    'int': '''2''',
    'opa': '''"print(\\"HELLO\\")"''',
    'important': '''"\\"foo\\bar"'''
}

inputo = {
    'nulls': {"test": {"null": "something", "key": ['1', ['opa', 2]]}, "test1": [4, 5], "null_obj": None, "ke'y1": "null"},
    'one_value': '25',
    'EXAMPLE': {"tags": ["dress", "black", "xxl"]},
    'tuple_obj': {"tuple_obj": (1, 2)},
    'set_obj': {"set_obj": {2, 5}},
    'bool': True,
    'int': "2",
    'test_list': [1, 2, 3, 4],
}

specific_dumps_values = {
    'tuple_obj': '''{"tuple_obj": [1, 2]}''',
    'set_obj': '''{"set_obj": [2, 5]}''',
    'bool': '''true''',
    'lambda': None,
    'test_list': '''[1, 2, 3, 4]'''
}

specific_loads_values = {
    'opa': 'print("HELLO")',
    'important': '"foo\bar'
}


class TestJsonParser(unittest.TestCase):

    def test_dumps(self):
        print('{line}TESTING dumps{line}'.format(line="-"*50))
        for k, v in inputo.items():
            try:
                val = JsonParser.dumps(v)
                if k in specific_dumps_values.keys():
                    # print(val.__repr__())
                    self.assertEqual(specific_dumps_values[k], val)
                else:
                    self.assertEqual(inputs[k], val)
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
                if k in specific_loads_values.keys():
                    self.assertEqual(specific_loads_values[k], val)
                else:
                    self.assertEqual(inputo[k], val)
                print(f'SUCCESS Tested value - {v}')
            except SyntaxError as e:
                print(f'FAILED with value - {v}', f'WITH ERROR - {e.msg}')


if __name__ == '__main__':
    unittest.main()
