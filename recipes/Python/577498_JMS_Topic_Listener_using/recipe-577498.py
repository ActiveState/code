#!/usr/bin/env python
# JMS Topic Listener
# FB - 201012116
import time
import threading
import pyactivemq
from pyactivemq import ActiveMQConnectionFactory
# from xml.dom.minidom import parseString # for pretty XML print
# import inspect # for inspect

receivedTotal = 0
receivedMessages = []
receivedTopics = []

class MessageListener(pyactivemq.MessageListener):
    def __init__(self, topic):
        pyactivemq.MessageListener.__init__(self)
        self.topic = topic

    def onMessage(self, message):
        global receivedTotal
        global receivedMessages
        global receivedTopics
        receivedTotal += 1
        # receivedMessages.append(message.text)
        receivedMessages.append(message)
        receivedTopics.append(self.topic.name)        

class JmsTopicListener( threading.Thread ):
    def __init__(self, brokerUrl, username, password, topics, sleep):
        threading.Thread.__init__(self)
        self.sleep = sleep
        global receivedTotal
        global receivedMessages
        global receivedTopics
        self.receivedTotal = 0
        self.receivedMessages = []
        self.receivedTopics = []
        self.f = ActiveMQConnectionFactory(brokerUrl)
        self.f.username = username;
        self.f.password = password;
        self.conn = self.f.createConnection()
        self.session = self.conn.createSession()

        # JMS filter
        messageSelector = ""
        # messageSelector = "destination = 'myDestination'"

        # create a consumer for each topic
        self.tops = []
        self.consumers = []
        self.listeners = []

        i = 0
        for name in topics:
            self.tops.append(self.session.createTopic(name))
            self.consumers.append(self.session.createConsumer(self.tops[i], \
                messageSelector))
            self.listeners.append(MessageListener(self.tops[i]))
            self.consumers[i].messageListener = self.listeners[i]
            i += 1

    def run ( self ):
        self.conn.start()
        time.sleep(self.sleep)
        self.conn.close()

    def getReceivedTotal(self):
        return receivedTotal

    def getReceivedTopics(self):
        return receivedTopics
    
    def getReceivedMessages(self):
        return receivedMessages

# MAIN
if __name__ == "__main__":

    brokerUrl = 'tcp://myPC:61616'
    username = 'myUsername'
    password = 'myPassword'
    topics = ['/topic/myFirstTopic', '/topic/mySecondTopic']
    sleep = 30 # listen messages for 30 seconds

    j = JmsTopicListener(brokerUrl, username, password, topics, sleep)
    j.start()
    j.join() # wait until the thread finished running
    n = j.getReceivedTotal()
    t = j.getReceivedTopics()
    m = j.getReceivedMessages()
    print "Number of messages: " + str(n)
    print

    for k in range(n):
        print "message # " + str(k + 1)
        print
        print "topic: " + t[k]
        print
        # print m[k]
        # print parseString(m[k].text).toprettyxml()
        # print

        message = m[k]
        # print inspect.getmembers(message)
        # print

        print "JMS header:"
        print
        print "correlationID: " + str(message.correlationID)
        print "deliveryMode: "  + str(message.deliveryMode)
        print "destination: "   + str(message.destination)
        print "expiration: "    + str(message.expiration)
        print "messageID: "     + str(message.messageID)
        print "priority: "      + str(message.priority)
        print "redelivered: "   + str(message.redelivered)
        print "replyTo: "       + str(message.replyTo)
        print "timestamp: "     + str(message.timestamp)
        print "type: "          + str(message.type)
        print

        try:
            print "Special message properties:"
            print
            print "Topic: " + str(message.getStringProperty("Topic"))
            print "Priority: " + str(message.getStringProperty("Priority"))
            print "RequestId: " + str(message.getStringProperty("RequestId"))
            print "TimeToLive: " + str(message.getStringProperty("TimeToLive"))
            print
        except Exception as e:
            # print e
            # print
            pass

        print "message text:"
        print message.text
