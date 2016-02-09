begin_unit
comment|'# Copyright (c) 2013 OpenStack Foundation'
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
name|'json'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'shutil'
newline|'\n'
name|'import'
name|'tempfile'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'import'
name|'uuid'
newline|'\n'
name|'import'
name|'mock'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'swob'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'middleware'
name|'import'
name|'container_sync'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'base'
name|'import'
name|'_get_cache_key'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'info'
name|'import'
name|'InfoController'
newline|'\n'
nl|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
name|'import'
name|'FakeLogger'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FakeApp
name|'class'
name|'FakeApp'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__call__
indent|'    '
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
name|'if'
name|'env'
op|'.'
name|'get'
op|'('
string|"'PATH_INFO'"
op|')'
op|'=='
string|"'/info'"
op|':'
newline|'\n'
indent|'            '
name|'controller'
op|'='
name|'InfoController'
op|'('
nl|'\n'
name|'app'
op|'='
name|'None'
op|','
name|'version'
op|'='
name|'None'
op|','
name|'expose_info'
op|'='
name|'True'
op|','
nl|'\n'
name|'disallowed_sections'
op|'='
op|'['
op|']'
op|','
name|'admin_key'
op|'='
name|'None'
op|')'
newline|'\n'
name|'handler'
op|'='
name|'getattr'
op|'('
name|'controller'
op|','
name|'env'
op|'.'
name|'get'
op|'('
string|"'REQUEST_METHOD'"
op|')'
op|')'
newline|'\n'
name|'return'
name|'handler'
op|'('
name|'swob'
op|'.'
name|'Request'
op|'('
name|'env'
op|')'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'env'
op|'.'
name|'get'
op|'('
string|"'swift.authorize_override'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'body'
op|'='
string|"'Response to Authorized Request'"
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'body'
op|'='
string|"'Pass-Through Response'"
newline|'\n'
dedent|''
name|'headers'
op|'='
op|'['
op|'('
string|"'Content-Length'"
op|','
name|'str'
op|'('
name|'len'
op|'('
name|'body'
op|')'
op|')'
op|')'
op|']'
newline|'\n'
name|'if'
string|"'HTTP_X_TIMESTAMP'"
name|'in'
name|'env'
op|':'
newline|'\n'
indent|'            '
name|'headers'
op|'.'
name|'append'
op|'('
op|'('
string|"'X-Timestamp'"
op|','
name|'env'
op|'['
string|"'HTTP_X_TIMESTAMP'"
op|']'
op|')'
op|')'
newline|'\n'
dedent|''
name|'start_response'
op|'('
string|"'200 OK'"
op|','
name|'headers'
op|')'
newline|'\n'
name|'return'
name|'body'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestContainerSync
dedent|''
dedent|''
name|'class'
name|'TestContainerSync'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|setUp
indent|'    '
name|'def'
name|'setUp'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'tempdir'
op|'='
name|'tempfile'
op|'.'
name|'mkdtemp'
op|'('
op|')'
newline|'\n'
name|'with'
name|'open'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'tempdir'
op|','
string|"'container-sync-realms.conf'"
op|')'
op|','
nl|'\n'
string|"'w'"
op|')'
name|'as'
name|'fp'
op|':'
newline|'\n'
indent|'            '
name|'fp'
op|'.'
name|'write'
op|'('
string|"'''\n[US]\nkey = 9ff3b71c849749dbaec4ccdd3cbab62b\nkey2 = 1a0a5a0cbd66448084089304442d6776\ncluster_dfw1 = http://dfw1.host/v1/\n            '''"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'app'
op|'='
name|'FakeApp'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'conf'
op|'='
op|'{'
string|"'swift_dir'"
op|':'
name|'self'
op|'.'
name|'tempdir'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'sync'
op|'='
name|'container_sync'
op|'.'
name|'ContainerSync'
op|'('
name|'self'
op|'.'
name|'app'
op|','
name|'self'
op|'.'
name|'conf'
op|')'
newline|'\n'
nl|'\n'
DECL|function|tearDown
dedent|''
name|'def'
name|'tearDown'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'shutil'
op|'.'
name|'rmtree'
op|'('
name|'self'
op|'.'
name|'tempdir'
op|','
name|'ignore_errors'
op|'='
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|function|test_current_not_set
dedent|''
name|'def'
name|'test_current_not_set'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|"# no 'current' option set by default"
nl|'\n'
indent|'        '
name|'self'
op|'.'
name|'assertIsNone'
op|'('
name|'self'
op|'.'
name|'sync'
op|'.'
name|'realm'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertIsNone'
op|'('
name|'self'
op|'.'
name|'sync'
op|'.'
name|'cluster'
op|')'
newline|'\n'
name|'info'
op|'='
op|'{'
op|'}'
newline|'\n'
nl|'\n'
DECL|function|capture_swift_info
name|'def'
name|'capture_swift_info'
op|'('
name|'key'
op|','
op|'**'
name|'options'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'info'
op|'['
name|'key'
op|']'
op|'='
name|'options'
newline|'\n'
nl|'\n'
dedent|''
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
nl|'\n'
string|"'swift.common.middleware.container_sync.register_swift_info'"
op|','
nl|'\n'
name|'new'
op|'='
name|'capture_swift_info'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'sync'
op|'.'
name|'register_info'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'for'
name|'realm'
op|','
name|'realm_info'
name|'in'
name|'info'
op|'['
string|"'container_sync'"
op|']'
op|'['
string|"'realms'"
op|']'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'cluster'
op|','
name|'options'
name|'in'
name|'realm_info'
op|'['
string|"'clusters'"
op|']'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'options'
op|'.'
name|'get'
op|'('
string|"'current'"
op|','
name|'False'
op|')'
op|','
name|'False'
op|')'
newline|'\n'
nl|'\n'
DECL|function|test_current_invalid
dedent|''
dedent|''
dedent|''
name|'def'
name|'test_current_invalid'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'conf'
op|'='
op|'{'
string|"'swift_dir'"
op|':'
name|'self'
op|'.'
name|'tempdir'
op|','
string|"'current'"
op|':'
string|"'foo'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'sync'
op|'='
name|'container_sync'
op|'.'
name|'ContainerSync'
op|'('
name|'self'
op|'.'
name|'app'
op|','
name|'self'
op|'.'
name|'conf'
op|','
nl|'\n'
name|'logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertIsNone'
op|'('
name|'self'
op|'.'
name|'sync'
op|'.'
name|'realm'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertIsNone'
op|'('
name|'self'
op|'.'
name|'sync'
op|'.'
name|'cluster'
op|')'
newline|'\n'
name|'info'
op|'='
op|'{'
op|'}'
newline|'\n'
nl|'\n'
DECL|function|capture_swift_info
name|'def'
name|'capture_swift_info'
op|'('
name|'key'
op|','
op|'**'
name|'options'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'info'
op|'['
name|'key'
op|']'
op|'='
name|'options'
newline|'\n'
nl|'\n'
dedent|''
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
nl|'\n'
string|"'swift.common.middleware.container_sync.register_swift_info'"
op|','
nl|'\n'
name|'new'
op|'='
name|'capture_swift_info'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'sync'
op|'.'
name|'register_info'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'for'
name|'realm'
op|','
name|'realm_info'
name|'in'
name|'info'
op|'['
string|"'container_sync'"
op|']'
op|'['
string|"'realms'"
op|']'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'cluster'
op|','
name|'options'
name|'in'
name|'realm_info'
op|'['
string|"'clusters'"
op|']'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'options'
op|'.'
name|'get'
op|'('
string|"'current'"
op|','
name|'False'
op|')'
op|','
name|'False'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'error_lines'
op|'='
name|'self'
op|'.'
name|'sync'
op|'.'
name|'logger'
op|'.'
name|'get_lines_for_level'
op|'('
string|"'error'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'error_lines'
op|','
op|'['
string|"'Invalid current '"
nl|'\n'
string|"'//REALM/CLUSTER (foo)'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|function|test_current_in_realms_conf
dedent|''
name|'def'
name|'test_current_in_realms_conf'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'conf'
op|'='
op|'{'
string|"'swift_dir'"
op|':'
name|'self'
op|'.'
name|'tempdir'
op|','
string|"'current'"
op|':'
string|"'//us/dfw1'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'sync'
op|'='
name|'container_sync'
op|'.'
name|'ContainerSync'
op|'('
name|'self'
op|'.'
name|'app'
op|','
name|'self'
op|'.'
name|'conf'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
string|"'US'"
op|','
name|'self'
op|'.'
name|'sync'
op|'.'
name|'realm'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
string|"'DFW1'"
op|','
name|'self'
op|'.'
name|'sync'
op|'.'
name|'cluster'
op|')'
newline|'\n'
name|'info'
op|'='
op|'{'
op|'}'
newline|'\n'
nl|'\n'
DECL|function|capture_swift_info
name|'def'
name|'capture_swift_info'
op|'('
name|'key'
op|','
op|'**'
name|'options'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'info'
op|'['
name|'key'
op|']'
op|'='
name|'options'
newline|'\n'
nl|'\n'
dedent|''
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
nl|'\n'
string|"'swift.common.middleware.container_sync.register_swift_info'"
op|','
nl|'\n'
name|'new'
op|'='
name|'capture_swift_info'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'sync'
op|'.'
name|'register_info'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'for'
name|'realm'
op|','
name|'realm_info'
name|'in'
name|'info'
op|'['
string|"'container_sync'"
op|']'
op|'['
string|"'realms'"
op|']'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'cluster'
op|','
name|'options'
name|'in'
name|'realm_info'
op|'['
string|"'clusters'"
op|']'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'options'
op|'.'
name|'get'
op|'('
string|"'current'"
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'break'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'realm'
op|','
name|'self'
op|'.'
name|'sync'
op|'.'
name|'realm'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'cluster'
op|','
name|'self'
op|'.'
name|'sync'
op|'.'
name|'cluster'
op|')'
newline|'\n'
nl|'\n'
DECL|function|test_missing_from_realms_conf
dedent|''
name|'def'
name|'test_missing_from_realms_conf'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'conf'
op|'='
op|'{'
string|"'swift_dir'"
op|':'
name|'self'
op|'.'
name|'tempdir'
op|','
string|"'current'"
op|':'
string|"'foo/bar'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'sync'
op|'='
name|'container_sync'
op|'.'
name|'ContainerSync'
op|'('
name|'self'
op|'.'
name|'app'
op|','
name|'self'
op|'.'
name|'conf'
op|','
nl|'\n'
name|'logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
string|"'FOO'"
op|','
name|'self'
op|'.'
name|'sync'
op|'.'
name|'realm'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
string|"'BAR'"
op|','
name|'self'
op|'.'
name|'sync'
op|'.'
name|'cluster'
op|')'
newline|'\n'
name|'info'
op|'='
op|'{'
op|'}'
newline|'\n'
nl|'\n'
DECL|function|capture_swift_info
name|'def'
name|'capture_swift_info'
op|'('
name|'key'
op|','
op|'**'
name|'options'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'info'
op|'['
name|'key'
op|']'
op|'='
name|'options'
newline|'\n'
nl|'\n'
dedent|''
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
nl|'\n'
string|"'swift.common.middleware.container_sync.register_swift_info'"
op|','
nl|'\n'
name|'new'
op|'='
name|'capture_swift_info'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'sync'
op|'.'
name|'register_info'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'for'
name|'realm'
op|','
name|'realm_info'
name|'in'
name|'info'
op|'['
string|"'container_sync'"
op|']'
op|'['
string|"'realms'"
op|']'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'cluster'
op|','
name|'options'
name|'in'
name|'realm_info'
op|'['
string|"'clusters'"
op|']'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'options'
op|'.'
name|'get'
op|'('
string|"'current'"
op|','
name|'False'
op|')'
op|','
name|'False'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'for'
name|'line'
name|'in'
name|'self'
op|'.'
name|'sync'
op|'.'
name|'logger'
op|'.'
name|'get_lines_for_level'
op|'('
string|"'error'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'line'
op|','
string|"'Unknown current '"
nl|'\n'
string|"'//REALM/CLUSTER (//FOO/BAR)'"
op|')'
newline|'\n'
nl|'\n'
DECL|function|test_pass_through
dedent|''
dedent|''
name|'def'
name|'test_pass_through'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'swob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a/c'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'sync'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status'
op|','
string|"'200 OK'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'body'
op|','
string|"'Pass-Through Response'"
op|')'
newline|'\n'
nl|'\n'
DECL|function|test_not_enough_args
dedent|''
name|'def'
name|'test_not_enough_args'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'swob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/v1/a/c'"
op|','
name|'headers'
op|'='
op|'{'
string|"'x-container-sync-auth'"
op|':'
string|"'a'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'sync'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status'
op|','
string|"'401 Unauthorized'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
nl|'\n'
name|'resp'
op|'.'
name|'body'
op|','
nl|'\n'
string|"'X-Container-Sync-Auth header not valid; contact cluster operator '"
nl|'\n'
string|"'for support.'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
nl|'\n'
string|"'cs:not-3-args'"
name|'in'
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift.log_info'"
op|')'
op|','
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift.log_info'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|function|test_realm_miss
dedent|''
name|'def'
name|'test_realm_miss'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'swob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/v1/a/c'"
op|','
name|'headers'
op|'='
op|'{'
string|"'x-container-sync-auth'"
op|':'
string|"'invalid nonce sig'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'sync'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status'
op|','
string|"'401 Unauthorized'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
nl|'\n'
name|'resp'
op|'.'
name|'body'
op|','
nl|'\n'
string|"'X-Container-Sync-Auth header not valid; contact cluster operator '"
nl|'\n'
string|"'for support.'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
nl|'\n'
string|"'cs:no-local-realm-key'"
name|'in'
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift.log_info'"
op|')'
op|','
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift.log_info'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|function|test_user_key_miss
dedent|''
name|'def'
name|'test_user_key_miss'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'swob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/v1/a/c'"
op|','
name|'headers'
op|'='
op|'{'
string|"'x-container-sync-auth'"
op|':'
string|"'US nonce sig'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'sync'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status'
op|','
string|"'401 Unauthorized'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
nl|'\n'
name|'resp'
op|'.'
name|'body'
op|','
nl|'\n'
string|"'X-Container-Sync-Auth header not valid; contact cluster operator '"
nl|'\n'
string|"'for support.'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
nl|'\n'
string|"'cs:no-local-user-key'"
name|'in'
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift.log_info'"
op|')'
op|','
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift.log_info'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|function|test_invalid_sig
dedent|''
name|'def'
name|'test_invalid_sig'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'swob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/v1/a/c'"
op|','
name|'headers'
op|'='
op|'{'
string|"'x-container-sync-auth'"
op|':'
string|"'US nonce sig'"
op|'}'
op|')'
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
name|'_get_cache_key'
op|'('
string|"'a'"
op|','
string|"'c'"
op|')'
op|'['
number|'1'
op|']'
op|']'
op|'='
op|'{'
string|"'sync_key'"
op|':'
string|"'abc'"
op|'}'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'sync'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status'
op|','
string|"'401 Unauthorized'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
nl|'\n'
name|'resp'
op|'.'
name|'body'
op|','
nl|'\n'
string|"'X-Container-Sync-Auth header not valid; contact cluster operator '"
nl|'\n'
string|"'for support.'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
nl|'\n'
string|"'cs:invalid-sig'"
name|'in'
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift.log_info'"
op|')'
op|','
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift.log_info'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|function|test_valid_sig
dedent|''
name|'def'
name|'test_valid_sig'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'ts'
op|'='
string|"'1455221706.726999_0123456789abcdef'"
newline|'\n'
name|'sig'
op|'='
name|'self'
op|'.'
name|'sync'
op|'.'
name|'realms_conf'
op|'.'
name|'get_sig'
op|'('
nl|'\n'
string|"'GET'"
op|','
string|"'/v1/a/c'"
op|','
name|'ts'
op|','
string|"'nonce'"
op|','
nl|'\n'
name|'self'
op|'.'
name|'sync'
op|'.'
name|'realms_conf'
op|'.'
name|'key'
op|'('
string|"'US'"
op|')'
op|','
string|"'abc'"
op|')'
newline|'\n'
name|'req'
op|'='
name|'swob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a/c'"
op|','
name|'headers'
op|'='
op|'{'
nl|'\n'
string|"'x-container-sync-auth'"
op|':'
string|"'US nonce '"
op|'+'
name|'sig'
op|','
nl|'\n'
string|"'x-backend-inbound-x-timestamp'"
op|':'
name|'ts'
op|'}'
op|')'
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
name|'_get_cache_key'
op|'('
string|"'a'"
op|','
string|"'c'"
op|')'
op|'['
number|'1'
op|']'
op|']'
op|'='
op|'{'
string|"'sync_key'"
op|':'
string|"'abc'"
op|'}'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'sync'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status'
op|','
string|"'200 OK'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'body'
op|','
string|"'Response to Authorized Request'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertIn'
op|'('
string|"'cs:valid'"
op|','
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift.log_info'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertIn'
op|'('
string|"'X-Timestamp'"
op|','
name|'resp'
op|'.'
name|'headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'ts'
op|','
name|'resp'
op|'.'
name|'headers'
op|'['
string|"'X-Timestamp'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|function|test_valid_sig2
dedent|''
name|'def'
name|'test_valid_sig2'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'sig'
op|'='
name|'self'
op|'.'
name|'sync'
op|'.'
name|'realms_conf'
op|'.'
name|'get_sig'
op|'('
nl|'\n'
string|"'GET'"
op|','
string|"'/v1/a/c'"
op|','
string|"'0'"
op|','
string|"'nonce'"
op|','
nl|'\n'
name|'self'
op|'.'
name|'sync'
op|'.'
name|'realms_conf'
op|'.'
name|'key2'
op|'('
string|"'US'"
op|')'
op|','
string|"'abc'"
op|')'
newline|'\n'
name|'req'
op|'='
name|'swob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/v1/a/c'"
op|','
name|'headers'
op|'='
op|'{'
string|"'x-container-sync-auth'"
op|':'
string|"'US nonce '"
op|'+'
name|'sig'
op|'}'
op|')'
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
name|'_get_cache_key'
op|'('
string|"'a'"
op|','
string|"'c'"
op|')'
op|'['
number|'1'
op|']'
op|']'
op|'='
op|'{'
string|"'sync_key'"
op|':'
string|"'abc'"
op|'}'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'sync'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status'
op|','
string|"'200 OK'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'body'
op|','
string|"'Response to Authorized Request'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
nl|'\n'
string|"'cs:valid'"
name|'in'
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift.log_info'"
op|')'
op|','
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift.log_info'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|function|test_info
dedent|''
name|'def'
name|'test_info'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'swob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/info'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'sync'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status'
op|','
string|"'200 OK'"
op|')'
newline|'\n'
name|'result'
op|'='
name|'json'
op|'.'
name|'loads'
op|'('
name|'resp'
op|'.'
name|'body'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
nl|'\n'
name|'result'
op|'.'
name|'get'
op|'('
string|"'container_sync'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'realms'"
op|':'
op|'{'
string|"'US'"
op|':'
op|'{'
string|"'clusters'"
op|':'
op|'{'
string|"'DFW1'"
op|':'
op|'{'
op|'}'
op|'}'
op|'}'
op|'}'
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|function|test_info_always_fresh
dedent|''
name|'def'
name|'test_info_always_fresh'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'swob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/info'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'sync'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status'
op|','
string|"'200 OK'"
op|')'
newline|'\n'
name|'result'
op|'='
name|'json'
op|'.'
name|'loads'
op|'('
name|'resp'
op|'.'
name|'body'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
nl|'\n'
name|'result'
op|'.'
name|'get'
op|'('
string|"'container_sync'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'realms'"
op|':'
op|'{'
string|"'US'"
op|':'
op|'{'
string|"'clusters'"
op|':'
op|'{'
string|"'DFW1'"
op|':'
op|'{'
op|'}'
op|'}'
op|'}'
op|'}'
op|'}'
op|')'
newline|'\n'
name|'with'
name|'open'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'tempdir'
op|','
string|"'container-sync-realms.conf'"
op|')'
op|','
nl|'\n'
string|"'w'"
op|')'
name|'as'
name|'fp'
op|':'
newline|'\n'
indent|'            '
name|'fp'
op|'.'
name|'write'
op|'('
string|"'''\n[US]\nkey = 9ff3b71c849749dbaec4ccdd3cbab62b\nkey2 = 1a0a5a0cbd66448084089304442d6776\ncluster_dfw1 = http://dfw1.host/v1/\n\n[UK]\nkey = 400b3b357a80413f9d956badff1d9dfe\ncluster_lon3 = http://lon3.host/v1/\n            '''"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'sync'
op|'.'
name|'realms_conf'
op|'.'
name|'reload'
op|'('
op|')'
newline|'\n'
name|'req'
op|'='
name|'swob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/info'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'sync'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status'
op|','
string|"'200 OK'"
op|')'
newline|'\n'
name|'result'
op|'='
name|'json'
op|'.'
name|'loads'
op|'('
name|'resp'
op|'.'
name|'body'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
nl|'\n'
name|'result'
op|'.'
name|'get'
op|'('
string|"'container_sync'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'realms'"
op|':'
op|'{'
nl|'\n'
string|"'US'"
op|':'
op|'{'
string|"'clusters'"
op|':'
op|'{'
string|"'DFW1'"
op|':'
op|'{'
op|'}'
op|'}'
op|'}'
op|','
nl|'\n'
string|"'UK'"
op|':'
op|'{'
string|"'clusters'"
op|':'
op|'{'
string|"'LON3'"
op|':'
op|'{'
op|'}'
op|'}'
op|'}'
op|'}'
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|function|test_allow_full_urls_setting
dedent|''
name|'def'
name|'test_allow_full_urls_setting'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'swob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/v1/a/c'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'x-container-sync-to'"
op|':'
string|"'http://host/v1/a/c'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'sync'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status'
op|','
string|"'200 OK'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'conf'
op|'='
op|'{'
string|"'swift_dir'"
op|':'
name|'self'
op|'.'
name|'tempdir'
op|','
string|"'allow_full_urls'"
op|':'
string|"'false'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'sync'
op|'='
name|'container_sync'
op|'.'
name|'ContainerSync'
op|'('
name|'self'
op|'.'
name|'app'
op|','
name|'self'
op|'.'
name|'conf'
op|')'
newline|'\n'
name|'req'
op|'='
name|'swob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/v1/a/c'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'x-container-sync-to'"
op|':'
string|"'http://host/v1/a/c'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'sync'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status'
op|','
string|"'400 Bad Request'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
nl|'\n'
name|'resp'
op|'.'
name|'body'
op|','
nl|'\n'
string|"'Full URLs are not allowed for X-Container-Sync-To values. Only '"
nl|'\n'
string|"'realm values of the format //realm/cluster/account/container are '"
nl|'\n'
string|"'allowed.\\n'"
op|')'
newline|'\n'
nl|'\n'
DECL|function|test_filter
dedent|''
name|'def'
name|'test_filter'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'FakeApp'
op|'('
op|')'
newline|'\n'
name|'unique'
op|'='
name|'uuid'
op|'.'
name|'uuid4'
op|'('
op|')'
op|'.'
name|'hex'
newline|'\n'
name|'sync'
op|'='
name|'container_sync'
op|'.'
name|'filter_factory'
op|'('
nl|'\n'
op|'{'
string|"'global'"
op|':'
string|"'global_value'"
op|','
string|"'swift_dir'"
op|':'
name|'unique'
op|'}'
op|','
nl|'\n'
op|'**'
op|'{'
string|"'local'"
op|':'
string|"'local_value'"
op|'}'
op|')'
op|'('
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'sync'
op|'.'
name|'app'
op|','
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'sync'
op|'.'
name|'conf'
op|','
op|'{'
nl|'\n'
string|"'global'"
op|':'
string|"'global_value'"
op|','
string|"'swift_dir'"
op|':'
name|'unique'
op|','
nl|'\n'
string|"'local'"
op|':'
string|"'local_value'"
op|'}'
op|')'
newline|'\n'
name|'req'
op|'='
name|'swob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/info'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'sync'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status'
op|','
string|"'200 OK'"
op|')'
newline|'\n'
name|'result'
op|'='
name|'json'
op|'.'
name|'loads'
op|'('
name|'resp'
op|'.'
name|'body'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'result'
op|'.'
name|'get'
op|'('
string|"'container_sync'"
op|')'
op|','
op|'{'
string|"'realms'"
op|':'
op|'{'
op|'}'
op|'}'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
dedent|''
name|'if'
name|'__name__'
op|'=='
string|"'__main__'"
op|':'
newline|'\n'
indent|'    '
name|'unittest'
op|'.'
name|'main'
op|'('
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
