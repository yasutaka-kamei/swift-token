begin_unit
comment|'#!/usr/bin/python -u'
nl|'\n'
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
name|'os'
name|'import'
name|'listdir'
newline|'\n'
name|'from'
name|'os'
op|'.'
name|'path'
name|'import'
name|'join'
name|'as'
name|'path_join'
newline|'\n'
name|'from'
name|'unittest'
name|'import'
name|'main'
newline|'\n'
name|'from'
name|'uuid'
name|'import'
name|'uuid4'
newline|'\n'
nl|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'GreenPool'
op|','
name|'Timeout'
newline|'\n'
name|'import'
name|'eventlet'
newline|'\n'
name|'from'
name|'sqlite3'
name|'import'
name|'connect'
newline|'\n'
name|'from'
name|'swiftclient'
name|'import'
name|'client'
newline|'\n'
nl|'\n'
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
name|'exceptions'
name|'import'
name|'ClientException'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'hash_path'
op|','
name|'readconf'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'probe'
op|'.'
name|'common'
name|'import'
name|'kill_nonprimary_server'
op|','
name|'kill_server'
op|','
name|'ReplProbeTest'
op|','
name|'start_server'
newline|'\n'
nl|'\n'
name|'eventlet'
op|'.'
name|'monkey_patch'
op|'('
name|'all'
op|'='
name|'False'
op|','
name|'socket'
op|'='
name|'True'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_db_file_path
name|'def'
name|'get_db_file_path'
op|'('
name|'obj_dir'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'files'
op|'='
name|'sorted'
op|'('
name|'listdir'
op|'('
name|'obj_dir'
op|')'
op|','
name|'reverse'
op|'='
name|'True'
op|')'
newline|'\n'
name|'for'
name|'filename'
name|'in'
name|'files'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'filename'
op|'.'
name|'endswith'
op|'('
string|"'db'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'path_join'
op|'('
name|'obj_dir'
op|','
name|'filename'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestContainerFailures
dedent|''
dedent|''
dedent|''
name|'class'
name|'TestContainerFailures'
op|'('
name|'ReplProbeTest'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_one_node_fails
indent|'    '
name|'def'
name|'test_one_node_fails'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# Create container1'
nl|'\n'
indent|'        '
name|'container1'
op|'='
string|"'container-%s'"
op|'%'
name|'uuid4'
op|'('
op|')'
newline|'\n'
name|'cpart'
op|','
name|'cnodes'
op|'='
name|'self'
op|'.'
name|'container_ring'
op|'.'
name|'get_nodes'
op|'('
name|'self'
op|'.'
name|'account'
op|','
name|'container1'
op|')'
newline|'\n'
name|'client'
op|'.'
name|'put_container'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
name|'container1'
op|')'
newline|'\n'
nl|'\n'
comment|'# Kill container1 servers excepting two of the primaries'
nl|'\n'
name|'kill_nonprimary_server'
op|'('
name|'cnodes'
op|','
name|'self'
op|'.'
name|'port2server'
op|','
name|'self'
op|'.'
name|'pids'
op|')'
newline|'\n'
name|'kill_server'
op|'('
name|'cnodes'
op|'['
number|'0'
op|']'
op|'['
string|"'port'"
op|']'
op|','
name|'self'
op|'.'
name|'port2server'
op|','
name|'self'
op|'.'
name|'pids'
op|')'
newline|'\n'
nl|'\n'
comment|'# Delete container1'
nl|'\n'
name|'client'
op|'.'
name|'delete_container'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
name|'container1'
op|')'
newline|'\n'
nl|'\n'
comment|'# Restart other container1 primary server'
nl|'\n'
name|'start_server'
op|'('
name|'cnodes'
op|'['
number|'0'
op|']'
op|'['
string|"'port'"
op|']'
op|','
name|'self'
op|'.'
name|'port2server'
op|','
name|'self'
op|'.'
name|'pids'
op|')'
newline|'\n'
nl|'\n'
comment|'# Create container1/object1 (allowed because at least server thinks the'
nl|'\n'
comment|'#   container exists)'
nl|'\n'
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
name|'container1'
op|','
string|"'object1'"
op|','
string|"'123'"
op|')'
newline|'\n'
nl|'\n'
comment|'# Get to a final state'
nl|'\n'
name|'self'
op|'.'
name|'get_to_final_state'
op|'('
op|')'
newline|'\n'
nl|'\n'
comment|'# Assert all container1 servers indicate container1 is alive and'
nl|'\n'
comment|'#   well with object1'
nl|'\n'
name|'for'
name|'cnode'
name|'in'
name|'cnodes'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEquals'
op|'('
nl|'\n'
op|'['
name|'o'
op|'['
string|"'name'"
op|']'
name|'for'
name|'o'
name|'in'
name|'direct_client'
op|'.'
name|'direct_get_container'
op|'('
nl|'\n'
name|'cnode'
op|','
name|'cpart'
op|','
name|'self'
op|'.'
name|'account'
op|','
name|'container1'
op|')'
op|'['
number|'1'
op|']'
op|']'
op|','
nl|'\n'
op|'['
string|"'object1'"
op|']'
op|')'
newline|'\n'
nl|'\n'
comment|'# Assert account level also indicates container1 is alive and'
nl|'\n'
comment|'#   well with object1'
nl|'\n'
dedent|''
name|'headers'
op|','
name|'containers'
op|'='
name|'client'
op|'.'
name|'get_account'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'headers'
op|'['
string|"'x-account-container-count'"
op|']'
op|','
string|"'1'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'headers'
op|'['
string|"'x-account-object-count'"
op|']'
op|','
string|"'1'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'headers'
op|'['
string|"'x-account-bytes-used'"
op|']'
op|','
string|"'3'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_two_nodes_fail
dedent|''
name|'def'
name|'test_two_nodes_fail'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# Create container1'
nl|'\n'
indent|'        '
name|'container1'
op|'='
string|"'container-%s'"
op|'%'
name|'uuid4'
op|'('
op|')'
newline|'\n'
name|'cpart'
op|','
name|'cnodes'
op|'='
name|'self'
op|'.'
name|'container_ring'
op|'.'
name|'get_nodes'
op|'('
name|'self'
op|'.'
name|'account'
op|','
name|'container1'
op|')'
newline|'\n'
name|'client'
op|'.'
name|'put_container'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
name|'container1'
op|')'
newline|'\n'
nl|'\n'
comment|'# Kill container1 servers excepting one of the primaries'
nl|'\n'
name|'cnp_port'
op|'='
name|'kill_nonprimary_server'
op|'('
name|'cnodes'
op|','
name|'self'
op|'.'
name|'port2server'
op|','
name|'self'
op|'.'
name|'pids'
op|')'
newline|'\n'
name|'kill_server'
op|'('
name|'cnodes'
op|'['
number|'0'
op|']'
op|'['
string|"'port'"
op|']'
op|','
name|'self'
op|'.'
name|'port2server'
op|','
name|'self'
op|'.'
name|'pids'
op|')'
newline|'\n'
name|'kill_server'
op|'('
name|'cnodes'
op|'['
number|'1'
op|']'
op|'['
string|"'port'"
op|']'
op|','
name|'self'
op|'.'
name|'port2server'
op|','
name|'self'
op|'.'
name|'pids'
op|')'
newline|'\n'
nl|'\n'
comment|'# Delete container1 directly to the one primary still up'
nl|'\n'
name|'direct_client'
op|'.'
name|'direct_delete_container'
op|'('
name|'cnodes'
op|'['
number|'2'
op|']'
op|','
name|'cpart'
op|','
name|'self'
op|'.'
name|'account'
op|','
nl|'\n'
name|'container1'
op|')'
newline|'\n'
nl|'\n'
comment|'# Restart other container1 servers'
nl|'\n'
name|'start_server'
op|'('
name|'cnodes'
op|'['
number|'0'
op|']'
op|'['
string|"'port'"
op|']'
op|','
name|'self'
op|'.'
name|'port2server'
op|','
name|'self'
op|'.'
name|'pids'
op|')'
newline|'\n'
name|'start_server'
op|'('
name|'cnodes'
op|'['
number|'1'
op|']'
op|'['
string|"'port'"
op|']'
op|','
name|'self'
op|'.'
name|'port2server'
op|','
name|'self'
op|'.'
name|'pids'
op|')'
newline|'\n'
name|'start_server'
op|'('
name|'cnp_port'
op|','
name|'self'
op|'.'
name|'port2server'
op|','
name|'self'
op|'.'
name|'pids'
op|')'
newline|'\n'
nl|'\n'
comment|'# Get to a final state'
nl|'\n'
name|'self'
op|'.'
name|'get_to_final_state'
op|'('
op|')'
newline|'\n'
nl|'\n'
comment|'# Assert all container1 servers indicate container1 is gone (happens'
nl|'\n'
comment|'#   because the one node that knew about the delete replicated to the'
nl|'\n'
comment|'#   others.)'
nl|'\n'
name|'for'
name|'cnode'
name|'in'
name|'cnodes'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'direct_client'
op|'.'
name|'direct_get_container'
op|'('
name|'cnode'
op|','
name|'cpart'
op|','
name|'self'
op|'.'
name|'account'
op|','
nl|'\n'
name|'container1'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'err'
op|'.'
name|'http_status'
op|','
number|'404'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'fail'
op|'('
string|'"Expected ClientException but didn\'t get it"'
op|')'
newline|'\n'
nl|'\n'
comment|'# Assert account level also indicates container1 is gone'
nl|'\n'
dedent|''
dedent|''
name|'headers'
op|','
name|'containers'
op|'='
name|'client'
op|'.'
name|'get_account'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'headers'
op|'['
string|"'x-account-container-count'"
op|']'
op|','
string|"'0'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'headers'
op|'['
string|"'x-account-object-count'"
op|']'
op|','
string|"'0'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'headers'
op|'['
string|"'x-account-bytes-used'"
op|']'
op|','
string|"'0'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|_get_container_db_files
dedent|''
name|'def'
name|'_get_container_db_files'
op|'('
name|'self'
op|','
name|'container'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'opart'
op|','
name|'onodes'
op|'='
name|'self'
op|'.'
name|'container_ring'
op|'.'
name|'get_nodes'
op|'('
name|'self'
op|'.'
name|'account'
op|','
name|'container'
op|')'
newline|'\n'
name|'onode'
op|'='
name|'onodes'
op|'['
number|'0'
op|']'
newline|'\n'
name|'db_files'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'onode'
name|'in'
name|'onodes'
op|':'
newline|'\n'
indent|'            '
name|'node_id'
op|'='
op|'('
name|'onode'
op|'['
string|"'port'"
op|']'
op|'-'
number|'6000'
op|')'
op|'/'
number|'10'
newline|'\n'
name|'device'
op|'='
name|'onode'
op|'['
string|"'device'"
op|']'
newline|'\n'
name|'hash_str'
op|'='
name|'hash_path'
op|'('
name|'self'
op|'.'
name|'account'
op|','
name|'container'
op|')'
newline|'\n'
name|'server_conf'
op|'='
name|'readconf'
op|'('
name|'self'
op|'.'
name|'configs'
op|'['
string|"'container-server'"
op|']'
op|'['
name|'node_id'
op|']'
op|')'
newline|'\n'
name|'devices'
op|'='
name|'server_conf'
op|'['
string|"'app:container-server'"
op|']'
op|'['
string|"'devices'"
op|']'
newline|'\n'
name|'obj_dir'
op|'='
string|"'%s/%s/containers/%s/%s/%s/'"
op|'%'
op|'('
name|'devices'
op|','
nl|'\n'
name|'device'
op|','
name|'opart'
op|','
nl|'\n'
name|'hash_str'
op|'['
op|'-'
number|'3'
op|':'
op|']'
op|','
name|'hash_str'
op|')'
newline|'\n'
name|'db_files'
op|'.'
name|'append'
op|'('
name|'get_db_file_path'
op|'('
name|'obj_dir'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'db_files'
newline|'\n'
nl|'\n'
DECL|member|test_locked_container_dbs
dedent|''
name|'def'
name|'test_locked_container_dbs'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|function|run_test
indent|'        '
name|'def'
name|'run_test'
op|'('
name|'num_locks'
op|','
name|'catch_503'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'container'
op|'='
string|"'container-%s'"
op|'%'
name|'uuid4'
op|'('
op|')'
newline|'\n'
name|'client'
op|'.'
name|'put_container'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
name|'container'
op|')'
newline|'\n'
name|'db_files'
op|'='
name|'self'
op|'.'
name|'_get_container_db_files'
op|'('
name|'container'
op|')'
newline|'\n'
name|'db_conns'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'i'
name|'in'
name|'range'
op|'('
name|'num_locks'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'db_conn'
op|'='
name|'connect'
op|'('
name|'db_files'
op|'['
name|'i'
op|']'
op|')'
newline|'\n'
name|'db_conn'
op|'.'
name|'execute'
op|'('
string|"'begin exclusive transaction'"
op|')'
newline|'\n'
name|'db_conns'
op|'.'
name|'append'
op|'('
name|'db_conn'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'catch_503'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'client'
op|'.'
name|'delete_container'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
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
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'err'
op|'.'
name|'http_status'
op|','
number|'503'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'fail'
op|'('
string|'"Expected ClientException but didn\'t get it"'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'client'
op|'.'
name|'delete_container'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
name|'container'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'pool'
op|'='
name|'GreenPool'
op|'('
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'Timeout'
op|'('
number|'15'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'pool'
op|'.'
name|'spawn'
op|'('
name|'run_test'
op|','
number|'1'
op|','
name|'False'
op|')'
newline|'\n'
name|'pool'
op|'.'
name|'spawn'
op|'('
name|'run_test'
op|','
number|'2'
op|','
name|'True'
op|')'
newline|'\n'
name|'pool'
op|'.'
name|'spawn'
op|'('
name|'run_test'
op|','
number|'3'
op|','
name|'True'
op|')'
newline|'\n'
name|'pool'
op|'.'
name|'waitall'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'Timeout'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
nl|'\n'
string|'"The server did not return a 503 on container db locks, "'
nl|'\n'
string|'"it just hangs: %s"'
op|'%'
name|'err'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
dedent|''
dedent|''
name|'if'
name|'__name__'
op|'=='
string|"'__main__'"
op|':'
newline|'\n'
indent|'    '
name|'main'
op|'('
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
