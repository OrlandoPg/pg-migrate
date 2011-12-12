import os.path, sys, hashlib, importlib

MIGRATION_EXTENSION = '.pg.sql'


def path ( *paths ):
    path = os.path.join(*paths)

    abspath = os.path.abspath(path)

    if not os.path.exists(abspath): raise IOError(
        'Specified path does not exist: %s' % path
    )

    return abspath


def with_debug ( parser ):
    parser.add_argument('-d', '--debug', action='store_true', dest='debug',
        help='display the full stack trace of errors instead of just the message'
    )


def with_migration_path ( parser ):
    return parser.add_argument('-M', '--migration-path', dest='migration_path', default='etc/migrations/',
        help='the path in which to store migrations, default: etc/migrations/')


def with_schema_file ( parser ):
    return parser.add_argument('-s', '--schema-file', dest='schema_file', default='etc/schema.pg.sql',
        help='the schema file to mark migrations from, default: etc/schema.pg.sql'
    )


def with_migration_name ( parser, **kwargs ):
    defaults = dict(type=str, dest='migration_name',
        help='the name of the migration to create (use the current hash of the schema file by default)'
    )

    defaults.update(kwargs); kwargs = defaults

    return parser.add_argument('-m', '--migration-name', **kwargs)


def with_psql_arguments ( parser ):
    parser.add_argument('DBNAME', nargs='?', default='')
    parser.add_argument('DBUSER', nargs='?', default='')


def get_HASH ( parser, schema_file, long_hash=False ):
    with open(schema_file) as f:
        HASH = hashlib.sha256(f.read()).hexdigest()

        return HASH if long_hash else HASH[0:7]


