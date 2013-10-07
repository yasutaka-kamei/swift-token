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
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'shutil'
newline|'\n'
nl|'\n'
name|'from'
name|'subprocess'
name|'import'
name|'call'
newline|'\n'
name|'from'
name|'unittest'
name|'import'
name|'main'
op|','
name|'TestCase'
newline|'\n'
name|'from'
name|'uuid'
name|'import'
name|'uuid4'
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
name|'test'
op|'.'
name|'probe'
op|'.'
name|'common'
name|'import'
name|'kill_server'
op|','
name|'kill_servers'
op|','
name|'reset_environment'
op|','
name|'start_server'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'readconf'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestEmptyDevice
name|'class'
name|'TestEmptyDevice'
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
DECL|member|_get_objects_dir
dedent|''
name|'def'
name|'_get_objects_dir'
op|'('
name|'self'
op|','
name|'onode'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'device'
op|'='
name|'onode'
op|'['
string|"'device'"
op|']'
newline|'\n'
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
name|'obj_server_conf'
op|'='
name|'readconf'
op|'('
name|'self'
op|'.'
name|'configs'
op|'['
string|"'object'"
op|']'
op|'%'
name|'node_id'
op|')'
newline|'\n'
name|'devices'
op|'='
name|'obj_server_conf'
op|'['
string|"'app:object-server'"
op|']'
op|'['
string|"'devices'"
op|']'
newline|'\n'
name|'obj_dir'
op|'='
string|"'%s/%s'"
op|'%'
op|'('
name|'devices'
op|','
name|'device'
op|')'
newline|'\n'
name|'return'
name|'obj_dir'
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
comment|'# Create container'
nl|'\n'
comment|'# Kill one container/obj primary server'
nl|'\n'
comment|'# Delete the "objects" directory on the primary server'
nl|'\n'
comment|'# Create container/obj (goes to two primary servers and one handoff)'
nl|'\n'
comment|'# Kill other two container/obj primary servers'
nl|'\n'
comment|'# Indirectly through proxy assert we can get container/obj'
nl|'\n'
comment|'# Restart those other two container/obj primary servers'
nl|'\n'
comment|'# Directly to handoff server assert we can get container/obj'
nl|'\n'
comment|'# Assert container listing (via proxy and directly) has container/obj'
nl|'\n'
comment|'# Bring the first container/obj primary server back up'
nl|'\n'
comment|"# Assert that it doesn't have container/obj yet"
nl|'\n'
comment|'# Run object replication for first container/obj primary server'
nl|'\n'
comment|'# Run object replication for handoff node'
nl|'\n'
comment|'# Assert the first container/obj primary server now has container/obj'
nl|'\n'
comment|'# Assert the handoff server no longer has container/obj'
nl|'\n'
nl|'\n'
indent|'        '
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
nl|'\n'
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
name|'container'
op|')'
newline|'\n'
name|'cnode'
op|'='
name|'cnodes'
op|'['
number|'0'
op|']'
newline|'\n'
name|'obj'
op|'='
string|"'object-%s'"
op|'%'
name|'uuid4'
op|'('
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
nl|'\n'
name|'self'
op|'.'
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
name|'onode'
op|'='
name|'onodes'
op|'['
number|'0'
op|']'
newline|'\n'
name|'kill_server'
op|'('
name|'onode'
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
name|'obj_dir'
op|'='
string|"'%s/objects'"
op|'%'
name|'self'
op|'.'
name|'_get_objects_dir'
op|'('
name|'onode'
op|')'
newline|'\n'
name|'shutil'
op|'.'
name|'rmtree'
op|'('
name|'obj_dir'
op|','
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'obj_dir'
op|')'
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
name|'container'
op|','
name|'obj'
op|','
string|"'VERIFY'"
op|')'
newline|'\n'
name|'odata'
op|'='
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
name|'container'
op|','
name|'obj'
op|')'
op|'['
op|'-'
number|'1'
op|']'
newline|'\n'
name|'if'
name|'odata'
op|'!='
string|"'VERIFY'"
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'Object GET did not return VERIFY, instead it '"
nl|'\n'
string|"'returned: %s'"
op|'%'
name|'repr'
op|'('
name|'odata'
op|')'
op|')'
newline|'\n'
comment|'# Kill all primaries to ensure GET handoff works'
nl|'\n'
dedent|''
name|'for'
name|'node'
name|'in'
name|'onodes'
op|'['
number|'1'
op|':'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'kill_server'
op|'('
name|'node'
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
dedent|''
name|'odata'
op|'='
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
name|'container'
op|','
name|'obj'
op|')'
op|'['
op|'-'
number|'1'
op|']'
newline|'\n'
name|'if'
name|'odata'
op|'!='
string|"'VERIFY'"
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'Object GET did not return VERIFY, instead it '"
nl|'\n'
string|"'returned: %s'"
op|'%'
name|'repr'
op|'('
name|'odata'
op|')'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'node'
name|'in'
name|'onodes'
op|'['
number|'1'
op|':'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'start_server'
op|'('
name|'node'
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
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'obj_dir'
op|')'
op|')'
newline|'\n'
comment|"# We've indirectly verified the handoff node has the object, but"
nl|'\n'
comment|"# let's directly verify it."
nl|'\n'
dedent|''
name|'another_onode'
op|'='
name|'self'
op|'.'
name|'object_ring'
op|'.'
name|'get_more_nodes'
op|'('
name|'opart'
op|')'
op|'.'
name|'next'
op|'('
op|')'
newline|'\n'
name|'odata'
op|'='
name|'direct_client'
op|'.'
name|'direct_get_object'
op|'('
nl|'\n'
name|'another_onode'
op|','
name|'opart'
op|','
name|'self'
op|'.'
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
op|'['
op|'-'
number|'1'
op|']'
newline|'\n'
name|'if'
name|'odata'
op|'!='
string|"'VERIFY'"
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'Direct object GET did not return VERIFY, instead '"
nl|'\n'
string|"'it returned: %s'"
op|'%'
name|'repr'
op|'('
name|'odata'
op|')'
op|')'
newline|'\n'
dedent|''
name|'objs'
op|'='
op|'['
name|'o'
op|'['
string|"'name'"
op|']'
name|'for'
name|'o'
name|'in'
nl|'\n'
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
name|'container'
op|')'
op|'['
number|'1'
op|']'
op|']'
newline|'\n'
name|'if'
name|'obj'
name|'not'
name|'in'
name|'objs'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'Container listing did not know about object'"
op|')'
newline|'\n'
dedent|''
name|'for'
name|'cnode'
name|'in'
name|'cnodes'
op|':'
newline|'\n'
indent|'            '
name|'objs'
op|'='
op|'['
name|'o'
op|'['
string|"'name'"
op|']'
name|'for'
name|'o'
name|'in'
nl|'\n'
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
name|'container'
op|')'
op|'['
number|'1'
op|']'
op|']'
newline|'\n'
name|'if'
name|'obj'
name|'not'
name|'in'
name|'objs'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'Exception'
op|'('
nl|'\n'
string|"'Container server %s:%s did not know about object'"
op|'%'
nl|'\n'
op|'('
name|'cnode'
op|'['
string|"'ip'"
op|']'
op|','
name|'cnode'
op|'['
string|"'port'"
op|']'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'start_server'
op|'('
name|'onode'
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
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'obj_dir'
op|')'
op|')'
newline|'\n'
name|'exc'
op|'='
name|'None'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'direct_client'
op|'.'
name|'direct_get_object'
op|'('
name|'onode'
op|','
name|'opart'
op|','
name|'self'
op|'.'
name|'account'
op|','
nl|'\n'
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'direct_client'
op|'.'
name|'ClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'exc'
op|'='
name|'err'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'exc'
op|'.'
name|'http_status'
op|','
number|'404'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'obj_dir'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'port_num'
op|'='
name|'onode'
op|'['
string|"'replication_port'"
op|']'
newline|'\n'
dedent|''
name|'except'
name|'KeyError'
op|':'
newline|'\n'
indent|'            '
name|'port_num'
op|'='
name|'onode'
op|'['
string|"'port'"
op|']'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'another_port_num'
op|'='
name|'another_onode'
op|'['
string|"'replication_port'"
op|']'
newline|'\n'
dedent|''
name|'except'
name|'KeyError'
op|':'
newline|'\n'
indent|'            '
name|'another_port_num'
op|'='
name|'another_onode'
op|'['
string|"'port'"
op|']'
newline|'\n'
dedent|''
name|'call'
op|'('
op|'['
string|"'swift-object-replicator'"
op|','
nl|'\n'
name|'self'
op|'.'
name|'configs'
op|'['
string|"'object-replicator'"
op|']'
op|'%'
nl|'\n'
op|'('
op|'('
name|'port_num'
op|'-'
number|'6000'
op|')'
op|'/'
number|'10'
op|')'
op|','
string|"'once'"
op|']'
op|')'
newline|'\n'
name|'call'
op|'('
op|'['
string|"'swift-object-replicator'"
op|','
nl|'\n'
name|'self'
op|'.'
name|'configs'
op|'['
string|"'object-replicator'"
op|']'
op|'%'
nl|'\n'
op|'('
op|'('
name|'another_port_num'
op|'-'
number|'6000'
op|')'
op|'/'
number|'10'
op|')'
op|','
string|"'once'"
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'odata'
op|'='
name|'direct_client'
op|'.'
name|'direct_get_object'
op|'('
name|'onode'
op|','
name|'opart'
op|','
name|'self'
op|'.'
name|'account'
op|','
nl|'\n'
name|'container'
op|','
name|'obj'
op|')'
op|'['
op|'-'
number|'1'
op|']'
newline|'\n'
name|'if'
name|'odata'
op|'!='
string|"'VERIFY'"
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'Direct object GET did not return VERIFY, instead '"
nl|'\n'
string|"'it returned: %s'"
op|'%'
name|'repr'
op|'('
name|'odata'
op|')'
op|')'
newline|'\n'
dedent|''
name|'exc'
op|'='
name|'None'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'direct_client'
op|'.'
name|'direct_get_object'
op|'('
name|'another_onode'
op|','
name|'opart'
op|','
name|'self'
op|'.'
name|'account'
op|','
nl|'\n'
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'direct_client'
op|'.'
name|'ClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'exc'
op|'='
name|'err'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'exc'
op|'.'
name|'http_status'
op|','
number|'404'
op|')'
newline|'\n'
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
