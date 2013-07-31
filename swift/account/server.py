begin_unit
comment|'# Copyright (c) 2010-2012 OpenStack, LLC.'
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
comment|'# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or'
nl|'\n'
comment|'# implied.'
nl|'\n'
comment|'# See the License for the specific language governing permissions and'
nl|'\n'
comment|'# limitations under the License.'
nl|'\n'
nl|'\n'
name|'from'
name|'__future__'
name|'import'
name|'with_statement'
newline|'\n'
nl|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'traceback'
newline|'\n'
name|'from'
name|'gettext'
name|'import'
name|'gettext'
name|'as'
name|'_'
newline|'\n'
nl|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'Timeout'
newline|'\n'
nl|'\n'
name|'import'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'db'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'account'
op|'.'
name|'utils'
name|'import'
name|'account_listing_response'
op|','
name|'account_listing_content_type'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'db'
name|'import'
name|'AccountBroker'
op|','
name|'DatabaseConnectionError'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'request_helpers'
name|'import'
name|'get_param'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'get_logger'
op|','
name|'hash_path'
op|','
name|'public'
op|','
name|'normalize_timestamp'
op|','
name|'storage_directory'
op|','
name|'config_true_value'
op|','
name|'validate_device_partition'
op|','
name|'json'
op|','
name|'timing_stats'
op|','
name|'replication'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'constraints'
name|'import'
name|'ACCOUNT_LISTING_LIMIT'
op|','
name|'check_mount'
op|','
name|'check_float'
op|','
name|'check_utf8'
op|','
name|'FORMAT2CONTENT_TYPE'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'db_replicator'
name|'import'
name|'ReplicatorRpc'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'HTTPAccepted'
op|','
name|'HTTPBadRequest'
op|','
name|'HTTPCreated'
op|','
name|'HTTPForbidden'
op|','
name|'HTTPInternalServerError'
op|','
name|'HTTPMethodNotAllowed'
op|','
name|'HTTPNoContent'
op|','
name|'HTTPNotFound'
op|','
name|'HTTPPreconditionFailed'
op|','
name|'HTTPConflict'
op|','
name|'Request'
op|','
name|'HTTPInsufficientStorage'
op|','
name|'HTTPNotAcceptable'
op|','
name|'HTTPException'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|variable|DATADIR
name|'DATADIR'
op|'='
string|"'accounts'"
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|AccountController
name|'class'
name|'AccountController'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""WSGI controller for the account server."""'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'conf'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'conf'
op|','
name|'log_route'
op|'='
string|"'account-server'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'root'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'devices'"
op|','
string|"'/srv/node'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'mount_check'
op|'='
name|'config_true_value'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'mount_check'"
op|','
string|"'true'"
op|')'
op|')'
newline|'\n'
name|'replication_server'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'replication_server'"
op|','
name|'None'
op|')'
newline|'\n'
name|'if'
name|'replication_server'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'replication_server'
op|'='
name|'config_true_value'
op|'('
name|'replication_server'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'replication_server'
op|'='
name|'replication_server'
newline|'\n'
name|'self'
op|'.'
name|'replicator_rpc'
op|'='
name|'ReplicatorRpc'
op|'('
name|'self'
op|'.'
name|'root'
op|','
name|'DATADIR'
op|','
name|'AccountBroker'
op|','
nl|'\n'
name|'self'
op|'.'
name|'mount_check'
op|','
nl|'\n'
name|'logger'
op|'='
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auto_create_account_prefix'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'auto_create_account_prefix'"
op|')'
name|'or'
string|"'.'"
newline|'\n'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'db'
op|'.'
name|'DB_PREALLOCATION'
op|'='
name|'config_true_value'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'db_preallocation'"
op|','
string|"'f'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_get_account_broker
dedent|''
name|'def'
name|'_get_account_broker'
op|'('
name|'self'
op|','
name|'drive'
op|','
name|'part'
op|','
name|'account'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'hsh'
op|'='
name|'hash_path'
op|'('
name|'account'
op|')'
newline|'\n'
name|'db_dir'
op|'='
name|'storage_directory'
op|'('
name|'DATADIR'
op|','
name|'part'
op|','
name|'hsh'
op|')'
newline|'\n'
name|'db_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'root'
op|','
name|'drive'
op|','
name|'db_dir'
op|','
name|'hsh'
op|'+'
string|"'.db'"
op|')'
newline|'\n'
name|'kwargs'
op|'.'
name|'setdefault'
op|'('
string|"'account'"
op|','
name|'account'
op|')'
newline|'\n'
name|'kwargs'
op|'.'
name|'setdefault'
op|'('
string|"'logger'"
op|','
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'return'
name|'AccountBroker'
op|'('
name|'db_path'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_deleted_response
dedent|''
name|'def'
name|'_deleted_response'
op|'('
name|'self'
op|','
name|'broker'
op|','
name|'req'
op|','
name|'resp'
op|','
name|'body'
op|'='
string|"''"
op|')'
op|':'
newline|'\n'
comment|'# We are here since either the account does not exist or'
nl|'\n'
comment|'# it exists but marked for deletion.'
nl|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
op|'}'
newline|'\n'
comment|'# Try to check if account exists and is marked for deletion'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'broker'
op|'.'
name|'is_status_deleted'
op|'('
op|')'
op|':'
newline|'\n'
comment|'# Account does exist and is marked for deletion'
nl|'\n'
indent|'                '
name|'headers'
op|'='
op|'{'
string|"'X-Account-Status'"
op|':'
string|"'Deleted'"
op|'}'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'DatabaseConnectionError'
op|':'
newline|'\n'
comment|'# Account does not exist!'
nl|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'return'
name|'resp'
op|'('
name|'request'
op|'='
name|'req'
op|','
name|'headers'
op|'='
name|'headers'
op|','
name|'charset'
op|'='
string|"'utf-8'"
op|','
name|'body'
op|'='
name|'body'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'public'
newline|'\n'
op|'@'
name|'timing_stats'
op|'('
op|')'
newline|'\n'
DECL|member|DELETE
name|'def'
name|'DELETE'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Handle HTTP DELETE request."""'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'drive'
op|','
name|'part'
op|','
name|'account'
op|'='
name|'req'
op|'.'
name|'split_path'
op|'('
number|'3'
op|')'
newline|'\n'
name|'validate_device_partition'
op|'('
name|'drive'
op|','
name|'part'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'body'
op|'='
name|'str'
op|'('
name|'err'
op|')'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'mount_check'
name|'and'
name|'not'
name|'check_mount'
op|'('
name|'self'
op|'.'
name|'root'
op|','
name|'drive'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPInsufficientStorage'
op|'('
name|'drive'
op|'='
name|'drive'
op|','
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'if'
string|"'x-timestamp'"
name|'not'
name|'in'
name|'req'
op|'.'
name|'headers'
name|'or'
name|'not'
name|'check_float'
op|'('
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-timestamp'"
op|']'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'body'
op|'='
string|"'Missing timestamp'"
op|','
name|'request'
op|'='
name|'req'
op|','
nl|'\n'
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
name|'broker'
op|'='
name|'self'
op|'.'
name|'_get_account_broker'
op|'('
name|'drive'
op|','
name|'part'
op|','
name|'account'
op|')'
newline|'\n'
name|'if'
name|'broker'
op|'.'
name|'is_deleted'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_deleted_response'
op|'('
name|'broker'
op|','
name|'req'
op|','
name|'HTTPNotFound'
op|')'
newline|'\n'
dedent|''
name|'broker'
op|'.'
name|'delete_db'
op|'('
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-timestamp'"
op|']'
op|')'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'_deleted_response'
op|'('
name|'broker'
op|','
name|'req'
op|','
name|'HTTPNoContent'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'public'
newline|'\n'
op|'@'
name|'timing_stats'
op|'('
op|')'
newline|'\n'
DECL|member|PUT
name|'def'
name|'PUT'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Handle HTTP PUT request."""'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'drive'
op|','
name|'part'
op|','
name|'account'
op|','
name|'container'
op|'='
name|'req'
op|'.'
name|'split_path'
op|'('
number|'3'
op|','
number|'4'
op|')'
newline|'\n'
name|'validate_device_partition'
op|'('
name|'drive'
op|','
name|'part'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'body'
op|'='
name|'str'
op|'('
name|'err'
op|')'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'mount_check'
name|'and'
name|'not'
name|'check_mount'
op|'('
name|'self'
op|'.'
name|'root'
op|','
name|'drive'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPInsufficientStorage'
op|'('
name|'drive'
op|'='
name|'drive'
op|','
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'container'
op|':'
comment|'# put account container'
newline|'\n'
indent|'            '
name|'pending_timeout'
op|'='
name|'None'
newline|'\n'
name|'if'
string|"'x-trans-id'"
name|'in'
name|'req'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'                '
name|'pending_timeout'
op|'='
number|'3'
newline|'\n'
dedent|''
name|'broker'
op|'='
name|'self'
op|'.'
name|'_get_account_broker'
op|'('
name|'drive'
op|','
name|'part'
op|','
name|'account'
op|','
nl|'\n'
name|'pending_timeout'
op|'='
name|'pending_timeout'
op|')'
newline|'\n'
name|'if'
name|'account'
op|'.'
name|'startswith'
op|'('
name|'self'
op|'.'
name|'auto_create_account_prefix'
op|')'
name|'and'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'broker'
op|'.'
name|'db_file'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'broker'
op|'.'
name|'initialize'
op|'('
name|'normalize_timestamp'
op|'('
nl|'\n'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-timestamp'"
op|')'
name|'or'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'db'
op|'.'
name|'DatabaseAlreadyExists'
op|':'
newline|'\n'
indent|'                    '
name|'pass'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-account-override-deleted'"
op|','
string|"'no'"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
op|'!='
string|"'yes'"
name|'and'
name|'broker'
op|'.'
name|'is_deleted'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'HTTPNotFound'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'broker'
op|'.'
name|'put_container'
op|'('
name|'container'
op|','
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-put-timestamp'"
op|']'
op|','
nl|'\n'
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-delete-timestamp'"
op|']'
op|','
nl|'\n'
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-object-count'"
op|']'
op|','
nl|'\n'
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-bytes-used'"
op|']'
op|')'
newline|'\n'
name|'if'
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-delete-timestamp'"
op|']'
op|'>'
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-put-timestamp'"
op|']'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'HTTPNoContent'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'HTTPCreated'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
comment|'# put account'
newline|'\n'
indent|'            '
name|'broker'
op|'='
name|'self'
op|'.'
name|'_get_account_broker'
op|'('
name|'drive'
op|','
name|'part'
op|','
name|'account'
op|')'
newline|'\n'
name|'timestamp'
op|'='
name|'normalize_timestamp'
op|'('
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-timestamp'"
op|']'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'broker'
op|'.'
name|'db_file'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'broker'
op|'.'
name|'initialize'
op|'('
name|'timestamp'
op|')'
newline|'\n'
name|'created'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'except'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'db'
op|'.'
name|'DatabaseAlreadyExists'
op|':'
newline|'\n'
indent|'                    '
name|'pass'
newline|'\n'
dedent|''
dedent|''
name|'elif'
name|'broker'
op|'.'
name|'is_status_deleted'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'self'
op|'.'
name|'_deleted_response'
op|'('
name|'broker'
op|','
name|'req'
op|','
name|'HTTPForbidden'
op|','
nl|'\n'
name|'body'
op|'='
string|"'Recently deleted'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'created'
op|'='
name|'broker'
op|'.'
name|'is_deleted'
op|'('
op|')'
newline|'\n'
name|'broker'
op|'.'
name|'update_put_timestamp'
op|'('
name|'timestamp'
op|')'
newline|'\n'
name|'if'
name|'broker'
op|'.'
name|'is_deleted'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'return'
name|'HTTPConflict'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'metadata'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'metadata'
op|'.'
name|'update'
op|'('
op|'('
name|'key'
op|','
op|'('
name|'value'
op|','
name|'timestamp'
op|')'
op|')'
nl|'\n'
name|'for'
name|'key'
op|','
name|'value'
name|'in'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'iteritems'
op|'('
op|')'
nl|'\n'
name|'if'
name|'key'
op|'.'
name|'lower'
op|'('
op|')'
op|'.'
name|'startswith'
op|'('
string|"'x-account-meta-'"
op|')'
op|')'
newline|'\n'
name|'if'
name|'metadata'
op|':'
newline|'\n'
indent|'                '
name|'broker'
op|'.'
name|'update_metadata'
op|'('
name|'metadata'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'created'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'HTTPCreated'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'HTTPAccepted'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
dedent|''
op|'@'
name|'public'
newline|'\n'
op|'@'
name|'timing_stats'
op|'('
op|')'
newline|'\n'
DECL|member|HEAD
name|'def'
name|'HEAD'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Handle HTTP HEAD request."""'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'drive'
op|','
name|'part'
op|','
name|'account'
op|'='
name|'req'
op|'.'
name|'split_path'
op|'('
number|'3'
op|')'
newline|'\n'
name|'validate_device_partition'
op|'('
name|'drive'
op|','
name|'part'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'body'
op|'='
name|'str'
op|'('
name|'err'
op|')'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'query_format'
op|'='
name|'get_param'
op|'('
name|'req'
op|','
string|"'format'"
op|')'
newline|'\n'
name|'if'
name|'query_format'
op|':'
newline|'\n'
indent|'            '
name|'req'
op|'.'
name|'accept'
op|'='
name|'FORMAT2CONTENT_TYPE'
op|'.'
name|'get'
op|'('
nl|'\n'
name|'query_format'
op|'.'
name|'lower'
op|'('
op|')'
op|','
name|'FORMAT2CONTENT_TYPE'
op|'['
string|"'plain'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'out_content_type'
op|'='
name|'req'
op|'.'
name|'accept'
op|'.'
name|'best_match'
op|'('
nl|'\n'
op|'['
string|"'text/plain'"
op|','
string|"'application/json'"
op|','
string|"'application/xml'"
op|','
string|"'text/xml'"
op|']'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'out_content_type'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPNotAcceptable'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'mount_check'
name|'and'
name|'not'
name|'check_mount'
op|'('
name|'self'
op|'.'
name|'root'
op|','
name|'drive'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPInsufficientStorage'
op|'('
name|'drive'
op|'='
name|'drive'
op|','
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'broker'
op|'='
name|'self'
op|'.'
name|'_get_account_broker'
op|'('
name|'drive'
op|','
name|'part'
op|','
name|'account'
op|','
nl|'\n'
name|'pending_timeout'
op|'='
number|'0.1'
op|','
nl|'\n'
name|'stale_reads_ok'
op|'='
name|'True'
op|')'
newline|'\n'
name|'if'
name|'broker'
op|'.'
name|'is_deleted'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_deleted_response'
op|'('
name|'broker'
op|','
name|'req'
op|','
name|'HTTPNotFound'
op|')'
newline|'\n'
dedent|''
name|'info'
op|'='
name|'broker'
op|'.'
name|'get_info'
op|'('
op|')'
newline|'\n'
name|'headers'
op|'='
op|'{'
nl|'\n'
string|"'X-Account-Container-Count'"
op|':'
name|'info'
op|'['
string|"'container_count'"
op|']'
op|','
nl|'\n'
string|"'X-Account-Object-Count'"
op|':'
name|'info'
op|'['
string|"'object_count'"
op|']'
op|','
nl|'\n'
string|"'X-Account-Bytes-Used'"
op|':'
name|'info'
op|'['
string|"'bytes_used'"
op|']'
op|','
nl|'\n'
string|"'X-Timestamp'"
op|':'
name|'info'
op|'['
string|"'created_at'"
op|']'
op|','
nl|'\n'
string|"'X-PUT-Timestamp'"
op|':'
name|'info'
op|'['
string|"'put_timestamp'"
op|']'
op|'}'
newline|'\n'
name|'headers'
op|'.'
name|'update'
op|'('
op|'('
name|'key'
op|','
name|'value'
op|')'
nl|'\n'
name|'for'
name|'key'
op|','
op|'('
name|'value'
op|','
name|'timestamp'
op|')'
name|'in'
nl|'\n'
name|'broker'
op|'.'
name|'metadata'
op|'.'
name|'iteritems'
op|'('
op|')'
name|'if'
name|'value'
op|'!='
string|"''"
op|')'
newline|'\n'
name|'headers'
op|'['
string|"'Content-Type'"
op|']'
op|'='
name|'out_content_type'
newline|'\n'
name|'return'
name|'HTTPNoContent'
op|'('
name|'request'
op|'='
name|'req'
op|','
name|'headers'
op|'='
name|'headers'
op|','
name|'charset'
op|'='
string|"'utf-8'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'public'
newline|'\n'
op|'@'
name|'timing_stats'
op|'('
op|')'
newline|'\n'
DECL|member|GET
name|'def'
name|'GET'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Handle HTTP GET request."""'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'drive'
op|','
name|'part'
op|','
name|'account'
op|'='
name|'req'
op|'.'
name|'split_path'
op|'('
number|'3'
op|')'
newline|'\n'
name|'validate_device_partition'
op|'('
name|'drive'
op|','
name|'part'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'body'
op|'='
name|'str'
op|'('
name|'err'
op|')'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'prefix'
op|'='
name|'get_param'
op|'('
name|'req'
op|','
string|"'prefix'"
op|')'
newline|'\n'
name|'delimiter'
op|'='
name|'get_param'
op|'('
name|'req'
op|','
string|"'delimiter'"
op|')'
newline|'\n'
name|'if'
name|'delimiter'
name|'and'
op|'('
name|'len'
op|'('
name|'delimiter'
op|')'
op|'>'
number|'1'
name|'or'
name|'ord'
op|'('
name|'delimiter'
op|')'
op|'>'
number|'254'
op|')'
op|':'
newline|'\n'
comment|'# delimiters can be made more flexible later'
nl|'\n'
indent|'            '
name|'return'
name|'HTTPPreconditionFailed'
op|'('
name|'body'
op|'='
string|"'Bad delimiter'"
op|')'
newline|'\n'
dedent|''
name|'limit'
op|'='
name|'ACCOUNT_LISTING_LIMIT'
newline|'\n'
name|'given_limit'
op|'='
name|'get_param'
op|'('
name|'req'
op|','
string|"'limit'"
op|')'
newline|'\n'
name|'if'
name|'given_limit'
name|'and'
name|'given_limit'
op|'.'
name|'isdigit'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'limit'
op|'='
name|'int'
op|'('
name|'given_limit'
op|')'
newline|'\n'
name|'if'
name|'limit'
op|'>'
name|'ACCOUNT_LISTING_LIMIT'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'HTTPPreconditionFailed'
op|'('
name|'request'
op|'='
name|'req'
op|','
nl|'\n'
name|'body'
op|'='
string|"'Maximum limit is %d'"
op|'%'
nl|'\n'
name|'ACCOUNT_LISTING_LIMIT'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'marker'
op|'='
name|'get_param'
op|'('
name|'req'
op|','
string|"'marker'"
op|','
string|"''"
op|')'
newline|'\n'
name|'end_marker'
op|'='
name|'get_param'
op|'('
name|'req'
op|','
string|"'end_marker'"
op|')'
newline|'\n'
name|'out_content_type'
op|','
name|'error'
op|'='
name|'account_listing_content_type'
op|'('
name|'req'
op|')'
newline|'\n'
name|'if'
name|'error'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'error'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'mount_check'
name|'and'
name|'not'
name|'check_mount'
op|'('
name|'self'
op|'.'
name|'root'
op|','
name|'drive'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPInsufficientStorage'
op|'('
name|'drive'
op|'='
name|'drive'
op|','
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'broker'
op|'='
name|'self'
op|'.'
name|'_get_account_broker'
op|'('
name|'drive'
op|','
name|'part'
op|','
name|'account'
op|','
nl|'\n'
name|'pending_timeout'
op|'='
number|'0.1'
op|','
nl|'\n'
name|'stale_reads_ok'
op|'='
name|'True'
op|')'
newline|'\n'
name|'if'
name|'broker'
op|'.'
name|'is_deleted'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_deleted_response'
op|'('
name|'broker'
op|','
name|'req'
op|','
name|'HTTPNotFound'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'account_listing_response'
op|'('
name|'account'
op|','
name|'req'
op|','
name|'out_content_type'
op|','
name|'broker'
op|','
nl|'\n'
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
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'public'
newline|'\n'
op|'@'
name|'replication'
newline|'\n'
op|'@'
name|'timing_stats'
op|'('
op|')'
newline|'\n'
DECL|member|REPLICATE
name|'def'
name|'REPLICATE'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Handle HTTP REPLICATE request.\n        Handler for RPC calls for account replication.\n        """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'post_args'
op|'='
name|'req'
op|'.'
name|'split_path'
op|'('
number|'3'
op|')'
newline|'\n'
name|'drive'
op|','
name|'partition'
op|','
name|'hash'
op|'='
name|'post_args'
newline|'\n'
name|'validate_device_partition'
op|'('
name|'drive'
op|','
name|'partition'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'body'
op|'='
name|'str'
op|'('
name|'err'
op|')'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'mount_check'
name|'and'
name|'not'
name|'check_mount'
op|'('
name|'self'
op|'.'
name|'root'
op|','
name|'drive'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPInsufficientStorage'
op|'('
name|'drive'
op|'='
name|'drive'
op|','
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'args'
op|'='
name|'json'
op|'.'
name|'load'
op|'('
name|'req'
op|'.'
name|'environ'
op|'['
string|"'wsgi.input'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'body'
op|'='
name|'str'
op|'('
name|'err'
op|')'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
name|'ret'
op|'='
name|'self'
op|'.'
name|'replicator_rpc'
op|'.'
name|'dispatch'
op|'('
name|'post_args'
op|','
name|'args'
op|')'
newline|'\n'
name|'ret'
op|'.'
name|'request'
op|'='
name|'req'
newline|'\n'
name|'return'
name|'ret'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'public'
newline|'\n'
op|'@'
name|'timing_stats'
op|'('
op|')'
newline|'\n'
DECL|member|POST
name|'def'
name|'POST'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Handle HTTP POST request."""'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'drive'
op|','
name|'part'
op|','
name|'account'
op|'='
name|'req'
op|'.'
name|'split_path'
op|'('
number|'3'
op|')'
newline|'\n'
name|'validate_device_partition'
op|'('
name|'drive'
op|','
name|'part'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'body'
op|'='
name|'str'
op|'('
name|'err'
op|')'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'if'
string|"'x-timestamp'"
name|'not'
name|'in'
name|'req'
op|'.'
name|'headers'
name|'or'
name|'not'
name|'check_float'
op|'('
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-timestamp'"
op|']'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'body'
op|'='
string|"'Missing or bad timestamp'"
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
nl|'\n'
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'mount_check'
name|'and'
name|'not'
name|'check_mount'
op|'('
name|'self'
op|'.'
name|'root'
op|','
name|'drive'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPInsufficientStorage'
op|'('
name|'drive'
op|'='
name|'drive'
op|','
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'broker'
op|'='
name|'self'
op|'.'
name|'_get_account_broker'
op|'('
name|'drive'
op|','
name|'part'
op|','
name|'account'
op|')'
newline|'\n'
name|'if'
name|'broker'
op|'.'
name|'is_deleted'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_deleted_response'
op|'('
name|'broker'
op|','
name|'req'
op|','
name|'HTTPNotFound'
op|')'
newline|'\n'
dedent|''
name|'timestamp'
op|'='
name|'normalize_timestamp'
op|'('
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-timestamp'"
op|']'
op|')'
newline|'\n'
name|'metadata'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'metadata'
op|'.'
name|'update'
op|'('
op|'('
name|'key'
op|','
op|'('
name|'value'
op|','
name|'timestamp'
op|')'
op|')'
nl|'\n'
name|'for'
name|'key'
op|','
name|'value'
name|'in'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'iteritems'
op|'('
op|')'
nl|'\n'
name|'if'
name|'key'
op|'.'
name|'lower'
op|'('
op|')'
op|'.'
name|'startswith'
op|'('
string|"'x-account-meta-'"
op|')'
op|')'
newline|'\n'
name|'if'
name|'metadata'
op|':'
newline|'\n'
indent|'            '
name|'broker'
op|'.'
name|'update_metadata'
op|'('
name|'metadata'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'HTTPNoContent'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
nl|'\n'
DECL|member|__call__
dedent|''
name|'def'
name|'__call__'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'start_time'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'txn_id'
op|'='
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-trans-id'"
op|','
name|'None'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'check_utf8'
op|'('
name|'req'
op|'.'
name|'path_info'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'res'
op|'='
name|'HTTPPreconditionFailed'
op|'('
name|'body'
op|'='
string|"'Invalid UTF8 or contains NULL'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
comment|'# disallow methods which are not publicly accessible'
nl|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'method'
op|'='
name|'getattr'
op|'('
name|'self'
op|','
name|'req'
op|'.'
name|'method'
op|')'
newline|'\n'
name|'getattr'
op|'('
name|'method'
op|','
string|"'publicly_accessible'"
op|')'
newline|'\n'
name|'replication_method'
op|'='
name|'getattr'
op|'('
name|'method'
op|','
string|"'replication'"
op|','
name|'False'
op|')'
newline|'\n'
name|'if'
op|'('
name|'self'
op|'.'
name|'replication_server'
name|'is'
name|'not'
name|'None'
name|'and'
nl|'\n'
name|'self'
op|'.'
name|'replication_server'
op|'!='
name|'replication_method'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'raise'
name|'AttributeError'
op|'('
string|"'Not allowed method.'"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'AttributeError'
op|':'
newline|'\n'
indent|'                    '
name|'res'
op|'='
name|'HTTPMethodNotAllowed'
op|'('
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'res'
op|'='
name|'method'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'HTTPException'
name|'as'
name|'error_response'
op|':'
newline|'\n'
indent|'                '
name|'res'
op|'='
name|'error_response'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'Timeout'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
name|'_'
op|'('
string|"'ERROR __call__ error with %(method)s'"
nl|'\n'
string|"' %(path)s '"
op|')'
op|','
nl|'\n'
op|'{'
string|"'method'"
op|':'
name|'req'
op|'.'
name|'method'
op|','
string|"'path'"
op|':'
name|'req'
op|'.'
name|'path'
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'HTTPInternalServerError'
op|'('
name|'body'
op|'='
name|'traceback'
op|'.'
name|'format_exc'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'trans_time'
op|'='
string|"'%.4f'"
op|'%'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'start_time'
op|')'
newline|'\n'
name|'additional_info'
op|'='
string|"''"
newline|'\n'
name|'if'
name|'res'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-container-timestamp'"
op|')'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'additional_info'
op|'+='
string|"'x-container-timestamp: %s'"
op|'%'
name|'res'
op|'.'
name|'headers'
op|'['
string|"'x-container-timestamp'"
op|']'
newline|'\n'
dedent|''
name|'log_message'
op|'='
string|'\'%s - - [%s] "%s %s" %s %s "%s" "%s" "%s" %s "%s"\''
op|'%'
op|'('
nl|'\n'
name|'req'
op|'.'
name|'remote_addr'
op|','
nl|'\n'
name|'time'
op|'.'
name|'strftime'
op|'('
string|"'%d/%b/%Y:%H:%M:%S +0000'"
op|','
name|'time'
op|'.'
name|'gmtime'
op|'('
op|')'
op|')'
op|','
nl|'\n'
name|'req'
op|'.'
name|'method'
op|','
name|'req'
op|'.'
name|'path'
op|','
nl|'\n'
name|'res'
op|'.'
name|'status'
op|'.'
name|'split'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|','
name|'res'
op|'.'
name|'content_length'
name|'or'
string|"'-'"
op|','
nl|'\n'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-trans-id'"
op|','
string|"'-'"
op|')'
op|','
nl|'\n'
name|'req'
op|'.'
name|'referer'
name|'or'
string|"'-'"
op|','
name|'req'
op|'.'
name|'user_agent'
name|'or'
string|"'-'"
op|','
nl|'\n'
name|'trans_time'
op|','
nl|'\n'
name|'additional_info'
op|')'
newline|'\n'
name|'if'
name|'req'
op|'.'
name|'method'
op|'.'
name|'upper'
op|'('
op|')'
op|'=='
string|"'REPLICATE'"
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'log_message'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'log_message'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'res'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|app_factory
dedent|''
dedent|''
name|'def'
name|'app_factory'
op|'('
name|'global_conf'
op|','
op|'**'
name|'local_conf'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""paste.deploy app factory for creating WSGI account server apps"""'
newline|'\n'
name|'conf'
op|'='
name|'global_conf'
op|'.'
name|'copy'
op|'('
op|')'
newline|'\n'
name|'conf'
op|'.'
name|'update'
op|'('
name|'local_conf'
op|')'
newline|'\n'
name|'return'
name|'AccountController'
op|'('
name|'conf'
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
