"""
Register a migration function with the "migrations" schema.
"""

import base, subprocess, os.path


@base.chain_parser
def parser ( parser ):
    base.with_migration_path(
    base.with_psql_arguments(
        parser
    )).add_argument('MIGRATION_FILE',
        help='the path to the migration file to register'
    )


def command ( migration_path, MIGRATION_FILE, DBNAME, DBUSER, **kwargs ):
    migration_path = base.path(migration_path)

    try:
        MIGRATION_FILE = base.path(MIGRATION_FILE)

    except IOError:
        MIGRATION_FILE = base.path(migration_path, MIGRATION_FILE)

    subprocess.call(('psql', DBNAME, DBUSER, '-1', '-f', MIGRATION_FILE))

