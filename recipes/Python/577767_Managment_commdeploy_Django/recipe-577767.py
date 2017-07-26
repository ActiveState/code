from django.core.management.base import BaseCommand, CommandError

from django.conf import settings

import commands, os
from optparse import make_option



class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
                make_option('--test', '-t', 
                            dest='test',
                            action='store_true',
                            default=False,
                            help='Simulate the synchronization.'),
    )
    help = 'It allows to sync your develop site project with the remote site repository.'

    def handle(self, *args, **options):
        """
        List of options in rsync command:
        -a:     Preserve the attibutes of the files.
        -v:     Verbose.
        -z:     Enables the compression.
        -u:     Update files.
        -r:     Recursive.
        -E:     Preserve Executability.
        -h:     Human readable.
        -n:     Simulate.
        """
        # Check the rsync command
        st, out = commands.getstatusoutput('rsync --version')
        if st !=0:
            self.stderr.write('Error: To use this command you need the rsync command.\n')
            exit(1)
        
            
        # Check for the settings parameters            
        try:
            # Deploy data
            USER_SERVER = settings.USER_SERVER
            DOMAIN_SERVER = settings.DOMAIN_SERVER
            DIR_SERVER = settings.DIR_SERVER
            DIR_LOCAL = settings.DIR_LOCAL
        except AttributeError:
            self.stderr.write('Error: You have to define the parameters in settings.py.\n')
            exit(1)
            

            
        opts = '-uhzravE --exclude="*.pyc" --exclude=settings.py --exclude="mydata.db"'
        if options['test']:
            opts = opts+' -n'
            
        os.system('rsync '+opts+' '+DIR_LOCAL+' '+USER_SERVER+'@'+DOMAIN_SERVER+':'+DIR_SERVER)
        self.stdout.write('\nWARNING: Consider that the file settings.py must be sent manually.\n'+ \
        'Don\'t apply any changes in the server directory except into settings.py\n')
        
        pass
