begin_unit
comment|'#!/usr/bin/python -u'
nl|'\n'
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
name|'unittest'
newline|'\n'
name|'from'
name|'os'
name|'import'
name|'kill'
newline|'\n'
name|'from'
name|'signal'
name|'import'
name|'SIGTERM'
newline|'\n'
name|'from'
name|'subprocess'
name|'import'
name|'Popen'
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'sleep'
newline|'\n'
nl|'\n'
name|'from'
name|'swiftclient'
name|'import'
name|'client'
newline|'\n'
nl|'\n'
name|'from'
name|'test'
op|'.'
name|'probe'
op|'.'
name|'common'
name|'import'
name|'get_to_final_state'
op|','
name|'kill_pids'
op|','
name|'reset_environment'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestRunningWithEachTypeDown
name|'class'
name|'TestRunningWithEachTypeDown'
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
name|'pids'
op|','
name|'self'
op|'.'
name|'port2server'
op|','
name|'self'
op|'.'
name|'account_ring'
op|','
name|'self'
op|'.'
name|'container_ring'
op|','
name|'self'
op|'.'
name|'object_ring'
op|','
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
name|'reset_environment'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|tearDown
dedent|''
name|'def'
name|'tearDown'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'kill_pids'
op|'('
name|'self'
op|'.'
name|'pids'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_main
dedent|''
name|'def'
name|'test_main'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# TODO: This test "randomly" pass or doesn\'t pass; need to find out why'
nl|'\n'
indent|'        '
name|'return'
newline|'\n'
name|'apart'
op|','
name|'anodes'
op|'='
name|'self'
op|'.'
name|'account_ring'
op|'.'
name|'get_nodes'
op|'('
name|'self'
op|'.'
name|'account'
op|')'
newline|'\n'
name|'kill'
op|'('
name|'self'
op|'.'
name|'pids'
op|'['
name|'self'
op|'.'
name|'port2server'
op|'['
name|'anodes'
op|'['
number|'0'
op|']'
op|'['
string|"'port'"
op|']'
op|']'
op|']'
op|','
name|'SIGTERM'
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
string|"'container1'"
op|')'
newline|'\n'
name|'kill'
op|'('
name|'self'
op|'.'
name|'pids'
op|'['
name|'self'
op|'.'
name|'port2server'
op|'['
name|'cnodes'
op|'['
number|'0'
op|']'
op|'['
string|"'port'"
op|']'
op|']'
op|']'
op|','
name|'SIGTERM'
op|')'
newline|'\n'
name|'opart'
op|','
name|'onodes'
op|'='
name|'self'
op|'.'
name|'object_ring'
op|'.'
name|'get_nodes'
op|'('
name|'self'
op|'.'
name|'account'
op|','
string|"'container1'"
op|','
string|"'object1'"
op|')'
newline|'\n'
name|'kill'
op|'('
name|'self'
op|'.'
name|'pids'
op|'['
name|'self'
op|'.'
name|'port2server'
op|'['
name|'onodes'
op|'['
number|'0'
op|']'
op|'['
string|"'port'"
op|']'
op|']'
op|']'
op|','
name|'SIGTERM'
op|')'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
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
string|"'container1'"
op|')'
newline|'\n'
dedent|''
name|'except'
name|'client'
op|'.'
name|'ClientException'
op|','
name|'err'
op|':'
newline|'\n'
comment|'# This might 503 if one of the up container nodes tries to update'
nl|'\n'
comment|"# the down account node. It'll still be saved on one node, but we"
nl|'\n'
comment|"# can't assure the user."
nl|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
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
string|"'container1'"
op|','
string|"'object1'"
op|','
string|"'1234'"
op|')'
newline|'\n'
name|'get_to_final_state'
op|'('
op|')'
newline|'\n'
name|'headers'
op|','
name|'containers'
op|'='
name|'client'
op|'.'
name|'head_account'
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
string|"'4'"
op|')'
newline|'\n'
name|'found1'
op|'='
name|'False'
newline|'\n'
name|'for'
name|'container'
name|'in'
name|'containers'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'container'
op|'['
string|"'name'"
op|']'
op|'=='
string|"'container1'"
op|':'
newline|'\n'
indent|'                '
name|'found1'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'container'
op|'['
string|"'count'"
op|']'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'container'
op|'['
string|"'bytes'"
op|']'
op|','
number|'4'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found1'
op|')'
newline|'\n'
name|'found1'
op|'='
name|'False'
newline|'\n'
name|'for'
name|'obj'
name|'in'
name|'client'
op|'.'
name|'get_container'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
string|"'container1'"
op|')'
op|'['
number|'1'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'obj'
op|'['
string|"'name'"
op|']'
op|'=='
string|"'object1'"
op|':'
newline|'\n'
indent|'                '
name|'found1'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'obj'
op|'['
string|"'bytes'"
op|']'
op|','
number|'4'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found1'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'pids'
op|'['
name|'self'
op|'.'
name|'port2server'
op|'['
name|'anodes'
op|'['
number|'0'
op|']'
op|'['
string|"'port'"
op|']'
op|']'
op|']'
op|'='
name|'Popen'
op|'('
op|'['
string|"'swift-account-server'"
op|','
nl|'\n'
string|"'/etc/swift/account-server/%d.conf'"
op|'%'
nl|'\n'
op|'('
op|'('
name|'anodes'
op|'['
number|'0'
op|']'
op|'['
string|"'port'"
op|']'
op|'-'
number|'6002'
op|')'
op|'/'
number|'10'
op|')'
op|']'
op|')'
op|'.'
name|'pid'
newline|'\n'
name|'self'
op|'.'
name|'pids'
op|'['
name|'self'
op|'.'
name|'port2server'
op|'['
name|'cnodes'
op|'['
number|'0'
op|']'
op|'['
string|"'port'"
op|']'
op|']'
op|']'
op|'='
name|'Popen'
op|'('
op|'['
string|"'swift-container-server'"
op|','
nl|'\n'
string|"'/etc/swift/container-server/%d.conf'"
op|'%'
nl|'\n'
op|'('
op|'('
name|'cnodes'
op|'['
number|'0'
op|']'
op|'['
string|"'port'"
op|']'
op|'-'
number|'6001'
op|')'
op|'/'
number|'10'
op|')'
op|']'
op|')'
op|'.'
name|'pid'
newline|'\n'
name|'self'
op|'.'
name|'pids'
op|'['
name|'self'
op|'.'
name|'port2server'
op|'['
name|'onodes'
op|'['
number|'0'
op|']'
op|'['
string|"'port'"
op|']'
op|']'
op|']'
op|'='
name|'Popen'
op|'('
op|'['
string|"'swift-object-server'"
op|','
nl|'\n'
string|"'/etc/swift/object-server/%d.conf'"
op|'%'
nl|'\n'
op|'('
op|'('
name|'onodes'
op|'['
number|'0'
op|']'
op|'['
string|"'port'"
op|']'
op|'-'
number|'6000'
op|')'
op|'/'
number|'10'
op|')'
op|']'
op|')'
op|'.'
name|'pid'
newline|'\n'
name|'sleep'
op|'('
number|'2'
op|')'
newline|'\n'
name|'headers'
op|','
name|'containers'
op|'='
name|'client'
op|'.'
name|'head_account'
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
string|"'4'"
op|')'
newline|'\n'
name|'found1'
op|'='
name|'False'
newline|'\n'
name|'for'
name|'container'
name|'in'
name|'containers'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'container'
op|'['
string|"'name'"
op|']'
op|'=='
string|"'container1'"
op|':'
newline|'\n'
indent|'                '
name|'found1'
op|'='
name|'True'
newline|'\n'
comment|'# The account node was previously down.'
nl|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assert_'
op|'('
name|'not'
name|'found1'
op|')'
newline|'\n'
name|'found1'
op|'='
name|'False'
newline|'\n'
name|'for'
name|'obj'
name|'in'
name|'client'
op|'.'
name|'get_container'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
string|"'container1'"
op|')'
op|'['
number|'1'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'obj'
op|'['
string|"'name'"
op|']'
op|'=='
string|"'object1'"
op|':'
newline|'\n'
indent|'                '
name|'found1'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'obj'
op|'['
string|"'bytes'"
op|']'
op|','
number|'4'
op|')'
newline|'\n'
comment|'# The first container node 404s, but the proxy will try the next node'
nl|'\n'
comment|'# and succeed.'
nl|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found1'
op|')'
newline|'\n'
nl|'\n'
name|'get_to_final_state'
op|'('
op|')'
newline|'\n'
name|'headers'
op|','
name|'containers'
op|'='
name|'client'
op|'.'
name|'head_account'
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
string|"'4'"
op|')'
newline|'\n'
name|'found1'
op|'='
name|'False'
newline|'\n'
name|'for'
name|'container'
name|'in'
name|'containers'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'container'
op|'['
string|"'name'"
op|']'
op|'=='
string|"'container1'"
op|':'
newline|'\n'
indent|'                '
name|'found1'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'container'
op|'['
string|"'count'"
op|']'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'container'
op|'['
string|"'bytes'"
op|']'
op|','
number|'4'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found1'
op|')'
newline|'\n'
name|'found1'
op|'='
name|'False'
newline|'\n'
name|'for'
name|'obj'
name|'in'
name|'client'
op|'.'
name|'get_container'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
string|"'container1'"
op|')'
op|'['
number|'1'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'obj'
op|'['
string|"'name'"
op|']'
op|'=='
string|"'object1'"
op|':'
newline|'\n'
indent|'                '
name|'found1'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'obj'
op|'['
string|"'bytes'"
op|']'
op|','
number|'4'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found1'
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
