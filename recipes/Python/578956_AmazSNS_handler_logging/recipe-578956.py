import logging
import boto.sns


class SNSHandler(logging.Handler):

    def __init__(self, topic_arn, *args, **kwargs):
        super(SnsHandler, self).__init__(*args, **kwargs)

        region_name = topic_arn.split(':')[3]
        self.sns_connection = boto.sns.connect_to_region(region_name)
        self.topic_arn = topic_arn

    def emit(self, record):
        subject = u'{}:{}'.format(record.name, record.levelname)
        self.sns_connection.publish(
            self.topic_arn,
            self.format(record),
            subject=subject.encode('ascii', errors='ignore')[:99])
