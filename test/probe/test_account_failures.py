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
name|'unittest'
name|'import'
name|'main'
op|','
name|'TestCase'
newline|'\n'
nl|'\n'
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
name|'manager'
name|'import'
name|'Manager'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'probe'
op|'.'
name|'common'
name|'import'
name|'get_to_final_state'
op|','
name|'kill_nonprimary_server'
op|','
name|'kill_server'
op|','
name|'kill_servers'
op|','
name|'reset_environment'
op|','
name|'start_server'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestAccountFailures
name|'class'
name|'TestAccountFailures'
op|'('
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
op|'('
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
nl|'\n'
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
nl|'\n'
name|'self'
op|'.'
name|'account'
op|','
name|'self'
op|'.'
name|'configs'
op|')'
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
name|'kill_servers'
op|'('
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
DECL|member|test_main
dedent|''
name|'def'
name|'test_main'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# Create container1 and container2'
nl|'\n'
comment|'# Assert account level sees them'
nl|'\n'
comment|'# Create container2/object1'
nl|'\n'
comment|"# Assert account level doesn't see it yet"
nl|'\n'
comment|'# Get to final state'
nl|'\n'
comment|'# Assert account level now sees the container2/object1'
nl|'\n'
comment|'# Kill account servers excepting two of the primaries'
nl|'\n'
comment|'# Delete container1'
nl|'\n'
comment|"# Assert account level knows container1 is gone but doesn't know about"
nl|'\n'
comment|'#   container2/object2 yet'
nl|'\n'
comment|'# Put container2/object2'
nl|'\n'
comment|'# Run container updaters'
nl|'\n'
comment|'# Assert account level now knows about container2/object2'
nl|'\n'
comment|'# Restart other primary account server'
nl|'\n'
comment|"# Assert that server doesn't know about container1's deletion or the"
nl|'\n'
comment|'#   new container2/object2 yet'
nl|'\n'
comment|'# Get to final state'
nl|'\n'
comment|'# Assert that server is now up to date'
nl|'\n'
nl|'\n'
indent|'        '
name|'container1'
op|'='
string|"'container1'"
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
name|'container2'
op|'='
string|"'container2'"
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
name|'container2'
op|')'
newline|'\n'
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
string|"'2'"
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
name|'found1'
op|'='
name|'False'
newline|'\n'
name|'found2'
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
name|'container1'
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
number|'0'
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
number|'0'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'container'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container2'
op|':'
newline|'\n'
indent|'                '
name|'found2'
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
number|'0'
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
number|'0'
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
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found2'
op|')'
newline|'\n'
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
name|'container2'
op|','
string|"'object1'"
op|','
string|"'1234'"
op|')'
newline|'\n'
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
string|"'2'"
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
name|'found1'
op|'='
name|'False'
newline|'\n'
name|'found2'
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
name|'container1'
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
number|'0'
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
number|'0'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'container'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container2'
op|':'
newline|'\n'
indent|'                '
name|'found2'
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
number|'0'
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
number|'0'
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
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found2'
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
string|"'2'"
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
name|'found2'
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
name|'container1'
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
number|'0'
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
number|'0'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'container'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container2'
op|':'
newline|'\n'
indent|'                '
name|'found2'
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
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found2'
op|')'
newline|'\n'
nl|'\n'
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
name|'kill_nonprimary_server'
op|'('
name|'anodes'
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
name|'anodes'
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
name|'container2'
op|','
string|"'object2'"
op|','
string|"'12345'"
op|')'
newline|'\n'
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
string|"'4'"
op|')'
newline|'\n'
name|'found1'
op|'='
name|'False'
newline|'\n'
name|'found2'
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
name|'container1'
op|':'
newline|'\n'
indent|'                '
name|'found1'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'elif'
name|'container'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container2'
op|':'
newline|'\n'
indent|'                '
name|'found2'
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
name|'not'
name|'found1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found2'
op|')'
newline|'\n'
nl|'\n'
name|'Manager'
op|'('
op|'['
string|"'container-updater'"
op|']'
op|')'
op|'.'
name|'once'
op|'('
op|')'
newline|'\n'
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
string|"'2'"
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
string|"'9'"
op|')'
newline|'\n'
name|'found1'
op|'='
name|'False'
newline|'\n'
name|'found2'
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
name|'container1'
op|':'
newline|'\n'
indent|'                '
name|'found1'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'elif'
name|'container'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container2'
op|':'
newline|'\n'
indent|'                '
name|'found2'
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
number|'2'
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
number|'9'
op|')'
newline|'\n'
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
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found2'
op|')'
newline|'\n'
nl|'\n'
name|'start_server'
op|'('
name|'anodes'
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
name|'headers'
op|','
name|'containers'
op|'='
name|'direct_client'
op|'.'
name|'direct_get_account'
op|'('
name|'anodes'
op|'['
number|'0'
op|']'
op|','
name|'apart'
op|','
name|'self'
op|'.'
name|'account'
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
string|"'2'"
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
name|'found2'
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
name|'container1'
op|':'
newline|'\n'
indent|'                '
name|'found1'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'elif'
name|'container'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container2'
op|':'
newline|'\n'
indent|'                '
name|'found2'
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
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found2'
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
name|'direct_client'
op|'.'
name|'direct_get_account'
op|'('
name|'anodes'
op|'['
number|'0'
op|']'
op|','
name|'apart'
op|','
name|'self'
op|'.'
name|'account'
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
string|"'2'"
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
string|"'9'"
op|')'
newline|'\n'
name|'found1'
op|'='
name|'False'
newline|'\n'
name|'found2'
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
name|'container1'
op|':'
newline|'\n'
indent|'                '
name|'found1'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'elif'
name|'container'
op|'['
string|"'name'"
op|']'
op|'=='
name|'container2'
op|':'
newline|'\n'
indent|'                '
name|'found2'
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
number|'2'
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
number|'9'
op|')'
newline|'\n'
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
name|'self'
op|'.'
name|'assert_'
op|'('
name|'found2'
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
name|'main'
op|'('
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
