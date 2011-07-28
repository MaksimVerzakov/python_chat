from protocol.serverprotocol import ChatProtocolFactory

def main():
    factory = ChatProtocolFactory()
    reactor.listenTCP(1025, factory)
    reactor.run() 
    
if __name__ == "__main__":
    main()
