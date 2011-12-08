#!/usr/bin/env python2.7

import base, subprocess, os.path


class MigrationRegister(base.MigrationCommand):
    def init_args ( self ):
        super(MigrationRegister, self).init_args(
        ).with_migration_path(
        ).with_psql_arguments(
        ).add_argument('MIGRATION_FILE',
            help='the path to the migration file to register'
        )


    def main ( self, migration_path, MIGRATION_FILE, DBNAME, DBUSER, **kwargs ):
        migration_path = base.path(migration_path)

        try: MIGRATION_FILE = base.path(MIGRATION_FILE)

        except IOError:
            MIGRATION_FILE = base.path(
                migration_path, MIGRATION_FILE
            )

        subprocess.call(('psql', DBNAME, DBUSER, '-1', '-f', MIGRATION_FILE))


if __name__ == '__main__':
    MigrationRegister()()

## vim: filetype=python
