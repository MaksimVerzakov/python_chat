
MAX_NICK_LENGHT = 15
    
commands = {}

class command:
    def __init__(self, cmd):
        self.name = cmd
    def __call__(self, func):
        commands[self.name] = func

@command('CONNECT')
def connectAction(protocol, prefix, args):
    if protocol.nickname:
        return
    users = open(protocol.factory.filename) 
    users_list = users.readlines()
    users.close()
    if len(args[0]) > MAX_NICK_LENGHT or \
       ('%s %s\n' %(args[0], args[1])) not in users_list:
           sendErrorMessage(protocol, 'err_incorrect_data')
    else:
        protocol.nickname = args[0]
        protocol.sendLine('OK')
        protocol.factory.activeUsers.append(protocol)
        sendServiceMessage(protocol.factory, args[0], serv_text['serv_connect'])
        refreshNicks(protocol.factory)
        
@command('NEW')
def newAction(protocol, prefix, args):
    if protocol.nickname:
        return
    users = open(protocol.factory.filename) 
    users_list = users.readlines()
    users.close()
    if len(args[0]) > MAX_NICK_LENGHT:
        sendErrorMessage(protocol, 'err_incorrect_data')
        return
    for account in users_list:
        if account.split()[0].startswith(args[0]):
            sendErrorMessage(protocol, 'err_user_exist')
            return
    users = open(protocol.factory.filename, 'a')
    users.write('%s %s\n' %(args[0], args[1]))
    users.close()
    protocol.nickname = args[0]
    protocol.sendLine('OK')
    protocol.factory.activeUsers.append(protocol)
    sendServiceMessage(protocol.factory, args[0], serv_text['serv_connect'])
    refreshNicks(protocol.factory)

@command('NICK')
def nickAction(protocol, prefix, args):
    if not protocol.nickname or prefix == args[0]:
        return
    if len(args[0]) > MAX_NICK_LENGHT:
        sendErrorMessage(protocol, 'err_incorrect_data')
        return
    for user in protocol.factory.activeUsers:
        if user.nickname == args[0]:
            sendErrorMessage(protocol, 'err_user_exist')
            return
    protocol.nickname = args[0]
    protocol.sendLine('OK')
    sendServiceMessage(protocol.factory, prefix, serv_text['serv_change_nick'] + args[0])
    refreshNicks(protocol.factory)

@command('NAMES')
def namesAction(protocol, prefix=0, args=0):
    if not protocol.nickname:
        return
    nicks = []
    for user in protocol.factory.activeUsers:
        nicks.append(user.nickname)
    protocol.sendLine('NAMES %s'  %' '.join(nicks))
    
@command('MSG')
def msgAction(protocol, prefix, args):
    if not protocol.nickname:
        return
    msg = 'MSG %s %s %s' %(prefix, args[0], args[1])
    for user in protocol.factory.activeUsers:
        user.sendLine(msg)

@command('QUIT')
def quitAction(protocol, prefix, args):
    print('quit')
    print args[0]
    if not protocol.nickname:
        return
    commands['MSG'](protocol, prefix, ['*', args[0]])
    fctry = protocol.factory
    sendServiceMessage(fctry, prefix, serv_text['serv_leave'])
    refreshNicks(fctry)
  #  protocol.transport.loseConnection()




err_text = {'err_incorrect_data' : 'Incorrect data',
            'err_user_exist' : 'User already exist'}

serv_text = {'serv_connect' : ' is connected to our daft party',
             'serv_change_nick' : ' now is known as ',
             'serv_leave' : ' just leave us all :('}

def sendServiceMessage(factory, nick, text, newnick=''):
    for user in factory.activeUsers:
        user.sendLine("SERVICE %s '%s'" %(nick, text))
    

def sendErrorMessage(protocol, error):
    protocol.sendLine("ERROR '%s'" %err_text[error])
    
def refreshNicks(factory):
    for user in factory.activeUsers:
        commands['NAMES'](user)

def closeProtocol(protocol):
    if protocol.nickname:
        sendServiceMessage(protocol.factory, protocol.nickname, serv_text['serv_leave'])
        protocol.factory.activeUsers.remove(protocol)
       # protocol.transport.loseConnection()
        
