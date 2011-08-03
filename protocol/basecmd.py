"""
A Server Protocol library, contains a command handlers

Export data :

    commands -- kind of {COMMAND: handlerFunctionName} dictionary
                that links each command with her handler function

Export functions :

    closeProtocol -- this procedure makes an actions which must be made
                     when user leaves the Server

"""

MAX_NICK_LENGHT = 15
    
commands = {}

class command(object):
    """An interface for addition elements in commands dictionary"""
    
    def __init__(self, cmd):
        """Constructor save name of new command"""
        self.name = cmd
        
    def __call__(self, func):
        """
        This method add handler for command and
        also add this pair in dictionary
        
        """
        commands[self.name] = func
        
class CmdException(BaseException):
    """Exception class for any command handler function exceptions"""
    
    def __init__(self, protocol, errorkey):
        """Set error message for exception"""
        self.protocol = protocol
        self.errorkey = errorkey
        
    def __call__(self):
        """Print exception error info"""
        sendErrorMessage(self.protocol, self.errorkey)
        
@command('CONNECT')
def connectAction(protocol, prefix, args):
    """
    This is the CONNECT command handler
    Calls when user want to enter the chat using his account
    
    :param protocol: protocol of connected user
    :param prefix : None, unused argument
    :param args: list with two string-type elements 
           first one is the login of connected user
           second one is the password for user login
    :raises: CmdException
    
     Result:
    
    - if user was authorithed successfully
         function send the "OK" message to client protocol
         for all users in chat will send service-information message
                                    and refreshed their users-list
    - else 
         function send any ErrorMessage to client protocol
         and also raise exception
         user doesn't enter the chat
    
    """
    users_list = protocol.factory.accountsData.get_acc_list()
    try:
        if  badNick(args[0]) or \
           ('%s %s\n' %(args[0], args[1])) not in users_list:
                raise CmdException, (protocol, 'err_incorrect_data')    
    except:
        raise CmdException, (protocol, 'err_incorrect_data')
    successConnect(protocol, args[0])
        
@command('NEW')
def newAction(protocol, prefix, args):
    """
    This is the NEW command handler
    Calls when user want to create new account and then enter the chat
    
    :param protocol: protocol of connected user
    :param prefix : None, unused argument
    :param args: list with two string-type elements 
           first one is the login of new user's account
           second one is the password for this account
    :raises: CmdException
    
    Result :
    
        - if account was created successfully
             function send the "OK" message to client protocol
             and then user will entered to the chat
             for all users in chat will send service-information message
                                        and refreshed their users-list
        - else 
             function send any ErrorMessage to client protocol
             and also raise exception
             user doesn't enter the chat
    
    """
    try:
        if badNick(args[0]):
            raise CmdException, (protocol, 'err_incorrect_data')
    except:
        raise CmdException, (protocol, 'err_incorrect_data')
    users_list = protocol.factory.accountsData.get_acc_list()
    for account in users_list:
        if account.split()[0].startswith(args[0]):
            raise CmdException, (protocol, 'err_user_exist')
    protocol.factory.accountsData.add_acc(args[0], args[1])
    successConnect(protocol, args[0])

@command('NICK')
def nickAction(protocol, prefix, args):
    """
    This is the NICK command handler
    Calls when user want to change his nick for another
 
    :param prefix: current user nick
    :type prefix: str
    :param args: list with one string-type element
                 new_nick that user want to use
    :raises: CmdException
    
    Result :
    
        - if user nick was changed successfully
             function send the "OK" message to client protocol
             for all users in chat will send service-information message
                                        and refreshed their users-list
        - else 
             function send any ErrorMessage to client protocol
             and also raise exception
             user's nick doesn't changes
    
    """    
    if not args or badNick(args[0]):
        raise CmdException, (protocol, 'err_incorrect_data')
        
    if prefix == args[0]:
        return
        
    for user in protocol.factory.activeUsers:
        if user.nickname == args[0]:
            raise CmdException, (protocol, 'err_user_exist')
    protocol.nickname = args[0]
    sendOK(protocol)
    sendServiceMessage(protocol.factory, prefix, 
                        serv_text['serv_change_nick'] + args[0])
    refreshNicks(protocol.factory)

