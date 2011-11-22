#!/usr/bin/env python2.7

import os.path, base


MIGRATION_TEMPLATE = """
    CREATE OR REPLACE FUNCTION %(migration_name)s ( varchar ) RETURNS VOID AS
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


class MigrationCreate(base.MigrationCommand):
    def init_args ( self ):
        super(MigrationCreate, self).init_args(
        ).add_argument('-s', '--schema-file', dest='schema_file', default='etc/schema.pg.sql',
            help='the schema file to mark migrations from, default: etc/schema.pg.sql'
        ).with_migration_path(
        ).with_migration_name(
        ).add_argument('--long-hash', action='store_true',
            help='use the full-length HASH in MIGRATION_NAME if "--migration-name" is not provided'
        ).add_argument('-f', '--force', action='store_true', dest='force',
            help='force overwrite of existing migration file'
        )



    def main ( self, schema_file, migration_path, migration_name, long_hash=False, **kwargs ):
        schema_file, migration_path = map(base.path, (schema_file, migration_path))

        migration_name = migration_name or ('migration_%s' % self.get_HASH(schema_file, long_hash))

        migration_file = os.path.join(migration_path, migration_name + '.pg.sql')

        if os.path.exists(migration_file) and not kwargs['force']:
            raise Exception, 'Existing migration file: %s (use --force to overwrite)' % migration_file

        with open(migration_file, 'w') as f:
            f.write(MIGRATION_TEMPLATE % locals())


if __name__ == '__main__':
    MigrationCreate()()

## vim: filetype=python