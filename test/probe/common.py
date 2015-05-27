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
name|'httplib'
name|'import'
name|'HTTPConnection'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'from'
name|'subprocess'
name|'import'
name|'Popen'
op|','
name|'PIPE'
newline|'\n'
name|'import'
name|'sys'
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'sleep'
op|','
name|'time'
newline|'\n'
name|'from'
name|'collections'
name|'import'
name|'defaultdict'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'from'
name|'nose'
name|'import'
name|'SkipTest'
newline|'\n'
nl|'\n'
name|'from'
name|'swiftclient'
name|'import'
name|'get_auth'
op|','
name|'head_account'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'obj'
op|'.'
name|'diskfile'
name|'import'
name|'get_data_dir'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'ring'
name|'import'
name|'Ring'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'readconf'
op|','
name|'renamer'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'manager'
name|'import'
name|'Manager'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'storage_policy'
name|'import'
name|'POLICIES'
op|','
name|'EC_POLICY'
op|','
name|'REPL_POLICY'
newline|'\n'
nl|'\n'
name|'from'
name|'test'
op|'.'
name|'probe'
name|'import'
name|'CHECK_SERVER_TIMEOUT'
op|','
name|'VALIDATE_RSYNC'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|variable|ENABLED_POLICIES
name|'ENABLED_POLICIES'
op|'='
op|'['
name|'p'
name|'for'
name|'p'
name|'in'
name|'POLICIES'
name|'if'
name|'not'
name|'p'
op|'.'
name|'is_deprecated'
op|']'
newline|'\n'
DECL|variable|POLICIES_BY_TYPE
name|'POLICIES_BY_TYPE'
op|'='
name|'defaultdict'
op|'('
name|'list'
op|')'
newline|'\n'
name|'for'
name|'p'
name|'in'
name|'POLICIES'
op|':'
newline|'\n'
indent|'    '
name|'POLICIES_BY_TYPE'
op|'['
name|'p'
op|'.'
name|'policy_type'
op|']'
op|'.'
name|'append'
op|'('
name|'p'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_server_number
dedent|''
name|'def'
name|'get_server_number'
op|'('
name|'port'
op|','
name|'port2server'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'server_number'
op|'='
name|'port2server'
op|'['
name|'port'
op|']'
newline|'\n'
name|'server'
op|','
name|'number'
op|'='
name|'server_number'
op|'['
op|':'
op|'-'
number|'1'
op|']'
op|','
name|'server_number'
op|'['
op|'-'
number|'1'
op|':'
op|']'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'number'
op|'='
name|'int'
op|'('
name|'number'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
comment|'# probably the proxy'
nl|'\n'
indent|'        '
name|'return'
name|'server_number'
op|','
name|'None'
newline|'\n'
dedent|''
name|'return'
name|'server'
op|','
name|'number'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|start_server
dedent|''
name|'def'
name|'start_server'
op|'('
name|'port'
op|','
name|'port2server'
op|','
name|'pids'
op|','
name|'check'
op|'='
name|'True'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'server'
op|','
name|'number'
op|'='
name|'get_server_number'
op|'('
name|'port'
op|','
name|'port2server'
op|')'
newline|'\n'
name|'err'
op|'='
name|'Manager'
op|'('
op|'['
name|'server'
op|']'
op|')'
op|'.'
name|'start'
op|'('
name|'number'
op|'='
name|'number'
op|','
name|'wait'
op|'='
name|'False'
op|')'
newline|'\n'
name|'if'
name|'err'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'Exception'
op|'('
string|"'unable to start %s'"
op|'%'
op|'('
nl|'\n'
name|'server'
name|'if'
name|'not'
name|'number'
name|'else'
string|"'%s%s'"
op|'%'
op|'('
name|'server'
op|','
name|'number'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'check'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'check_server'
op|'('
name|'port'
op|','
name|'port2server'
op|','
name|'pids'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'None'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|check_server
dedent|''
name|'def'
name|'check_server'
op|'('
name|'port'
op|','
name|'port2server'
op|','
name|'pids'
op|','
name|'timeout'
op|'='
name|'CHECK_SERVER_TIMEOUT'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'server'
op|'='
name|'port2server'
op|'['
name|'port'
op|']'
newline|'\n'
name|'if'
name|'server'
op|'['
op|':'
op|'-'
number|'1'
op|']'
name|'in'
op|'('
string|"'account'"
op|','
string|"'container'"
op|','
string|"'object'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'int'
op|'('
name|'server'
op|'['
op|'-'
number|'1'
op|']'
op|')'
op|'>'
number|'4'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'None'
newline|'\n'
dedent|''
name|'path'
op|'='
string|"'/connect/1/2'"
newline|'\n'
name|'if'
name|'server'
op|'['
op|':'
op|'-'
number|'1'
op|']'
op|'=='
string|"'container'"
op|':'
newline|'\n'
indent|'            '
name|'path'
op|'+='
string|"'/3'"
newline|'\n'
dedent|''
name|'elif'
name|'server'
op|'['
op|':'
op|'-'
number|'1'
op|']'
op|'=='
string|"'object'"
op|':'
newline|'\n'
indent|'            '
name|'path'
op|'+='
string|"'/3/4'"
newline|'\n'
dedent|''
name|'try_until'
op|'='
name|'time'
op|'('
op|')'
op|'+'
name|'timeout'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'conn'
op|'='
name|'HTTPConnection'
op|'('
string|"'127.0.0.1'"
op|','
name|'port'
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'request'
op|'('
string|"'GET'"
op|','
name|'path'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'conn'
op|'.'
name|'getresponse'
op|'('
op|')'
newline|'\n'
comment|"# 404 because it's a nonsense path (and mount_check is false)"
nl|'\n'
comment|'# 507 in case the test target is a VM using mount_check'
nl|'\n'
name|'if'
name|'resp'
op|'.'
name|'status'
name|'not'
name|'in'
op|'('
number|'404'
op|','
number|'507'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
name|'Exception'
op|'('
nl|'\n'
string|"'Unexpected status %s'"
op|'%'
name|'resp'
op|'.'
name|'status'
op|')'
newline|'\n'
dedent|''
name|'break'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'time'
op|'('
op|')'
op|'>'
name|'try_until'
op|':'
newline|'\n'
indent|'                    '
name|'print'
name|'err'
newline|'\n'
name|'print'
string|"'Giving up on %s:%s after %s seconds.'"
op|'%'
op|'('
nl|'\n'
name|'server'
op|','
name|'port'
op|','
name|'timeout'
op|')'
newline|'\n'
name|'raise'
name|'err'
newline|'\n'
dedent|''
name|'sleep'
op|'('
number|'0.1'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'        '
name|'try_until'
op|'='
name|'time'
op|'('
op|')'
op|'+'
name|'timeout'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'url'
op|','
name|'token'
op|'='
name|'get_auth'
op|'('
string|"'http://127.0.0.1:8080/auth/v1.0'"
op|','
nl|'\n'
string|"'test:tester'"
op|','
string|"'testing'"
op|')'
newline|'\n'
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
name|'head_account'
op|'('
name|'url'
op|','
name|'token'
op|')'
newline|'\n'
name|'return'
name|'url'
op|','
name|'token'
op|','
name|'account'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'time'
op|'('
op|')'
op|'>'
name|'try_until'
op|':'
newline|'\n'
indent|'                    '
name|'print'
name|'err'
newline|'\n'
name|'print'
string|"'Giving up on proxy:8080 after 30 seconds.'"
newline|'\n'
name|'raise'
name|'err'
newline|'\n'
dedent|''
name|'sleep'
op|'('
number|'0.1'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'return'
name|'None'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|kill_server
dedent|''
name|'def'
name|'kill_server'
op|'('
name|'port'
op|','
name|'port2server'
op|','
name|'pids'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'server'
op|','
name|'number'
op|'='
name|'get_server_number'
op|'('
name|'port'
op|','
name|'port2server'
op|')'
newline|'\n'
name|'err'
op|'='
name|'Manager'
op|'('
op|'['
name|'server'
op|']'
op|')'
op|'.'
name|'kill'
op|'('
name|'number'
op|'='
name|'number'
op|')'
newline|'\n'
name|'if'
name|'err'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'Exception'
op|'('
string|"'unable to kill %s'"
op|'%'
op|'('
name|'server'
name|'if'
name|'not'
name|'number'
name|'else'
nl|'\n'
string|"'%s%s'"
op|'%'
op|'('
name|'server'
op|','
name|'number'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'try_until'
op|'='
name|'time'
op|'('
op|')'
op|'+'
number|'30'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'='
name|'HTTPConnection'
op|'('
string|"'127.0.0.1'"
op|','
name|'port'
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'request'
op|'('
string|"'GET'"
op|','
string|"'/'"
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'getresponse'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'break'
newline|'\n'
dedent|''
name|'if'
name|'time'
op|'('
op|')'
op|'>'
name|'try_until'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
nl|'\n'
string|"'Still answering on port %s after 30 seconds'"
op|'%'
name|'port'
op|')'
newline|'\n'
dedent|''
name|'sleep'
op|'('
number|'0.1'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|kill_nonprimary_server
dedent|''
dedent|''
name|'def'
name|'kill_nonprimary_server'
op|'('
name|'primary_nodes'
op|','
name|'port2server'
op|','
name|'pids'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'primary_ports'
op|'='
op|'['
name|'n'
op|'['
string|"'port'"
op|']'
name|'for'
name|'n'
name|'in'
name|'primary_nodes'
op|']'
newline|'\n'
name|'for'
name|'port'
op|','
name|'server'
name|'in'
name|'port2server'
op|'.'
name|'iteritems'
op|'('
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'port'
name|'in'
name|'primary_ports'
op|':'
newline|'\n'
indent|'            '
name|'server_type'
op|'='
name|'server'
op|'['
op|':'
op|'-'
number|'1'
op|']'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'Exception'
op|'('
string|"'Cannot figure out server type for %r'"
op|'%'
name|'primary_nodes'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'port'
op|','
name|'server'
name|'in'
name|'list'
op|'('
name|'port2server'
op|'.'
name|'iteritems'
op|'('
op|')'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'server'
op|'['
op|':'
op|'-'
number|'1'
op|']'
op|'=='
name|'server_type'
name|'and'
name|'port'
name|'not'
name|'in'
name|'primary_ports'
op|':'
newline|'\n'
indent|'            '
name|'kill_server'
op|'('
name|'port'
op|','
name|'port2server'
op|','
name|'pids'
op|')'
newline|'\n'
name|'return'
name|'port'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|build_port_to_conf
dedent|''
dedent|''
dedent|''
name|'def'
name|'build_port_to_conf'
op|'('
name|'server'
op|')'
op|':'
newline|'\n'
comment|'# map server to config by port'
nl|'\n'
indent|'    '
name|'port_to_config'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'server_'
name|'in'
name|'Manager'
op|'('
op|'['
name|'server'
op|']'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'config_path'
name|'in'
name|'server_'
op|'.'
name|'conf_files'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'conf'
op|'='
name|'readconf'
op|'('
name|'config_path'
op|','
nl|'\n'
name|'section_name'
op|'='
string|"'%s-replicator'"
op|'%'
name|'server_'
op|'.'
name|'type'
op|')'
newline|'\n'
name|'port_to_config'
op|'['
name|'int'
op|'('
name|'conf'
op|'['
string|"'bind_port'"
op|']'
op|')'
op|']'
op|'='
name|'conf'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'port_to_config'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_ring
dedent|''
name|'def'
name|'get_ring'
op|'('
name|'ring_name'
op|','
name|'required_replicas'
op|','
name|'required_devices'
op|','
nl|'\n'
name|'server'
op|'='
name|'None'
op|','
name|'force_validate'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'if'
name|'not'
name|'server'
op|':'
newline|'\n'
indent|'        '
name|'server'
op|'='
name|'ring_name'
newline|'\n'
dedent|''
name|'ring'
op|'='
name|'Ring'
op|'('
string|"'/etc/swift'"
op|','
name|'ring_name'
op|'='
name|'ring_name'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'VALIDATE_RSYNC'
name|'and'
name|'not'
name|'force_validate'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'ring'
newline|'\n'
comment|'# easy sanity checks'
nl|'\n'
dedent|''
name|'if'
name|'ring'
op|'.'
name|'replica_count'
op|'!='
name|'required_replicas'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'SkipTest'
op|'('
string|"'%s has %s replicas instead of %s'"
op|'%'
op|'('
nl|'\n'
name|'ring'
op|'.'
name|'serialized_path'
op|','
name|'ring'
op|'.'
name|'replica_count'
op|','
name|'required_replicas'
op|')'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'len'
op|'('
name|'ring'
op|'.'
name|'devs'
op|')'
op|'!='
name|'required_devices'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'SkipTest'
op|'('
string|"'%s has %s devices instead of %s'"
op|'%'
op|'('
nl|'\n'
name|'ring'
op|'.'
name|'serialized_path'
op|','
name|'len'
op|'('
name|'ring'
op|'.'
name|'devs'
op|')'
op|','
name|'required_devices'
op|')'
op|')'
newline|'\n'
dedent|''
name|'port_to_config'
op|'='
name|'build_port_to_conf'
op|'('
name|'server'
op|')'
newline|'\n'
name|'for'
name|'dev'
name|'in'
name|'ring'
op|'.'
name|'devs'
op|':'
newline|'\n'
comment|'# verify server is exposing mounted device'
nl|'\n'
indent|'        '
name|'conf'
op|'='
name|'port_to_config'
op|'['
name|'dev'
op|'['
string|"'port'"
op|']'
op|']'
newline|'\n'
name|'for'
name|'device'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'conf'
op|'['
string|"'devices'"
op|']'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'device'
op|'=='
name|'dev'
op|'['
string|"'device'"
op|']'
op|':'
newline|'\n'
indent|'                '
name|'dev_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'conf'
op|'['
string|"'devices'"
op|']'
op|','
name|'device'
op|')'
newline|'\n'
name|'full_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'realpath'
op|'('
name|'dev_path'
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
name|'full_path'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
name|'SkipTest'
op|'('
nl|'\n'
string|"'device %s in %s was not found (%s)'"
op|'%'
nl|'\n'
op|'('
name|'device'
op|','
name|'conf'
op|'['
string|"'devices'"
op|']'
op|','
name|'full_path'
op|')'
op|')'
newline|'\n'
dedent|''
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'SkipTest'
op|'('
nl|'\n'
string|'"unable to find ring device %s under %s\'s devices (%s)"'
op|'%'
op|'('
nl|'\n'
name|'dev'
op|'['
string|"'device'"
op|']'
op|','
name|'server'
op|','
name|'conf'
op|'['
string|"'devices'"
op|']'
op|')'
op|')'
newline|'\n'
comment|'# verify server is exposing rsync device'
nl|'\n'
dedent|''
name|'if'
name|'port_to_config'
op|'['
name|'dev'
op|'['
string|"'port'"
op|']'
op|']'
op|'.'
name|'get'
op|'('
string|"'vm_test_mode'"
op|','
name|'False'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'rsync_export'
op|'='
string|"'%s%s'"
op|'%'
op|'('
name|'server'
op|','
name|'dev'
op|'['
string|"'replication_port'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'rsync_export'
op|'='
name|'server'
newline|'\n'
dedent|''
name|'cmd'
op|'='
string|'"rsync rsync://localhost/%s"'
op|'%'
name|'rsync_export'
newline|'\n'
name|'p'
op|'='
name|'Popen'
op|'('
name|'cmd'
op|','
name|'shell'
op|'='
name|'True'
op|','
name|'stdout'
op|'='
name|'PIPE'
op|')'
newline|'\n'
name|'stdout'
op|','
name|'_stderr'
op|'='
name|'p'
op|'.'
name|'communicate'
op|'('
op|')'
newline|'\n'
name|'if'
name|'p'
op|'.'
name|'returncode'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'SkipTest'
op|'('
string|"'unable to connect to rsync '"
nl|'\n'
string|"'export %s (%s)'"
op|'%'
op|'('
name|'rsync_export'
op|','
name|'cmd'
op|')'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'line'
name|'in'
name|'stdout'
op|'.'
name|'splitlines'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'line'
op|'.'
name|'rsplit'
op|'('
name|'None'
op|','
number|'1'
op|')'
op|'['
op|'-'
number|'1'
op|']'
op|'=='
name|'dev'
op|'['
string|"'device'"
op|']'
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'SkipTest'
op|'('
string|'"unable to find ring device %s under rsync\'s "'
nl|'\n'
string|'"exported devices for %s (%s)"'
op|'%'
nl|'\n'
op|'('
name|'dev'
op|'['
string|"'device'"
op|']'
op|','
name|'rsync_export'
op|','
name|'cmd'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'ring'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_policy
dedent|''
name|'def'
name|'get_policy'
op|'('
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'kwargs'
op|'.'
name|'setdefault'
op|'('
string|"'is_deprecated'"
op|','
name|'False'
op|')'
newline|'\n'
comment|'# go through the policies and make sure they match the'
nl|'\n'
comment|'# requirements of kwargs'
nl|'\n'
name|'for'
name|'policy'
name|'in'
name|'POLICIES'
op|':'
newline|'\n'
comment|'# TODO: for EC, pop policy type here and check it first'
nl|'\n'
indent|'        '
name|'matches'
op|'='
name|'True'
newline|'\n'
name|'for'
name|'key'
op|','
name|'value'
name|'in'
name|'kwargs'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'getattr'
op|'('
name|'policy'
op|','
name|'key'
op|')'
op|'!='
name|'value'
op|':'
newline|'\n'
indent|'                    '
name|'matches'
op|'='
name|'False'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'AttributeError'
op|':'
newline|'\n'
indent|'                '
name|'matches'
op|'='
name|'False'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'matches'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'policy'
newline|'\n'
dedent|''
dedent|''
name|'raise'
name|'SkipTest'
op|'('
string|"'No policy matching %s'"
op|'%'
name|'kwargs'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ProbeTest
dedent|''
name|'class'
name|'ProbeTest'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Don\'t instantiate this directly, use a child class instead.\n    """'
newline|'\n'
nl|'\n'
DECL|member|setUp
name|'def'
name|'setUp'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'p'
op|'='
name|'Popen'
op|'('
string|'"resetswift 2>&1"'
op|','
name|'shell'
op|'='
name|'True'
op|','
name|'stdout'
op|'='
name|'PIPE'
op|')'
newline|'\n'
name|'stdout'
op|','
name|'_stderr'
op|'='
name|'p'
op|'.'
name|'communicate'
op|'('
op|')'
newline|'\n'
name|'print'
name|'stdout'
newline|'\n'
name|'Manager'
op|'('
op|'['
string|"'all'"
op|']'
op|')'
op|'.'
name|'stop'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'pids'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'account_ring'
op|'='
name|'get_ring'
op|'('
nl|'\n'
string|"'account'"
op|','
nl|'\n'
name|'self'
op|'.'
name|'acct_cont_required_replicas'
op|','
nl|'\n'
name|'self'
op|'.'
name|'acct_cont_required_devices'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'container_ring'
op|'='
name|'get_ring'
op|'('
nl|'\n'
string|"'container'"
op|','
nl|'\n'
name|'self'
op|'.'
name|'acct_cont_required_replicas'
op|','
nl|'\n'
name|'self'
op|'.'
name|'acct_cont_required_devices'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'policy'
op|'='
name|'get_policy'
op|'('
op|'**'
name|'self'
op|'.'
name|'policy_requirements'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'object_ring'
op|'='
name|'get_ring'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'policy'
op|'.'
name|'ring_name'
op|','
nl|'\n'
name|'self'
op|'.'
name|'obj_required_replicas'
op|','
nl|'\n'
name|'self'
op|'.'
name|'obj_required_devices'
op|','
nl|'\n'
name|'server'
op|'='
string|"'object'"
op|')'
newline|'\n'
name|'Manager'
op|'('
op|'['
string|"'main'"
op|']'
op|')'
op|'.'
name|'start'
op|'('
name|'wait'
op|'='
name|'False'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'port2server'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'server'
op|','
name|'port'
name|'in'
op|'['
op|'('
string|"'account'"
op|','
number|'6002'
op|')'
op|','
op|'('
string|"'container'"
op|','
number|'6001'
op|')'
op|','
nl|'\n'
op|'('
string|"'object'"
op|','
number|'6000'
op|')'
op|']'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'number'
name|'in'
name|'xrange'
op|'('
number|'1'
op|','
number|'9'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'port2server'
op|'['
name|'port'
op|'+'
op|'('
name|'number'
op|'*'
number|'10'
op|')'
op|']'
op|'='
string|"'%s%d'"
op|'%'
op|'('
name|'server'
op|','
name|'number'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'for'
name|'port'
name|'in'
name|'self'
op|'.'
name|'port2server'
op|':'
newline|'\n'
indent|'                '
name|'check_server'
op|'('
name|'port'
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
dedent|''
name|'self'
op|'.'
name|'port2server'
op|'['
number|'8080'
op|']'
op|'='
string|"'proxy'"
newline|'\n'
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
name|'self'
op|'.'
name|'account'
op|'='
name|'check_server'
op|'('
number|'8080'
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
name|'self'
op|'.'
name|'configs'
op|'='
name|'defaultdict'
op|'('
name|'dict'
op|')'
newline|'\n'
name|'for'
name|'name'
name|'in'
op|'('
string|"'account'"
op|','
string|"'container'"
op|','
string|"'object'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'server_name'
name|'in'
op|'('
name|'name'
op|','
string|"'%s-replicator'"
op|'%'
name|'name'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'for'
name|'server'
name|'in'
name|'Manager'
op|'('
op|'['
name|'server_name'
op|']'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'for'
name|'i'
op|','
name|'conf'
name|'in'
name|'enumerate'
op|'('
name|'server'
op|'.'
name|'conf_files'
op|'('
op|')'
op|','
number|'1'
op|')'
op|':'
newline|'\n'
indent|'                            '
name|'self'
op|'.'
name|'configs'
op|'['
name|'server'
op|'.'
name|'server'
op|']'
op|'['
name|'i'
op|']'
op|'='
name|'conf'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
name|'self'
op|'.'
name|'replicators'
op|'='
name|'Manager'
op|'('
nl|'\n'
op|'['
string|"'account-replicator'"
op|','
string|"'container-replicator'"
op|','
nl|'\n'
string|"'object-replicator'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'updaters'
op|'='
name|'Manager'
op|'('
op|'['
string|"'container-updater'"
op|','
string|"'object-updater'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'server_port_to_conf'
op|'='
op|'{'
op|'}'
newline|'\n'
comment|'# get some configs backend daemon configs loaded up'
nl|'\n'
name|'for'
name|'server'
name|'in'
op|'('
string|"'account'"
op|','
string|"'container'"
op|','
string|"'object'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'server_port_to_conf'
op|'['
name|'server'
op|']'
op|'='
name|'build_port_to_conf'
op|'('
name|'server'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'BaseException'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'raise'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'Manager'
op|'('
op|'['
string|"'all'"
op|']'
op|')'
op|'.'
name|'kill'
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
nl|'\n'
DECL|member|tearDown
dedent|''
dedent|''
dedent|''
dedent|''
name|'def'
name|'tearDown'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'Manager'
op|'('
op|'['
string|"'all'"
op|']'
op|')'
op|'.'
name|'kill'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|device_dir
dedent|''
name|'def'
name|'device_dir'
op|'('
name|'self'
op|','
name|'server'
op|','
name|'node'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'conf'
op|'='
name|'self'
op|'.'
name|'server_port_to_conf'
op|'['
name|'server'
op|']'
op|'['
name|'node'
op|'['
string|"'port'"
op|']'
op|']'
newline|'\n'
name|'return'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'conf'
op|'['
string|"'devices'"
op|']'
op|','
name|'node'
op|'['
string|"'device'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|storage_dir
dedent|''
name|'def'
name|'storage_dir'
op|'('
name|'self'
op|','
name|'server'
op|','
name|'node'
op|','
name|'part'
op|'='
name|'None'
op|','
name|'policy'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'policy'
op|'='
name|'policy'
name|'or'
name|'self'
op|'.'
name|'policy'
newline|'\n'
name|'device_path'
op|'='
name|'self'
op|'.'
name|'device_dir'
op|'('
name|'server'
op|','
name|'node'
op|')'
newline|'\n'
name|'path_parts'
op|'='
op|'['
name|'device_path'
op|','
name|'get_data_dir'
op|'('
name|'policy'
op|')'
op|']'
newline|'\n'
name|'if'
name|'part'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'path_parts'
op|'.'
name|'append'
op|'('
name|'str'
op|'('
name|'part'
op|')'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
op|'*'
name|'path_parts'
op|')'
newline|'\n'
nl|'\n'
DECL|member|config_number
dedent|''
name|'def'
name|'config_number'
op|'('
name|'self'
op|','
name|'node'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'_server_type'
op|','
name|'config_number'
op|'='
name|'get_server_number'
op|'('
nl|'\n'
name|'node'
op|'['
string|"'port'"
op|']'
op|','
name|'self'
op|'.'
name|'port2server'
op|')'
newline|'\n'
name|'return'
name|'config_number'
newline|'\n'
nl|'\n'
DECL|member|get_to_final_state
dedent|''
name|'def'
name|'get_to_final_state'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# these .stop()s are probably not strictly necessary,'
nl|'\n'
comment|'# but may prevent race conditions'
nl|'\n'
indent|'        '
name|'self'
op|'.'
name|'replicators'
op|'.'
name|'stop'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'updaters'
op|'.'
name|'stop'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'replicators'
op|'.'
name|'once'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'updaters'
op|'.'
name|'once'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'replicators'
op|'.'
name|'once'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|kill_drive
dedent|''
name|'def'
name|'kill_drive'
op|'('
name|'self'
op|','
name|'device'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'os'
op|'.'
name|'path'
op|'.'
name|'ismount'
op|'('
name|'device'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'os'
op|'.'
name|'system'
op|'('
string|"'sudo umount %s'"
op|'%'
name|'device'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'renamer'
op|'('
name|'device'
op|','
name|'device'
op|'+'
string|'"X"'
op|')'
newline|'\n'
nl|'\n'
DECL|member|revive_drive
dedent|''
dedent|''
name|'def'
name|'revive_drive'
op|'('
name|'self'
op|','
name|'device'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'disabled_name'
op|'='
name|'device'
op|'+'
string|'"X"'
newline|'\n'
name|'if'
name|'os'
op|'.'
name|'path'
op|'.'
name|'isdir'
op|'('
name|'disabled_name'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'renamer'
op|'('
name|'device'
op|'+'
string|'"X"'
op|','
name|'device'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'os'
op|'.'
name|'system'
op|'('
string|"'sudo mount %s'"
op|'%'
name|'device'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ReplProbeTest
dedent|''
dedent|''
dedent|''
name|'class'
name|'ReplProbeTest'
op|'('
name|'ProbeTest'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|variable|acct_cont_required_replicas
indent|'    '
name|'acct_cont_required_replicas'
op|'='
number|'3'
newline|'\n'
DECL|variable|acct_cont_required_devices
name|'acct_cont_required_devices'
op|'='
number|'4'
newline|'\n'
DECL|variable|obj_required_replicas
name|'obj_required_replicas'
op|'='
number|'3'
newline|'\n'
DECL|variable|obj_required_devices
name|'obj_required_devices'
op|'='
number|'4'
newline|'\n'
DECL|variable|policy_requirements
name|'policy_requirements'
op|'='
op|'{'
string|"'policy_type'"
op|':'
name|'REPL_POLICY'
op|'}'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ECProbeTest
dedent|''
name|'class'
name|'ECProbeTest'
op|'('
name|'ProbeTest'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|variable|acct_cont_required_replicas
indent|'    '
name|'acct_cont_required_replicas'
op|'='
number|'3'
newline|'\n'
DECL|variable|acct_cont_required_devices
name|'acct_cont_required_devices'
op|'='
number|'4'
newline|'\n'
DECL|variable|obj_required_replicas
name|'obj_required_replicas'
op|'='
number|'6'
newline|'\n'
DECL|variable|obj_required_devices
name|'obj_required_devices'
op|'='
number|'8'
newline|'\n'
DECL|variable|policy_requirements
name|'policy_requirements'
op|'='
op|'{'
string|"'policy_type'"
op|':'
name|'EC_POLICY'
op|'}'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
name|'if'
name|'__name__'
op|'=='
string|'"__main__"'
op|':'
newline|'\n'
indent|'    '
name|'for'
name|'server'
name|'in'
op|'('
string|"'account'"
op|','
string|"'container'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'get_ring'
op|'('
name|'server'
op|','
number|'3'
op|','
number|'4'
op|','
nl|'\n'
DECL|variable|force_validate
name|'force_validate'
op|'='
name|'True'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'SkipTest'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'sys'
op|'.'
name|'exit'
op|'('
string|"'%s ERROR: %s'"
op|'%'
op|'('
name|'server'
op|','
name|'err'
op|')'
op|')'
newline|'\n'
dedent|''
name|'print'
string|"'%s OK'"
op|'%'
name|'server'
newline|'\n'
dedent|''
name|'for'
name|'policy'
name|'in'
name|'POLICIES'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'get_ring'
op|'('
name|'policy'
op|'.'
name|'ring_name'
op|','
number|'3'
op|','
number|'4'
op|','
nl|'\n'
name|'server'
op|'='
string|"'object'"
op|','
name|'force_validate'
op|'='
name|'True'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'SkipTest'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'sys'
op|'.'
name|'exit'
op|'('
string|"'object ERROR (%s): %s'"
op|'%'
op|'('
name|'policy'
op|'.'
name|'name'
op|','
name|'err'
op|')'
op|')'
newline|'\n'
dedent|''
name|'print'
string|"'object OK (%s)'"
op|'%'
name|'policy'
op|'.'
name|'name'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
