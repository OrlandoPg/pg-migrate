#!/usr/bin/env python2.7

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
""",
    'DOWN' : 'DROP SCHEMA "migrations" CASCADE;'
}

class MigrationInit(base.MigrationCommand):
    def main ( self, uninstall, DBNAME, DBUSER, **kwargs ):
        migration = MIGRATION_SCHEMA['DOWN'] if uninstall else MIGRATION_SCHEMA['UP']

        subprocess.call(('psql', DBNAME, DBUSER, '-1', '-c', migration))


if __name__ == '__main__':
    command = MigrationInit(
    ).add_argument('--uninstall', action='store_true', help='uninstall the migrations schema instead'
    ).with_psql_arguments(
    )

    command()

# vim: filetype=python