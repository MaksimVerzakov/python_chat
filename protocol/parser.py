"""
A Client-Server commands parser module

Export functions :

parsingCommand -- the command-parser function, using regular expressions

"""

import re
import unittest



PTRN = r"""
            (?:!(\S+)\ )?    # prefix part
            ([A-Z]+)\ ?    # command part
            ((?:[^ \t\n\r\f\v']\S*\ ?)*)    # parametrs
            ('[^']*')?    # text
        """

REGEXP = re.compile(PTRN, re.VERBOSE)

def parsingCommand(line):
    """
       Return the tuple (prefix, cmd, args) - parts of string;
       but if string don't satisfy the command-pattern, 
       will return (None, None, None)
       
       Arguments :
       
       line -- the input data string
       
       Global variables using :
       
       PTRN -- the pattern of correct command
       REGEXP -- the regular expression that describes the PTRN
       
    """
    m = REGEXP.match(line)
    prefix, cmd, args = None, None, None
    if m:   
        cmd = m.group(2)
        prefix = m.group(1)
        args = m.group(3).split()
        if m.group(4):
            args.append(m.group(4))
    return (prefix, cmd, args)


class ParserTests(unittest.TestCase):
    def test_parsing(self):
        good = "!prefix CMD param1 param2 'text'"
        res = ('prefix', 'CMD', ['param1', 'param2', "'text'"])
        self.assertEqual(parsingCommand(good), res)
        
        good = "OK"
        res = (None, 'OK', [])
        self.assertEqual(parsingCommand(good),res)
        
        good = "!prefix CMD 'text'"
        res = ('prefix', 'CMD', ["'text'"])
        self.assertEqual(parsingCommand(good),res)
        
        good = "CMD param1"
        res = (None, 'CMD', ['param1'])
        self.assertEqual(parsingCommand(good), res)
        
        bad = "CMD 'text1' 'text2'"
        res = (None, 'CMD', ["'text1'"])
        self.assertEqual(parsingCommand(bad), res)


if __name__ == '__main__':
    unittest.main()
    
