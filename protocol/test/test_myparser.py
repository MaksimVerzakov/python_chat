import sys
sys.path.append('/home/volodya/projects/python_chat/python_chat/')

from protocol.myparser import parsingCommand

import unittest

class ParserTests(unittest.TestCase):
    
    def test_correct_parsing(self):
        good = "!prefix CMD param1 param2 'text'"
        res = ('prefix', 'CMD', ['param1', 'param2', "'text'"])
        self.assertEqual(parsingCommand(good), res)
        
    def test_ok_parsing(self):
        good = "OK"
        res = (None, 'OK', [])
        self.assertEqual(parsingCommand(good),res)
        
    def test_message_parsing(self):
        good = "!prefix CMD 'text'"
        res = ('prefix', 'CMD', ["'text'"])
        self.assertEqual(parsingCommand(good),res)
        
    def test_not_message_parsing(self):
        good = "CMD param1"
        res = (None, 'CMD', ['param1'])
        self.assertEqual(parsingCommand(good), res)
        
    def test_two_texts_fail(self):
        bad = "CMD 'text1' 'text2'"
        res = (None, 'CMD', ["'text1'"])
        self.assertEqual(parsingCommand(bad), res)


if __name__ == '__main__':
    unittest.main()
