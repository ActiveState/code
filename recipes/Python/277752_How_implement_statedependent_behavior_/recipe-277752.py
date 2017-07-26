#!/usr/bin/env python
#
# Author: Bschorer Elmar
# State-Pattern Demo

class NetworkCardState:
    """Abstract State Object"""
    def send(self):
        raise "NetworkCardState.send - not overwritten"
    
    def receive(self):
        raise "NetworkCardState.receive - not overwritten"

    
class Online(NetworkCardState):
    """Online state for NetworkCard"""
    def send(self):
        print "sending Data"
        
    def receive(self):
        print "receiving Data"


class Offline(NetworkCardState):
    """Offline state for NetworkCard"""
    def send(self):
        print "cannot send...Offline"
        
    def receive(self):
        print "cannot receive...Offline"

    
class NetworkCard:
    def __init__(self):
        self.online = Online()
        self.offline = Offline()
        ##default state is Offline
        self.currentState = self.offline 
    
    def startConnection(self):
        self.currentState = self.online

    def stopConnection(self):
        self.currentState = self.offline
    
    def send(self):
        self.currentState.send()
        
    def receive(self):
        self.currentState.receive()
        

def main():
    myNetworkCard = NetworkCard()
    print "without connection:"
    myNetworkCard.send()
    myNetworkCard.receive()
    print "starting connection"
    myNetworkCard.startConnection()
    myNetworkCard.send()
    myNetworkCard.receive()

if __name__ == '__main__':
    main()
        

        

        
