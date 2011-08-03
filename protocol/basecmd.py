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

class command:
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
        
class ExClass(BaseException):
    """Exception class for any command handler function exceptions"""
    
    def __init__(self):
        """Set error message for exception"""
        self.msg = self.__class__.__name__
    def __str__(self):
        """Print exception error info"""
        return self.msg
        
class ExIncorrectData(ExClass):
    """
    Exception class for err_incorrect_data error in 
    CONNECT and NICK and NEW commands
    
    """
    pass
    
class ExUserExist(ExClass):
    """
    Exception class for err_user_exist error in 
    NEW and NICK commands
    """
    pass

@command('CONNECT')
def connectAction(protocol, prefix, args):
    """
    This is the CONNECT command handler
    Calls when user want to enter the chat using his account
    
    Arguments : 
    
        prefix -- None, unused argument

        args -- list with two string-type elements 
           first one is the login of connected user
           second one is the password for user login
    
    Result :
    
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
    if len(args[0]) > MAX_NICK_LENGHT or ' ' in args[0]  or \
       ('%s %s\n' %(args[0], args[1])) not in users_list:
           sendErrorMessage(protocol, 'err_incorrect_data')
           raise ExIncorrectData
    else:
        successConnect(protocol, args[0])
        
@command('NEW')
def newAction(protocol, prefix, args):
    """
    This is the NEW command handler
    Calls when user want to create new account and then enter the chat
    
    Arguments : 
    
        prefix -- None, unused argument

        args -- list with two string-type elements 
                first one is the login of new user's account
                second one is the password for this account
    
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
    if len(args[0]) > MAX_NICK_LENGHT or ' ' in args[0]:
        sendErrorMessage(protocol, 'err_incorrect_data')
        raise ExIncorrectData
    users_list = protocol.factory.accountsData.get_acc_list()
    for account in users_list:
        if account.split()[0].startswith(args[0]):
            sendErrorMessage(protocol, 'err_user_exist')
            raise ExUserExist
    protocol.factory.accountsData.add_acc(args[0], args[1])
    successConnect(protocol, args[0])

@command('NICK')
def nickAction(protocol, prefix, args):
    """
    This is the NICK command handler
    Calls when user want to change his nick for another
    
    Arguments : 
    
        prefix -- type-string current user nick

        args -- list with one string-type element
            new_nick that user want to use
    
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
    if prefix != args[0]:
        if len(args[0]) > MAX_NICK_LENGHT or ' ' in args[0]:
            sendErrorMessage(protocol, 'err_incorrect_data')
            raise ExIncorrectData
        for user in protocol.factory.activeUsers:
            if user.nickname == args[0]:
                sendErrorMessage(protocol, 'err_user_exist')
                raise ExUserExist
        protocol.nickname = args[0]
        protocol.sendLine('OK')
        sendServiceMessage(protocol.factory, prefix, serv_text['serv_change_nick'] + args[0])
        refreshNicks(protocol.factory)

@command('NAMES')
def namesAction(protocol, prefix=0, args=0):
    """
    This is the NAMES command handler
    Calls when user want to take nicks of all active users
    
    Arguments : 
    
        prefix -- string-type user nick, unused parametr

        args -- None, unused parametr
    
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
    
    Arguments : 
    
        prefix -- string-type user nick

        args -- list with two string-type elements 
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

@command('QUIT')
def quitAction(protocol, prefix, args):
    """
    This is the QUIT command handler
    Calls when user close his chat window
    
    Arguments : 
    
        prefix -- string-type user nick

        args -- list with one string-type element 
           element is a 'goodbye'-message for other users
    
    Result :
    
        Server send service to all users
        and call procedure that makes an actions 
        which must be made when user leaves the Server
    
    """
    if not protocol.nickname:
        return
    closeProtocol(protocol, args[0])


err_text = {'err_incorrect_data' : 'Incorrect data',
            'err_user_exist' : 'User already exist'}

serv_text = {'serv_connect' : ' is connected to our daft party',
             'serv_change_nick' : ' now is known as ',
             'serv_leave' : ' just leave us all'}
             
def successConnect(protocol, nick):
    """
    This procedure calls when user entered the chat
    
    Arguments :
    
        protocol -- the protocol of authorized user

        nick -- string-type user's nick
    
    Result :
    
        -set the user nick

        -send 'OK' message for client 

        -allows using the chat for user

        -send service-information message to other users in chat

        -refresh users-lists for all active users
    
    """
    protocol.nickname = nick
    protocol.sendLine('OK')
    protocol.factory.activeUsers.append(protocol)
    sendServiceMessage(protocol.factory, nick, serv_text['serv_connect'])
    refreshNicks(protocol.factory)

def sendServiceMessage(factory, nick, text):
    """
    This procedure sends any kind of service-information to all active users
    
    Arguments :
    
        factory -- the server protocol factory that contains info of activeusers

        nick -- string-type user nick which is object of service information

        text -- string-type service message
    
    """
    for user in factory.activeUsers:
        user.sendLine("SERVICE %s '%s'" %(nick, text))
    

def sendErrorMessage(protocol, error):
    """
    This procedure sends any kind of error-information to user
    
    Arguments :
    
        protocol -- client protocol of user-reciever error message

        error -- string-literal error key. 
                 error message is a value of this key in error dictionary
    
    """
    protocol.sendLine("ERROR '%s'" %err_text[error])
    
def refreshNicks(factory):
    """Refresh users-lists for all active users in chat"""
    for user in factory.activeUsers:
        commands['NAMES'](user)

def closeProtocol(protocol, arg=''):
    """
    This procedure makes an actions which must be made 
    when user leaves the Server
    
    Arguments :
    
        protocol -- client protocol of leaving user

        arg -- string-type farewall message of leaving user
    
    Result :
    
        Deacivate this user
        Send service message to all active users
        Refresh users-lists for all active users in chat
        If user send farewall message it send with service message
    
    """
    if protocol.nickname and (protocol in protocol.factory.activeUsers):
        protocol.factory.activeUsers.remove(protocol)
        msg = serv_text['serv_leave']
        if arg != '':
            msg += ' and tell : %s' % arg
        sendServiceMessage(protocol.factory, protocol.nickname, msg)
        refreshNicks(protocol.factory)
        

