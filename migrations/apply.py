#!/usr/bin/env python2.7

import base, subprocess

class MigrationApply(base.MigrationCommand):
    def init_args ( self ):
        super(MigrationApply, self).init_args(
        ).with_schema_file(
        ).with_migration_path(
        ).with_psql_arguments(
        ).add_argument('MIGRATION_NAME',
            help='the name of the migration to apply'
        ).add_argument('-u', '--up-from', action='store_const',
            const=True, dest='direction', default=True,
            help='apply the migration in the "UP" direction'
        ).add_argument('-D', '--down-to', action='store_const',
            const=False, dest='direction',
            help='apply the migration in the "DOWN" direction'
        )


    def up_from ( self, DBNAME, DBUSER, hash ):
        subprocess.call(('psql', DBNAME, DBUSER, '-1c',
            '''SELECT 1 FROM "migrations"."migrate" ('%(hash)s', 'UP');''' % locals()
        ))

        # TODO: Make dumping the schema to file automatic...?
        #subprocess.call(('pg_dump', DBNAME, '-xOsn public') + (('--username', DBUSER) if DBUSER else ( )))


    def down_to ( self, DBNAME, DBUSER, hash ):
        subprocess.call(('psql', DBNAME, DBUSER, '-1c',
            '''SELECT 1 FROM "migrations"."migrate" ('%(hash)', 'DOWN');''' % locals()
        ))


    def main ( self, schema_file, migration_path, DBNAME, DBUSER, MIGRATION_NAME, direction, **kwargs ):
        schema_file, migration_path = map(base.path, (schema_file, migration_path))

        for search in (migration_path, 'migration_', '.pg.sql'):
            MIGRATION_NAME = MIGRATION_NAME.replace(search, '')

        args = (DBNAME, DBUSER, MIGRATION_NAME)

        self.up_from(*args) if direction else self.down_to(*args)


if __name__ == '__main__':
        MigrationApply()()

