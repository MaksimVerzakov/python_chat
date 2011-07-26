import re

def parsingCommand(line):
    ptrn = r"(!\S+ )?([A-Z]+) ?(([^ \t\n\r\f\v']\S* ?)*)('.*')?"
    p = re.compile(ptrn)
    m = p.match(line)
    if not m:
        return (None, None, None)
    cmd = m.group(2)
    prefix = m.group(1)[1:-1] if m.group(1) else None
    args = m.group(3).split()
    if m.group(5):
        args.append(m.group(5))
    return (prefix, cmd, args)
