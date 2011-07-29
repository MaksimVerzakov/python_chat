"""
Module contains the function which runs the server

"""
from twisted.internet import reactor
from protocol.serverprotocol import ChatProtocolFactory

def main():
    """
    This function starts the server through twisted framework
    Than server will be available as localhost with 1025 port
    
    """
    factory = ChatProtocolFactory()
    reactor.listenTCP(1025, factory)
    reactor.run() 
    
if __name__ == "__main__":
    main()
