begin_unit
comment|'# Copyright (c) 2010 OpenStack, LLC.'
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
name|'contextlib'
name|'import'
name|'contextmanager'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'logging'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'db_replicator'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'db'
op|','
name|'utils'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'container'
name|'import'
name|'server'
name|'as'
name|'container_server'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|teardown_module
name|'def'
name|'teardown_module'
op|'('
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"clean up my monkey patching"'
newline|'\n'
name|'reload'
op|'('
name|'db_replicator'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'contextmanager'
newline|'\n'
DECL|function|lock_parent_directory
name|'def'
name|'lock_parent_directory'
op|'('
name|'filename'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'yield'
name|'True'
newline|'\n'
nl|'\n'
DECL|class|FakeRing
dedent|''
name|'class'
name|'FakeRing'
op|':'
newline|'\n'
DECL|class|Ring
indent|'    '
name|'class'
name|'Ring'
op|':'
newline|'\n'
DECL|variable|devs
indent|'        '
name|'devs'
op|'='
op|'['
op|']'
newline|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'path'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
DECL|member|get_part_nodes
dedent|''
name|'def'
name|'get_part_nodes'
op|'('
name|'self'
op|','
name|'part'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
op|'['
op|']'
newline|'\n'
DECL|member|get_more_nodes
dedent|''
name|'def'
name|'get_more_nodes'
op|'('
name|'self'
op|','
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
op|'['
op|']'
newline|'\n'
nl|'\n'
DECL|class|FakeProcess
dedent|''
dedent|''
dedent|''
name|'class'
name|'FakeProcess'
op|':'
newline|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
op|'*'
name|'codes'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'codes'
op|'='
name|'iter'
op|'('
name|'codes'
op|')'
newline|'\n'
DECL|member|__call__
dedent|''
name|'def'
name|'__call__'
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
DECL|class|Failure
indent|'        '
name|'class'
name|'Failure'
op|':'
newline|'\n'
DECL|member|communicate
indent|'            '
name|'def'
name|'communicate'
op|'('
name|'innerself'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'next'
op|'='
name|'self'
op|'.'
name|'codes'
op|'.'
name|'next'
op|'('
op|')'
newline|'\n'
name|'if'
name|'isinstance'
op|'('
name|'next'
op|','
name|'int'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'innerself'
op|'.'
name|'returncode'
op|'='
name|'next'
newline|'\n'
name|'return'
name|'next'
newline|'\n'
dedent|''
name|'raise'
name|'next'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'Failure'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
op|'@'
name|'contextmanager'
newline|'\n'
DECL|function|_mock_process
name|'def'
name|'_mock_process'
op|'('
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'orig_process'
op|'='
name|'db_replicator'
op|'.'
name|'subprocess'
op|'.'
name|'Popen'
newline|'\n'
name|'db_replicator'
op|'.'
name|'subprocess'
op|'.'
name|'Popen'
op|'='
name|'FakeProcess'
op|'('
op|'*'
name|'args'
op|')'
newline|'\n'
name|'yield'
newline|'\n'
name|'db_replicator'
op|'.'
name|'subprocess'
op|'.'
name|'Popen'
op|'='
name|'orig_process'
newline|'\n'
nl|'\n'
DECL|class|PostReplHttp
dedent|''
name|'class'
name|'PostReplHttp'
op|':'
newline|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'response'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'response'
op|'='
name|'response'
newline|'\n'
DECL|variable|posted
dedent|''
name|'posted'
op|'='
name|'False'
newline|'\n'
DECL|variable|host
name|'host'
op|'='
string|"'localhost'"
newline|'\n'
DECL|member|post
name|'def'
name|'post'
op|'('
name|'self'
op|','
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'posted'
op|'='
name|'True'
newline|'\n'
DECL|class|Response
name|'class'
name|'Response'
op|':'
newline|'\n'
DECL|variable|status
indent|'            '
name|'status'
op|'='
number|'200'
newline|'\n'
DECL|variable|data
name|'data'
op|'='
name|'self'
op|'.'
name|'response'
newline|'\n'
DECL|member|read
name|'def'
name|'read'
op|'('
name|'innerself'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'self'
op|'.'
name|'response'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'Response'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|class|ChangingMtimesOs
dedent|''
dedent|''
name|'class'
name|'ChangingMtimesOs'
op|':'
newline|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'mtime'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'path'
op|'='
name|'self'
newline|'\n'
name|'self'
op|'.'
name|'basename'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'basename'
newline|'\n'
DECL|member|getmtime
dedent|''
name|'def'
name|'getmtime'
op|'('
name|'self'
op|','
name|'file'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'mtime'
op|'+='
number|'1'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'mtime'
newline|'\n'
nl|'\n'
DECL|class|FakeBroker
dedent|''
dedent|''
name|'class'
name|'FakeBroker'
op|':'
newline|'\n'
DECL|variable|db_file
indent|'    '
name|'db_file'
op|'='
name|'__file__'
newline|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
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
name|'return'
name|'None'
newline|'\n'
dedent|''
op|'@'
name|'contextmanager'
newline|'\n'
DECL|member|lock
name|'def'
name|'lock'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'yield'
name|'True'
newline|'\n'
DECL|member|get_sync
dedent|''
name|'def'
name|'get_sync'
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
name|'return'
number|'5'
newline|'\n'
DECL|member|get_syncs
dedent|''
name|'def'
name|'get_syncs'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
op|'['
op|']'
newline|'\n'
DECL|member|get_items_since
dedent|''
name|'def'
name|'get_items_since'
op|'('
name|'self'
op|','
name|'point'
op|','
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'point'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'return'
op|'['
op|'{'
string|"'ROWID'"
op|':'
number|'1'
op|'}'
op|']'
newline|'\n'
dedent|''
name|'return'
op|'['
op|']'
newline|'\n'
DECL|member|merge_syncs
dedent|''
name|'def'
name|'merge_syncs'
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
name|'self'
op|'.'
name|'args'
op|'='
name|'args'
newline|'\n'
DECL|member|merge_items
dedent|''
name|'def'
name|'merge_items'
op|'('
name|'self'
op|','
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'args'
op|'='
name|'args'
newline|'\n'
DECL|member|get_replication_info
dedent|''
name|'def'
name|'get_replication_info'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
op|'{'
string|"'delete_timestamp'"
op|':'
number|'0'
op|','
string|"'put_timestamp'"
op|':'
number|'1'
op|','
string|"'count'"
op|':'
number|'0'
op|'}'
newline|'\n'
DECL|member|reclaim
dedent|''
name|'def'
name|'reclaim'
op|'('
name|'self'
op|','
name|'item_timestamp'
op|','
name|'sync_timestamp'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'db_replicator'
op|'.'
name|'ring'
op|'='
name|'FakeRing'
op|'('
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestReplicator
name|'class'
name|'TestReplicator'
op|'('
name|'db_replicator'
op|'.'
name|'Replicator'
op|')'
op|':'
newline|'\n'
DECL|variable|server_type
indent|'    '
name|'server_type'
op|'='
string|"'container'"
newline|'\n'
DECL|variable|ring_file
name|'ring_file'
op|'='
string|"'container.ring.gz'"
newline|'\n'
DECL|variable|brokerclass
name|'brokerclass'
op|'='
name|'FakeBroker'
newline|'\n'
DECL|variable|datadir
name|'datadir'
op|'='
name|'container_server'
op|'.'
name|'DATADIR'
newline|'\n'
DECL|variable|default_port
name|'default_port'
op|'='
number|'1000'
newline|'\n'
nl|'\n'
DECL|class|TestDBReplicator
dedent|''
name|'class'
name|'TestDBReplicator'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_repl_connection
indent|'    '
name|'def'
name|'test_repl_connection'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'node'
op|'='
op|'{'
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
string|"'port'"
op|':'
number|'80'
op|','
string|"'device'"
op|':'
string|"'sdb1'"
op|'}'
newline|'\n'
name|'conn'
op|'='
name|'db_replicator'
op|'.'
name|'ReplConnection'
op|'('
name|'node'
op|','
string|"'1234567890'"
op|','
string|"'abcdefg'"
op|','
nl|'\n'
name|'logging'
op|'.'
name|'getLogger'
op|'('
op|')'
op|')'
newline|'\n'
DECL|function|req
name|'def'
name|'req'
op|'('
name|'method'
op|','
name|'path'
op|','
name|'body'
op|','
name|'headers'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'method'
op|','
string|"'POST'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'headers'
op|'['
string|"'Content-Type'"
op|']'
op|','
string|"'application/json'"
op|')'
newline|'\n'
DECL|class|Resp
dedent|''
name|'class'
name|'Resp'
op|':'
newline|'\n'
DECL|member|read
indent|'            '
name|'def'
name|'read'
op|'('
name|'self'
op|')'
op|':'
name|'return'
string|"'data'"
newline|'\n'
dedent|''
name|'resp'
op|'='
name|'Resp'
op|'('
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'request'
op|'='
name|'req'
newline|'\n'
name|'conn'
op|'.'
name|'getresponse'
op|'='
name|'lambda'
op|'*'
name|'args'
op|':'
name|'resp'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'conn'
op|'.'
name|'post'
op|'('
number|'1'
op|','
number|'2'
op|','
number|'3'
op|')'
op|','
name|'resp'
op|')'
newline|'\n'
DECL|function|other_req
name|'def'
name|'other_req'
op|'('
name|'method'
op|','
name|'path'
op|','
name|'body'
op|','
name|'headers'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'blah'"
op|')'
newline|'\n'
dedent|''
name|'conn'
op|'.'
name|'request'
op|'='
name|'other_req'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'conn'
op|'.'
name|'post'
op|'('
number|'1'
op|','
number|'2'
op|','
number|'3'
op|')'
op|','
name|'None'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_rsync_file
dedent|''
name|'def'
name|'test_rsync_file'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'replicator'
op|'='
name|'TestReplicator'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'with'
name|'_mock_process'
op|'('
op|'-'
number|'1'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'fake_device'
op|'='
op|'{'
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
string|"'device'"
op|':'
string|"'sda1'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'False'
op|','
nl|'\n'
name|'replicator'
op|'.'
name|'_rsync_file'
op|'('
string|"'/some/file'"
op|','
string|"'remote:/some/file'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'with'
name|'_mock_process'
op|'('
number|'0'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'fake_device'
op|'='
op|'{'
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
string|"'device'"
op|':'
string|"'sda1'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'True'
op|','
nl|'\n'
name|'replicator'
op|'.'
name|'_rsync_file'
op|'('
string|"'/some/file'"
op|','
string|"'remote:/some/file'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_rsync_db
dedent|''
dedent|''
name|'def'
name|'test_rsync_db'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'replicator'
op|'='
name|'TestReplicator'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'replicator'
op|'.'
name|'_rsync_file'
op|'='
name|'lambda'
op|'*'
name|'args'
op|':'
name|'True'
newline|'\n'
name|'fake_device'
op|'='
op|'{'
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
string|"'device'"
op|':'
string|"'sda1'"
op|'}'
newline|'\n'
name|'replicator'
op|'.'
name|'_rsync_db'
op|'('
name|'FakeBroker'
op|'('
op|')'
op|','
name|'fake_device'
op|','
name|'PostReplHttp'
op|'('
op|')'
op|','
string|"'abcd'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_in_sync
dedent|''
name|'def'
name|'test_in_sync'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'replicator'
op|'='
name|'TestReplicator'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'replicator'
op|'.'
name|'_in_sync'
op|'('
nl|'\n'
op|'{'
string|"'id'"
op|':'
string|"'a'"
op|','
string|"'point'"
op|':'
op|'-'
number|'1'
op|','
string|"'max_row'"
op|':'
number|'0'
op|','
string|"'hash'"
op|':'
string|"'b'"
op|'}'
op|','
nl|'\n'
op|'{'
string|"'id'"
op|':'
string|"'a'"
op|','
string|"'point'"
op|':'
op|'-'
number|'1'
op|','
string|"'max_row'"
op|':'
number|'0'
op|','
string|"'hash'"
op|':'
string|"'b'"
op|'}'
op|','
nl|'\n'
name|'FakeBroker'
op|'('
op|')'
op|','
op|'-'
number|'1'
op|')'
op|','
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'replicator'
op|'.'
name|'_in_sync'
op|'('
nl|'\n'
op|'{'
string|"'id'"
op|':'
string|"'a'"
op|','
string|"'point'"
op|':'
op|'-'
number|'1'
op|','
string|"'max_row'"
op|':'
number|'0'
op|','
string|"'hash'"
op|':'
string|"'b'"
op|'}'
op|','
nl|'\n'
op|'{'
string|"'id'"
op|':'
string|"'a'"
op|','
string|"'point'"
op|':'
op|'-'
number|'1'
op|','
string|"'max_row'"
op|':'
number|'10'
op|','
string|"'hash'"
op|':'
string|"'b'"
op|'}'
op|','
nl|'\n'
name|'FakeBroker'
op|'('
op|')'
op|','
op|'-'
number|'1'
op|')'
op|','
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'bool'
op|'('
name|'replicator'
op|'.'
name|'_in_sync'
op|'('
nl|'\n'
op|'{'
string|"'id'"
op|':'
string|"'a'"
op|','
string|"'point'"
op|':'
op|'-'
number|'1'
op|','
string|"'max_row'"
op|':'
number|'0'
op|','
string|"'hash'"
op|':'
string|"'c'"
op|'}'
op|','
nl|'\n'
op|'{'
string|"'id'"
op|':'
string|"'a'"
op|','
string|"'point'"
op|':'
op|'-'
number|'1'
op|','
string|"'max_row'"
op|':'
number|'10'
op|','
string|"'hash'"
op|':'
string|"'d'"
op|'}'
op|','
nl|'\n'
name|'FakeBroker'
op|'('
op|')'
op|','
op|'-'
number|'1'
op|')'
op|')'
op|','
name|'False'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_replicate_once
dedent|''
name|'def'
name|'test_replicate_once'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'replicator'
op|'='
name|'TestReplicator'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'replicator'
op|'.'
name|'replicate_once'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_usync
dedent|''
name|'def'
name|'test_usync'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'fake_http'
op|'='
name|'PostReplHttp'
op|'('
op|')'
newline|'\n'
name|'replicator'
op|'='
name|'TestReplicator'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'replicator'
op|'.'
name|'_usync_db'
op|'('
number|'0'
op|','
name|'FakeBroker'
op|'('
op|')'
op|','
name|'fake_http'
op|','
string|"'12345'"
op|','
string|"'67890'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_repl_to_node
dedent|''
name|'def'
name|'test_repl_to_node'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'replicator'
op|'='
name|'TestReplicator'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'fake_node'
op|'='
op|'{'
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
string|"'device'"
op|':'
string|"'sda1'"
op|','
string|"'port'"
op|':'
number|'1000'
op|'}'
newline|'\n'
name|'fake_info'
op|'='
op|'{'
string|"'id'"
op|':'
string|"'a'"
op|','
string|"'point'"
op|':'
op|'-'
number|'1'
op|','
string|"'max_row'"
op|':'
number|'0'
op|','
string|"'hash'"
op|':'
string|"'b'"
op|','
nl|'\n'
string|"'created_at'"
op|':'
number|'100'
op|','
string|"'put_timestamp'"
op|':'
number|'0'
op|','
nl|'\n'
string|"'delete_timestamp'"
op|':'
number|'0'
op|'}'
newline|'\n'
name|'replicator'
op|'.'
name|'_http_connect'
op|'='
name|'lambda'
op|'*'
name|'args'
op|':'
name|'PostReplHttp'
op|'('
string|'\'{"id": 3, "point": -1}\''
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'replicator'
op|'.'
name|'_repl_to_node'
op|'('
nl|'\n'
name|'fake_node'
op|','
name|'FakeBroker'
op|'('
op|')'
op|','
string|"'0'"
op|','
name|'fake_info'
op|')'
op|','
name|'True'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_stats
dedent|''
name|'def'
name|'test_stats'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|"# I'm not sure how to test that this logs the right thing,"
nl|'\n'
comment|'# but we can at least make sure it gets covered.'
nl|'\n'
indent|'        '
name|'replicator'
op|'='
name|'TestReplicator'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'replicator'
op|'.'
name|'_zero_stats'
op|'('
op|')'
newline|'\n'
name|'replicator'
op|'.'
name|'_report_stats'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_replicate_object
dedent|''
name|'def'
name|'test_replicate_object'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'db_replicator'
op|'.'
name|'lock_parent_directory'
op|'='
name|'lock_parent_directory'
newline|'\n'
name|'replicator'
op|'='
name|'TestReplicator'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'replicator'
op|'.'
name|'_replicate_object'
op|'('
string|"'0'"
op|','
string|"'file'"
op|','
string|"'node_id'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
comment|'#    def test_dispatch(self):'
nl|'\n'
comment|"#        rpc = db_replicator.ReplicatorRpc('/', '/', FakeBroker, False)"
nl|'\n'
comment|'#        no_op = lambda *args, **kwargs: True'
nl|'\n'
comment|"#        self.assertEquals(rpc.dispatch(('drv', 'part', 'hash'), ('op',)"
nl|'\n'
comment|'#                ).status_int, 400)'
nl|'\n'
comment|'#        rpc.mount_check = True'
nl|'\n'
comment|"#        self.assertEquals(rpc.dispatch(('drv', 'part', 'hash'), ['op',]"
nl|'\n'
comment|'#                ).status_int, 507)'
nl|'\n'
comment|'#        rpc.mount_check = False'
nl|'\n'
comment|"#        rpc.rsync_then_merge = lambda drive, db_file, args: self.assertEquals(args, ['test1'])"
nl|'\n'
comment|"#        rpc.complete_rsync = lambda drive, db_file, args: self.assertEquals(args, ['test2'])"
nl|'\n'
comment|"#        rpc.dispatch(('drv', 'part', 'hash'), ['rsync_then_merge','test1'])"
nl|'\n'
comment|"#        rpc.dispatch(('drv', 'part', 'hash'), ['complete_rsync','test2'])"
nl|'\n'
comment|"#        rpc.dispatch(('drv', 'part', 'hash'), ['other_op',])"
nl|'\n'
nl|'\n'
DECL|member|test_rsync_then_merge
dedent|''
name|'def'
name|'test_rsync_then_merge'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'rpc'
op|'='
name|'db_replicator'
op|'.'
name|'ReplicatorRpc'
op|'('
string|"'/'"
op|','
string|"'/'"
op|','
name|'FakeBroker'
op|','
name|'False'
op|')'
newline|'\n'
name|'rpc'
op|'.'
name|'rsync_then_merge'
op|'('
string|"'sda1'"
op|','
string|"'/srv/swift/blah'"
op|','
op|'('
string|"'a'"
op|','
string|"'b'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_merge_items
dedent|''
name|'def'
name|'test_merge_items'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'rpc'
op|'='
name|'db_replicator'
op|'.'
name|'ReplicatorRpc'
op|'('
string|"'/'"
op|','
string|"'/'"
op|','
name|'FakeBroker'
op|','
name|'False'
op|')'
newline|'\n'
name|'fake_broker'
op|'='
name|'FakeBroker'
op|'('
op|')'
newline|'\n'
name|'args'
op|'='
op|'('
string|"'a'"
op|','
string|"'b'"
op|')'
newline|'\n'
name|'rpc'
op|'.'
name|'merge_items'
op|'('
name|'fake_broker'
op|','
name|'args'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'fake_broker'
op|'.'
name|'args'
op|','
name|'args'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_merge_syncs
dedent|''
name|'def'
name|'test_merge_syncs'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'rpc'
op|'='
name|'db_replicator'
op|'.'
name|'ReplicatorRpc'
op|'('
string|"'/'"
op|','
string|"'/'"
op|','
name|'FakeBroker'
op|','
name|'False'
op|')'
newline|'\n'
name|'fake_broker'
op|'='
name|'FakeBroker'
op|'('
op|')'
newline|'\n'
name|'args'
op|'='
op|'('
string|"'a'"
op|','
string|"'b'"
op|')'
newline|'\n'
name|'rpc'
op|'.'
name|'merge_syncs'
op|'('
name|'fake_broker'
op|','
name|'args'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'fake_broker'
op|'.'
name|'args'
op|','
op|'('
name|'args'
op|'['
number|'0'
op|']'
op|','
op|')'
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
name|'unittest'
op|'.'
name|'main'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
endmarker|''
end_unit
