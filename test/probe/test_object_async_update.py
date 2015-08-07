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
name|'io'
name|'import'
name|'StringIO'
newline|'\n'
name|'from'
name|'tempfile'
name|'import'
name|'mkdtemp'
newline|'\n'
name|'from'
name|'textwrap'
name|'import'
name|'dedent'
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
op|','
name|'internal_client'
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
name|'kill_nonprimary_server'
op|','
name|'kill_server'
op|','
name|'ReplProbeTest'
op|','
name|'start_server'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestObjectAsyncUpdate
name|'class'
name|'TestObjectAsyncUpdate'
op|'('
name|'ReplProbeTest'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_main
indent|'    '
name|'def'
name|'test_main'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# Create container'
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
comment|'# Kill container servers excepting two of the primaries'
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
name|'kill_nonprimary_server'
op|'('
name|'cnodes'
op|','
name|'self'
op|'.'
name|'ipport2server'
op|','
name|'self'
op|'.'
name|'pids'
op|')'
newline|'\n'
name|'kill_server'
op|'('
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
op|','
nl|'\n'
name|'self'
op|'.'
name|'ipport2server'
op|','
name|'self'
op|'.'
name|'pids'
op|')'
newline|'\n'
nl|'\n'
comment|'# Create container/obj'
nl|'\n'
name|'obj'
op|'='
string|"'object-%s'"
op|'%'
name|'uuid4'
op|'('
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
string|"''"
op|')'
newline|'\n'
nl|'\n'
comment|'# Restart other primary server'
nl|'\n'
name|'start_server'
op|'('
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
op|','
nl|'\n'
name|'self'
op|'.'
name|'ipport2server'
op|','
name|'self'
op|'.'
name|'pids'
op|')'
newline|'\n'
nl|'\n'
comment|'# Assert it does not know about container/obj'
nl|'\n'
name|'self'
op|'.'
name|'assertFalse'
op|'('
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
op|')'
newline|'\n'
nl|'\n'
comment|'# Run the object-updaters'
nl|'\n'
name|'Manager'
op|'('
op|'['
string|"'object-updater'"
op|']'
op|')'
op|'.'
name|'once'
op|'('
op|')'
newline|'\n'
nl|'\n'
comment|'# Assert the other primary server now knows about container/obj'
nl|'\n'
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
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'obj'
name|'in'
name|'objs'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestUpdateOverrides
dedent|''
dedent|''
name|'class'
name|'TestUpdateOverrides'
op|'('
name|'ReplProbeTest'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Use an internal client to PUT an object to proxy server,\n    bypassing gatekeeper so that X-Backend- headers can be included.\n    Verify that the update override headers take effect and override\n    values propagate to the container server.\n    """'
newline|'\n'
DECL|member|setUp
name|'def'
name|'setUp'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Reset all environment and start all servers.\n        """'
newline|'\n'
name|'super'
op|'('
name|'TestUpdateOverrides'
op|','
name|'self'
op|')'
op|'.'
name|'setUp'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'tempdir'
op|'='
name|'mkdtemp'
op|'('
op|')'
newline|'\n'
name|'conf_path'
op|'='
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
string|"'internal_client.conf'"
op|')'
newline|'\n'
name|'conf_body'
op|'='
string|'"""\n        [DEFAULT]\n        swift_dir = /etc/swift\n\n        [pipeline:main]\n        pipeline = catch_errors cache proxy-server\n\n        [app:proxy-server]\n        use = egg:swift#proxy\n\n        [filter:cache]\n        use = egg:swift#memcache\n\n        [filter:catch_errors]\n        use = egg:swift#catch_errors\n        """'
newline|'\n'
name|'with'
name|'open'
op|'('
name|'conf_path'
op|','
string|"'w'"
op|')'
name|'as'
name|'f'
op|':'
newline|'\n'
indent|'            '
name|'f'
op|'.'
name|'write'
op|'('
name|'dedent'
op|'('
name|'conf_body'
op|')'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'int_client'
op|'='
name|'internal_client'
op|'.'
name|'InternalClient'
op|'('
name|'conf_path'
op|','
string|"'test'"
op|','
number|'1'
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
name|'super'
op|'('
name|'TestUpdateOverrides'
op|','
name|'self'
op|')'
op|'.'
name|'tearDown'
op|'('
op|')'
newline|'\n'
name|'shutil'
op|'.'
name|'rmtree'
op|'('
name|'self'
op|'.'
name|'tempdir'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test
dedent|''
name|'def'
name|'test'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
nl|'\n'
string|"'Content-Type'"
op|':'
string|"'text/plain'"
op|','
nl|'\n'
string|"'X-Backend-Container-Update-Override-Etag'"
op|':'
string|"'override-etag'"
op|','
nl|'\n'
string|"'X-Backend-Container-Update-Override-Content-Type'"
op|':'
string|"'override-type'"
nl|'\n'
op|'}'
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
string|"'c1'"
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Storage-Policy'"
op|':'
nl|'\n'
name|'self'
op|'.'
name|'policy'
op|'.'
name|'name'
op|'}'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'int_client'
op|'.'
name|'upload_object'
op|'('
name|'StringIO'
op|'('
string|"u'stuff'"
op|')'
op|','
name|'self'
op|'.'
name|'account'
op|','
nl|'\n'
string|"'c1'"
op|','
string|"'o1'"
op|','
name|'headers'
op|')'
newline|'\n'
nl|'\n'
comment|'# Run the object-updaters to be sure updates are done'
nl|'\n'
name|'Manager'
op|'('
op|'['
string|"'object-updater'"
op|']'
op|')'
op|'.'
name|'once'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'meta'
op|'='
name|'self'
op|'.'
name|'int_client'
op|'.'
name|'get_object_metadata'
op|'('
name|'self'
op|'.'
name|'account'
op|','
string|"'c1'"
op|','
string|"'o1'"
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
string|"'text/plain'"
op|','
name|'meta'
op|'['
string|"'content-type'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
string|"'c13d88cb4cb02003daedb8a84e5d272a'"
op|','
name|'meta'
op|'['
string|"'etag'"
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'obj_iter'
op|'='
name|'self'
op|'.'
name|'int_client'
op|'.'
name|'iter_objects'
op|'('
name|'self'
op|'.'
name|'account'
op|','
string|"'c1'"
op|')'
newline|'\n'
name|'for'
name|'obj'
name|'in'
name|'obj_iter'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'obj'
op|'['
string|"'name'"
op|']'
op|'=='
string|"'o1'"
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'assertEqual'
op|'('
string|"'override-etag'"
op|','
name|'obj'
op|'['
string|"'hash'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
string|"'override-type'"
op|','
name|'obj'
op|'['
string|"'content_type'"
op|']'
op|')'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'fail'
op|'('
string|"'Failed to find object o1 in listing'"
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
