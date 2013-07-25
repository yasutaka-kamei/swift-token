begin_unit
comment|'#!/usr/bin/env python'
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
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'proxy'
name|'import'
name|'server'
name|'as'
name|'proxy_server'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
name|'import'
name|'FakeRing'
op|','
name|'FakeMemcache'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestObjControllerWriteAffinity
name|'class'
name|'TestObjControllerWriteAffinity'
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
name|'self'
op|'.'
name|'app'
op|'='
name|'proxy_server'
op|'.'
name|'Application'
op|'('
nl|'\n'
name|'None'
op|','
name|'FakeMemcache'
op|'('
op|')'
op|','
name|'account_ring'
op|'='
name|'FakeRing'
op|'('
op|')'
op|','
nl|'\n'
name|'container_ring'
op|'='
name|'FakeRing'
op|'('
op|')'
op|','
name|'object_ring'
op|'='
name|'FakeRing'
op|'('
name|'max_more_nodes'
op|'='
number|'9'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'request_node_count'
op|'='
name|'lambda'
name|'ring'
op|':'
number|'10000000'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'sort_nodes'
op|'='
name|'lambda'
name|'l'
op|':'
name|'l'
comment|'# stop shuffling the primary nodes'
newline|'\n'
nl|'\n'
DECL|member|test_iter_nodes_local_first_noops_when_no_affinity
dedent|''
name|'def'
name|'test_iter_nodes_local_first_noops_when_no_affinity'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'controller'
op|'='
name|'proxy_server'
op|'.'
name|'ObjectController'
op|'('
name|'self'
op|'.'
name|'app'
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'write_affinity_is_local_fn'
op|'='
name|'None'
newline|'\n'
nl|'\n'
name|'all_nodes'
op|'='
name|'self'
op|'.'
name|'app'
op|'.'
name|'object_ring'
op|'.'
name|'get_part_nodes'
op|'('
number|'1'
op|')'
newline|'\n'
name|'all_nodes'
op|'.'
name|'extend'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'object_ring'
op|'.'
name|'get_more_nodes'
op|'('
number|'1'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'local_first_nodes'
op|'='
name|'list'
op|'('
name|'controller'
op|'.'
name|'iter_nodes_local_first'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'object_ring'
op|','
number|'1'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'maxDiff'
op|'='
name|'None'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'all_nodes'
op|','
name|'local_first_nodes'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_iter_nodes_local_first_moves_locals_first
dedent|''
name|'def'
name|'test_iter_nodes_local_first_moves_locals_first'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'controller'
op|'='
name|'proxy_server'
op|'.'
name|'ObjectController'
op|'('
name|'self'
op|'.'
name|'app'
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'write_affinity_is_local_fn'
op|'='
op|'('
name|'lambda'
name|'node'
op|':'
name|'node'
op|'['
string|"'region'"
op|']'
op|'=='
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'write_affinity_node_count'
op|'='
name|'lambda'
name|'ring'
op|':'
number|'4'
newline|'\n'
nl|'\n'
name|'all_nodes'
op|'='
name|'self'
op|'.'
name|'app'
op|'.'
name|'object_ring'
op|'.'
name|'get_part_nodes'
op|'('
number|'1'
op|')'
newline|'\n'
name|'all_nodes'
op|'.'
name|'extend'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'object_ring'
op|'.'
name|'get_more_nodes'
op|'('
number|'1'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'local_first_nodes'
op|'='
name|'list'
op|'('
name|'controller'
op|'.'
name|'iter_nodes_local_first'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'object_ring'
op|','
number|'1'
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# the local nodes move up in the ordering'
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
op|'['
number|'1'
op|','
number|'1'
op|','
number|'1'
op|','
number|'1'
op|']'
op|','
nl|'\n'
op|'['
name|'node'
op|'['
string|"'region'"
op|']'
name|'for'
name|'node'
name|'in'
name|'local_first_nodes'
op|'['
op|':'
number|'4'
op|']'
op|']'
op|')'
newline|'\n'
comment|"# we don't skip any nodes"
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'sorted'
op|'('
name|'all_nodes'
op|')'
op|','
name|'sorted'
op|'('
name|'local_first_nodes'
op|')'
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
