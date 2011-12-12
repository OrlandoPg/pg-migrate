"""
Apply a migration registered with the database in the "up" or "down" direction.
"""

import base, subprocess


@base.chain_parser
def parser ( parser ):
    base.with_schema_file(
    base.with_migration_path(
    base.with_psql_arguments(
        parser
    )))

    parser.add_argument('MIGRATION_NAME',
        help='the name of the migration to apply'
    )

    parser.add_argument('-u', '--up-from', action='store_const',
        const=True, dest='direction', default=True,
        help='apply the migration in the "UP" direction'
    )

    parser.add_argument('-D', '--down-to', action='store_const',
        const=False, dest='direction',
        help='apply the migration in the "DOWN" direction'
    )


def _up_from ( DBNAME, DBUSER, hash ):
    subprocess.call(('psql', DBNAME, DBUSER, '-1c',
        '''SELECT 1 FROM "migrations"."migrate" ('%(hash)s', 'UP');''' % locals()
    ))


def _down_to ( DBNAME, DBUSER, hash ):
    subprocess.call(('psql', DBNAME, DBUSER, '-1c',
        '''SELECT 1 FROM "migrations"."migrate" ('%(hash)', 'DOWN');''' % locals()
    ))


def command ( schema_file, migration_path, DBNAME, DBUSER, MIGRATION_NAME, direction, **kwargs ):
    schema_file, migration_path = map(base.path, (schema_file, migration_path))

    for search in (migration_path, 'migration_', '.pg.sql'):
        MIGRATION_NAME = MIGRATION_NAME.replace(search, '')

    args = (DBNAME, DBUSER, MIGRATION_NAME)

    _up_from(*args) if direction else _down_to(*args)

