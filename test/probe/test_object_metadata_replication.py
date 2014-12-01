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
name|'import'
name|'functools'
newline|'\n'
nl|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'shutil'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'import'
name|'uuid'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'internal_client'
op|','
name|'utils'
newline|'\n'
nl|'\n'
name|'from'
name|'test'
op|'.'
name|'probe'
op|'.'
name|'brain'
name|'import'
name|'BrainSplitter'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'probe'
op|'.'
name|'common'
name|'import'
name|'kill_servers'
op|','
name|'reset_environment'
op|','
name|'get_to_final_state'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|_sync_methods
name|'def'
name|'_sync_methods'
op|'('
name|'object_server_config_paths'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Get the set of all configured sync_methods for the object-replicator\n    sections in the list of config paths.\n    """'
newline|'\n'
name|'sync_methods'
op|'='
name|'set'
op|'('
op|')'
newline|'\n'
name|'for'
name|'config_path'
name|'in'
name|'object_server_config_paths'
op|':'
newline|'\n'
indent|'        '
name|'options'
op|'='
name|'utils'
op|'.'
name|'readconf'
op|'('
name|'config_path'
op|','
string|"'object-replicator'"
op|')'
newline|'\n'
name|'sync_methods'
op|'.'
name|'add'
op|'('
name|'options'
op|'.'
name|'get'
op|'('
string|"'sync_method'"
op|','
string|"'rsync'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'sync_methods'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|expected_failure_with_ssync
dedent|''
name|'def'
name|'expected_failure_with_ssync'
op|'('
name|'m'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Wrapper for probetests that don\'t pass if you use ssync\n    """'
newline|'\n'
op|'@'
name|'functools'
op|'.'
name|'wraps'
op|'('
name|'m'
op|')'
newline|'\n'
DECL|function|wrapper
name|'def'
name|'wrapper'
op|'('
name|'self'
op|','
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'obj_conf'
op|'='
name|'self'
op|'.'
name|'configs'
op|'['
string|"'object-server'"
op|']'
newline|'\n'
name|'config_paths'
op|'='
op|'['
name|'v'
name|'for'
name|'k'
op|','
name|'v'
name|'in'
name|'obj_conf'
op|'.'
name|'items'
op|'('
op|')'
nl|'\n'
name|'if'
name|'k'
name|'in'
name|'self'
op|'.'
name|'brain'
op|'.'
name|'handoff_numbers'
op|']'
newline|'\n'
name|'using_ssync'
op|'='
string|"'ssync'"
name|'in'
name|'_sync_methods'
op|'('
name|'config_paths'
op|')'
newline|'\n'
name|'failed'
op|'='
name|'False'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'m'
op|'('
name|'self'
op|','
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'AssertionError'
op|':'
newline|'\n'
indent|'            '
name|'failed'
op|'='
name|'True'
newline|'\n'
name|'if'
name|'not'
name|'using_ssync'
op|':'
newline|'\n'
indent|'                '
name|'raise'
newline|'\n'
dedent|''
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'using_ssync'
name|'and'
name|'not'
name|'failed'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'fail'
op|'('
string|"'This test is expected to fail with ssync'"
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'return'
name|'wrapper'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|Test
dedent|''
name|'class'
name|'Test'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
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
string|'"""\n        Reset all environment and start all servers.\n        """'
newline|'\n'
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
name|'policy'
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
name|'self'
op|'.'
name|'container_name'
op|'='
string|"'container-%s'"
op|'%'
name|'uuid'
op|'.'
name|'uuid4'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'object_name'
op|'='
string|"'object-%s'"
op|'%'
name|'uuid'
op|'.'
name|'uuid4'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'brain'
op|'='
name|'BrainSplitter'
op|'('
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
name|'container_name'
op|','
nl|'\n'
name|'self'
op|'.'
name|'object_name'
op|','
string|"'object'"
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
string|'"""\n        [DEFAULT]\n        swift_dir = /etc/swift\n\n        [pipeline:main]\n        pipeline = catch_errors cache proxy-server\n\n        [app:proxy-server]\n        use = egg:swift#proxy\n        object_post_as_copy = false\n\n        [filter:cache]\n        use = egg:swift#memcache\n\n        [filter:catch_errors]\n        use = egg:swift#catch_errors\n        """'
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
string|'"""\n        Stop all servers.\n        """'
newline|'\n'
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
DECL|member|_put_object
dedent|''
name|'def'
name|'_put_object'
op|'('
name|'self'
op|','
name|'headers'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
name|'headers'
name|'or'
op|'{'
op|'}'
newline|'\n'
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
name|'self'
op|'.'
name|'container_name'
op|','
nl|'\n'
name|'self'
op|'.'
name|'object_name'
op|','
name|'headers'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_post_object
dedent|''
name|'def'
name|'_post_object'
op|'('
name|'self'
op|','
name|'headers'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'int_client'
op|'.'
name|'set_object_metadata'
op|'('
name|'self'
op|'.'
name|'account'
op|','
name|'self'
op|'.'
name|'container_name'
op|','
nl|'\n'
name|'self'
op|'.'
name|'object_name'
op|','
name|'headers'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_get_object_metadata
dedent|''
name|'def'
name|'_get_object_metadata'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
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
nl|'\n'
name|'self'
op|'.'
name|'container_name'
op|','
nl|'\n'
name|'self'
op|'.'
name|'object_name'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'expected_failure_with_ssync'
newline|'\n'
DECL|member|test_sysmeta_after_replication_with_subsequent_post
name|'def'
name|'test_sysmeta_after_replication_with_subsequent_post'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'sysmeta'
op|'='
op|'{'
string|"'x-object-sysmeta-foo'"
op|':'
string|"'sysmeta-foo'"
op|'}'
newline|'\n'
name|'usermeta'
op|'='
op|'{'
string|"'x-object-meta-bar'"
op|':'
string|"'meta-bar'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'brain'
op|'.'
name|'put_container'
op|'('
name|'policy_index'
op|'='
number|'0'
op|')'
newline|'\n'
comment|'# put object'
nl|'\n'
name|'self'
op|'.'
name|'_put_object'
op|'('
op|')'
newline|'\n'
comment|'# put newer object with sysmeta to first server subset'
nl|'\n'
name|'self'
op|'.'
name|'brain'
op|'.'
name|'stop_primary_half'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_put_object'
op|'('
name|'headers'
op|'='
name|'sysmeta'
op|')'
newline|'\n'
name|'metadata'
op|'='
name|'self'
op|'.'
name|'_get_object_metadata'
op|'('
op|')'
newline|'\n'
name|'for'
name|'key'
name|'in'
name|'sysmeta'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'key'
name|'in'
name|'metadata'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'metadata'
op|'['
name|'key'
op|']'
op|','
name|'sysmeta'
op|'['
name|'key'
op|']'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'brain'
op|'.'
name|'start_primary_half'
op|'('
op|')'
newline|'\n'
nl|'\n'
comment|'# post some user meta to second server subset'
nl|'\n'
name|'self'
op|'.'
name|'brain'
op|'.'
name|'stop_handoff_half'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_post_object'
op|'('
name|'usermeta'
op|')'
newline|'\n'
name|'metadata'
op|'='
name|'self'
op|'.'
name|'_get_object_metadata'
op|'('
op|')'
newline|'\n'
name|'for'
name|'key'
name|'in'
name|'usermeta'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'key'
name|'in'
name|'metadata'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'metadata'
op|'['
name|'key'
op|']'
op|','
name|'usermeta'
op|'['
name|'key'
op|']'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'key'
name|'in'
name|'sysmeta'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'key'
name|'in'
name|'metadata'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'brain'
op|'.'
name|'start_handoff_half'
op|'('
op|')'
newline|'\n'
nl|'\n'
comment|'# run replicator'
nl|'\n'
name|'get_to_final_state'
op|'('
op|')'
newline|'\n'
nl|'\n'
comment|'# check user metadata has been replicated to first server subset'
nl|'\n'
comment|'# and sysmeta is unchanged'
nl|'\n'
name|'self'
op|'.'
name|'brain'
op|'.'
name|'stop_primary_half'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'='
name|'self'
op|'.'
name|'_get_object_metadata'
op|'('
op|')'
newline|'\n'
name|'expected'
op|'='
name|'dict'
op|'('
name|'sysmeta'
op|')'
newline|'\n'
name|'expected'
op|'.'
name|'update'
op|'('
name|'usermeta'
op|')'
newline|'\n'
name|'for'
name|'key'
name|'in'
name|'expected'
op|'.'
name|'keys'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'key'
name|'in'
name|'metadata'
op|','
name|'key'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'metadata'
op|'['
name|'key'
op|']'
op|','
name|'expected'
op|'['
name|'key'
op|']'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'brain'
op|'.'
name|'start_primary_half'
op|'('
op|')'
newline|'\n'
nl|'\n'
comment|'# check user metadata and sysmeta both on second server subset'
nl|'\n'
name|'self'
op|'.'
name|'brain'
op|'.'
name|'stop_handoff_half'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'='
name|'self'
op|'.'
name|'_get_object_metadata'
op|'('
op|')'
newline|'\n'
name|'for'
name|'key'
name|'in'
name|'expected'
op|'.'
name|'keys'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'key'
name|'in'
name|'metadata'
op|','
name|'key'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'metadata'
op|'['
name|'key'
op|']'
op|','
name|'expected'
op|'['
name|'key'
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_sysmeta_after_replication_with_prior_post
dedent|''
dedent|''
name|'def'
name|'test_sysmeta_after_replication_with_prior_post'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'sysmeta'
op|'='
op|'{'
string|"'x-object-sysmeta-foo'"
op|':'
string|"'sysmeta-foo'"
op|'}'
newline|'\n'
name|'usermeta'
op|'='
op|'{'
string|"'x-object-meta-bar'"
op|':'
string|"'meta-bar'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'brain'
op|'.'
name|'put_container'
op|'('
name|'policy_index'
op|'='
number|'0'
op|')'
newline|'\n'
comment|'# put object'
nl|'\n'
name|'self'
op|'.'
name|'_put_object'
op|'('
op|')'
newline|'\n'
nl|'\n'
comment|'# put user meta to first server subset'
nl|'\n'
name|'self'
op|'.'
name|'brain'
op|'.'
name|'stop_handoff_half'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_post_object'
op|'('
name|'headers'
op|'='
name|'usermeta'
op|')'
newline|'\n'
name|'metadata'
op|'='
name|'self'
op|'.'
name|'_get_object_metadata'
op|'('
op|')'
newline|'\n'
name|'for'
name|'key'
name|'in'
name|'usermeta'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'key'
name|'in'
name|'metadata'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'metadata'
op|'['
name|'key'
op|']'
op|','
name|'usermeta'
op|'['
name|'key'
op|']'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'brain'
op|'.'
name|'start_handoff_half'
op|'('
op|')'
newline|'\n'
nl|'\n'
comment|'# put newer object with sysmeta to second server subset'
nl|'\n'
name|'self'
op|'.'
name|'brain'
op|'.'
name|'stop_primary_half'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_put_object'
op|'('
name|'headers'
op|'='
name|'sysmeta'
op|')'
newline|'\n'
name|'metadata'
op|'='
name|'self'
op|'.'
name|'_get_object_metadata'
op|'('
op|')'
newline|'\n'
name|'for'
name|'key'
name|'in'
name|'sysmeta'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'key'
name|'in'
name|'metadata'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'metadata'
op|'['
name|'key'
op|']'
op|','
name|'sysmeta'
op|'['
name|'key'
op|']'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'brain'
op|'.'
name|'start_primary_half'
op|'('
op|')'
newline|'\n'
nl|'\n'
comment|'# run replicator'
nl|'\n'
name|'get_to_final_state'
op|'('
op|')'
newline|'\n'
nl|'\n'
comment|'# check stale user metadata is not replicated to first server subset'
nl|'\n'
comment|'# and sysmeta is unchanged'
nl|'\n'
name|'self'
op|'.'
name|'brain'
op|'.'
name|'stop_primary_half'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'='
name|'self'
op|'.'
name|'_get_object_metadata'
op|'('
op|')'
newline|'\n'
name|'for'
name|'key'
name|'in'
name|'sysmeta'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'key'
name|'in'
name|'metadata'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'metadata'
op|'['
name|'key'
op|']'
op|','
name|'sysmeta'
op|'['
name|'key'
op|']'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'key'
name|'in'
name|'usermeta'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'key'
name|'in'
name|'metadata'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'brain'
op|'.'
name|'start_primary_half'
op|'('
op|')'
newline|'\n'
nl|'\n'
comment|'# check stale user metadata is removed from second server subset'
nl|'\n'
comment|'# and sysmeta is replicated'
nl|'\n'
name|'self'
op|'.'
name|'brain'
op|'.'
name|'stop_handoff_half'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'='
name|'self'
op|'.'
name|'_get_object_metadata'
op|'('
op|')'
newline|'\n'
name|'for'
name|'key'
name|'in'
name|'sysmeta'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'key'
name|'in'
name|'metadata'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'metadata'
op|'['
name|'key'
op|']'
op|','
name|'sysmeta'
op|'['
name|'key'
op|']'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'key'
name|'in'
name|'usermeta'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'key'
name|'in'
name|'metadata'
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
string|'"__main__"'
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
