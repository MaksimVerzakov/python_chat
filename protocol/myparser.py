"""A Client-Server commands parser module

Export functions :

parsingCommand -- the command-parser function, using regular expressions

"""

import re

PTRN = r'''
            (?:!(\S+)\ )?    # prefix part
            ([A-Z]+)\ ?    # command part
            ((?:[^ \t\n\r\f\v']\S*\ ?)*)    # parametrs
            ('[^']*')?    # text
        '''

REGEXP = re.compile(PTRN, re.VERBOSE)

def parsingCommand(line):
    """Return the tuple (prefix, cmd, args) - parts of string;
    but if string don't satisfy the command-pattern, 
    will return (None, None, None)
       
    :param line: the input data string
    :type line: str
       
       Global variables using :
       
       PTRN -- the pattern of correct command
       REGEXP -- the regular expression that describes the PTRN
    
    :returns: (prefix, cmd, args) - parts of line
    :rtype: tuple
       
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
