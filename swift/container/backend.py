begin_unit
comment|'# Copyright (c) 2010-2012 OpenStack Foundation'
nl|'\n'
comment|'#'
nl|'\n'
comment|'# Licensed under the Apache License, Version 2.0 (the "License");'
nl|'\n'
comment|'# you may not use this file except in compliance with the License.'
nl|'\n'
comment|'# You may obtain a copy of the License at'
nl|'\n'
comment|'#'
nl|'\n'
comment|'#    http://www.apache.org/licenses/LICENSE-2.0'
nl|'\n'
comment|'#'
nl|'\n'
comment|'# Unless required by applicable law or agreed to in writing, software'
nl|'\n'
comment|'# distributed under the License is distributed on an "AS IS" BASIS,'
nl|'\n'
comment|'# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'
nl|'\n'
comment|'# See the License for the specific language governing permissions and'
nl|'\n'
comment|'# limitations under the License.'
nl|'\n'
nl|'\n'
string|'"""\nPluggable Back-ends for Container Server\n"""'
newline|'\n'
nl|'\n'
name|'import'
name|'os'
newline|'\n'
name|'from'
name|'uuid'
name|'import'
name|'uuid4'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'cPickle'
name|'as'
name|'pickle'
newline|'\n'
name|'import'
name|'errno'
newline|'\n'
nl|'\n'
name|'import'
name|'sqlite3'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'normalize_timestamp'
op|','
name|'lock_parent_directory'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'db'
name|'import'
name|'DatabaseBroker'
op|','
name|'DatabaseConnectionError'
op|','
name|'PENDING_CAP'
op|','
name|'PICKLE_PROTOCOL'
op|','
name|'utf8encode'
newline|'\n'
nl|'\n'
DECL|variable|DATADIR
name|'DATADIR'
op|'='
string|"'containers'"
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ContainerBroker
name|'class'
name|'ContainerBroker'
op|'('
name|'DatabaseBroker'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Encapsulates working with a container database."""'
newline|'\n'
DECL|variable|db_type
name|'db_type'
op|'='
string|"'container'"
newline|'\n'
DECL|variable|db_contains_type
name|'db_contains_type'
op|'='
string|"'object'"
newline|'\n'
DECL|variable|db_reclaim_timestamp
name|'db_reclaim_timestamp'
op|'='
string|"'created_at'"
newline|'\n'
nl|'\n'
DECL|member|_initialize
name|'def'
name|'_initialize'
op|'('
name|'self'
op|','
name|'conn'
op|','
name|'put_timestamp'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Create a brand new container database (tables, indices, triggers, etc.)\n        """'
newline|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'account'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'ValueError'
op|'('
nl|'\n'
string|"'Attempting to create a new database with no account set'"
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'self'
op|'.'
name|'container'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'ValueError'
op|'('
nl|'\n'
string|"'Attempting to create a new database with no container set'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'create_object_table'
op|'('
name|'conn'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'create_container_stat_table'
op|'('
name|'conn'
op|','
name|'put_timestamp'
op|')'
newline|'\n'
nl|'\n'
DECL|member|create_object_table
dedent|''
name|'def'
name|'create_object_table'
op|'('
name|'self'
op|','
name|'conn'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Create the object table which is specific to the container DB.\n        Not a part of Pluggable Back-ends, internal to the baseline code.\n\n        :param conn: DB connection object\n        """'
newline|'\n'
name|'conn'
op|'.'
name|'executescript'
op|'('
string|'"""\n            CREATE TABLE object (\n                ROWID INTEGER PRIMARY KEY AUTOINCREMENT,\n                name TEXT,\n                created_at TEXT,\n                size INTEGER,\n                content_type TEXT,\n                etag TEXT,\n                deleted INTEGER DEFAULT 0\n            );\n\n            CREATE INDEX ix_object_deleted_name ON object (deleted, name);\n\n            CREATE TRIGGER object_insert AFTER INSERT ON object\n            BEGIN\n                UPDATE container_stat\n                SET object_count = object_count + (1 - new.deleted),\n                    bytes_used = bytes_used + new.size,\n                    hash = chexor(hash, new.name, new.created_at);\n            END;\n\n            CREATE TRIGGER object_update BEFORE UPDATE ON object\n            BEGIN\n                SELECT RAISE(FAIL, \'UPDATE not allowed; DELETE and INSERT\');\n            END;\n\n            CREATE TRIGGER object_delete AFTER DELETE ON object\n            BEGIN\n                UPDATE container_stat\n                SET object_count = object_count - (1 - old.deleted),\n                    bytes_used = bytes_used - old.size,\n                    hash = chexor(hash, old.name, old.created_at);\n            END;\n        """'
op|')'
newline|'\n'
nl|'\n'
DECL|member|create_container_stat_table
dedent|''
name|'def'
name|'create_container_stat_table'
op|'('
name|'self'
op|','
name|'conn'
op|','
name|'put_timestamp'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Create the container_stat table which is specific to the container DB.\n        Not a part of Pluggable Back-ends, internal to the baseline code.\n\n        :param conn: DB connection object\n        :param put_timestamp: put timestamp\n        """'
newline|'\n'
name|'if'
name|'put_timestamp'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'put_timestamp'
op|'='
name|'normalize_timestamp'
op|'('
number|'0'
op|')'
newline|'\n'
dedent|''
name|'conn'
op|'.'
name|'executescript'
op|'('
string|'"""\n            CREATE TABLE container_stat (\n                account TEXT,\n                container TEXT,\n                created_at TEXT,\n                put_timestamp TEXT DEFAULT \'0\',\n                delete_timestamp TEXT DEFAULT \'0\',\n                object_count INTEGER,\n                bytes_used INTEGER,\n                reported_put_timestamp TEXT DEFAULT \'0\',\n                reported_delete_timestamp TEXT DEFAULT \'0\',\n                reported_object_count INTEGER DEFAULT 0,\n                reported_bytes_used INTEGER DEFAULT 0,\n                hash TEXT default \'00000000000000000000000000000000\',\n                id TEXT,\n                status TEXT DEFAULT \'\',\n                status_changed_at TEXT DEFAULT \'0\',\n                metadata TEXT DEFAULT \'\',\n                x_container_sync_point1 INTEGER DEFAULT -1,\n                x_container_sync_point2 INTEGER DEFAULT -1\n            );\n\n            INSERT INTO container_stat (object_count, bytes_used)\n                VALUES (0, 0);\n        """'
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n            UPDATE container_stat\n            SET account = ?, container = ?, created_at = ?, id = ?,\n                put_timestamp = ?\n        '''"
op|','
op|'('
name|'self'
op|'.'
name|'account'
op|','
name|'self'
op|'.'
name|'container'
op|','
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|','
nl|'\n'
name|'str'
op|'('
name|'uuid4'
op|'('
op|')'
op|')'
op|','
name|'put_timestamp'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_db_version
dedent|''
name|'def'
name|'get_db_version'
op|'('
name|'self'
op|','
name|'conn'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'self'
op|'.'
name|'_db_version'
op|'=='
op|'-'
number|'1'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_db_version'
op|'='
number|'0'
newline|'\n'
name|'for'
name|'row'
name|'in'
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n                    SELECT name FROM sqlite_master\n                    WHERE name = 'ix_object_deleted_name' '''"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'_db_version'
op|'='
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'self'
op|'.'
name|'_db_version'
newline|'\n'
nl|'\n'
DECL|member|_newid
dedent|''
name|'def'
name|'_newid'
op|'('
name|'self'
op|','
name|'conn'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n            UPDATE container_stat\n            SET reported_put_timestamp = 0, reported_delete_timestamp = 0,\n                reported_object_count = 0, reported_bytes_used = 0'''"
op|')'
newline|'\n'
nl|'\n'
DECL|member|_delete_db
dedent|''
name|'def'
name|'_delete_db'
op|'('
name|'self'
op|','
name|'conn'
op|','
name|'timestamp'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Mark the DB as deleted\n\n        :param conn: DB connection object\n        :param timestamp: timestamp to mark as deleted\n        """'
newline|'\n'
name|'conn'
op|'.'
name|'execute'
op|'('
string|'"""\n            UPDATE container_stat\n            SET delete_timestamp = ?,\n                status = \'DELETED\',\n                status_changed_at = ?\n            WHERE delete_timestamp < ? """'
op|','
op|'('
name|'timestamp'
op|','
name|'timestamp'
op|','
name|'timestamp'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_commit_puts_load
dedent|''
name|'def'
name|'_commit_puts_load'
op|'('
name|'self'
op|','
name|'item_list'
op|','
name|'entry'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""See :func:`swift.common.db.DatabaseBroker._commit_puts_load`"""'
newline|'\n'
op|'('
name|'name'
op|','
name|'timestamp'
op|','
name|'size'
op|','
name|'content_type'
op|','
name|'etag'
op|','
name|'deleted'
op|')'
op|'='
name|'pickle'
op|'.'
name|'loads'
op|'('
name|'entry'
op|'.'
name|'decode'
op|'('
string|"'base64'"
op|')'
op|')'
newline|'\n'
name|'item_list'
op|'.'
name|'append'
op|'('
op|'{'
string|"'name'"
op|':'
name|'name'
op|','
nl|'\n'
string|"'created_at'"
op|':'
name|'timestamp'
op|','
nl|'\n'
string|"'size'"
op|':'
name|'size'
op|','
nl|'\n'
string|"'content_type'"
op|':'
name|'content_type'
op|','
nl|'\n'
string|"'etag'"
op|':'
name|'etag'
op|','
nl|'\n'
string|"'deleted'"
op|':'
name|'deleted'
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|member|empty
dedent|''
name|'def'
name|'empty'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Check if container DB is empty.\n\n        :returns: True if the database has no active objects, False otherwise\n        """'
newline|'\n'
name|'self'
op|'.'
name|'_commit_puts_stale_ok'
op|'('
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'get'
op|'('
op|')'
name|'as'
name|'conn'
op|':'
newline|'\n'
indent|'            '
name|'row'
op|'='
name|'conn'
op|'.'
name|'execute'
op|'('
nl|'\n'
string|"'SELECT object_count from container_stat'"
op|')'
op|'.'
name|'fetchone'
op|'('
op|')'
newline|'\n'
name|'return'
op|'('
name|'row'
op|'['
number|'0'
op|']'
op|'=='
number|'0'
op|')'
newline|'\n'
nl|'\n'
DECL|member|delete_object
dedent|''
dedent|''
name|'def'
name|'delete_object'
op|'('
name|'self'
op|','
name|'name'
op|','
name|'timestamp'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Mark an object deleted.\n\n        :param name: object name to be deleted\n        :param timestamp: timestamp when the object was marked as deleted\n        """'
newline|'\n'
name|'self'
op|'.'
name|'put_object'
op|'('
name|'name'
op|','
name|'timestamp'
op|','
number|'0'
op|','
string|"'application/deleted'"
op|','
string|"'noetag'"
op|','
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|put_object
dedent|''
name|'def'
name|'put_object'
op|'('
name|'self'
op|','
name|'name'
op|','
name|'timestamp'
op|','
name|'size'
op|','
name|'content_type'
op|','
name|'etag'
op|','
name|'deleted'
op|'='
number|'0'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Creates an object in the DB with its metadata.\n\n        :param name: object name to be created\n        :param timestamp: timestamp of when the object was created\n        :param size: object size\n        :param content_type: object content-type\n        :param etag: object etag\n        :param deleted: if True, marks the object as deleted and sets the\n                        deteleted_at timestamp to timestamp\n        """'
newline|'\n'
name|'record'
op|'='
op|'{'
string|"'name'"
op|':'
name|'name'
op|','
string|"'created_at'"
op|':'
name|'timestamp'
op|','
string|"'size'"
op|':'
name|'size'
op|','
nl|'\n'
string|"'content_type'"
op|':'
name|'content_type'
op|','
string|"'etag'"
op|':'
name|'etag'
op|','
nl|'\n'
string|"'deleted'"
op|':'
name|'deleted'
op|'}'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'db_file'
op|'=='
string|"':memory:'"
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'merge_items'
op|'('
op|'['
name|'record'
op|']'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'self'
op|'.'
name|'db_file'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'DatabaseConnectionError'
op|'('
name|'self'
op|'.'
name|'db_file'
op|','
string|'"DB doesn\'t exist"'
op|')'
newline|'\n'
dedent|''
name|'pending_size'
op|'='
number|'0'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'pending_size'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'getsize'
op|'('
name|'self'
op|'.'
name|'pending_file'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'OSError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'err'
op|'.'
name|'errno'
op|'!='
name|'errno'
op|'.'
name|'ENOENT'
op|':'
newline|'\n'
indent|'                '
name|'raise'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'pending_size'
op|'>'
name|'PENDING_CAP'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_commit_puts'
op|'('
op|'['
name|'record'
op|']'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'lock_parent_directory'
op|'('
name|'self'
op|'.'
name|'pending_file'
op|','
nl|'\n'
name|'self'
op|'.'
name|'pending_timeout'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'with'
name|'open'
op|'('
name|'self'
op|'.'
name|'pending_file'
op|','
string|"'a+b'"
op|')'
name|'as'
name|'fp'
op|':'
newline|'\n'
comment|"# Colons aren't used in base64 encoding; so they are our"
nl|'\n'
comment|'# delimiter'
nl|'\n'
indent|'                    '
name|'fp'
op|'.'
name|'write'
op|'('
string|"':'"
op|')'
newline|'\n'
name|'fp'
op|'.'
name|'write'
op|'('
name|'pickle'
op|'.'
name|'dumps'
op|'('
nl|'\n'
op|'('
name|'name'
op|','
name|'timestamp'
op|','
name|'size'
op|','
name|'content_type'
op|','
name|'etag'
op|','
name|'deleted'
op|')'
op|','
nl|'\n'
name|'protocol'
op|'='
name|'PICKLE_PROTOCOL'
op|')'
op|'.'
name|'encode'
op|'('
string|"'base64'"
op|')'
op|')'
newline|'\n'
name|'fp'
op|'.'
name|'flush'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|is_deleted
dedent|''
dedent|''
dedent|''
dedent|''
name|'def'
name|'is_deleted'
op|'('
name|'self'
op|','
name|'timestamp'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Check if the DB is considered to be deleted.\n\n        :returns: True if the DB is considered to be deleted, False otherwise\n        """'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'db_file'
op|'!='
string|"':memory:'"
name|'and'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'self'
op|'.'
name|'db_file'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'True'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'_commit_puts_stale_ok'
op|'('
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'get'
op|'('
op|')'
name|'as'
name|'conn'
op|':'
newline|'\n'
indent|'            '
name|'row'
op|'='
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n                SELECT put_timestamp, delete_timestamp, object_count\n                FROM container_stat'''"
op|')'
op|'.'
name|'fetchone'
op|'('
op|')'
newline|'\n'
comment|'# leave this db as a tombstone for a consistency window'
nl|'\n'
name|'if'
name|'timestamp'
name|'and'
name|'row'
op|'['
string|"'delete_timestamp'"
op|']'
op|'>'
name|'timestamp'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'False'
newline|'\n'
comment|'# The container is considered deleted if the delete_timestamp'
nl|'\n'
comment|'# value is greater than the put_timestamp, and there are no'
nl|'\n'
comment|'# objects in the container.'
nl|'\n'
dedent|''
name|'return'
op|'('
name|'row'
op|'['
string|"'object_count'"
op|']'
name|'in'
op|'('
name|'None'
op|','
string|"''"
op|','
number|'0'
op|','
string|"'0'"
op|')'
op|')'
name|'and'
op|'('
name|'float'
op|'('
name|'row'
op|'['
string|"'delete_timestamp'"
op|']'
op|')'
op|'>'
name|'float'
op|'('
name|'row'
op|'['
string|"'put_timestamp'"
op|']'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_info
dedent|''
dedent|''
name|'def'
name|'get_info'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Get global data for the container.\n\n        :returns: dict with keys: account, container, created_at,\n                  put_timestamp, delete_timestamp, object_count, bytes_used,\n                  reported_put_timestamp, reported_delete_timestamp,\n                  reported_object_count, reported_bytes_used, hash, id,\n                  x_container_sync_point1, and x_container_sync_point2.\n        """'
newline|'\n'
name|'self'
op|'.'
name|'_commit_puts_stale_ok'
op|'('
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'get'
op|'('
op|')'
name|'as'
name|'conn'
op|':'
newline|'\n'
indent|'            '
name|'data'
op|'='
name|'None'
newline|'\n'
name|'trailing'
op|'='
string|"'x_container_sync_point1, x_container_sync_point2'"
newline|'\n'
name|'while'
name|'not'
name|'data'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'data'
op|'='
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n                        SELECT account, container, created_at, put_timestamp,\n                            delete_timestamp, object_count, bytes_used,\n                            reported_put_timestamp, reported_delete_timestamp,\n                            reported_object_count, reported_bytes_used, hash,\n                            id, %s\n                        FROM container_stat\n                    '''"
op|'%'
op|'('
name|'trailing'
op|','
op|')'
op|')'
op|'.'
name|'fetchone'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'sqlite3'
op|'.'
name|'OperationalError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                    '
name|'if'
string|"'no such column: x_container_sync_point'"
name|'in'
name|'str'
op|'('
name|'err'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'trailing'
op|'='
string|"'-1 AS x_container_sync_point1, '"
string|"'-1 AS x_container_sync_point2'"
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'raise'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'data'
op|'='
name|'dict'
op|'('
name|'data'
op|')'
newline|'\n'
name|'return'
name|'data'
newline|'\n'
nl|'\n'
DECL|member|set_x_container_sync_points
dedent|''
dedent|''
name|'def'
name|'set_x_container_sync_points'
op|'('
name|'self'
op|','
name|'sync_point1'
op|','
name|'sync_point2'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'with'
name|'self'
op|'.'
name|'get'
op|'('
op|')'
name|'as'
name|'conn'
op|':'
newline|'\n'
indent|'            '
name|'orig_isolation_level'
op|'='
name|'conn'
op|'.'
name|'isolation_level'
newline|'\n'
name|'try'
op|':'
newline|'\n'
comment|'# We turn off auto-transactions to ensure the alter table'
nl|'\n'
comment|'# commands are part of the transaction.'
nl|'\n'
indent|'                '
name|'conn'
op|'.'
name|'isolation_level'
op|'='
name|'None'
newline|'\n'
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'BEGIN'"
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'_set_x_container_sync_points'
op|'('
name|'conn'
op|','
name|'sync_point1'
op|','
nl|'\n'
name|'sync_point2'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'sqlite3'
op|'.'
name|'OperationalError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                    '
name|'if'
string|"'no such column: x_container_sync_point'"
name|'not'
name|'in'
name|'str'
op|'('
name|'err'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'raise'
newline|'\n'
dedent|''
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n                        ALTER TABLE container_stat\n                        ADD COLUMN x_container_sync_point1 INTEGER DEFAULT -1\n                    '''"
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n                        ALTER TABLE container_stat\n                        ADD COLUMN x_container_sync_point2 INTEGER DEFAULT -1\n                    '''"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_set_x_container_sync_points'
op|'('
name|'conn'
op|','
name|'sync_point1'
op|','
nl|'\n'
name|'sync_point2'
op|')'
newline|'\n'
dedent|''
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'COMMIT'"
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'                '
name|'conn'
op|'.'
name|'isolation_level'
op|'='
name|'orig_isolation_level'
newline|'\n'
nl|'\n'
DECL|member|_set_x_container_sync_points
dedent|''
dedent|''
dedent|''
name|'def'
name|'_set_x_container_sync_points'
op|'('
name|'self'
op|','
name|'conn'
op|','
name|'sync_point1'
op|','
name|'sync_point2'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'sync_point1'
name|'is'
name|'not'
name|'None'
name|'and'
name|'sync_point2'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n                UPDATE container_stat\n                SET x_container_sync_point1 = ?,\n                    x_container_sync_point2 = ?\n            '''"
op|','
op|'('
name|'sync_point1'
op|','
name|'sync_point2'
op|')'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'sync_point1'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n                UPDATE container_stat\n                SET x_container_sync_point1 = ?\n            '''"
op|','
op|'('
name|'sync_point1'
op|','
op|')'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'sync_point2'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n                UPDATE container_stat\n                SET x_container_sync_point2 = ?\n            '''"
op|','
op|'('
name|'sync_point2'
op|','
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|reported
dedent|''
dedent|''
name|'def'
name|'reported'
op|'('
name|'self'
op|','
name|'put_timestamp'
op|','
name|'delete_timestamp'
op|','
name|'object_count'
op|','
nl|'\n'
name|'bytes_used'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Update reported stats, available with container\'s `get_info`.\n\n        :param put_timestamp: put_timestamp to update\n        :param delete_timestamp: delete_timestamp to update\n        :param object_count: object_count to update\n        :param bytes_used: bytes_used to update\n        """'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'get'
op|'('
op|')'
name|'as'
name|'conn'
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n                UPDATE container_stat\n                SET reported_put_timestamp = ?, reported_delete_timestamp = ?,\n                    reported_object_count = ?, reported_bytes_used = ?\n            '''"
op|','
op|'('
name|'put_timestamp'
op|','
name|'delete_timestamp'
op|','
name|'object_count'
op|','
name|'bytes_used'
op|')'
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'commit'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|list_objects_iter
dedent|''
dedent|''
name|'def'
name|'list_objects_iter'
op|'('
name|'self'
op|','
name|'limit'
op|','
name|'marker'
op|','
name|'end_marker'
op|','
name|'prefix'
op|','
name|'delimiter'
op|','
nl|'\n'
name|'path'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Get a list of objects sorted by name starting at marker onward, up\n        to limit entries.  Entries will begin with the prefix and will not\n        have the delimiter after the prefix.\n\n        :param limit: maximum number of entries to get\n        :param marker: marker query\n        :param end_marker: end marker query\n        :param prefix: prefix query\n        :param delimiter: delimiter for query\n        :param path: if defined, will set the prefix and delimter based on\n                     the path\n\n        :returns: list of tuples of (name, created_at, size, content_type,\n                  etag)\n        """'
newline|'\n'
name|'delim_force_gte'
op|'='
name|'False'
newline|'\n'
op|'('
name|'marker'
op|','
name|'end_marker'
op|','
name|'prefix'
op|','
name|'delimiter'
op|','
name|'path'
op|')'
op|'='
name|'utf8encode'
op|'('
nl|'\n'
name|'marker'
op|','
name|'end_marker'
op|','
name|'prefix'
op|','
name|'delimiter'
op|','
name|'path'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_commit_puts_stale_ok'
op|'('
op|')'
newline|'\n'
name|'if'
name|'path'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'prefix'
op|'='
name|'path'
newline|'\n'
name|'if'
name|'path'
op|':'
newline|'\n'
indent|'                '
name|'prefix'
op|'='
name|'path'
op|'='
name|'path'
op|'.'
name|'rstrip'
op|'('
string|"'/'"
op|')'
op|'+'
string|"'/'"
newline|'\n'
dedent|''
name|'delimiter'
op|'='
string|"'/'"
newline|'\n'
dedent|''
name|'elif'
name|'delimiter'
name|'and'
name|'not'
name|'prefix'
op|':'
newline|'\n'
indent|'            '
name|'prefix'
op|'='
string|"''"
newline|'\n'
dedent|''
name|'orig_marker'
op|'='
name|'marker'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'get'
op|'('
op|')'
name|'as'
name|'conn'
op|':'
newline|'\n'
indent|'            '
name|'results'
op|'='
op|'['
op|']'
newline|'\n'
name|'while'
name|'len'
op|'('
name|'results'
op|')'
op|'<'
name|'limit'
op|':'
newline|'\n'
indent|'                '
name|'query'
op|'='
string|"'''SELECT name, created_at, size, content_type, etag\n                           FROM object WHERE'''"
newline|'\n'
name|'query_args'
op|'='
op|'['
op|']'
newline|'\n'
name|'if'
name|'end_marker'
op|':'
newline|'\n'
indent|'                    '
name|'query'
op|'+='
string|"' name < ? AND'"
newline|'\n'
name|'query_args'
op|'.'
name|'append'
op|'('
name|'end_marker'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'delim_force_gte'
op|':'
newline|'\n'
indent|'                    '
name|'query'
op|'+='
string|"' name >= ? AND'"
newline|'\n'
name|'query_args'
op|'.'
name|'append'
op|'('
name|'marker'
op|')'
newline|'\n'
comment|'# Always set back to False'
nl|'\n'
name|'delim_force_gte'
op|'='
name|'False'
newline|'\n'
dedent|''
name|'elif'
name|'marker'
name|'and'
name|'marker'
op|'>='
name|'prefix'
op|':'
newline|'\n'
indent|'                    '
name|'query'
op|'+='
string|"' name > ? AND'"
newline|'\n'
name|'query_args'
op|'.'
name|'append'
op|'('
name|'marker'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'prefix'
op|':'
newline|'\n'
indent|'                    '
name|'query'
op|'+='
string|"' name >= ? AND'"
newline|'\n'
name|'query_args'
op|'.'
name|'append'
op|'('
name|'prefix'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'get_db_version'
op|'('
name|'conn'
op|')'
op|'<'
number|'1'
op|':'
newline|'\n'
indent|'                    '
name|'query'
op|'+='
string|"' +deleted = 0'"
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'query'
op|'+='
string|"' deleted = 0'"
newline|'\n'
dedent|''
name|'query'
op|'+='
string|"' ORDER BY name LIMIT ?'"
newline|'\n'
name|'query_args'
op|'.'
name|'append'
op|'('
name|'limit'
op|'-'
name|'len'
op|'('
name|'results'
op|')'
op|')'
newline|'\n'
name|'curs'
op|'='
name|'conn'
op|'.'
name|'execute'
op|'('
name|'query'
op|','
name|'query_args'
op|')'
newline|'\n'
name|'curs'
op|'.'
name|'row_factory'
op|'='
name|'None'
newline|'\n'
nl|'\n'
name|'if'
name|'prefix'
name|'is'
name|'None'
op|':'
newline|'\n'
comment|'# A delimiter without a specified prefix is ignored'
nl|'\n'
indent|'                    '
name|'return'
op|'['
name|'r'
name|'for'
name|'r'
name|'in'
name|'curs'
op|']'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'delimiter'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'not'
name|'prefix'
op|':'
newline|'\n'
comment|'# It is possible to have a delimiter but no prefix'
nl|'\n'
comment|'# specified. As above, the prefix will be set to the'
nl|'\n'
comment|'# empty string, so avoid performing the extra work to'
nl|'\n'
comment|'# check against an empty prefix.'
nl|'\n'
indent|'                        '
name|'return'
op|'['
name|'r'
name|'for'
name|'r'
name|'in'
name|'curs'
op|']'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'return'
op|'['
name|'r'
name|'for'
name|'r'
name|'in'
name|'curs'
name|'if'
name|'r'
op|'['
number|'0'
op|']'
op|'.'
name|'startswith'
op|'('
name|'prefix'
op|')'
op|']'
newline|'\n'
nl|'\n'
comment|'# We have a delimiter and a prefix (possibly empty string) to'
nl|'\n'
comment|'# handle'
nl|'\n'
dedent|''
dedent|''
name|'rowcount'
op|'='
number|'0'
newline|'\n'
name|'for'
name|'row'
name|'in'
name|'curs'
op|':'
newline|'\n'
indent|'                    '
name|'rowcount'
op|'+='
number|'1'
newline|'\n'
name|'marker'
op|'='
name|'name'
op|'='
name|'row'
op|'['
number|'0'
op|']'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'results'
op|')'
op|'>='
name|'limit'
name|'or'
name|'not'
name|'name'
op|'.'
name|'startswith'
op|'('
name|'prefix'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'curs'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
name|'return'
name|'results'
newline|'\n'
dedent|''
name|'end'
op|'='
name|'name'
op|'.'
name|'find'
op|'('
name|'delimiter'
op|','
name|'len'
op|'('
name|'prefix'
op|')'
op|')'
newline|'\n'
name|'if'
name|'path'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'                        '
name|'if'
name|'name'
op|'=='
name|'path'
op|':'
newline|'\n'
indent|'                            '
name|'continue'
newline|'\n'
dedent|''
name|'if'
name|'end'
op|'>='
number|'0'
name|'and'
name|'len'
op|'('
name|'name'
op|')'
op|'>'
name|'end'
op|'+'
name|'len'
op|'('
name|'delimiter'
op|')'
op|':'
newline|'\n'
indent|'                            '
name|'marker'
op|'='
name|'name'
op|'['
op|':'
name|'end'
op|']'
op|'+'
name|'chr'
op|'('
name|'ord'
op|'('
name|'delimiter'
op|')'
op|'+'
number|'1'
op|')'
newline|'\n'
name|'curs'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'elif'
name|'end'
op|'>'
number|'0'
op|':'
newline|'\n'
indent|'                        '
name|'marker'
op|'='
name|'name'
op|'['
op|':'
name|'end'
op|']'
op|'+'
name|'chr'
op|'('
name|'ord'
op|'('
name|'delimiter'
op|')'
op|'+'
number|'1'
op|')'
newline|'\n'
comment|'# we want result to be inclusinve of delim+1'
nl|'\n'
name|'delim_force_gte'
op|'='
name|'True'
newline|'\n'
name|'dir_name'
op|'='
name|'name'
op|'['
op|':'
name|'end'
op|'+'
number|'1'
op|']'
newline|'\n'
name|'if'
name|'dir_name'
op|'!='
name|'orig_marker'
op|':'
newline|'\n'
indent|'                            '
name|'results'
op|'.'
name|'append'
op|'('
op|'['
name|'dir_name'
op|','
string|"'0'"
op|','
number|'0'
op|','
name|'None'
op|','
string|"''"
op|']'
op|')'
newline|'\n'
dedent|''
name|'curs'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
name|'results'
op|'.'
name|'append'
op|'('
name|'row'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'rowcount'
op|':'
newline|'\n'
indent|'                    '
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'results'
newline|'\n'
nl|'\n'
DECL|member|merge_items
dedent|''
dedent|''
name|'def'
name|'merge_items'
op|'('
name|'self'
op|','
name|'item_list'
op|','
name|'source'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Merge items into the object table.\n\n        :param item_list: list of dictionaries of {\'name\', \'created_at\',\n                          \'size\', \'content_type\', \'etag\', \'deleted\'}\n        :param source: if defined, update incoming_sync with the source\n        """'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'get'
op|'('
op|')'
name|'as'
name|'conn'
op|':'
newline|'\n'
indent|'            '
name|'max_rowid'
op|'='
op|'-'
number|'1'
newline|'\n'
name|'for'
name|'rec'
name|'in'
name|'item_list'
op|':'
newline|'\n'
indent|'                '
name|'query'
op|'='
string|"'''\n                    DELETE FROM object\n                    WHERE name = ? AND (created_at < ?)\n                '''"
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'get_db_version'
op|'('
name|'conn'
op|')'
op|'>='
number|'1'
op|':'
newline|'\n'
indent|'                    '
name|'query'
op|'+='
string|"' AND deleted IN (0, 1)'"
newline|'\n'
dedent|''
name|'conn'
op|'.'
name|'execute'
op|'('
name|'query'
op|','
op|'('
name|'rec'
op|'['
string|"'name'"
op|']'
op|','
name|'rec'
op|'['
string|"'created_at'"
op|']'
op|')'
op|')'
newline|'\n'
name|'query'
op|'='
string|"'SELECT 1 FROM object WHERE name = ?'"
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'get_db_version'
op|'('
name|'conn'
op|')'
op|'>='
number|'1'
op|':'
newline|'\n'
indent|'                    '
name|'query'
op|'+='
string|"' AND deleted IN (0, 1)'"
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'conn'
op|'.'
name|'execute'
op|'('
name|'query'
op|','
op|'('
name|'rec'
op|'['
string|"'name'"
op|']'
op|','
op|')'
op|')'
op|'.'
name|'fetchall'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n                        INSERT INTO object (name, created_at, size,\n                            content_type, etag, deleted)\n                        VALUES (?, ?, ?, ?, ?, ?)\n                    '''"
op|','
op|'('
op|'['
name|'rec'
op|'['
string|"'name'"
op|']'
op|','
name|'rec'
op|'['
string|"'created_at'"
op|']'
op|','
name|'rec'
op|'['
string|"'size'"
op|']'
op|','
nl|'\n'
name|'rec'
op|'['
string|"'content_type'"
op|']'
op|','
name|'rec'
op|'['
string|"'etag'"
op|']'
op|','
name|'rec'
op|'['
string|"'deleted'"
op|']'
op|']'
op|')'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'source'
op|':'
newline|'\n'
indent|'                    '
name|'max_rowid'
op|'='
name|'max'
op|'('
name|'max_rowid'
op|','
name|'rec'
op|'['
string|"'ROWID'"
op|']'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'source'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n                        INSERT INTO incoming_sync (sync_point, remote_id)\n                        VALUES (?, ?)\n                    '''"
op|','
op|'('
name|'max_rowid'
op|','
name|'source'
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'sqlite3'
op|'.'
name|'IntegrityError'
op|':'
newline|'\n'
indent|'                    '
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n                        UPDATE incoming_sync SET sync_point=max(?, sync_point)\n                        WHERE remote_id=?\n                    '''"
op|','
op|'('
name|'max_rowid'
op|','
name|'source'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'conn'
op|'.'
name|'commit'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
endmarker|''
end_unit
