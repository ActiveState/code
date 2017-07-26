#!/usr/bin/python2.5

from sauce import Twitter

def write_heyer(replies):
    last_reply_id = str(replies[len(replies)-1].id)
    hf = open('.heyer', 'w')
    hf.write(last_reply_id)
    hf.close()

def main():
    hf = open('.heyer', 'r')
    dot_heyer = hf.read()
    hf.close()
    api = Twitter(USERNAMW, PASSWORD)
    if len(dot_heyer) == 0:
        replies = api.get_replies()
        write_heyer(replies)
    else:
        replies = api.get_replies(since_id=dot_heyer)
        if len(replies) != 0:
            write_heyer(replies)
            for reply in replies:
                api.post_tweet("@%s YOUR MESSAGE HERE" % reply.user.screen_name)

if __name__ == '__main__':
    main()
