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
name|'import'
name|'re'
newline|'\n'
name|'import'
name|'sys'
newline|'\n'
name|'import'
name|'uuid'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'random'
newline|'\n'
name|'import'
name|'signal'
newline|'\n'
name|'import'
name|'socket'
newline|'\n'
name|'import'
name|'logging'
newline|'\n'
name|'from'
name|'contextlib'
name|'import'
name|'contextmanager'
newline|'\n'
name|'from'
name|'optparse'
name|'import'
name|'Values'
newline|'\n'
nl|'\n'
name|'import'
name|'eventlet'
newline|'\n'
name|'import'
name|'eventlet'
op|'.'
name|'pools'
newline|'\n'
name|'from'
name|'eventlet'
op|'.'
name|'green'
op|'.'
name|'httplib'
name|'import'
name|'CannotSendRequest'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'config_true_value'
op|','
name|'LogAdapter'
newline|'\n'
name|'import'
name|'swiftclient'
name|'as'
name|'client'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'direct_client'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'http'
name|'import'
name|'HTTP_CONFLICT'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'    '
name|'import'
name|'simplejson'
name|'as'
name|'json'
newline|'\n'
dedent|''
name|'except'
name|'ImportError'
op|':'
newline|'\n'
indent|'    '
name|'import'
name|'json'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|_func_on_containers
dedent|''
name|'def'
name|'_func_on_containers'
op|'('
name|'logger'
op|','
name|'conf'
op|','
name|'concurrency_key'
op|','
name|'func'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Run a function on each container with concurrency."""'
newline|'\n'
nl|'\n'
name|'bench'
op|'='
name|'Bench'
op|'('
name|'logger'
op|','
name|'conf'
op|','
op|'['
op|']'
op|')'
newline|'\n'
name|'pool'
op|'='
name|'eventlet'
op|'.'
name|'GreenPool'
op|'('
name|'int'
op|'('
name|'getattr'
op|'('
name|'conf'
op|','
name|'concurrency_key'
op|')'
op|')'
op|')'
newline|'\n'
name|'for'
name|'container'
name|'in'
name|'conf'
op|'.'
name|'containers'
op|':'
newline|'\n'
indent|'        '
name|'pool'
op|'.'
name|'spawn_n'
op|'('
name|'func'
op|','
name|'bench'
op|'.'
name|'url'
op|','
name|'bench'
op|'.'
name|'token'
op|','
name|'container'
op|')'
newline|'\n'
dedent|''
name|'pool'
op|'.'
name|'waitall'
op|'('
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|delete_containers
dedent|''
name|'def'
name|'delete_containers'
op|'('
name|'logger'
op|','
name|'conf'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Utility function to delete benchmark containers."""'
newline|'\n'
nl|'\n'
DECL|function|_deleter
name|'def'
name|'_deleter'
op|'('
name|'url'
op|','
name|'token'
op|','
name|'container'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'client'
op|'.'
name|'delete_container'
op|'('
name|'url'
op|','
name|'token'
op|','
name|'container'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'client'
op|'.'
name|'ClientException'
op|','
name|'e'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'e'
op|'.'
name|'http_status'
op|'!='
name|'HTTP_CONFLICT'
op|':'
newline|'\n'
indent|'                '
name|'logger'
op|'.'
name|'warn'
op|'('
string|'"Unable to delete container \'%s\'. "'
nl|'\n'
string|'"Got http status \'%d\'."'
nl|'\n'
op|'%'
op|'('
name|'container'
op|','
name|'e'
op|'.'
name|'http_status'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
dedent|''
name|'_func_on_containers'
op|'('
name|'logger'
op|','
name|'conf'
op|','
string|"'del_concurrency'"
op|','
name|'_deleter'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|create_containers
dedent|''
name|'def'
name|'create_containers'
op|'('
name|'logger'
op|','
name|'conf'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Utility function to create benchmark containers."""'
newline|'\n'
nl|'\n'
name|'_func_on_containers'
op|'('
name|'logger'
op|','
name|'conf'
op|','
string|"'put_concurrency'"
op|','
name|'client'
op|'.'
name|'put_container'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ConnectionPool
dedent|''
name|'class'
name|'ConnectionPool'
op|'('
name|'eventlet'
op|'.'
name|'pools'
op|'.'
name|'Pool'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'url'
op|','
name|'size'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'url'
op|'='
name|'url'
newline|'\n'
name|'eventlet'
op|'.'
name|'pools'
op|'.'
name|'Pool'
op|'.'
name|'__init__'
op|'('
name|'self'
op|','
name|'size'
op|','
name|'size'
op|')'
newline|'\n'
nl|'\n'
DECL|member|create
dedent|''
name|'def'
name|'create'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'client'
op|'.'
name|'http_connection'
op|'('
name|'self'
op|'.'
name|'url'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|BenchServer
dedent|''
dedent|''
name|'class'
name|'BenchServer'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    A BenchServer binds to an IP/port and listens for bench jobs.  A bench\n    job consists of the normal conf "dict" encoded in JSON, terminated with an\n    EOF.  The log level is at least INFO, but DEBUG may also be specified in\n    the conf dict.\n\n    The server will wait forever for jobs, running them one at a time.\n    """'
newline|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'logger'
op|','
name|'bind_ip'
op|','
name|'bind_port'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'logger'
op|'='
name|'logger'
newline|'\n'
name|'self'
op|'.'
name|'bind_ip'
op|'='
name|'bind_ip'
newline|'\n'
name|'self'
op|'.'
name|'bind_port'
op|'='
name|'int'
op|'('
name|'bind_port'
op|')'
newline|'\n'
nl|'\n'
DECL|member|run
dedent|''
name|'def'
name|'run'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'s'
op|'='
name|'socket'
op|'.'
name|'socket'
op|'('
name|'socket'
op|'.'
name|'AF_INET'
op|','
name|'socket'
op|'.'
name|'SOCK_STREAM'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
string|"'Binding to %s:%s'"
op|','
name|'self'
op|'.'
name|'bind_ip'
op|','
name|'self'
op|'.'
name|'bind_port'
op|')'
newline|'\n'
name|'s'
op|'.'
name|'bind'
op|'('
op|'('
name|'self'
op|'.'
name|'bind_ip'
op|','
name|'self'
op|'.'
name|'bind_port'
op|')'
op|')'
newline|'\n'
name|'s'
op|'.'
name|'listen'
op|'('
number|'20'
op|')'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'client'
op|','
name|'address'
op|'='
name|'s'
op|'.'
name|'accept'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
string|"'Accepting connection from %s:%s'"
op|','
op|'*'
name|'address'
op|')'
newline|'\n'
name|'client_file'
op|'='
name|'client'
op|'.'
name|'makefile'
op|'('
string|"'rb+'"
op|','
number|'1'
op|')'
newline|'\n'
name|'json_data'
op|'='
name|'client_file'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'conf'
op|'='
name|'Values'
op|'('
name|'json'
op|'.'
name|'loads'
op|'('
name|'json_data'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
nl|'\n'
string|"'Starting run for %s:%s [put/get/del_concurrency: %s/%s/%s, '"
nl|'\n'
string|"'num_objects: %s, num_gets: %s]'"
op|','
name|'address'
op|'['
number|'0'
op|']'
op|','
name|'address'
op|'['
number|'1'
op|']'
op|','
nl|'\n'
name|'conf'
op|'.'
name|'put_concurrency'
op|','
name|'conf'
op|'.'
name|'get_concurrency'
op|','
nl|'\n'
name|'conf'
op|'.'
name|'del_concurrency'
op|','
name|'conf'
op|'.'
name|'num_objects'
op|','
name|'conf'
op|'.'
name|'num_gets'
op|')'
newline|'\n'
nl|'\n'
name|'logger'
op|'='
name|'logging'
op|'.'
name|'getLogger'
op|'('
string|"'bench-server'"
op|')'
newline|'\n'
name|'level'
op|'='
name|'logging'
op|'.'
name|'DEBUG'
name|'if'
name|'conf'
op|'.'
name|'log_level'
op|'.'
name|'lower'
op|'('
op|')'
op|'=='
string|"'debug'"
name|'else'
name|'logging'
op|'.'
name|'INFO'
newline|'\n'
name|'logger'
op|'.'
name|'setLevel'
op|'('
name|'level'
op|')'
newline|'\n'
name|'loghandler'
op|'='
name|'logging'
op|'.'
name|'StreamHandler'
op|'('
name|'client_file'
op|')'
newline|'\n'
name|'logformat'
op|'='
name|'logging'
op|'.'
name|'Formatter'
op|'('
nl|'\n'
string|"'%(server)s %(asctime)s %(levelname)s %(message)s'"
op|')'
newline|'\n'
name|'loghandler'
op|'.'
name|'setFormatter'
op|'('
name|'logformat'
op|')'
newline|'\n'
name|'logger'
op|'.'
name|'addHandler'
op|'('
name|'loghandler'
op|')'
newline|'\n'
name|'logger'
op|'='
name|'LogAdapter'
op|'('
name|'logger'
op|','
string|"'swift-bench-server'"
op|')'
newline|'\n'
nl|'\n'
name|'controller'
op|'='
name|'BenchController'
op|'('
name|'logger'
op|','
name|'conf'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'controller'
op|'.'
name|'run'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'socket'
op|'.'
name|'error'
op|':'
newline|'\n'
indent|'                '
name|'logger'
op|'.'
name|'warning'
op|'('
string|"'Socket error'"
op|','
name|'exc_info'
op|'='
number|'1'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'logger'
op|'.'
name|'logger'
op|'.'
name|'removeHandler'
op|'('
name|'loghandler'
op|')'
newline|'\n'
name|'client_file'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
name|'client'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
string|"'...bench run completed; waiting for next run.'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|Bench
dedent|''
dedent|''
dedent|''
name|'class'
name|'Bench'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'logger'
op|','
name|'conf'
op|','
name|'names'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'logger'
op|'='
name|'logger'
newline|'\n'
name|'self'
op|'.'
name|'aborted'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'user'
op|'='
name|'conf'
op|'.'
name|'user'
newline|'\n'
name|'self'
op|'.'
name|'key'
op|'='
name|'conf'
op|'.'
name|'key'
newline|'\n'
name|'self'
op|'.'
name|'auth_url'
op|'='
name|'conf'
op|'.'
name|'auth'
newline|'\n'
name|'self'
op|'.'
name|'use_proxy'
op|'='
name|'config_true_value'
op|'('
name|'conf'
op|'.'
name|'use_proxy'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auth_version'
op|'='
name|'conf'
op|'.'
name|'auth_version'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
string|'"Auth version: %s"'
op|'%'
name|'self'
op|'.'
name|'auth_version'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'use_proxy'
op|':'
newline|'\n'
indent|'            '
name|'url'
op|','
name|'token'
op|'='
name|'client'
op|'.'
name|'get_auth'
op|'('
name|'self'
op|'.'
name|'auth_url'
op|','
name|'self'
op|'.'
name|'user'
op|','
name|'self'
op|'.'
name|'key'
op|','
nl|'\n'
name|'auth_version'
op|'='
name|'self'
op|'.'
name|'auth_version'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'token'
op|'='
name|'token'
newline|'\n'
name|'self'
op|'.'
name|'account'
op|'='
name|'url'
op|'.'
name|'split'
op|'('
string|"'/'"
op|')'
op|'['
op|'-'
number|'1'
op|']'
newline|'\n'
name|'if'
name|'conf'
op|'.'
name|'url'
op|'=='
string|"''"
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'url'
op|'='
name|'url'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'url'
op|'='
name|'conf'
op|'.'
name|'url'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'token'
op|'='
string|"'SlapChop!'"
newline|'\n'
name|'self'
op|'.'
name|'account'
op|'='
name|'conf'
op|'.'
name|'account'
newline|'\n'
name|'self'
op|'.'
name|'url'
op|'='
name|'conf'
op|'.'
name|'url'
newline|'\n'
name|'self'
op|'.'
name|'ip'
op|','
name|'self'
op|'.'
name|'port'
op|'='
name|'self'
op|'.'
name|'url'
op|'.'
name|'split'
op|'('
string|"'/'"
op|')'
op|'['
number|'2'
op|']'
op|'.'
name|'split'
op|'('
string|"':'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'object_size'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'object_size'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'object_sources'
op|'='
name|'conf'
op|'.'
name|'object_sources'
newline|'\n'
name|'self'
op|'.'
name|'lower_object_size'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'lower_object_size'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'upper_object_size'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'upper_object_size'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'files'
op|'='
op|'['
op|']'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'object_sources'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'object_sources'
op|'='
name|'self'
op|'.'
name|'object_sources'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'files'
op|'='
op|'['
name|'file'
op|'('
name|'f'
op|','
string|"'rb'"
op|')'
op|'.'
name|'read'
op|'('
op|')'
name|'for'
name|'f'
name|'in'
name|'self'
op|'.'
name|'object_sources'
op|']'
newline|'\n'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'put_concurrency'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'put_concurrency'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'get_concurrency'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get_concurrency'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'del_concurrency'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'del_concurrency'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'total_objects'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'num_objects'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'total_gets'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'num_gets'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'timeout'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'timeout'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'devices'
op|'='
name|'conf'
op|'.'
name|'devices'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'names'
op|'='
name|'names'
newline|'\n'
name|'self'
op|'.'
name|'conn_pool'
op|'='
name|'ConnectionPool'
op|'('
name|'self'
op|'.'
name|'url'
op|','
nl|'\n'
name|'max'
op|'('
name|'self'
op|'.'
name|'put_concurrency'
op|','
nl|'\n'
name|'self'
op|'.'
name|'get_concurrency'
op|','
nl|'\n'
name|'self'
op|'.'
name|'del_concurrency'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_log_status
dedent|''
name|'def'
name|'_log_status'
op|'('
name|'self'
op|','
name|'title'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'total'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'self'
op|'.'
name|'beginbeat'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|"'%(complete)s %(title)s [%(fail)s failures], '"
nl|'\n'
string|"'%(rate).01f/s'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'title'"
op|':'
name|'title'
op|','
string|"'complete'"
op|':'
name|'self'
op|'.'
name|'complete'
op|','
nl|'\n'
string|"'fail'"
op|':'
name|'self'
op|'.'
name|'failures'
op|','
nl|'\n'
string|"'rate'"
op|':'
op|'('
name|'float'
op|'('
name|'self'
op|'.'
name|'complete'
op|')'
op|'/'
name|'total'
op|')'
op|'}'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'contextmanager'
newline|'\n'
DECL|member|connection
name|'def'
name|'connection'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'hc'
op|'='
name|'self'
op|'.'
name|'conn_pool'
op|'.'
name|'get'
op|'('
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'yield'
name|'hc'
newline|'\n'
dedent|''
name|'except'
name|'CannotSendRequest'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|'"CannotSendRequest.  Skipping..."'
op|')'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'hc'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'                    '
name|'pass'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'failures'
op|'+='
number|'1'
newline|'\n'
name|'hc'
op|'='
name|'self'
op|'.'
name|'conn_pool'
op|'.'
name|'create'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'conn_pool'
op|'.'
name|'put'
op|'('
name|'hc'
op|')'
newline|'\n'
nl|'\n'
DECL|member|run
dedent|''
dedent|''
name|'def'
name|'run'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'pool'
op|'='
name|'eventlet'
op|'.'
name|'GreenPool'
op|'('
name|'self'
op|'.'
name|'concurrency'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'beginbeat'
op|'='
name|'self'
op|'.'
name|'heartbeat'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'heartbeat'
op|'-='
number|'13'
comment|'# just to get the first report quicker'
newline|'\n'
name|'self'
op|'.'
name|'failures'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'complete'
op|'='
number|'0'
newline|'\n'
name|'for'
name|'i'
name|'in'
name|'xrange'
op|'('
name|'self'
op|'.'
name|'total'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'self'
op|'.'
name|'aborted'
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
name|'pool'
op|'.'
name|'spawn_n'
op|'('
name|'self'
op|'.'
name|'_run'
op|','
name|'i'
op|')'
newline|'\n'
dedent|''
name|'pool'
op|'.'
name|'waitall'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_log_status'
op|'('
name|'self'
op|'.'
name|'msg'
op|'+'
string|"' **FINAL**'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|_run
dedent|''
name|'def'
name|'_run'
op|'('
name|'self'
op|','
name|'thread'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DistributedBenchController
dedent|''
dedent|''
name|'class'
name|'DistributedBenchController'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    This class manages a distributed swift-bench run.  For this Controller\n    class to make sense, the conf.bench_clients list must contain at least one\n    entry.\n\n    The idea is to split the configured load between one or more\n    swift-bench-client processes, each of which use eventlet for concurrency.\n    We deliberately take a simple, naive approach with these limitations:\n        1) Concurrency, num_objects, and num_gets are spread evenly between the\n           swift-bench-client processes.  With a low concurrency to\n           swift-bench-client count ratio, rounding may result in a greater\n           than desired aggregate concurrency.\n        2) Each swift-bench-client process runs independently so some may\n           finish up before others, i.e. the target aggregate concurrency is\n           not necessarily present the whole time.  This may bias aggregate\n           reported rates lower than a more efficient architecture.\n        3) Because of #2, some swift-bench-client processes may be running GETs\n           while others are still runinng their PUTs.  Because of this\n           potential skew, distributed runs will not isolate one operation at a\n           time like a single swift-bench run will.\n        3) Reported aggregate rates are simply the sum of each\n           swift-bench-client process reported FINAL number.  That\'s probably\n           inaccurate somehow.\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'logger'
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
name|'logger'
newline|'\n'
comment|'# ... INFO 1000 PUTS **FINAL** [0 failures], 34.9/s'
nl|'\n'
name|'self'
op|'.'
name|'final_re'
op|'='
name|'re'
op|'.'
name|'compile'
op|'('
nl|'\n'
string|"'INFO (\\d+) (.*) \\*\\*FINAL\\*\\* \\[(\\d+) failures\\], (\\d+\\.\\d+)/s'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'clients'
op|'='
name|'conf'
op|'.'
name|'bench_clients'
newline|'\n'
name|'del'
name|'conf'
op|'.'
name|'bench_clients'
newline|'\n'
name|'for'
name|'k'
name|'in'
op|'['
string|"'put_concurrency'"
op|','
string|"'get_concurrency'"
op|','
string|"'del_concurrency'"
op|','
nl|'\n'
string|"'num_objects'"
op|','
string|"'num_gets'"
op|']'
op|':'
newline|'\n'
indent|'            '
name|'setattr'
op|'('
name|'conf'
op|','
name|'k'
op|','
name|'max'
op|'('
number|'1'
op|','
name|'int'
op|'('
name|'getattr'
op|'('
name|'conf'
op|','
name|'k'
op|')'
op|')'
op|'/'
name|'len'
op|'('
name|'self'
op|'.'
name|'clients'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'conf'
op|'='
name|'conf'
newline|'\n'
nl|'\n'
DECL|member|run
dedent|''
name|'def'
name|'run'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'eventlet'
op|'.'
name|'patcher'
op|'.'
name|'monkey_patch'
op|'('
name|'socket'
op|'='
name|'True'
op|')'
newline|'\n'
name|'pool'
op|'='
name|'eventlet'
op|'.'
name|'GreenPool'
op|'('
name|'size'
op|'='
name|'len'
op|'('
name|'self'
op|'.'
name|'clients'
op|')'
op|')'
newline|'\n'
name|'pile'
op|'='
name|'eventlet'
op|'.'
name|'GreenPile'
op|'('
name|'pool'
op|')'
newline|'\n'
name|'for'
name|'client'
name|'in'
name|'self'
op|'.'
name|'clients'
op|':'
newline|'\n'
indent|'            '
name|'pile'
op|'.'
name|'spawn'
op|'('
name|'self'
op|'.'
name|'do_run'
op|','
name|'client'
op|')'
newline|'\n'
dedent|''
name|'results'
op|'='
op|'{'
nl|'\n'
string|"'PUTS'"
op|':'
name|'dict'
op|'('
name|'count'
op|'='
number|'0'
op|','
name|'failures'
op|'='
number|'0'
op|','
name|'rate'
op|'='
number|'0.0'
op|')'
op|','
nl|'\n'
string|"'GETS'"
op|':'
name|'dict'
op|'('
name|'count'
op|'='
number|'0'
op|','
name|'failures'
op|'='
number|'0'
op|','
name|'rate'
op|'='
number|'0.0'
op|')'
op|','
nl|'\n'
string|"'DEL'"
op|':'
name|'dict'
op|'('
name|'count'
op|'='
number|'0'
op|','
name|'failures'
op|'='
number|'0'
op|','
name|'rate'
op|'='
number|'0.0'
op|')'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'for'
name|'result'
name|'in'
name|'pile'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'k'
op|','
name|'v'
name|'in'
name|'result'
op|'.'
name|'iteritems'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'target'
op|'='
name|'results'
op|'['
name|'k'
op|']'
newline|'\n'
name|'target'
op|'['
string|"'count'"
op|']'
op|'+='
name|'int'
op|'('
name|'v'
op|'['
string|"'count'"
op|']'
op|')'
newline|'\n'
name|'target'
op|'['
string|"'failures'"
op|']'
op|'+='
name|'int'
op|'('
name|'v'
op|'['
string|"'failures'"
op|']'
op|')'
newline|'\n'
name|'target'
op|'['
string|"'rate'"
op|']'
op|'+='
name|'float'
op|'('
name|'v'
op|'['
string|"'rate'"
op|']'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'for'
name|'k'
name|'in'
op|'['
string|"'PUTS'"
op|','
string|"'GETS'"
op|','
string|"'DEL'"
op|']'
op|':'
newline|'\n'
indent|'            '
name|'v'
op|'='
name|'results'
op|'['
name|'k'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
string|"'%d %s **FINAL** [%d failures], %.1f/s'"
op|'%'
op|'('
nl|'\n'
name|'v'
op|'['
string|"'count'"
op|']'
op|','
name|'k'
op|','
name|'v'
op|'['
string|"'failures'"
op|']'
op|','
name|'v'
op|'['
string|"'rate'"
op|']'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|do_run
dedent|''
dedent|''
name|'def'
name|'do_run'
op|'('
name|'self'
op|','
name|'client'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'s'
op|'='
name|'socket'
op|'.'
name|'socket'
op|'('
name|'socket'
op|'.'
name|'AF_INET'
op|','
name|'socket'
op|'.'
name|'SOCK_STREAM'
op|')'
newline|'\n'
name|'ip'
op|','
name|'port'
op|'='
name|'client'
op|'.'
name|'split'
op|'('
string|"':'"
op|')'
newline|'\n'
name|'s'
op|'.'
name|'connect'
op|'('
op|'('
name|'ip'
op|','
name|'int'
op|'('
name|'port'
op|')'
op|')'
op|')'
newline|'\n'
name|'s'
op|'.'
name|'sendall'
op|'('
name|'json'
op|'.'
name|'dumps'
op|'('
name|'self'
op|'.'
name|'conf'
op|'.'
name|'__dict__'
op|')'
op|')'
newline|'\n'
name|'s'
op|'.'
name|'shutdown'
op|'('
name|'socket'
op|'.'
name|'SHUT_WR'
op|')'
newline|'\n'
name|'s_file'
op|'='
name|'s'
op|'.'
name|'makefile'
op|'('
string|"'rb'"
op|','
number|'1'
op|')'
newline|'\n'
name|'result'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'line'
name|'in'
name|'s_file'
op|':'
newline|'\n'
indent|'            '
name|'match'
op|'='
name|'self'
op|'.'
name|'final_re'
op|'.'
name|'search'
op|'('
name|'line'
op|')'
newline|'\n'
name|'if'
name|'match'
op|':'
newline|'\n'
indent|'                '
name|'g'
op|'='
name|'match'
op|'.'
name|'groups'
op|'('
op|')'
newline|'\n'
name|'result'
op|'['
name|'g'
op|'['
number|'1'
op|']'
op|']'
op|'='
op|'{'
nl|'\n'
string|"'count'"
op|':'
name|'g'
op|'['
number|'0'
op|']'
op|','
nl|'\n'
string|"'failures'"
op|':'
name|'g'
op|'['
number|'2'
op|']'
op|','
nl|'\n'
string|"'rate'"
op|':'
name|'g'
op|'['
number|'3'
op|']'
op|','
nl|'\n'
op|'}'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'sys'
op|'.'
name|'stderr'
op|'.'
name|'write'
op|'('
string|"'%s %s'"
op|'%'
op|'('
name|'client'
op|','
name|'line'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'result'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|BenchController
dedent|''
dedent|''
name|'class'
name|'BenchController'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'logger'
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
name|'logger'
newline|'\n'
name|'self'
op|'.'
name|'conf'
op|'='
name|'conf'
newline|'\n'
name|'self'
op|'.'
name|'names'
op|'='
op|'['
op|']'
newline|'\n'
name|'self'
op|'.'
name|'delete'
op|'='
name|'config_true_value'
op|'('
name|'conf'
op|'.'
name|'delete'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'gets'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'num_gets'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'aborted'
op|'='
name|'False'
newline|'\n'
nl|'\n'
DECL|member|sigint1
dedent|''
name|'def'
name|'sigint1'
op|'('
name|'self'
op|','
name|'signum'
op|','
name|'frame'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'self'
op|'.'
name|'delete'
op|':'
newline|'\n'
indent|'            '
name|'print'
op|'>>'
name|'sys'
op|'.'
name|'stderr'
op|','
op|'('
nl|'\n'
string|"'SIGINT received; finishing up and running DELETE.\\n'"
nl|'\n'
string|"'Send one more SIGINT to exit *immediately*.'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'aborted'
op|'='
name|'True'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'running'
name|'and'
name|'not'
name|'isinstance'
op|'('
name|'self'
op|'.'
name|'running'
op|','
name|'BenchDELETE'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'running'
op|'.'
name|'aborted'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'signal'
op|'.'
name|'signal'
op|'('
name|'signal'
op|'.'
name|'SIGINT'
op|','
name|'self'
op|'.'
name|'sigint2'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'sigint2'
op|'('
name|'signum'
op|','
name|'frame'
op|')'
newline|'\n'
nl|'\n'
DECL|member|sigint2
dedent|''
dedent|''
name|'def'
name|'sigint2'
op|'('
name|'self'
op|','
name|'signum'
op|','
name|'frame'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'sys'
op|'.'
name|'exit'
op|'('
string|"'Final SIGINT received.'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|run
dedent|''
name|'def'
name|'run'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'signal'
op|'.'
name|'signal'
op|'('
name|'signal'
op|'.'
name|'SIGINT'
op|','
name|'self'
op|'.'
name|'sigint1'
op|')'
newline|'\n'
name|'puts'
op|'='
name|'BenchPUT'
op|'('
name|'self'
op|'.'
name|'logger'
op|','
name|'self'
op|'.'
name|'conf'
op|','
name|'self'
op|'.'
name|'names'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'running'
op|'='
name|'puts'
newline|'\n'
name|'puts'
op|'.'
name|'run'
op|'('
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'gets'
name|'and'
name|'not'
name|'self'
op|'.'
name|'aborted'
op|':'
newline|'\n'
indent|'            '
name|'gets'
op|'='
name|'BenchGET'
op|'('
name|'self'
op|'.'
name|'logger'
op|','
name|'self'
op|'.'
name|'conf'
op|','
name|'self'
op|'.'
name|'names'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'running'
op|'='
name|'gets'
newline|'\n'
name|'gets'
op|'.'
name|'run'
op|'('
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'delete'
op|':'
newline|'\n'
indent|'            '
name|'dels'
op|'='
name|'BenchDELETE'
op|'('
name|'self'
op|'.'
name|'logger'
op|','
name|'self'
op|'.'
name|'conf'
op|','
name|'self'
op|'.'
name|'names'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'running'
op|'='
name|'dels'
newline|'\n'
name|'dels'
op|'.'
name|'run'
op|'('
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|BenchDELETE
dedent|''
dedent|''
dedent|''
name|'class'
name|'BenchDELETE'
op|'('
name|'Bench'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'logger'
op|','
name|'conf'
op|','
name|'names'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'Bench'
op|'.'
name|'__init__'
op|'('
name|'self'
op|','
name|'logger'
op|','
name|'conf'
op|','
name|'names'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'concurrency'
op|'='
name|'self'
op|'.'
name|'del_concurrency'
newline|'\n'
name|'self'
op|'.'
name|'total'
op|'='
name|'len'
op|'('
name|'names'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'msg'
op|'='
string|"'DEL'"
newline|'\n'
nl|'\n'
DECL|member|_run
dedent|''
name|'def'
name|'_run'
op|'('
name|'self'
op|','
name|'thread'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'self'
op|'.'
name|'heartbeat'
op|'>='
number|'15'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'heartbeat'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_log_status'
op|'('
string|"'DEL'"
op|')'
newline|'\n'
dedent|''
name|'device'
op|','
name|'partition'
op|','
name|'name'
op|','
name|'container_name'
op|'='
name|'self'
op|'.'
name|'names'
op|'.'
name|'pop'
op|'('
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'connection'
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
name|'if'
name|'self'
op|'.'
name|'use_proxy'
op|':'
newline|'\n'
indent|'                    '
name|'client'
op|'.'
name|'delete_object'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
nl|'\n'
name|'container_name'
op|','
name|'name'
op|','
name|'http_conn'
op|'='
name|'conn'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'node'
op|'='
op|'{'
string|"'ip'"
op|':'
name|'self'
op|'.'
name|'ip'
op|','
string|"'port'"
op|':'
name|'self'
op|'.'
name|'port'
op|','
string|"'device'"
op|':'
name|'device'
op|'}'
newline|'\n'
name|'direct_client'
op|'.'
name|'direct_delete_object'
op|'('
name|'node'
op|','
name|'partition'
op|','
nl|'\n'
name|'self'
op|'.'
name|'account'
op|','
nl|'\n'
name|'container_name'
op|','
name|'name'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'client'
op|'.'
name|'ClientException'
op|','
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'str'
op|'('
name|'e'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'failures'
op|'+='
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'complete'
op|'+='
number|'1'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|BenchGET
dedent|''
dedent|''
name|'class'
name|'BenchGET'
op|'('
name|'Bench'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'logger'
op|','
name|'conf'
op|','
name|'names'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'Bench'
op|'.'
name|'__init__'
op|'('
name|'self'
op|','
name|'logger'
op|','
name|'conf'
op|','
name|'names'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'concurrency'
op|'='
name|'self'
op|'.'
name|'get_concurrency'
newline|'\n'
name|'self'
op|'.'
name|'total'
op|'='
name|'self'
op|'.'
name|'total_gets'
newline|'\n'
name|'self'
op|'.'
name|'msg'
op|'='
string|"'GETS'"
newline|'\n'
nl|'\n'
DECL|member|_run
dedent|''
name|'def'
name|'_run'
op|'('
name|'self'
op|','
name|'thread'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'self'
op|'.'
name|'heartbeat'
op|'>='
number|'15'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'heartbeat'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_log_status'
op|'('
string|"'GETS'"
op|')'
newline|'\n'
dedent|''
name|'device'
op|','
name|'partition'
op|','
name|'name'
op|','
name|'container_name'
op|'='
name|'random'
op|'.'
name|'choice'
op|'('
name|'self'
op|'.'
name|'names'
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'connection'
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
name|'if'
name|'self'
op|'.'
name|'use_proxy'
op|':'
newline|'\n'
indent|'                    '
name|'client'
op|'.'
name|'get_object'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
nl|'\n'
name|'container_name'
op|','
name|'name'
op|','
name|'http_conn'
op|'='
name|'conn'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'node'
op|'='
op|'{'
string|"'ip'"
op|':'
name|'self'
op|'.'
name|'ip'
op|','
string|"'port'"
op|':'
name|'self'
op|'.'
name|'port'
op|','
string|"'device'"
op|':'
name|'device'
op|'}'
newline|'\n'
name|'direct_client'
op|'.'
name|'direct_get_object'
op|'('
name|'node'
op|','
name|'partition'
op|','
nl|'\n'
name|'self'
op|'.'
name|'account'
op|','
nl|'\n'
name|'container_name'
op|','
name|'name'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'client'
op|'.'
name|'ClientException'
op|','
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'str'
op|'('
name|'e'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'failures'
op|'+='
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'complete'
op|'+='
number|'1'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|BenchPUT
dedent|''
dedent|''
name|'class'
name|'BenchPUT'
op|'('
name|'Bench'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'logger'
op|','
name|'conf'
op|','
name|'names'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'Bench'
op|'.'
name|'__init__'
op|'('
name|'self'
op|','
name|'logger'
op|','
name|'conf'
op|','
name|'names'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'concurrency'
op|'='
name|'self'
op|'.'
name|'put_concurrency'
newline|'\n'
name|'self'
op|'.'
name|'total'
op|'='
name|'self'
op|'.'
name|'total_objects'
newline|'\n'
name|'self'
op|'.'
name|'msg'
op|'='
string|"'PUTS'"
newline|'\n'
name|'self'
op|'.'
name|'containers'
op|'='
name|'conf'
op|'.'
name|'containers'
newline|'\n'
nl|'\n'
DECL|member|_run
dedent|''
name|'def'
name|'_run'
op|'('
name|'self'
op|','
name|'thread'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'self'
op|'.'
name|'heartbeat'
op|'>='
number|'15'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'heartbeat'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_log_status'
op|'('
string|"'PUTS'"
op|')'
newline|'\n'
dedent|''
name|'name'
op|'='
name|'uuid'
op|'.'
name|'uuid4'
op|'('
op|')'
op|'.'
name|'hex'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'object_sources'
op|':'
newline|'\n'
indent|'            '
name|'source'
op|'='
name|'random'
op|'.'
name|'choice'
op|'('
name|'self'
op|'.'
name|'files'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'self'
op|'.'
name|'upper_object_size'
op|'>'
name|'self'
op|'.'
name|'lower_object_size'
op|':'
newline|'\n'
indent|'            '
name|'source'
op|'='
string|"'0'"
op|'*'
name|'random'
op|'.'
name|'randint'
op|'('
name|'self'
op|'.'
name|'lower_object_size'
op|','
nl|'\n'
name|'self'
op|'.'
name|'upper_object_size'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'source'
op|'='
string|"'0'"
op|'*'
name|'self'
op|'.'
name|'object_size'
newline|'\n'
dedent|''
name|'device'
op|'='
name|'random'
op|'.'
name|'choice'
op|'('
name|'self'
op|'.'
name|'devices'
op|')'
newline|'\n'
name|'partition'
op|'='
name|'str'
op|'('
name|'random'
op|'.'
name|'randint'
op|'('
number|'1'
op|','
number|'3000'
op|')'
op|')'
newline|'\n'
name|'container_name'
op|'='
name|'random'
op|'.'
name|'choice'
op|'('
name|'self'
op|'.'
name|'containers'
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'connection'
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
name|'if'
name|'self'
op|'.'
name|'use_proxy'
op|':'
newline|'\n'
indent|'                    '
name|'client'
op|'.'
name|'put_object'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
nl|'\n'
name|'container_name'
op|','
name|'name'
op|','
name|'source'
op|','
nl|'\n'
name|'content_length'
op|'='
name|'len'
op|'('
name|'source'
op|')'
op|','
nl|'\n'
name|'http_conn'
op|'='
name|'conn'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'node'
op|'='
op|'{'
string|"'ip'"
op|':'
name|'self'
op|'.'
name|'ip'
op|','
string|"'port'"
op|':'
name|'self'
op|'.'
name|'port'
op|','
string|"'device'"
op|':'
name|'device'
op|'}'
newline|'\n'
name|'direct_client'
op|'.'
name|'direct_put_object'
op|'('
name|'node'
op|','
name|'partition'
op|','
nl|'\n'
name|'self'
op|'.'
name|'account'
op|','
nl|'\n'
name|'container_name'
op|','
name|'name'
op|','
nl|'\n'
name|'source'
op|','
nl|'\n'
name|'content_length'
op|'='
name|'len'
op|'('
name|'source'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'client'
op|'.'
name|'ClientException'
op|','
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'str'
op|'('
name|'e'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'failures'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'names'
op|'.'
name|'append'
op|'('
op|'('
name|'device'
op|','
name|'partition'
op|','
name|'name'
op|','
name|'container_name'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'complete'
op|'+='
number|'1'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
