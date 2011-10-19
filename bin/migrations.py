import argparse, os.path, sys

def path ( value ):
    abspath = os.path.abspath(value)

    if not os.path.exists(abspath): raise Exception(
        'Specified path does not exist: %s' % value
    )

    return abspath


class Command(argparse.ArgumentParser):
    def __init__ ( self, *args, **kwargs ):
        super(Command, self).__init__(*args, **kwargs)

        self.add_argument('-d', '--debug', action='store_true', dest='debug',
            help='display the full stack trace of errors instead of just the message'
        ).add_argument('-c', '--config', dest='config_file', default='.pg-migrate',
            help='the configuration file to use (command flags override config options)'
        ).add_argument('--no-config', dest='config_file', action='store_const', const=None,
            help='do not use a configuration file at all'
        )


    def add_argument ( self, *args, **kwargs ):
        super(Command, self).add_argument(*args, **kwargs)

        return self


    def __call__ ( self, args=None ):
        args = None

        try:
            args = self.parse_args(args)

            if args.config_file: pass ## TODO: Load / save args to config_file...?

            self.main(**vars(args))

        except Exception, error:
            if args and args.debug: raise

            if hasattr(error, 'returncode'):
                self.exit(error.returncode)

            self.exit(1, str(error))


    def main ( self, *args, **kwargs ):
        pass
