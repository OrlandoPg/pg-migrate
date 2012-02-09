"""
Create a new migration file from the current database schema file.
"""

import os.path, base


MIGRATION_TEMPLATE = """
    CREATE OR REPLACE FUNCTION "migrations"."%(migration_name)s" ( varchar ) RETURNS VOID AS
    $BODY$
    DECLARE
        _direction varchar := UPPER($1);
    BEGIN
        CASE
            WHEN _direction = 'UP' THEN
                PERFORM 1; -- TODO: Write UP migration...

            WHEN _direction = 'DOWN' THEN
                PERFORM 1; -- TODO: Write DOWN migration...

        END CASE;
    END;
    $BODY$
    LANGUAGE plpgsql;
"""


@base.chain_parser
def parser ( parser ):
    base.with_schema_file(
    base.with_migration_path(
    base.with_migration_name(
        parser
    )))

    parser.add_argument('--long-hash', action='store_true',
        help='use the full-length HASH in MIGRATION_NAME if "--migration-name" is not provided'
    )

    parser.add_argument('-f', '--force', action='store_true', dest='force',
        help='force overwrite of existing migration file'
    )



def command ( schema_file, migration_path, migration_name, long_hash=False, **kwargs ):
    schema_file, migration_path = map(base.path, (schema_file, migration_path))

    migration_name = migration_name or ('migration_%s' % base.hash(schema_file, long_hash))

    migration_file = os.path.join(
        migration_path, migration_name + base.MIGRATION_EXTENSION
    )

    if os.path.exists(migration_file) and not kwargs['force']:
        raise Exception, 'Existing migration file: %s (use --force to overwrite)' % migration_file

    with open(migration_file, 'w') as f:
        f.write(MIGRATION_TEMPLATE % locals())

    print migration_file

