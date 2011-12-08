import argparse, os.path, sys, hashlib, importlib

MIGRATION_EXTENSION = '.pg.sql'


def path ( *paths ):
    path = os.path.join(*paths)

    abspath = os.path.abspath(path)

    if not os.path.exists(abspath): raise IOError(
        'Specified path does not exist: %s' % path
    )

    return abspath


class Command(argparse.ArgumentParser):
    def __init__ ( self, *args, **kwargs ):
        super(Command, self).__init__(*args, **kwargs)

        self.init_args()


    def add_argument ( self, *args, **kwargs ):
        super(Command, self).add_argument(*args, **kwargs)

        return self


    def init_args ( self ):
        return self.add_argument('-d', '--debug', action='store_true', dest='debug',
            help='display the full stack trace of errors instead of just the message'
        )


    def __call__ ( self, args=None ):
        args = None

        try:
            args = self.parse_args(args)

            ## TODO: Add config file support...
            #if args.config_file: pass ## TODO: Load / save args to config_file...?

            self.main(**vars(args))

        except Exception, error:
            if args and args.debug: raise

            if hasattr(error, 'returncode'):
                self.exit(error.returncode)

            self.exit(1, str(error))


    def main ( self, *args, **kwargs ):
        pass


class MigrationCommand(Command):
    def with_migration_path ( self ):
        return self.add_argument('-M', '--migration-path', dest='migration_path', default='etc/migrations/',
            help='the path in which to store migrations, default: etc/migrations/')


    def with_schema_file ( self ):
        return self.add_argument('-s', '--schema-file', dest='schema_file', default='etc/schema.pg.sql',
            help='the schema file to mark migrations from, default: etc/schema.pg.sql'
        )


    def with_migration_name ( self, **kwargs ):
        defaults = dict(type=str, dest='migration_name',
            help='the name of the migration to create (use the current hash of the schema file by default)'
        )

        defaults.update(kwargs); kwargs = defaults

        return self.add_argument('-m', '--migration-name', **kwargs)


    def with_psql_arguments ( self ):
        return self.add_argument('DBNAME', nargs='?', default='',
        ).add_argument('DBUSER', nargs='?', default='',
        )


    def get_HASH ( self, schema_file, long_hash=False ):
        with open(schema_file) as f:
            HASH = hashlib.sha256(f.read()).hexdigest()

            return HASH if long_hash else HASH[0:7]


class Migrations(Command):
    def init_args ( self ):
        super(Migrations, self).init_args(
        ).add_argument(
            'COMMAND', nargs=1 choices = (
                'init', 'create', 'register', 'apply'
            )
        )


    def main ( self, command ):
        module = importlib.import_module(command)

        return module.command()


def command ( ): return Migrations()
