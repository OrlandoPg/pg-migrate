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
        migration_path = migrations.path(migration_path)

        try: MIGRATION_FILE = migrations.path(MIGRATION_FILE)

        except IOError:
            MIGRATION_FILE = migrations.path(
                migration_path, MIGRATION_FILE
            )

        migration_name = os.path.basename(MIGRATION_FILE).split('.', 1).pop(0)

        subprocess.call(('psql', DBNAME, DBUSER, '-1', '-f', MIGRATION_FILE))


if __name__ == '__main__':
    MigrationRegister()()

## vim: filetype=python