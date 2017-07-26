## Amazon SNS handler for the logging module  
Originally published: 2014-11-06 17:29:23  
Last updated: 2014-11-06 17:32:26  
Author: Andrea Corbellini  
  
This is a handler for the standard [logging](https://docs.python.org/library/logging.html) module that sends notifications to the [Amazon Simple Notification Service](http://aws.amazon.com/sns/).

You can use it like so:

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
                          '%(thread)d %(message)s',
            },
            'simple': {
                'format': '%(levelname)s %(message)s',
            },
        },
        'handlers': {
            'sns': {
                'level': 'INFO',
                'class': 'SNSHandler',
                'formatter': 'verbose',
                'topic_arn': 'YOUR SNS TOPIC ARN',
            },
        },
        'loggers': {
            'YOUR MODULE': {
                'handlers': ['sns'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }