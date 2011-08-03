"""
Module contains a simple class which realize interface for work with
server information about users : logins and passwords restiored in file

Export classes :

    AccountsClass

"""
class AccountsClass(object):
    """
    Realize simple interface for work with
    server information about users
    
    Contruct for input name of the file with data
    
    Publec methods :
    
        get_acc_list -- method returns list of strings that contains 
                        login and password for chat user

        add_acc -- method adds new account, restores login and 
                                                password of new user
    
    """
    
    def __init__(self, filename):
        self.filename = filename
        
    def get_acc_list(self):
        """
        Reads data file and returns list of strings of file
        
        :returns: list of stings in file
        
        """

        accs = open(self.filename) 
        acc_list = accs.readlines()
        accs.close()
        return acc_list
        
    def add_acc(self, login, password):
        """
        Creates new string in server data file and restores
        login and password of new user there
        
        
        """
        accs = open(self.filename, 'a')
        accs.write('%s %s\n' %(login, password))
        accs.close()
