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
string|'"""\nPluggable Back-end for Account Server\n"""'
newline|'\n'
nl|'\n'
name|'from'
name|'uuid'
name|'import'
name|'uuid4'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'six'
op|'.'
name|'moves'
op|'.'
name|'cPickle'
name|'as'
name|'pickle'
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
name|'Timestamp'
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
name|'utf8encode'
newline|'\n'
nl|'\n'
DECL|variable|DATADIR
name|'DATADIR'
op|'='
string|"'accounts'"
newline|'\n'
nl|'\n'
nl|'\n'
name|'POLICY_STAT_TRIGGER_SCRIPT'
op|'='
string|'"""\n    CREATE TRIGGER container_insert_ps AFTER INSERT ON container\n    BEGIN\n        INSERT OR IGNORE INTO policy_stat\n            (storage_policy_index, container_count, object_count, bytes_used)\n            VALUES (new.storage_policy_index, 0, 0, 0);\n        UPDATE policy_stat\n        SET container_count = container_count + (1 - new.deleted),\n            object_count = object_count + new.object_count,\n            bytes_used = bytes_used + new.bytes_used\n        WHERE storage_policy_index = new.storage_policy_index;\n    END;\n    CREATE TRIGGER container_delete_ps AFTER DELETE ON container\n    BEGIN\n        UPDATE policy_stat\n        SET container_count = container_count - (1 - old.deleted),\n            object_count = object_count - old.object_count,\n            bytes_used = bytes_used - old.bytes_used\n        WHERE storage_policy_index = old.storage_policy_index;\n    END;\n\n"""'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|AccountBroker
name|'class'
name|'AccountBroker'
op|'('
name|'DatabaseBroker'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Encapsulates working with an account database."""'
newline|'\n'
DECL|variable|db_type
name|'db_type'
op|'='
string|"'account'"
newline|'\n'
DECL|variable|db_contains_type
name|'db_contains_type'
op|'='
string|"'container'"
newline|'\n'
DECL|variable|db_reclaim_timestamp
name|'db_reclaim_timestamp'
op|'='
string|"'delete_timestamp'"
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
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Create a brand new account database (tables, indices, triggers, etc.)\n\n        :param conn: DB connection object\n        :param put_timestamp: put timestamp\n        """'
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
name|'self'
op|'.'
name|'create_container_table'
op|'('
name|'conn'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'create_account_stat_table'
op|'('
name|'conn'
op|','
name|'put_timestamp'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'create_policy_stat_table'
op|'('
name|'conn'
op|')'
newline|'\n'
nl|'\n'
DECL|member|create_container_table
dedent|''
name|'def'
name|'create_container_table'
op|'('
name|'self'
op|','
name|'conn'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Create container table which is specific to the account DB.\n\n        :param conn: DB connection object\n        """'
newline|'\n'
name|'conn'
op|'.'
name|'executescript'
op|'('
string|'"""\n            CREATE TABLE container (\n                ROWID INTEGER PRIMARY KEY AUTOINCREMENT,\n                name TEXT,\n                put_timestamp TEXT,\n                delete_timestamp TEXT,\n                object_count INTEGER,\n                bytes_used INTEGER,\n                deleted INTEGER DEFAULT 0,\n                storage_policy_index INTEGER DEFAULT 0\n            );\n\n            CREATE INDEX ix_container_deleted_name ON\n                container (deleted, name);\n\n            CREATE TRIGGER container_insert AFTER INSERT ON container\n            BEGIN\n                UPDATE account_stat\n                SET container_count = container_count + (1 - new.deleted),\n                    object_count = object_count + new.object_count,\n                    bytes_used = bytes_used + new.bytes_used,\n                    hash = chexor(hash, new.name,\n                                  new.put_timestamp || \'-\' ||\n                                    new.delete_timestamp || \'-\' ||\n                                    new.object_count || \'-\' || new.bytes_used);\n            END;\n\n            CREATE TRIGGER container_update BEFORE UPDATE ON container\n            BEGIN\n                SELECT RAISE(FAIL, \'UPDATE not allowed; DELETE and INSERT\');\n            END;\n\n\n            CREATE TRIGGER container_delete AFTER DELETE ON container\n            BEGIN\n                UPDATE account_stat\n                SET container_count = container_count - (1 - old.deleted),\n                    object_count = object_count - old.object_count,\n                    bytes_used = bytes_used - old.bytes_used,\n                    hash = chexor(hash, old.name,\n                                  old.put_timestamp || \'-\' ||\n                                    old.delete_timestamp || \'-\' ||\n                                    old.object_count || \'-\' || old.bytes_used);\n            END;\n        """'
op|'+'
name|'POLICY_STAT_TRIGGER_SCRIPT'
op|')'
newline|'\n'
nl|'\n'
DECL|member|create_account_stat_table
dedent|''
name|'def'
name|'create_account_stat_table'
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
string|'"""\n        Create account_stat table which is specific to the account DB.\n        Not a part of Pluggable Back-ends, internal to the baseline code.\n\n        :param conn: DB connection object\n        :param put_timestamp: put timestamp\n        """'
newline|'\n'
name|'conn'
op|'.'
name|'executescript'
op|'('
string|'"""\n            CREATE TABLE account_stat (\n                account TEXT,\n                created_at TEXT,\n                put_timestamp TEXT DEFAULT \'0\',\n                delete_timestamp TEXT DEFAULT \'0\',\n                container_count INTEGER,\n                object_count INTEGER DEFAULT 0,\n                bytes_used INTEGER DEFAULT 0,\n                hash TEXT default \'00000000000000000000000000000000\',\n                id TEXT,\n                status TEXT DEFAULT \'\',\n                status_changed_at TEXT DEFAULT \'0\',\n                metadata TEXT DEFAULT \'\'\n            );\n\n            INSERT INTO account_stat (container_count) VALUES (0);\n        """'
op|')'
newline|'\n'
nl|'\n'
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n            UPDATE account_stat SET account = ?, created_at = ?, id = ?,\n                   put_timestamp = ?, status_changed_at = ?\n            '''"
op|','
op|'('
name|'self'
op|'.'
name|'account'
op|','
name|'Timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|'.'
name|'internal'
op|','
name|'str'
op|'('
name|'uuid4'
op|'('
op|')'
op|')'
op|','
nl|'\n'
name|'put_timestamp'
op|','
name|'put_timestamp'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|create_policy_stat_table
dedent|''
name|'def'
name|'create_policy_stat_table'
op|'('
name|'self'
op|','
name|'conn'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Create policy_stat table which is specific to the account DB.\n        Not a part of Pluggable Back-ends, internal to the baseline code.\n\n        :param conn: DB connection object\n        """'
newline|'\n'
name|'conn'
op|'.'
name|'executescript'
op|'('
string|'"""\n            CREATE TABLE policy_stat (\n                storage_policy_index INTEGER PRIMARY KEY,\n                container_count INTEGER DEFAULT 0,\n                object_count INTEGER DEFAULT 0,\n                bytes_used INTEGER DEFAULT 0\n            );\n            INSERT OR IGNORE INTO policy_stat (\n                storage_policy_index, container_count, object_count,\n                bytes_used\n            )\n            SELECT 0, container_count, object_count, bytes_used\n            FROM account_stat\n            WHERE container_count > 0;\n        """'
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
string|"'''\n                    SELECT name FROM sqlite_master\n                    WHERE name = 'ix_container_deleted_name' '''"
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
op|','
name|'force'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Mark the DB as deleted.\n\n        :param conn: DB connection object\n        :param timestamp: timestamp to mark as deleted\n        """'
newline|'\n'
name|'conn'
op|'.'
name|'execute'
op|'('
string|'"""\n            UPDATE account_stat\n            SET delete_timestamp = ?,\n                status = \'DELETED\',\n                status_changed_at = ?\n            WHERE delete_timestamp < ? """'
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
name|'loaded'
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
comment|'# check to see if the update includes policy_index or not'
nl|'\n'
op|'('
name|'name'
op|','
name|'put_timestamp'
op|','
name|'delete_timestamp'
op|','
name|'object_count'
op|','
name|'bytes_used'
op|','
nl|'\n'
name|'deleted'
op|')'
op|'='
name|'loaded'
op|'['
op|':'
number|'6'
op|']'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'loaded'
op|')'
op|'>'
number|'6'
op|':'
newline|'\n'
indent|'            '
name|'storage_policy_index'
op|'='
name|'loaded'
op|'['
number|'6'
op|']'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
comment|'# legacy support during upgrade until first non legacy storage'
nl|'\n'
comment|'# policy is defined'
nl|'\n'
indent|'            '
name|'storage_policy_index'
op|'='
number|'0'
newline|'\n'
dedent|''
name|'item_list'
op|'.'
name|'append'
op|'('
nl|'\n'
op|'{'
string|"'name'"
op|':'
name|'name'
op|','
nl|'\n'
string|"'put_timestamp'"
op|':'
name|'put_timestamp'
op|','
nl|'\n'
string|"'delete_timestamp'"
op|':'
name|'delete_timestamp'
op|','
nl|'\n'
string|"'object_count'"
op|':'
name|'object_count'
op|','
nl|'\n'
string|"'bytes_used'"
op|':'
name|'bytes_used'
op|','
nl|'\n'
string|"'deleted'"
op|':'
name|'deleted'
op|','
nl|'\n'
string|"'storage_policy_index'"
op|':'
name|'storage_policy_index'
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
string|'"""\n        Check if the account DB is empty.\n\n        :returns: True if the database has no active containers.\n        """'
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
string|"'SELECT container_count from account_stat'"
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
DECL|member|make_tuple_for_pickle
dedent|''
dedent|''
name|'def'
name|'make_tuple_for_pickle'
op|'('
name|'self'
op|','
name|'record'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
op|'('
name|'record'
op|'['
string|"'name'"
op|']'
op|','
name|'record'
op|'['
string|"'put_timestamp'"
op|']'
op|','
nl|'\n'
name|'record'
op|'['
string|"'delete_timestamp'"
op|']'
op|','
name|'record'
op|'['
string|"'object_count'"
op|']'
op|','
nl|'\n'
name|'record'
op|'['
string|"'bytes_used'"
op|']'
op|','
name|'record'
op|'['
string|"'deleted'"
op|']'
op|','
nl|'\n'
name|'record'
op|'['
string|"'storage_policy_index'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|put_container
dedent|''
name|'def'
name|'put_container'
op|'('
name|'self'
op|','
name|'name'
op|','
name|'put_timestamp'
op|','
name|'delete_timestamp'
op|','
nl|'\n'
name|'object_count'
op|','
name|'bytes_used'
op|','
name|'storage_policy_index'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Create a container with the given attributes.\n\n        :param name: name of the container to create\n        :param put_timestamp: put_timestamp of the container to create\n        :param delete_timestamp: delete_timestamp of the container to create\n        :param object_count: number of objects in the container\n        :param bytes_used: number of bytes used by the container\n        :param storage_policy_index:  the storage policy for this container\n        """'
newline|'\n'
name|'if'
name|'delete_timestamp'
op|'>'
name|'put_timestamp'
name|'and'
name|'object_count'
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
op|':'
newline|'\n'
indent|'            '
name|'deleted'
op|'='
number|'1'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'deleted'
op|'='
number|'0'
newline|'\n'
dedent|''
name|'record'
op|'='
op|'{'
string|"'name'"
op|':'
name|'name'
op|','
string|"'put_timestamp'"
op|':'
name|'put_timestamp'
op|','
nl|'\n'
string|"'delete_timestamp'"
op|':'
name|'delete_timestamp'
op|','
nl|'\n'
string|"'object_count'"
op|':'
name|'object_count'
op|','
nl|'\n'
string|"'bytes_used'"
op|':'
name|'bytes_used'
op|','
nl|'\n'
string|"'deleted'"
op|':'
name|'deleted'
op|','
nl|'\n'
string|"'storage_policy_index'"
op|':'
name|'storage_policy_index'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'put_record'
op|'('
name|'record'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_is_deleted_info
dedent|''
name|'def'
name|'_is_deleted_info'
op|'('
name|'self'
op|','
name|'status'
op|','
name|'container_count'
op|','
name|'delete_timestamp'
op|','
nl|'\n'
name|'put_timestamp'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Apply delete logic to database info.\n\n        :returns: True if the DB is considered to be deleted, False otherwise\n        """'
newline|'\n'
name|'return'
name|'status'
op|'=='
string|"'DELETED'"
name|'or'
op|'('
nl|'\n'
name|'container_count'
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
name|'and'
nl|'\n'
name|'Timestamp'
op|'('
name|'delete_timestamp'
op|')'
op|'>'
name|'Timestamp'
op|'('
name|'put_timestamp'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_is_deleted
dedent|''
name|'def'
name|'_is_deleted'
op|'('
name|'self'
op|','
name|'conn'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Check account_stat table and evaluate info.\n\n        :param conn: database conn\n\n        :returns: True if the DB is considered to be deleted, False otherwise\n        """'
newline|'\n'
name|'info'
op|'='
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n            SELECT put_timestamp, delete_timestamp, container_count, status\n            FROM account_stat'''"
op|')'
op|'.'
name|'fetchone'
op|'('
op|')'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'_is_deleted_info'
op|'('
op|'**'
name|'info'
op|')'
newline|'\n'
nl|'\n'
DECL|member|is_status_deleted
dedent|''
name|'def'
name|'is_status_deleted'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Only returns true if the status field is set to DELETED."""'
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
string|"'''\n                SELECT put_timestamp, delete_timestamp, status\n                FROM account_stat'''"
op|')'
op|'.'
name|'fetchone'
op|'('
op|')'
newline|'\n'
name|'return'
name|'row'
op|'['
string|"'status'"
op|']'
op|'=='
string|'"DELETED"'
name|'or'
op|'('
nl|'\n'
name|'row'
op|'['
string|"'delete_timestamp'"
op|']'
op|'>'
name|'row'
op|'['
string|"'put_timestamp'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_policy_stats
dedent|''
dedent|''
name|'def'
name|'get_policy_stats'
op|'('
name|'self'
op|','
name|'do_migrations'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Get global policy stats for the account.\n\n        :param do_migrations: boolean, if True the policy stat dicts will\n                              always include the \'container_count\' key;\n                              otherwise it may be omitted on legacy databases\n                              until they are migrated.\n\n        :returns: dict of policy stats where the key is the policy index and\n                  the value is a dictionary like {\'object_count\': M,\n                  \'bytes_used\': N, \'container_count\': L}\n        """'
newline|'\n'
name|'columns'
op|'='
op|'['
nl|'\n'
string|"'storage_policy_index'"
op|','
nl|'\n'
string|"'container_count'"
op|','
nl|'\n'
string|"'object_count'"
op|','
nl|'\n'
string|"'bytes_used'"
op|','
nl|'\n'
op|']'
newline|'\n'
nl|'\n'
DECL|function|run_query
name|'def'
name|'run_query'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
op|'('
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n                SELECT %s\n                FROM policy_stat\n                '''"
op|'%'
string|"', '"
op|'.'
name|'join'
op|'('
name|'columns'
op|')'
op|')'
op|'.'
name|'fetchall'
op|'('
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'_commit_puts_stale_ok'
op|'('
op|')'
newline|'\n'
name|'info'
op|'='
op|'['
op|']'
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
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'info'
op|'='
name|'run_query'
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
indent|'                '
name|'if'
string|'"no such column: container_count"'
name|'in'
name|'str'
op|'('
name|'err'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'do_migrations'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'_migrate_add_container_count'
op|'('
name|'conn'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'columns'
op|'.'
name|'remove'
op|'('
string|"'container_count'"
op|')'
newline|'\n'
dedent|''
name|'info'
op|'='
name|'run_query'
op|'('
op|')'
newline|'\n'
dedent|''
name|'elif'
string|'"no such table: policy_stat"'
name|'not'
name|'in'
name|'str'
op|'('
name|'err'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
dedent|''
name|'policy_stats'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'row'
name|'in'
name|'info'
op|':'
newline|'\n'
indent|'            '
name|'stats'
op|'='
name|'dict'
op|'('
name|'row'
op|')'
newline|'\n'
name|'key'
op|'='
name|'stats'
op|'.'
name|'pop'
op|'('
string|"'storage_policy_index'"
op|')'
newline|'\n'
name|'policy_stats'
op|'['
name|'key'
op|']'
op|'='
name|'stats'
newline|'\n'
dedent|''
name|'return'
name|'policy_stats'
newline|'\n'
nl|'\n'
DECL|member|get_info
dedent|''
name|'def'
name|'get_info'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Get global data for the account.\n\n        :returns: dict with keys: account, created_at, put_timestamp,\n                  delete_timestamp, status_changed_at, container_count,\n                  object_count, bytes_used, hash, id\n        """'
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
name|'return'
name|'dict'
op|'('
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n                SELECT account, created_at,  put_timestamp, delete_timestamp,\n                       status_changed_at, container_count, object_count,\n                       bytes_used, hash, id\n                FROM account_stat\n            '''"
op|')'
op|'.'
name|'fetchone'
op|'('
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|list_containers_iter
dedent|''
dedent|''
name|'def'
name|'list_containers_iter'
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
nl|'\n'
name|'delimiter'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Get a list of containers sorted by name starting at marker onward, up\n        to limit entries. Entries will begin with the prefix and will not have\n        the delimiter after the prefix.\n\n        :param limit: maximum number of entries to get\n        :param marker: marker query\n        :param end_marker: end marker query\n        :param prefix: prefix query\n        :param delimiter: delimiter for query\n\n        :returns: list of tuples of (name, object_count, bytes_used, 0)\n        """'
newline|'\n'
op|'('
name|'marker'
op|','
name|'end_marker'
op|','
name|'prefix'
op|','
name|'delimiter'
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
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_commit_puts_stale_ok'
op|'('
op|')'
newline|'\n'
name|'if'
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
string|'"""\n                    SELECT name, object_count, bytes_used, 0\n                    FROM container\n                    WHERE deleted = 0 AND """'
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
number|'0'
op|','
number|'0'
op|','
number|'1'
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
string|'"""\n        Merge items into the container table.\n\n        :param item_list: list of dictionaries of {\'name\', \'put_timestamp\',\n                          \'delete_timestamp\', \'object_count\', \'bytes_used\',\n                          \'deleted\', \'storage_policy_index\'}\n        :param source: if defined, update incoming_sync with the source\n        """'
newline|'\n'
DECL|function|_really_merge_items
name|'def'
name|'_really_merge_items'
op|'('
name|'conn'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'max_rowid'
op|'='
op|'-'
number|'1'
newline|'\n'
name|'curs'
op|'='
name|'conn'
op|'.'
name|'cursor'
op|'('
op|')'
newline|'\n'
name|'for'
name|'rec'
name|'in'
name|'item_list'
op|':'
newline|'\n'
indent|'                '
name|'rec'
op|'.'
name|'setdefault'
op|'('
string|"'storage_policy_index'"
op|','
number|'0'
op|')'
comment|'# legacy'
newline|'\n'
name|'record'
op|'='
op|'['
name|'rec'
op|'['
string|"'name'"
op|']'
op|','
name|'rec'
op|'['
string|"'put_timestamp'"
op|']'
op|','
nl|'\n'
name|'rec'
op|'['
string|"'delete_timestamp'"
op|']'
op|','
name|'rec'
op|'['
string|"'object_count'"
op|']'
op|','
nl|'\n'
name|'rec'
op|'['
string|"'bytes_used'"
op|']'
op|','
name|'rec'
op|'['
string|"'deleted'"
op|']'
op|','
nl|'\n'
name|'rec'
op|'['
string|"'storage_policy_index'"
op|']'
op|']'
newline|'\n'
name|'query'
op|'='
string|"'''\n                    SELECT name, put_timestamp, delete_timestamp,\n                           object_count, bytes_used, deleted,\n                           storage_policy_index\n                    FROM container WHERE name = ?\n                '''"
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
name|'curs_row'
op|'='
name|'curs'
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
newline|'\n'
name|'curs_row'
op|'.'
name|'row_factory'
op|'='
name|'None'
newline|'\n'
name|'row'
op|'='
name|'curs_row'
op|'.'
name|'fetchone'
op|'('
op|')'
newline|'\n'
name|'if'
name|'row'
op|':'
newline|'\n'
indent|'                    '
name|'row'
op|'='
name|'list'
op|'('
name|'row'
op|')'
newline|'\n'
name|'for'
name|'i'
name|'in'
name|'range'
op|'('
number|'5'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'if'
name|'record'
op|'['
name|'i'
op|']'
name|'is'
name|'None'
name|'and'
name|'row'
op|'['
name|'i'
op|']'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'                            '
name|'record'
op|'['
name|'i'
op|']'
op|'='
name|'row'
op|'['
name|'i'
op|']'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'row'
op|'['
number|'1'
op|']'
op|'>'
name|'record'
op|'['
number|'1'
op|']'
op|':'
comment|'# Keep newest put_timestamp'
newline|'\n'
indent|'                        '
name|'record'
op|'['
number|'1'
op|']'
op|'='
name|'row'
op|'['
number|'1'
op|']'
newline|'\n'
dedent|''
name|'if'
name|'row'
op|'['
number|'2'
op|']'
op|'>'
name|'record'
op|'['
number|'2'
op|']'
op|':'
comment|'# Keep newest delete_timestamp'
newline|'\n'
indent|'                        '
name|'record'
op|'['
number|'2'
op|']'
op|'='
name|'row'
op|'['
number|'2'
op|']'
newline|'\n'
comment|'# If deleted, mark as such'
nl|'\n'
dedent|''
name|'if'
name|'record'
op|'['
number|'2'
op|']'
op|'>'
name|'record'
op|'['
number|'1'
op|']'
name|'and'
name|'record'
op|'['
number|'3'
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
op|':'
newline|'\n'
indent|'                        '
name|'record'
op|'['
number|'5'
op|']'
op|'='
number|'1'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'record'
op|'['
number|'5'
op|']'
op|'='
number|'0'
newline|'\n'
dedent|''
dedent|''
name|'curs'
op|'.'
name|'execute'
op|'('
string|"'''\n                    DELETE FROM container WHERE name = ? AND\n                                                deleted IN (0, 1)\n                '''"
op|','
op|'('
name|'record'
op|'['
number|'0'
op|']'
op|','
op|')'
op|')'
newline|'\n'
name|'curs'
op|'.'
name|'execute'
op|'('
string|"'''\n                    INSERT INTO container (name, put_timestamp,\n                        delete_timestamp, object_count, bytes_used,\n                        deleted, storage_policy_index)\n                    VALUES (?, ?, ?, ?, ?, ?, ?)\n                '''"
op|','
name|'record'
op|')'
newline|'\n'
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
name|'curs'
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
name|'curs'
op|'.'
name|'execute'
op|'('
string|"'''\n                        UPDATE incoming_sync\n                        SET sync_point=max(?, sync_point)\n                        WHERE remote_id=?\n                    '''"
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
nl|'\n'
dedent|''
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
comment|'# create the policy stat table if needed and add spi to container'
nl|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'_really_merge_items'
op|'('
name|'conn'
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
indent|'                '
name|'if'
string|"'no such column: storage_policy_index'"
name|'not'
name|'in'
name|'str'
op|'('
name|'err'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'_migrate_add_storage_policy_index'
op|'('
name|'conn'
op|')'
newline|'\n'
name|'_really_merge_items'
op|'('
name|'conn'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_migrate_add_container_count
dedent|''
dedent|''
dedent|''
name|'def'
name|'_migrate_add_container_count'
op|'('
name|'self'
op|','
name|'conn'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Add the container_count column to the \'policy_stat\' table and\n        update it\n\n        :param conn: DB connection object\n        """'
newline|'\n'
comment|'# add the container_count column'
nl|'\n'
name|'curs'
op|'='
name|'conn'
op|'.'
name|'cursor'
op|'('
op|')'
newline|'\n'
name|'curs'
op|'.'
name|'executescript'
op|'('
string|"'''\n            DROP TRIGGER container_delete_ps;\n            DROP TRIGGER container_insert_ps;\n            ALTER TABLE policy_stat\n            ADD COLUMN container_count INTEGER DEFAULT 0;\n        '''"
op|'+'
name|'POLICY_STAT_TRIGGER_SCRIPT'
op|')'
newline|'\n'
nl|'\n'
comment|"# keep the simple case simple, if there's only one entry in the"
nl|'\n'
comment|'# policy_stat table we just copy the total container count from the'
nl|'\n'
comment|'# account_stat table'
nl|'\n'
nl|'\n'
comment|'# if that triggers an update then the where changes <> 0 *would* exist'
nl|'\n'
comment|"# and the insert or replace from the count subqueries won't execute"
nl|'\n'
nl|'\n'
name|'curs'
op|'.'
name|'executescript'
op|'('
string|'"""\n        UPDATE policy_stat\n        SET container_count = (\n            SELECT container_count\n            FROM account_stat)\n        WHERE (\n            SELECT COUNT(storage_policy_index)\n            FROM policy_stat\n        ) <= 1;\n\n        INSERT OR REPLACE INTO policy_stat (\n            storage_policy_index,\n            container_count,\n            object_count,\n            bytes_used\n        )\n        SELECT p.storage_policy_index,\n               c.count,\n               p.object_count,\n               p.bytes_used\n        FROM (\n            SELECT storage_policy_index,\n                   COUNT(*) as count\n            FROM container\n            WHERE deleted = 0\n            GROUP BY storage_policy_index\n        ) c\n        JOIN policy_stat p\n        ON p.storage_policy_index = c.storage_policy_index\n        WHERE NOT EXISTS(\n            SELECT changes() as change\n            FROM policy_stat\n            WHERE change <> 0\n        );\n        """'
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'commit'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|_migrate_add_storage_policy_index
dedent|''
name|'def'
name|'_migrate_add_storage_policy_index'
op|'('
name|'self'
op|','
name|'conn'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Add the storage_policy_index column to the \'container\' table and\n        set up triggers, creating the policy_stat table if needed.\n\n        :param conn: DB connection object\n        """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'create_policy_stat_table'
op|'('
name|'conn'
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
indent|'            '
name|'if'
string|"'table policy_stat already exists'"
name|'not'
name|'in'
name|'str'
op|'('
name|'err'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
newline|'\n'
dedent|''
dedent|''
name|'conn'
op|'.'
name|'executescript'
op|'('
string|"'''\n            ALTER TABLE container\n            ADD COLUMN storage_policy_index INTEGER DEFAULT 0;\n        '''"
op|'+'
name|'POLICY_STAT_TRIGGER_SCRIPT'
op|')'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
