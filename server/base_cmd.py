
MAX_NICK_LENGHT = 15


def ParsingCommand(line):
    ind = line.find(" '")
    msg = []
    if ind == -1:
        msg = line.split()
    else:
        msg = line[:ind].split()
        msg.append(line[ind + 1:])
    prefix = None
    index = 0
    if msg[0].startswith('!'):
        prefix = msg[0][1:]
        index = 1
    cmd = msg[index]
    args = msg[index + 1 : ]
    if cmd not in commands:
        cmd = None
    return (prefix, cmd, args)

def ConnectAction(protocol, prefix, args):
    if protocol.nickname:
        return
    users = open(protocol.factory.filename) 
    users_list = users.readlines()
    users.close()
    if len(args[0]) > MAX_NICK_LENGHT or \
       args[0] + ' ' + args[1] + '\n' not in users_list:
           SendErrorMessage(protocol, 'err_incorrect_data')
    else:
        protocol.nickname = args[0]
        protocol.sendLine('OK')
        protocol.factory.activeUsers.append(protocol)
        SendServiceMessage(protocol.factory, args[0], serv_text['serv_connect'])
        RefreshNicks(protocol.factory)
        
            
def NewAction(protocol, prefix, args):
    if protocol.nickname:
        return
    users = open(protocol.factory.filename) 
    users_list = users.readlines()
    users.close()
    if len(args[0]) > MAX_NICK_LENGHT:
        SendErrorMessage(protocol, 'err_incorrect_data')
        return
    for account in users_list:
        if account.split()[0].startswith(args[0]):
            SendErrorMessage(protocol, 'err_user_exist')
            return
    users = open(protocol.factory.filename, 'a')
    users.write(args[0] + ' ' + args[1] + '\n')
    users.close()
    protocol.nickname = args[0]
    protocol.sendLine('OK')
    protocol.factory.activeUsers.append(protocol)
    SendServiceMessage(protocol.factory, args[0], serv_text['serv_connect'])
    RefreshNicks(protocol.factory)

def NickAction(protocol, prefix, args):
    if not protocol.nickname or prefix == args[0]:
        return
    if len(args[0]) > MAX_NICK_LENGHT:
        SendErrorMessage(protocol, 'err_incorrect_data')
        return
    for user in protocol.factory.activeUsers:
        if user.nickname == args[0]:
            SendErrorMessage(protocol, 'err_user_exist')
            return
    protocol.nickname = args[0]
    SendServiceMessage(protocol.factory, prefix, serv_text['serv_change_nick'] + args[0])
    RefreshNicks(protocol.factory)

def NamesAction(protocol, prefix=0, args=0):
    if not protocol.nickname:
        return
    nicks = []
    for user in protocol.factory.activeUsers:
        nicks.append(user.nickname)
    protocol.sendLine('NAMES ' + ' '.join(nicks))
    
def MsgAction(protocol, prefix, args):
    if not protocol.nickname:
        return
    msg = 'MSG ' + prefix + ' ' + args[0] + ' ' + args[1]
    for user in protocol.factory.activeUsers:
        user.sendLine(msg)

def QuitAction(protocol, prefix, args):
    if not protocol.nickname:
        return
    MsgAction(protocol, prefix, ['*', args[0]])
    fctry = protocol.factory
    protocol.factory.activeUsers.remove(protocol)
    protocol.transport.loseConnection()
    SendServiceMessage(fctry, prefix, serv_text['serv_leave'])


commands = {'CONNECT' : ConnectAction,
            'NEW' : NewAction,
            'NICK' : NickAction,
            'NAMES' : NamesAction,
            'MSG' : MsgAction,
            'QUIT' : QuitAction}

err_text = {'err_incorrect_data' : 'Incorrect data',
            'err_user_exist' : 'User already exist'}

serv_text = {'serv_connect' : ' is connected to our daft party',
             'serv_change_nick' : ' now is known as ',
             'serv_leave' : ' just leave us all :('}

def SendServiceMessage(factory, nick, text, newnick=''):
    for user in factory.activeUsers:
        user.sendLine("SERVICE " + nick + " '" + text + "'")
    

def SendErrorMessage(protocol, error):
    protocol.sendLine("ERROR '" + err_text[error] + "'")
    
def RefreshNicks(factory):
    for user in factory.activeUsers:
        NamesAction(user)

def CloseProtocol(protocol):
    if protocol.nickname:
        SendServiceMessage(protocol.factory, protocol.nickname, serv_text['serv_leave'])
        protocol.factory.activeUsers.remove(protocol) 
    protocol.factory.clientProtocols.remove(protocol) 
