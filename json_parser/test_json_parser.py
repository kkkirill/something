import unittest
from json_parser import JsonParser
from sys import argv, path


inputs = {
    'nulls': '''{"test": {"null": "something", "key": [1, 2]}, "test1": [4, 5], "null_obj": null, "ke'y1": "null"}''',
    'with_other_iterables': '''{"tuple_obj": [4, 5], "set_obj": {2, 5}, "null_obj": "null"}''',
    'one_value': '''25''',
    'incorrect_syntax': '''{"list_obj": [4, 5], '''
}

inputo = {
    'nulls': {"test": {"null": "something", "key": [1, 2]}, "test1": [4, 5], "null_obj": None, "ke'y1": "null"},
    'with_other_iterables': {"tuple_obj": (4, 5), "set_obj": {2, 5}, "null_obj": "null"},
    'one_value': '25',
}


class TestJsonParser(unittest.TestCase):

    def test_dumps(self):
        print('{line}TESTING dumps{line}'.format(line="-"*50))
        for k, v in inputo.items():
            try:
                val = JsonParser.dumps(v)
                self.assertEqual(val, inputs[k])
                print(f'SUCCESS Tested value - {v}')
            except SyntaxError as e:
                print(f'FAILED with value - {v}', f'WITH ERROR - {e.msg}')
        test_tuple_str = '''{"tuple_obj": [1, 2]}'''
        test_tuple_obj = {"tuple_obj": (1, 2)}
        val = JsonParser.dumps(test_tuple_obj)
        self.assertEqual(val, test_tuple_str)
        print(f'SUCCESS Tested value - {str(test_tuple_obj)}, Expected - {test_tuple_str}')

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
