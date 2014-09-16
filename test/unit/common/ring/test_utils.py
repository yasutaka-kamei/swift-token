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
name|'import'
name|'unittest'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'ring'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'ring'
op|'.'
name|'utils'
name|'import'
op|'('
name|'build_tier_tree'
op|','
name|'tiers_for_dev'
op|','
nl|'\n'
name|'parse_search_value'
op|','
name|'parse_args'
op|','
nl|'\n'
name|'build_dev_from_opts'
op|','
name|'find_parts'
op|','
nl|'\n'
name|'parse_builder_ring_filename_args'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestUtils
name|'class'
name|'TestUtils'
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
name|'test_dev'
op|'='
op|'{'
string|"'region'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'192.168.1.1'"
op|','
nl|'\n'
string|"'port'"
op|':'
string|"'6000'"
op|','
string|"'id'"
op|':'
number|'0'
op|'}'
newline|'\n'
nl|'\n'
DECL|function|get_test_devs
name|'def'
name|'get_test_devs'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'dev0'
op|'='
op|'{'
string|"'region'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'192.168.1.1'"
op|','
nl|'\n'
string|"'port'"
op|':'
string|"'6000'"
op|','
string|"'id'"
op|':'
number|'0'
op|'}'
newline|'\n'
name|'dev1'
op|'='
op|'{'
string|"'region'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'192.168.1.1'"
op|','
nl|'\n'
string|"'port'"
op|':'
string|"'6000'"
op|','
string|"'id'"
op|':'
number|'1'
op|'}'
newline|'\n'
name|'dev2'
op|'='
op|'{'
string|"'region'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'192.168.1.1'"
op|','
nl|'\n'
string|"'port'"
op|':'
string|"'6000'"
op|','
string|"'id'"
op|':'
number|'2'
op|'}'
newline|'\n'
name|'dev3'
op|'='
op|'{'
string|"'region'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'192.168.1.2'"
op|','
nl|'\n'
string|"'port'"
op|':'
string|"'6000'"
op|','
string|"'id'"
op|':'
number|'3'
op|'}'
newline|'\n'
name|'dev4'
op|'='
op|'{'
string|"'region'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'192.168.1.2'"
op|','
nl|'\n'
string|"'port'"
op|':'
string|"'6000'"
op|','
string|"'id'"
op|':'
number|'4'
op|'}'
newline|'\n'
name|'dev5'
op|'='
op|'{'
string|"'region'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'192.168.1.2'"
op|','
nl|'\n'
string|"'port'"
op|':'
string|"'6000'"
op|','
string|"'id'"
op|':'
number|'5'
op|'}'
newline|'\n'
name|'dev6'
op|'='
op|'{'
string|"'region'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'2'
op|','
string|"'ip'"
op|':'
string|"'192.168.2.1'"
op|','
nl|'\n'
string|"'port'"
op|':'
string|"'6000'"
op|','
string|"'id'"
op|':'
number|'6'
op|'}'
newline|'\n'
name|'dev7'
op|'='
op|'{'
string|"'region'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'2'
op|','
string|"'ip'"
op|':'
string|"'192.168.2.1'"
op|','
nl|'\n'
string|"'port'"
op|':'
string|"'6000'"
op|','
string|"'id'"
op|':'
number|'7'
op|'}'
newline|'\n'
name|'dev8'
op|'='
op|'{'
string|"'region'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'2'
op|','
string|"'ip'"
op|':'
string|"'192.168.2.1'"
op|','
nl|'\n'
string|"'port'"
op|':'
string|"'6000'"
op|','
string|"'id'"
op|':'
number|'8'
op|'}'
newline|'\n'
name|'dev9'
op|'='
op|'{'
string|"'region'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'2'
op|','
string|"'ip'"
op|':'
string|"'192.168.2.2'"
op|','
nl|'\n'
string|"'port'"
op|':'
string|"'6000'"
op|','
string|"'id'"
op|':'
number|'9'
op|'}'
newline|'\n'
name|'dev10'
op|'='
op|'{'
string|"'region'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'2'
op|','
string|"'ip'"
op|':'
string|"'192.168.2.2'"
op|','
nl|'\n'
string|"'port'"
op|':'
string|"'6000'"
op|','
string|"'id'"
op|':'
number|'10'
op|'}'
newline|'\n'
name|'dev11'
op|'='
op|'{'
string|"'region'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'2'
op|','
string|"'ip'"
op|':'
string|"'192.168.2.2'"
op|','
nl|'\n'
string|"'port'"
op|':'
string|"'6000'"
op|','
string|"'id'"
op|':'
number|'11'
op|'}'
newline|'\n'
name|'return'
op|'['
name|'dev0'
op|','
name|'dev1'
op|','
name|'dev2'
op|','
name|'dev3'
op|','
name|'dev4'
op|','
name|'dev5'
op|','
nl|'\n'
name|'dev6'
op|','
name|'dev7'
op|','
name|'dev8'
op|','
name|'dev9'
op|','
name|'dev10'
op|','
name|'dev11'
op|']'
newline|'\n'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'test_devs'
op|'='
name|'get_test_devs'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_tiers_for_dev
dedent|''
name|'def'
name|'test_tiers_for_dev'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'assertEqual'
op|'('
nl|'\n'
name|'tiers_for_dev'
op|'('
name|'self'
op|'.'
name|'test_dev'
op|')'
op|','
nl|'\n'
op|'('
op|'('
number|'1'
op|','
op|')'
op|','
nl|'\n'
op|'('
number|'1'
op|','
number|'1'
op|')'
op|','
nl|'\n'
op|'('
number|'1'
op|','
number|'1'
op|','
string|"'192.168.1.1:6000'"
op|')'
op|','
nl|'\n'
op|'('
number|'1'
op|','
number|'1'
op|','
string|"'192.168.1.1:6000'"
op|','
number|'0'
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_build_tier_tree
dedent|''
name|'def'
name|'test_build_tier_tree'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'ret'
op|'='
name|'build_tier_tree'
op|'('
name|'self'
op|'.'
name|'test_devs'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'len'
op|'('
name|'ret'
op|')'
op|','
number|'8'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'ret'
op|'['
op|'('
op|')'
op|']'
op|','
name|'set'
op|'('
op|'['
op|'('
number|'1'
op|','
op|')'
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'ret'
op|'['
op|'('
number|'1'
op|','
op|')'
op|']'
op|','
name|'set'
op|'('
op|'['
op|'('
number|'1'
op|','
number|'1'
op|')'
op|','
op|'('
number|'1'
op|','
number|'2'
op|')'
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'ret'
op|'['
op|'('
number|'1'
op|','
number|'1'
op|')'
op|']'
op|','
nl|'\n'
name|'set'
op|'('
op|'['
op|'('
number|'1'
op|','
number|'1'
op|','
string|"'192.168.1.2:6000'"
op|')'
op|','
nl|'\n'
op|'('
number|'1'
op|','
number|'1'
op|','
string|"'192.168.1.1:6000'"
op|')'
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'ret'
op|'['
op|'('
number|'1'
op|','
number|'2'
op|')'
op|']'
op|','
nl|'\n'
name|'set'
op|'('
op|'['
op|'('
number|'1'
op|','
number|'2'
op|','
string|"'192.168.2.2:6000'"
op|')'
op|','
nl|'\n'
op|'('
number|'1'
op|','
number|'2'
op|','
string|"'192.168.2.1:6000'"
op|')'
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'ret'
op|'['
op|'('
number|'1'
op|','
number|'1'
op|','
string|"'192.168.1.1:6000'"
op|')'
op|']'
op|','
nl|'\n'
name|'set'
op|'('
op|'['
op|'('
number|'1'
op|','
number|'1'
op|','
string|"'192.168.1.1:6000'"
op|','
number|'0'
op|')'
op|','
nl|'\n'
op|'('
number|'1'
op|','
number|'1'
op|','
string|"'192.168.1.1:6000'"
op|','
number|'1'
op|')'
op|','
nl|'\n'
op|'('
number|'1'
op|','
number|'1'
op|','
string|"'192.168.1.1:6000'"
op|','
number|'2'
op|')'
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'ret'
op|'['
op|'('
number|'1'
op|','
number|'1'
op|','
string|"'192.168.1.2:6000'"
op|')'
op|']'
op|','
nl|'\n'
name|'set'
op|'('
op|'['
op|'('
number|'1'
op|','
number|'1'
op|','
string|"'192.168.1.2:6000'"
op|','
number|'3'
op|')'
op|','
nl|'\n'
op|'('
number|'1'
op|','
number|'1'
op|','
string|"'192.168.1.2:6000'"
op|','
number|'4'
op|')'
op|','
nl|'\n'
op|'('
number|'1'
op|','
number|'1'
op|','
string|"'192.168.1.2:6000'"
op|','
number|'5'
op|')'
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'ret'
op|'['
op|'('
number|'1'
op|','
number|'2'
op|','
string|"'192.168.2.1:6000'"
op|')'
op|']'
op|','
nl|'\n'
name|'set'
op|'('
op|'['
op|'('
number|'1'
op|','
number|'2'
op|','
string|"'192.168.2.1:6000'"
op|','
number|'6'
op|')'
op|','
nl|'\n'
op|'('
number|'1'
op|','
number|'2'
op|','
string|"'192.168.2.1:6000'"
op|','
number|'7'
op|')'
op|','
nl|'\n'
op|'('
number|'1'
op|','
number|'2'
op|','
string|"'192.168.2.1:6000'"
op|','
number|'8'
op|')'
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'ret'
op|'['
op|'('
number|'1'
op|','
number|'2'
op|','
string|"'192.168.2.2:6000'"
op|')'
op|']'
op|','
nl|'\n'
name|'set'
op|'('
op|'['
op|'('
number|'1'
op|','
number|'2'
op|','
string|"'192.168.2.2:6000'"
op|','
number|'9'
op|')'
op|','
nl|'\n'
op|'('
number|'1'
op|','
number|'2'
op|','
string|"'192.168.2.2:6000'"
op|','
number|'10'
op|')'
op|','
nl|'\n'
op|'('
number|'1'
op|','
number|'2'
op|','
string|"'192.168.2.2:6000'"
op|','
number|'11'
op|')'
op|']'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_parse_search_value
dedent|''
name|'def'
name|'test_parse_search_value'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'res'
op|'='
name|'parse_search_value'
op|'('
string|"'r0'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'res'
op|','
op|'{'
string|"'region'"
op|':'
number|'0'
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'parse_search_value'
op|'('
string|"'r1'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'res'
op|','
op|'{'
string|"'region'"
op|':'
number|'1'
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'parse_search_value'
op|'('
string|"'r1z2'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'res'
op|','
op|'{'
string|"'region'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'2'
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'parse_search_value'
op|'('
string|"'d1'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'res'
op|','
op|'{'
string|"'id'"
op|':'
number|'1'
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'parse_search_value'
op|'('
string|"'z1'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'res'
op|','
op|'{'
string|"'zone'"
op|':'
number|'1'
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'parse_search_value'
op|'('
string|"'-127.0.0.1'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'res'
op|','
op|'{'
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'parse_search_value'
op|'('
string|"'-[127.0.0.1]:10001'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'res'
op|','
op|'{'
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
string|"'port'"
op|':'
number|'10001'
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'parse_search_value'
op|'('
string|"':10001'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'res'
op|','
op|'{'
string|"'port'"
op|':'
number|'10001'
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'parse_search_value'
op|'('
string|"'R127.0.0.10'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'res'
op|','
op|'{'
string|"'replication_ip'"
op|':'
string|"'127.0.0.10'"
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'parse_search_value'
op|'('
string|"'R[127.0.0.10]:20000'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'res'
op|','
op|'{'
string|"'replication_ip'"
op|':'
string|"'127.0.0.10'"
op|','
nl|'\n'
string|"'replication_port'"
op|':'
number|'20000'
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'parse_search_value'
op|'('
string|"'R:20000'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'res'
op|','
op|'{'
string|"'replication_port'"
op|':'
number|'20000'
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'parse_search_value'
op|'('
string|"'/sdb1'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'res'
op|','
op|'{'
string|"'device'"
op|':'
string|"'sdb1'"
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'parse_search_value'
op|'('
string|"'_meta1'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'res'
op|','
op|'{'
string|"'meta'"
op|':'
string|"'meta1'"
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'parse_search_value'
op|','
string|"'OMGPONIES'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_replication_defaults
dedent|''
name|'def'
name|'test_replication_defaults'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'args'
op|'='
string|"'-r 1 -z 1 -i 127.0.0.1 -p 6010 -d d1 -w 100'"
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'opts'
op|','
name|'_'
op|'='
name|'parse_args'
op|'('
name|'args'
op|')'
newline|'\n'
name|'device'
op|'='
name|'build_dev_from_opts'
op|'('
name|'opts'
op|')'
newline|'\n'
name|'expected'
op|'='
op|'{'
nl|'\n'
string|"'device'"
op|':'
string|"'d1'"
op|','
nl|'\n'
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
string|"'meta'"
op|':'
string|"''"
op|','
nl|'\n'
string|"'port'"
op|':'
number|'6010'
op|','
nl|'\n'
string|"'region'"
op|':'
number|'1'
op|','
nl|'\n'
string|"'replication_ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
string|"'replication_port'"
op|':'
number|'6010'
op|','
nl|'\n'
string|"'weight'"
op|':'
number|'100.0'
op|','
nl|'\n'
string|"'zone'"
op|':'
number|'1'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'device'
op|','
name|'expected'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_parse_builder_ring_filename_args
dedent|''
name|'def'
name|'test_parse_builder_ring_filename_args'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'args'
op|'='
string|"'swift-ring-builder object.builder write_ring'"
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
op|'('
nl|'\n'
string|"'object.builder'"
op|','
string|"'object.ring.gz'"
nl|'\n'
op|')'
op|','
name|'parse_builder_ring_filename_args'
op|'('
name|'args'
op|'.'
name|'split'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
name|'args'
op|'='
string|"'swift-ring-builder container.ring.gz write_builder'"
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
op|'('
nl|'\n'
string|"'container.builder'"
op|','
string|"'container.ring.gz'"
nl|'\n'
op|')'
op|','
name|'parse_builder_ring_filename_args'
op|'('
name|'args'
op|'.'
name|'split'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
comment|'# builder name arg should always fall through'
nl|'\n'
name|'args'
op|'='
string|"'swift-ring-builder test create'"
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
op|'('
nl|'\n'
string|"'test'"
op|','
string|"'test.ring.gz'"
nl|'\n'
op|')'
op|','
name|'parse_builder_ring_filename_args'
op|'('
name|'args'
op|'.'
name|'split'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
name|'args'
op|'='
string|"'swift-ring-builder my.file.name create'"
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
op|'('
nl|'\n'
string|"'my.file.name'"
op|','
string|"'my.file.name.ring.gz'"
nl|'\n'
op|')'
op|','
name|'parse_builder_ring_filename_args'
op|'('
name|'args'
op|'.'
name|'split'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_find_parts
dedent|''
name|'def'
name|'test_find_parts'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'rb'
op|'='
name|'ring'
op|'.'
name|'RingBuilder'
op|'('
number|'8'
op|','
number|'3'
op|','
number|'0'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'add_dev'
op|'('
op|'{'
string|"'id'"
op|':'
number|'0'
op|','
string|"'region'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'0'
op|','
string|"'weight'"
op|':'
number|'100'
op|','
nl|'\n'
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
string|"'port'"
op|':'
number|'10000'
op|','
string|"'device'"
op|':'
string|"'sda1'"
op|'}'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'add_dev'
op|'('
op|'{'
string|"'id'"
op|':'
number|'1'
op|','
string|"'region'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'1'
op|','
string|"'weight'"
op|':'
number|'100'
op|','
nl|'\n'
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
string|"'port'"
op|':'
number|'10001'
op|','
string|"'device'"
op|':'
string|"'sda1'"
op|'}'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'add_dev'
op|'('
op|'{'
string|"'id'"
op|':'
number|'2'
op|','
string|"'region'"
op|':'
number|'1'
op|','
string|"'zone'"
op|':'
number|'2'
op|','
string|"'weight'"
op|':'
number|'100'
op|','
nl|'\n'
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
string|"'port'"
op|':'
number|'10002'
op|','
string|"'device'"
op|':'
string|"'sda1'"
op|'}'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'rebalance'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'rb'
op|'.'
name|'add_dev'
op|'('
op|'{'
string|"'id'"
op|':'
number|'3'
op|','
string|"'region'"
op|':'
number|'2'
op|','
string|"'zone'"
op|':'
number|'1'
op|','
string|"'weight'"
op|':'
number|'10'
op|','
nl|'\n'
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
string|"'port'"
op|':'
number|'10004'
op|','
string|"'device'"
op|':'
string|"'sda1'"
op|'}'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'pretend_min_part_hours_passed'
op|'('
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'rebalance'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'argv'
op|'='
op|'['
string|"'swift-ring-builder'"
op|','
string|"'object.builder'"
op|','
nl|'\n'
string|"'list_parts'"
op|','
string|"'127.0.0.1'"
op|']'
newline|'\n'
name|'sorted_partition_count'
op|'='
name|'find_parts'
op|'('
name|'rb'
op|','
name|'argv'
op|')'
newline|'\n'
nl|'\n'
comment|'# Expect 256 partitions in the output'
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
number|'256'
op|','
name|'len'
op|'('
name|'sorted_partition_count'
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# Each partitions should have 3 replicas'
nl|'\n'
name|'for'
name|'partition'
op|','
name|'count'
name|'in'
name|'sorted_partition_count'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEqual'
op|'('
nl|'\n'
number|'3'
op|','
name|'count'
op|','
string|'"Partition %d has only %d replicas"'
op|'%'
nl|'\n'
op|'('
name|'partition'
op|','
name|'count'
op|')'
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
name|'unittest'
op|'.'
name|'main'
op|'('
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
