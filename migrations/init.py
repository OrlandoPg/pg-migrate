"""
Initialize the "migrations" schema.
"""

import base, subprocess


MIGRATION_SCHEMA = {
    'UP' : """
CREATE SCHEMA "migrations";

CREATE TABLE "migrations"."history" (
    "migration_id" serial PRIMARY KEY,
    "next_migration_id" int DEFAULT NULL,
    "hash" varchar NOT NULL UNIQUE,
    "applied" boolean DEFAULT false,
    FOREIGN KEY ( "next_migration_id" ) REFERENCES
        "migrations"."history" ( "migration_id" )
);

CREATE INDEX "history_migration_id_idx" ON "migrations"."history" ( "migration_id" DESC );

CREATE INDEX "history_next_migration_id_idx" ON "migrations"."history" ( "next_migration_id" DESC NULLS FIRST );

CREATE INDEX "history_applied_idx" ON "migrations"."history" ( "applied" );

CREATE OR REPLACE FUNCTION "migrations"."migrate" ( _hash varchar, varchar ) RETURNS VOID AS
$BODY$
DECLARE
    _HISTORY_ varchar := '"migrations"."history"';

    _direction varchar := UPPER($2);
    _migration varchar := '"migrations"."migration_' || _hash || '"';

    _migration_id int; _old_tail_id int; _new_tail_id int;
BEGIN
    -- Always execute the "_migration" in the specified "_direction"...
    EXECUTE 'SELECT 1 FROM ' || _migration || ' ( $1 )' USING _direction;

    -- Determine if the "_hash" has already been registered...
    EXECUTE 'SELECT "migration_id" FROM ' || _HISTORY_ || ' WHERE "hash" = $1 FOR UPDATE'
        INTO _migration_id USING _hash;

    CASE
        WHEN _migration_id IS NOT NULL THEN
            EXECUTE 'UPDATE ' || _HISTORY_ || ' SET "applied" = $2 ' ||
                'WHERE "migration_id" = $1'
            USING _migration_id, CASE
                WHEN _direction = 'UP' THEN true
                WHEN _direction = 'DOWN' THEN false
            END;

        WHEN _migration_id IS NULL AND _direction = 'UP' THEN
            -- TODO: Move into INSERT trigger on "migrations"."history"...?
            EXECUTE 'SELECT "migration_id" FROM ' || _HISTORY_ ||
                ' WHERE "next_migration_id" IS NULL FOR UPDATE'
            INTO _old_tail_id;

            EXECUTE 'INSERT INTO ' || _HISTORY_ || ' ( "hash", "applied" ) ' ||
                'VALUES ( $1, true ) RETURNING "migration_id"'
            INTO _new_tail_id
            USING _hash;

            EXECUTE 'UPDATE ' || _HISTORY_ || ' SET "next_migration_id" = $1 ' ||
                'WHERE "migration_id" = $2'
            USING _new_tail_id, _old_tail_id;
    END CASE;
END;
$BODY$
LANGUAGE plpgsql;

""",
    'DOWN' : 'DROP SCHEMA "migrations" CASCADE;'
}


@base.chain_parser
def parser ( parser ):
    base.with_psql_arguments(
        parser
    ).add_argument('--uninstall', action='store_true',
        help='uninstall the migrations schema instead'
    )

    return parser


def command ( uninstall, DBNAME, DBUSER, **kwargs ):
    migration = (
        MIGRATION_SCHEMA['DOWN'] if uninstall else MIGRATION_SCHEMA['UP']
    )

    subprocess.call(('psql', DBNAME, DBUSER, '-1', '-c', migration))

