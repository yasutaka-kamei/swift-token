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
name|'hashlib'
name|'import'
name|'md5'
newline|'\n'
name|'import'
name|'itertools'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'import'
name|'uuid'
newline|'\n'
name|'import'
name|'random'
newline|'\n'
name|'import'
name|'shutil'
newline|'\n'
name|'from'
name|'collections'
name|'import'
name|'defaultdict'
newline|'\n'
nl|'\n'
name|'from'
name|'test'
op|'.'
name|'probe'
op|'.'
name|'common'
name|'import'
name|'ECProbeTest'
op|','
name|'Body'
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
name|'storage_policy'
name|'import'
name|'EC_POLICY'
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
name|'obj'
name|'import'
name|'reconstructor'
newline|'\n'
nl|'\n'
name|'from'
name|'swiftclient'
name|'import'
name|'client'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestReconstructorRevert
name|'class'
name|'TestReconstructorRevert'
op|'('
name|'ECProbeTest'
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
name|'super'
op|'('
name|'TestReconstructorRevert'
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
nl|'\n'
comment|'# sanity'
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'self'
op|'.'
name|'policy'
op|'.'
name|'policy_type'
op|','
name|'EC_POLICY'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'reconstructor'
op|'='
name|'Manager'
op|'('
op|'['
string|'"object-reconstructor"'
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|proxy_get
dedent|''
name|'def'
name|'proxy_get'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# GET object'
nl|'\n'
indent|'        '
name|'headers'
op|','
name|'body'
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
nl|'\n'
name|'resp_chunk_size'
op|'='
number|'64'
op|'*'
number|'2'
op|'**'
number|'10'
op|')'
newline|'\n'
name|'resp_checksum'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'for'
name|'chunk'
name|'in'
name|'body'
op|':'
newline|'\n'
indent|'            '
name|'resp_checksum'
op|'.'
name|'update'
op|'('
name|'chunk'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'resp_checksum'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|direct_get
dedent|''
name|'def'
name|'direct_get'
op|'('
name|'self'
op|','
name|'node'
op|','
name|'part'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req_headers'
op|'='
op|'{'
string|"'X-Backend-Storage-Policy-Index'"
op|':'
name|'int'
op|'('
name|'self'
op|'.'
name|'policy'
op|')'
op|'}'
newline|'\n'
name|'headers'
op|','
name|'data'
op|'='
name|'direct_client'
op|'.'
name|'direct_get_object'
op|'('
nl|'\n'
name|'node'
op|','
name|'part'
op|','
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
op|'='
name|'req_headers'
op|','
nl|'\n'
name|'resp_chunk_size'
op|'='
number|'64'
op|'*'
number|'2'
op|'**'
number|'20'
op|')'
newline|'\n'
name|'hasher'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'for'
name|'chunk'
name|'in'
name|'data'
op|':'
newline|'\n'
indent|'            '
name|'hasher'
op|'.'
name|'update'
op|'('
name|'chunk'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'hasher'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_revert_object
dedent|''
name|'def'
name|'test_revert_object'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# create EC container'
nl|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
string|"'X-Storage-Policy'"
op|':'
name|'self'
op|'.'
name|'policy'
op|'.'
name|'name'
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
name|'self'
op|'.'
name|'container_name'
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
newline|'\n'
nl|'\n'
comment|'# get our node lists'
nl|'\n'
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
name|'self'
op|'.'
name|'container_name'
op|','
name|'self'
op|'.'
name|'object_name'
op|')'
newline|'\n'
name|'hnodes'
op|'='
name|'self'
op|'.'
name|'object_ring'
op|'.'
name|'get_more_nodes'
op|'('
name|'opart'
op|')'
newline|'\n'
nl|'\n'
comment|'# kill 2 a parity count number of primary nodes so we can'
nl|'\n'
comment|'# force data onto handoffs, we do that by renaming dev dirs'
nl|'\n'
comment|'# to induce 507'
nl|'\n'
name|'p_dev1'
op|'='
name|'self'
op|'.'
name|'device_dir'
op|'('
string|"'object'"
op|','
name|'onodes'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'p_dev2'
op|'='
name|'self'
op|'.'
name|'device_dir'
op|'('
string|"'object'"
op|','
name|'onodes'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'kill_drive'
op|'('
name|'p_dev1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'kill_drive'
op|'('
name|'p_dev2'
op|')'
newline|'\n'
nl|'\n'
comment|'# PUT object'
nl|'\n'
name|'contents'
op|'='
name|'Body'
op|'('
op|')'
newline|'\n'
name|'headers'
op|'='
op|'{'
string|"'x-object-meta-foo'"
op|':'
string|"'meta-foo'"
op|'}'
newline|'\n'
name|'headers_post'
op|'='
op|'{'
string|"'x-object-meta-bar'"
op|':'
string|"'meta-bar'"
op|'}'
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
name|'self'
op|'.'
name|'container_name'
op|','
nl|'\n'
name|'self'
op|'.'
name|'object_name'
op|','
name|'contents'
op|'='
name|'contents'
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
newline|'\n'
name|'client'
op|'.'
name|'post_object'
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
name|'headers'
op|'='
name|'headers_post'
op|')'
newline|'\n'
name|'del'
name|'headers_post'
op|'['
string|"'X-Auth-Token'"
op|']'
comment|'# WTF, where did this come from?'
newline|'\n'
nl|'\n'
comment|"# these primaries can't serve the data any more, we expect 507"
nl|'\n'
comment|"# here and not 404 because we're using mount_check to kill nodes"
nl|'\n'
name|'for'
name|'onode'
name|'in'
op|'('
name|'onodes'
op|'['
number|'0'
op|']'
op|','
name|'onodes'
op|'['
number|'1'
op|']'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'direct_get'
op|'('
name|'onode'
op|','
name|'opart'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'direct_client'
op|'.'
name|'DirectClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'err'
op|'.'
name|'http_status'
op|','
number|'507'
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
string|"'Node data on %r was not fully destroyed!'"
op|'%'
nl|'\n'
op|'('
name|'onode'
op|','
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# now take out another primary'
nl|'\n'
dedent|''
dedent|''
name|'p_dev3'
op|'='
name|'self'
op|'.'
name|'device_dir'
op|'('
string|"'object'"
op|','
name|'onodes'
op|'['
number|'2'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'kill_drive'
op|'('
name|'p_dev3'
op|')'
newline|'\n'
nl|'\n'
comment|"# this node can't servce the data any more"
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'direct_get'
op|'('
name|'onodes'
op|'['
number|'2'
op|']'
op|','
name|'opart'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'direct_client'
op|'.'
name|'DirectClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'err'
op|'.'
name|'http_status'
op|','
number|'507'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'fail'
op|'('
string|"'Node data on %r was not fully destroyed!'"
op|'%'
nl|'\n'
op|'('
name|'onode'
op|','
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# make sure we can still GET the object and its correct'
nl|'\n'
comment|"# we're now pulling from handoffs and reconstructing"
nl|'\n'
dedent|''
name|'etag'
op|'='
name|'self'
op|'.'
name|'proxy_get'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'etag'
op|','
name|'contents'
op|'.'
name|'etag'
op|')'
newline|'\n'
nl|'\n'
comment|"# rename the dev dirs so they don't 507 anymore"
nl|'\n'
name|'self'
op|'.'
name|'revive_drive'
op|'('
name|'p_dev1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'revive_drive'
op|'('
name|'p_dev2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'revive_drive'
op|'('
name|'p_dev3'
op|')'
newline|'\n'
nl|'\n'
comment|'# fire up reconstructor on handoff nodes only'
nl|'\n'
name|'for'
name|'hnode'
name|'in'
name|'hnodes'
op|':'
newline|'\n'
indent|'            '
name|'hnode_id'
op|'='
op|'('
name|'hnode'
op|'['
string|"'port'"
op|']'
op|'-'
number|'6200'
op|')'
op|'/'
number|'10'
newline|'\n'
name|'self'
op|'.'
name|'reconstructor'
op|'.'
name|'once'
op|'('
name|'number'
op|'='
name|'hnode_id'
op|')'
newline|'\n'
nl|'\n'
comment|'# first three primaries have data again'
nl|'\n'
dedent|''
name|'for'
name|'onode'
name|'in'
op|'('
name|'onodes'
op|'['
number|'0'
op|']'
op|','
name|'onodes'
op|'['
number|'2'
op|']'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'direct_get'
op|'('
name|'onode'
op|','
name|'opart'
op|')'
newline|'\n'
nl|'\n'
comment|'# check meta'
nl|'\n'
dedent|''
name|'meta'
op|'='
name|'client'
op|'.'
name|'head_object'
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
name|'for'
name|'key'
name|'in'
name|'headers_post'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'key'
name|'in'
name|'meta'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'meta'
op|'['
name|'key'
op|']'
op|','
name|'headers_post'
op|'['
name|'key'
op|']'
op|')'
newline|'\n'
nl|'\n'
comment|'# handoffs are empty'
nl|'\n'
dedent|''
name|'for'
name|'hnode'
name|'in'
name|'hnodes'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'direct_get'
op|'('
name|'hnode'
op|','
name|'opart'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'direct_client'
op|'.'
name|'DirectClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'assertEqual'
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
string|"'Node data on %r was not fully destroyed!'"
op|'%'
nl|'\n'
op|'('
name|'hnode'
op|','
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_delete_propagate
dedent|''
dedent|''
dedent|''
name|'def'
name|'test_delete_propagate'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# create EC container'
nl|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
string|"'X-Storage-Policy'"
op|':'
name|'self'
op|'.'
name|'policy'
op|'.'
name|'name'
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
name|'self'
op|'.'
name|'container_name'
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
newline|'\n'
nl|'\n'
comment|'# get our node lists'
nl|'\n'
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
name|'self'
op|'.'
name|'container_name'
op|','
name|'self'
op|'.'
name|'object_name'
op|')'
newline|'\n'
name|'hnodes'
op|'='
name|'list'
op|'('
name|'itertools'
op|'.'
name|'islice'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'object_ring'
op|'.'
name|'get_more_nodes'
op|'('
name|'opart'
op|')'
op|','
number|'2'
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# PUT object'
nl|'\n'
name|'contents'
op|'='
name|'Body'
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
name|'self'
op|'.'
name|'container_name'
op|','
nl|'\n'
name|'self'
op|'.'
name|'object_name'
op|','
name|'contents'
op|'='
name|'contents'
op|')'
newline|'\n'
nl|'\n'
comment|'# now lets shut down a couple primaries'
nl|'\n'
name|'failed_nodes'
op|'='
name|'random'
op|'.'
name|'sample'
op|'('
name|'onodes'
op|','
number|'2'
op|')'
newline|'\n'
name|'for'
name|'node'
name|'in'
name|'failed_nodes'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'kill_drive'
op|'('
name|'self'
op|'.'
name|'device_dir'
op|'('
string|"'object'"
op|','
name|'node'
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# Write tombstones over the nodes that are still online'
nl|'\n'
dedent|''
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
comment|'# spot check the primary nodes that are still online'
nl|'\n'
name|'delete_timestamp'
op|'='
name|'None'
newline|'\n'
name|'for'
name|'node'
name|'in'
name|'onodes'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'node'
name|'in'
name|'failed_nodes'
op|':'
newline|'\n'
indent|'                '
name|'continue'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'direct_get'
op|'('
name|'node'
op|','
name|'opart'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'direct_client'
op|'.'
name|'DirectClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'err'
op|'.'
name|'http_status'
op|','
number|'404'
op|')'
newline|'\n'
name|'delete_timestamp'
op|'='
name|'err'
op|'.'
name|'http_headers'
op|'['
string|"'X-Backend-Timestamp'"
op|']'
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
string|"'Node data on %r was not fully destroyed!'"
op|'%'
nl|'\n'
op|'('
name|'node'
op|','
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# repair the first primary'
nl|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'revive_drive'
op|'('
name|'self'
op|'.'
name|'device_dir'
op|'('
string|"'object'"
op|','
name|'failed_nodes'
op|'['
number|'0'
op|']'
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# run the reconstructor on the *second* handoff node'
nl|'\n'
name|'self'
op|'.'
name|'reconstructor'
op|'.'
name|'once'
op|'('
name|'number'
op|'='
name|'self'
op|'.'
name|'config_number'
op|'('
name|'hnodes'
op|'['
number|'1'
op|']'
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|"# make sure it's tombstone was pushed out"
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'direct_get'
op|'('
name|'hnodes'
op|'['
number|'1'
op|']'
op|','
name|'opart'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'direct_client'
op|'.'
name|'DirectClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'err'
op|'.'
name|'http_status'
op|','
number|'404'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertNotIn'
op|'('
string|"'X-Backend-Timestamp'"
op|','
name|'err'
op|'.'
name|'http_headers'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'fail'
op|'('
string|"'Found obj data on %r'"
op|'%'
name|'hnodes'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
nl|'\n'
comment|"# ... and it's on the first failed (now repaired) primary"
nl|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'direct_get'
op|'('
name|'failed_nodes'
op|'['
number|'0'
op|']'
op|','
name|'opart'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'direct_client'
op|'.'
name|'DirectClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'err'
op|'.'
name|'http_status'
op|','
number|'404'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'err'
op|'.'
name|'http_headers'
op|'['
string|"'X-Backend-Timestamp'"
op|']'
op|','
nl|'\n'
name|'delete_timestamp'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'fail'
op|'('
string|"'Found obj data on %r'"
op|'%'
name|'failed_nodes'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
nl|'\n'
comment|'# repair the second primary'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'revive_drive'
op|'('
name|'self'
op|'.'
name|'device_dir'
op|'('
string|"'object'"
op|','
name|'failed_nodes'
op|'['
number|'1'
op|']'
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# run the reconstructor on the *first* handoff node'
nl|'\n'
name|'self'
op|'.'
name|'reconstructor'
op|'.'
name|'once'
op|'('
name|'number'
op|'='
name|'self'
op|'.'
name|'config_number'
op|'('
name|'hnodes'
op|'['
number|'0'
op|']'
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|"# make sure it's tombstone was pushed out"
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'direct_get'
op|'('
name|'hnodes'
op|'['
number|'0'
op|']'
op|','
name|'opart'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'direct_client'
op|'.'
name|'DirectClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'err'
op|'.'
name|'http_status'
op|','
number|'404'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertNotIn'
op|'('
string|"'X-Backend-Timestamp'"
op|','
name|'err'
op|'.'
name|'http_headers'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'fail'
op|'('
string|"'Found obj data on %r'"
op|'%'
name|'hnodes'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
nl|'\n'
comment|"# ... and now it's on the second failed primary too!"
nl|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'direct_get'
op|'('
name|'failed_nodes'
op|'['
number|'1'
op|']'
op|','
name|'opart'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'direct_client'
op|'.'
name|'DirectClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'err'
op|'.'
name|'http_status'
op|','
number|'404'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'err'
op|'.'
name|'http_headers'
op|'['
string|"'X-Backend-Timestamp'"
op|']'
op|','
nl|'\n'
name|'delete_timestamp'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'fail'
op|'('
string|"'Found obj data on %r'"
op|'%'
name|'failed_nodes'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
nl|'\n'
comment|"# sanity make sure proxy get can't find it"
nl|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'proxy_get'
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
name|'self'
op|'.'
name|'assertEqual'
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
indent|'            '
name|'self'
op|'.'
name|'fail'
op|'('
string|"'Node data on %r was not fully destroyed!'"
op|'%'
nl|'\n'
op|'('
name|'onodes'
op|'['
number|'0'
op|']'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_reconstruct_from_reverted_fragment_archive
dedent|''
dedent|''
name|'def'
name|'test_reconstruct_from_reverted_fragment_archive'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
string|"'X-Storage-Policy'"
op|':'
name|'self'
op|'.'
name|'policy'
op|'.'
name|'name'
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
name|'self'
op|'.'
name|'container_name'
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
newline|'\n'
nl|'\n'
comment|'# get our node lists'
nl|'\n'
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
name|'self'
op|'.'
name|'container_name'
op|','
name|'self'
op|'.'
name|'object_name'
op|')'
newline|'\n'
nl|'\n'
comment|"# find a primary server that only has one of it's devices in the"
nl|'\n'
comment|'# primary node list'
nl|'\n'
name|'group_nodes_by_config'
op|'='
name|'defaultdict'
op|'('
name|'list'
op|')'
newline|'\n'
name|'for'
name|'n'
name|'in'
name|'onodes'
op|':'
newline|'\n'
indent|'            '
name|'group_nodes_by_config'
op|'['
name|'self'
op|'.'
name|'config_number'
op|'('
name|'n'
op|')'
op|']'
op|'.'
name|'append'
op|'('
name|'n'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'config_number'
op|','
name|'node_list'
name|'in'
name|'group_nodes_by_config'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'len'
op|'('
name|'node_list'
op|')'
op|'=='
number|'1'
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
name|'self'
op|'.'
name|'fail'
op|'('
string|"'ring balancing did not use all available nodes'"
op|')'
newline|'\n'
dedent|''
name|'primary_node'
op|'='
name|'node_list'
op|'['
number|'0'
op|']'
newline|'\n'
nl|'\n'
comment|"# ... and 507 it's device"
nl|'\n'
name|'primary_device'
op|'='
name|'self'
op|'.'
name|'device_dir'
op|'('
string|"'object'"
op|','
name|'primary_node'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'kill_drive'
op|'('
name|'primary_device'
op|')'
newline|'\n'
nl|'\n'
comment|'# PUT object'
nl|'\n'
name|'contents'
op|'='
name|'Body'
op|'('
op|')'
newline|'\n'
name|'etag'
op|'='
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
name|'self'
op|'.'
name|'container_name'
op|','
nl|'\n'
name|'self'
op|'.'
name|'object_name'
op|','
name|'contents'
op|'='
name|'contents'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'contents'
op|'.'
name|'etag'
op|','
name|'etag'
op|')'
newline|'\n'
nl|'\n'
comment|'# fix the primary device and sanity GET'
nl|'\n'
name|'self'
op|'.'
name|'revive_drive'
op|'('
name|'primary_device'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'etag'
op|','
name|'self'
op|'.'
name|'proxy_get'
op|'('
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# find a handoff holding the fragment'
nl|'\n'
name|'for'
name|'hnode'
name|'in'
name|'self'
op|'.'
name|'object_ring'
op|'.'
name|'get_more_nodes'
op|'('
name|'opart'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'reverted_fragment_etag'
op|'='
name|'self'
op|'.'
name|'direct_get'
op|'('
name|'hnode'
op|','
name|'opart'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'direct_client'
op|'.'
name|'DirectClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'err'
op|'.'
name|'http_status'
op|'!='
number|'404'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
newline|'\n'
dedent|''
dedent|''
name|'else'
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
name|'self'
op|'.'
name|'fail'
op|'('
string|"'Unable to find handoff fragment!'"
op|')'
newline|'\n'
nl|'\n'
comment|"# we'll force the handoff device to revert instead of potentially"
nl|'\n'
comment|'# racing with rebuild by deleting any other fragments that may be on'
nl|'\n'
comment|'# the same server'
nl|'\n'
dedent|''
name|'handoff_fragment_etag'
op|'='
name|'None'
newline|'\n'
name|'for'
name|'node'
name|'in'
name|'onodes'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'self'
op|'.'
name|'is_local_to'
op|'('
name|'node'
op|','
name|'hnode'
op|')'
op|':'
newline|'\n'
comment|"# we'll keep track of the etag of this fragment we're removing"
nl|'\n'
comment|'# in case we need it later (queue forshadowing music)...'
nl|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'handoff_fragment_etag'
op|'='
name|'self'
op|'.'
name|'direct_get'
op|'('
name|'node'
op|','
name|'opart'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'direct_client'
op|'.'
name|'DirectClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'err'
op|'.'
name|'http_status'
op|'!='
number|'404'
op|':'
newline|'\n'
indent|'                        '
name|'raise'
newline|'\n'
comment|'# this just means our handoff device was on the same'
nl|'\n'
comment|'# machine as the primary!'
nl|'\n'
dedent|''
name|'continue'
newline|'\n'
comment|'# use the primary nodes device - not the hnode device'
nl|'\n'
dedent|''
name|'part_dir'
op|'='
name|'self'
op|'.'
name|'storage_dir'
op|'('
string|"'object'"
op|','
name|'node'
op|','
name|'part'
op|'='
name|'opart'
op|')'
newline|'\n'
name|'shutil'
op|'.'
name|'rmtree'
op|'('
name|'part_dir'
op|','
name|'True'
op|')'
newline|'\n'
nl|'\n'
comment|'# revert from handoff device with reconstructor'
nl|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'reconstructor'
op|'.'
name|'once'
op|'('
name|'number'
op|'='
name|'self'
op|'.'
name|'config_number'
op|'('
name|'hnode'
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# verify fragment reverted to primary server'
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'reverted_fragment_etag'
op|','
nl|'\n'
name|'self'
op|'.'
name|'direct_get'
op|'('
name|'primary_node'
op|','
name|'opart'
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|"# now we'll remove some data on one of the primary node's partners"
nl|'\n'
name|'partner'
op|'='
name|'random'
op|'.'
name|'choice'
op|'('
name|'reconstructor'
op|'.'
name|'_get_partners'
op|'('
nl|'\n'
name|'primary_node'
op|'['
string|"'index'"
op|']'
op|','
name|'onodes'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'rebuilt_fragment_etag'
op|'='
name|'self'
op|'.'
name|'direct_get'
op|'('
name|'partner'
op|','
name|'opart'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'direct_client'
op|'.'
name|'DirectClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'err'
op|'.'
name|'http_status'
op|'!='
number|'404'
op|':'
newline|'\n'
indent|'                '
name|'raise'
newline|'\n'
comment|"# partner already had it's fragment removed"
nl|'\n'
dedent|''
name|'if'
op|'('
name|'handoff_fragment_etag'
name|'is'
name|'not'
name|'None'
name|'and'
nl|'\n'
name|'self'
op|'.'
name|'is_local_to'
op|'('
name|'hnode'
op|','
name|'partner'
op|')'
op|')'
op|':'
newline|'\n'
comment|'# oh, well that makes sense then...'
nl|'\n'
indent|'                '
name|'rebuilt_fragment_etag'
op|'='
name|'handoff_fragment_etag'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
comment|'# I wonder what happened?'
nl|'\n'
indent|'                '
name|'self'
op|'.'
name|'fail'
op|'('
string|"'Partner inexplicably missing fragment!'"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'part_dir'
op|'='
name|'self'
op|'.'
name|'storage_dir'
op|'('
string|"'object'"
op|','
name|'partner'
op|','
name|'part'
op|'='
name|'opart'
op|')'
newline|'\n'
name|'shutil'
op|'.'
name|'rmtree'
op|'('
name|'part_dir'
op|','
name|'True'
op|')'
newline|'\n'
nl|'\n'
comment|"# sanity, it's gone"
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'direct_get'
op|'('
name|'partner'
op|','
name|'opart'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'direct_client'
op|'.'
name|'DirectClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'err'
op|'.'
name|'http_status'
op|'!='
number|'404'
op|':'
newline|'\n'
indent|'                '
name|'raise'
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
string|"'successful GET of removed partner fragment archive!?'"
op|')'
newline|'\n'
nl|'\n'
comment|'# and force the primary node to do a rebuild'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'reconstructor'
op|'.'
name|'once'
op|'('
name|'number'
op|'='
name|'self'
op|'.'
name|'config_number'
op|'('
name|'primary_node'
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# and validate the partners rebuilt_fragment_etag'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'rebuilt_fragment_etag'
op|','
nl|'\n'
name|'self'
op|'.'
name|'direct_get'
op|'('
name|'partner'
op|','
name|'opart'
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'direct_client'
op|'.'
name|'DirectClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'err'
op|'.'
name|'http_status'
op|'!='
number|'404'
op|':'
newline|'\n'
indent|'                '
name|'raise'
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
string|"'Did not find rebuilt fragment on partner node'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
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
