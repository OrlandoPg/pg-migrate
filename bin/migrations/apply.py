#!/usr/bin/env python2.7

import base

class MigrationApply(base.MigrationCommand):
    def init_args ( self ):
        super(MigrationApply, self).init_args(
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


    def main ( self, migration_path, DBNAME, DBUSER, direction, **kwargs ):
        print migration_path, DBNAME, DBUSER, direction

if __name__ == '__main__':
        MigrationApply()()

