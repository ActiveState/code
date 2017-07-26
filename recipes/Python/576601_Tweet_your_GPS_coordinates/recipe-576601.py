import sys
import appuifw
import messaging
import positioning

class Worker(object):
    def tweet_position(self, position):
        def call_back(state):
            if state == messaging.ESent:
                sys.stdout.write(u"Tweeted!\n")
            elif state == messaging.ESendFailed:
                sys.stdout.write(u"Something went wrong :(\n")
        
        sms = u"""%s
        I am here http://maps.google.com/maps?q=%s,%s
        """ % ((appuifw.query(u"tweet @, or cancel to tweet everybody:", "text") or ""),
            position['latitude'],position['longitude'])
        
        sys.stdout.write(u"Tweeting position ... ")
        messaging.sms_send(u"+8988", sms, callback=call_back) # +8988 -- Twitter number
    
    def get_position(self):
        positioning.select_module(270526860) # A-GPS -- you need at least a working GPRS connection
        positioning.set_requestors([{"type":"service","format":"application","data":"iamhere"}])
        sys.stdout.write(u"Retrieving position ...\n")
        return positioning.position()['position']
        
def main():
    worker = Worker()
    worker.tweet_position(worker.get_position())
    
if __name__ == '__main__':
    main()
