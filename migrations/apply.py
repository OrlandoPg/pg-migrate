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

    parser.add_argument('--dump', action='store_const',
        const=True, dest='dump_schema', default=False,
        help='Also dump the contents of the DB schema into SCHEMA_FILE if successful'
    )


def _up_from ( DBNAME, DBUSER, hash ):
    subprocess.check_call(('psql', DBNAME, DBUSER, '-1xtc',
        '''SELECT 'up from %(hash)s' AS "direction" FROM "migrations"."migrate" ('%(hash)s', 'UP');''' % locals()
    ))


def _down_to ( DBNAME, DBUSER, hash ):
    subprocess.check_call(('psql', DBNAME, DBUSER, '-1xtc',
        '''SELECT 'down to %(hash)s' AS "direction" FROM "migrations"."migrate" ('%(hash)s', 'DOWN');''' % locals()
    ))


def _dump_schema ( schema_file, DBNAME, DBUSER ):
    with open(schema_file, 'w') as f:
        output = subprocess.check_output(( 
            ('pg_dump', '-xOsn', 'public', DBNAME) + ('--username', DBUSER) if DBUSER else ()
        )).splitlines(True)

        f.writelines(( line for line in output if not (
            line.startswith(('--', 'SET')) or ('pg_catalog.setval' in line)
        ) ))



def command ( schema_file, migration_path, DBNAME, DBUSER, MIGRATION_NAME, direction, dump_schema, **kwargs ):
    schema_file, migration_path = map(base.path, (schema_file, migration_path))

    for search in (migration_path, 'migration_', '.pg.sql'):
        MIGRATION_NAME = MIGRATION_NAME.replace(search, '')

    args = (DBNAME, DBUSER, MIGRATION_NAME)

    _up_from(*args) if direction else _down_to(*args)

    if dump_schema: _dump_schema(schema_file, DBNAME, DBUSER)

