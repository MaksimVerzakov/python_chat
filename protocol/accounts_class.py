class AccountsClass:
    
    def __init__(self, filename):
        self.file = filename
        
    def get_acc_list(self):
        accs = open(self.file) 
        acc_list = accs.readlines()
        accs.close()
        return acc_list
        
    def add_acc(self, lgn, psswrd):
        accs = open(self.file, 'a')
        accs.write('%s %s\n' %(lgn, psswrd))
        accs.close()