@command('NAMES')
def namesAction(protocol, prefix=0, args=0):
    """
    This is the NAMES command handler
    Calls when user want to take nicks of all active users
    
    
    :param prefix: user nick, unused parametr
    :param args: None, unused parametr
    
    Result :
    
        Server send to client list of all users nickanames
    
    """
    nicks = []
    for user in protocol.factory.activeUsers:
        nicks.append(user.nickname)
    protocol.sendLine('NAMES %s'  %' '.join(nicks))
    
@command('MSG')
def msgAction(protocol, prefix, args):
    """
    This is the MSG command handler
    Calls when user want to send message to chat
    
    :param prefix: user nick
    :type prefix: str
    :param args: list with two string-type elements 
           first one is the destination of user's message :
                     * for all users or username of targer user
           second one is the messae text concluded in '' 
                      ('text_message' style)
    
    Result :
    
        Server send this message (in another form) to all users
    
    """
    if protocol.nickname:
        msg = 'MSG %s %s %s' %(prefix, args[0], args[1])
        for user in protocol.factory.activeUsers:
            user.sendLine(msg)
"""
@command('QUIT')
def quitAction(protocol, prefix, args):
 
    This is the QUIT command handler
    Calls when user close his chat window
    
    
    :param prefix: user nick
    :type prefix: str
    :param args: list with one string-type element 
           element is a 'goodbye'-message for other users
    
    Result :
    
        Server send service to all users
        and call procedure that makes an actions 
        which must be made when user leaves the Server
    
    if not protocol.nickname:
        return
    closeProtocol(protocol, args[0])
    protocol.transport.loseConnection()
"""


err_text = {'err_incorrect_data' : 'Incorrect data',
            'err_user_exist' : 'User already exist'}

serv_text = {'serv_connect' : ' is connected to our daft party',
             'serv_change_nick' : ' now is known as ',
             'serv_leave' : ' just leave us all'}
             
def successConnect(protocol, nick):
    """
    This procedure calls when user entered the chat
        
    :param protocol: the protocol of authorized user

    :param nick: string-type user's nick
    
    Result :
    
        -set the user nick

        -send 'OK' message for client 

        -allows using the chat for user

        -send service-information message to other users in chat

        -refresh users-lists for all active users
    
    """
    protocol.nickname = nick
    sendOK(protocol)
    protocol.factory.activeUsers.append(protocol)
    sendServiceMessage(protocol.factory, nick, 
                       serv_text['serv_connect'])
    refreshNicks(protocol.factory)

def sendServiceMessage(factory, nick, text):
    """
    This procedure sends any kind of service-information 
    to all active users
        
    :param factory: the server protocol factory that 
            contains info of activeusers
    :param nick: string-type user nick which is 
        object of service information
    :param text: string-type service message
    
    """
    for user in factory.activeUsers:
        user.sendLine("SERVICE %s '%s'" %(nick, text))
    

def sendErrorMessage(protocol, error):
    """
    This procedure sends any kind of error-information to user
    
    :param protocol: client protocol of user-reciever error message

    :param error: string-literal error key. 
                 error message is a value of this key 
                 in error dictionary
    
    """
    protocol.sendLine("ERROR '%s'" %err_text[error])
    
def refreshNicks(factory):
    """Refresh users-lists for all active users in chat"""
    for user in factory.activeUsers:
        commands['NAMES'](user)

def closeProtocol(protocol):
    """
    This procedure makes an actions which must be made 
    when user leaves the Server

    :param protocol: client protocol of leaving user

    Result :
    
        Deacivate this user
        Send service message to all active users
        Refresh users-lists for all active users in chat
    
    """
    if protocol not in protocol.factory.activeUsers:
        return
    protocol.factory.activeUsers.remove(protocol)
    sendServiceMessage(protocol.factory, protocol.nickname, serv_text['serv_leave'])
    refreshNicks(protocol.factory)

def badNick(nickname):
    """
    Check correctable of nickname. 
    Returns false if nickname is correct
    """
    return (not nickname or len(nickname) > MAX_NICK_LENGHT or ' ' in nickname)

def sendOK(protocol):
    """Send OK message for client"""
    protocol.sendLine('OK')
