begin_unit
comment|'# Copyright (c) 2010-2011 OpenStack, LLC.'
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
name|'unittest'
newline|'\n'
name|'from'
name|'shutil'
name|'import'
name|'rmtree'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'ring'
name|'import'
name|'RingBuilder'
op|','
name|'RingData'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'ring'
newline|'\n'
nl|'\n'
DECL|class|TestRingBuilder
name|'class'
name|'TestRingBuilder'
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
name|'testdir'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'dirname'
op|'('
name|'__file__'
op|')'
op|','
nl|'\n'
string|"'ring_builder'"
op|')'
newline|'\n'
name|'rmtree'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
name|'ignore_errors'
op|'='
number|'1'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'mkdir'
op|'('
name|'self'
op|'.'
name|'testdir'
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
name|'rmtree'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
name|'ignore_errors'
op|'='
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_init
dedent|''
name|'def'
name|'test_init'
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
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'rb'
op|'.'
name|'part_power'
op|','
number|'8'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'rb'
op|'.'
name|'replicas'
op|','
number|'3'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'rb'
op|'.'
name|'min_part_hours'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'rb'
op|'.'
name|'parts'
op|','
number|'2'
op|'**'
number|'8'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'rb'
op|'.'
name|'devs'
op|','
op|'['
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'rb'
op|'.'
name|'devs_changed'
op|','
name|'False'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'rb'
op|'.'
name|'version'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_ring
dedent|''
name|'def'
name|'test_get_ring'
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
number|'1'
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
string|"'zone'"
op|':'
number|'0'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
string|"'zone'"
op|':'
number|'1'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
string|"'zone'"
op|':'
number|'2'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
name|'add_dev'
op|'('
op|'{'
string|"'id'"
op|':'
number|'3'
op|','
string|"'zone'"
op|':'
number|'1'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
name|'remove_dev'
op|'('
number|'1'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'rebalance'
op|'('
op|')'
newline|'\n'
name|'r'
op|'='
name|'rb'
op|'.'
name|'get_ring'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'isinstance'
op|'('
name|'r'
op|','
name|'ring'
op|'.'
name|'RingData'
op|')'
op|')'
newline|'\n'
name|'r2'
op|'='
name|'rb'
op|'.'
name|'get_ring'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'r'
name|'is'
name|'r2'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'rebalance'
op|'('
op|')'
newline|'\n'
name|'r3'
op|'='
name|'rb'
op|'.'
name|'get_ring'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'r3'
name|'is'
name|'not'
name|'r2'
op|')'
newline|'\n'
name|'r4'
op|'='
name|'rb'
op|'.'
name|'get_ring'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'r3'
name|'is'
name|'r4'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_add_dev
dedent|''
name|'def'
name|'test_add_dev'
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
number|'1'
op|')'
newline|'\n'
name|'dev'
op|'='
op|'{'
string|"'id'"
op|':'
number|'0'
op|','
string|"'zone'"
op|':'
number|'0'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
string|"'port'"
op|':'
number|'10000'
op|'}'
newline|'\n'
name|'rb'
op|'.'
name|'add_dev'
op|'('
name|'dev'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'Exception'
op|','
name|'rb'
op|'.'
name|'add_dev'
op|','
name|'dev'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_set_dev_weight
dedent|''
name|'def'
name|'test_set_dev_weight'
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
number|'1'
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
string|"'zone'"
op|':'
number|'0'
op|','
string|"'weight'"
op|':'
number|'0.5'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
string|"'zone'"
op|':'
number|'0'
op|','
string|"'weight'"
op|':'
number|'0.5'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
string|"'zone'"
op|':'
number|'1'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
name|'add_dev'
op|'('
op|'{'
string|"'id'"
op|':'
number|'3'
op|','
string|"'zone'"
op|':'
number|'2'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
string|"'port'"
op|':'
number|'10003'
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
name|'r'
op|'='
name|'rb'
op|'.'
name|'get_ring'
op|'('
op|')'
newline|'\n'
name|'counts'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'part2dev_id'
name|'in'
name|'r'
op|'.'
name|'_replica2part2dev_id'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'dev_id'
name|'in'
name|'part2dev_id'
op|':'
newline|'\n'
indent|'                '
name|'counts'
op|'['
name|'dev_id'
op|']'
op|'='
name|'counts'
op|'.'
name|'get'
op|'('
name|'dev_id'
op|','
number|'0'
op|')'
op|'+'
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'counts'
op|','
op|'{'
number|'0'
op|':'
number|'128'
op|','
number|'1'
op|':'
number|'128'
op|','
number|'2'
op|':'
number|'256'
op|','
number|'3'
op|':'
number|'256'
op|'}'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'set_dev_weight'
op|'('
number|'0'
op|','
number|'0.75'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'set_dev_weight'
op|'('
number|'1'
op|','
number|'0.25'
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
name|'r'
op|'='
name|'rb'
op|'.'
name|'get_ring'
op|'('
op|')'
newline|'\n'
name|'counts'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'part2dev_id'
name|'in'
name|'r'
op|'.'
name|'_replica2part2dev_id'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'dev_id'
name|'in'
name|'part2dev_id'
op|':'
newline|'\n'
indent|'                '
name|'counts'
op|'['
name|'dev_id'
op|']'
op|'='
name|'counts'
op|'.'
name|'get'
op|'('
name|'dev_id'
op|','
number|'0'
op|')'
op|'+'
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'counts'
op|','
op|'{'
number|'0'
op|':'
number|'192'
op|','
number|'1'
op|':'
number|'64'
op|','
number|'2'
op|':'
number|'256'
op|','
number|'3'
op|':'
number|'256'
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_remove_dev
dedent|''
name|'def'
name|'test_remove_dev'
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
number|'1'
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
string|"'zone'"
op|':'
number|'0'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
string|"'zone'"
op|':'
number|'1'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
string|"'zone'"
op|':'
number|'2'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
name|'add_dev'
op|'('
op|'{'
string|"'id'"
op|':'
number|'3'
op|','
string|"'zone'"
op|':'
number|'3'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
string|"'port'"
op|':'
number|'10003'
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
name|'r'
op|'='
name|'rb'
op|'.'
name|'get_ring'
op|'('
op|')'
newline|'\n'
name|'counts'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'part2dev_id'
name|'in'
name|'r'
op|'.'
name|'_replica2part2dev_id'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'dev_id'
name|'in'
name|'part2dev_id'
op|':'
newline|'\n'
indent|'                '
name|'counts'
op|'['
name|'dev_id'
op|']'
op|'='
name|'counts'
op|'.'
name|'get'
op|'('
name|'dev_id'
op|','
number|'0'
op|')'
op|'+'
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'counts'
op|','
op|'{'
number|'0'
op|':'
number|'192'
op|','
number|'1'
op|':'
number|'192'
op|','
number|'2'
op|':'
number|'192'
op|','
number|'3'
op|':'
number|'192'
op|'}'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'remove_dev'
op|'('
number|'1'
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
name|'r'
op|'='
name|'rb'
op|'.'
name|'get_ring'
op|'('
op|')'
newline|'\n'
name|'counts'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'part2dev_id'
name|'in'
name|'r'
op|'.'
name|'_replica2part2dev_id'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'dev_id'
name|'in'
name|'part2dev_id'
op|':'
newline|'\n'
indent|'                '
name|'counts'
op|'['
name|'dev_id'
op|']'
op|'='
name|'counts'
op|'.'
name|'get'
op|'('
name|'dev_id'
op|','
number|'0'
op|')'
op|'+'
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'counts'
op|','
op|'{'
number|'0'
op|':'
number|'256'
op|','
number|'2'
op|':'
number|'256'
op|','
number|'3'
op|':'
number|'256'
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_shuffled_gather
dedent|''
name|'def'
name|'test_shuffled_gather'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'self'
op|'.'
name|'_shuffled_gather_helper'
op|'('
op|')'
name|'and'
name|'self'
op|'.'
name|'_shuffled_gather_helper'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'AssertionError'
op|'('
string|"'It is highly likely the ring is no '"
nl|'\n'
string|"'longer shuffling the set of partitions to reassign on a '"
nl|'\n'
string|"'rebalance.'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|_shuffled_gather_helper
dedent|''
dedent|''
name|'def'
name|'_shuffled_gather_helper'
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
number|'1'
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
string|"'zone'"
op|':'
number|'0'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
string|"'zone'"
op|':'
number|'1'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
string|"'zone'"
op|':'
number|'2'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
name|'rb'
op|'.'
name|'add_dev'
op|'('
op|'{'
string|"'id'"
op|':'
number|'3'
op|','
string|"'zone'"
op|':'
number|'3'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
string|"'port'"
op|':'
number|'10003'
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
name|'parts'
op|'='
name|'rb'
op|'.'
name|'_gather_reassign_parts'
op|'('
op|')'
newline|'\n'
name|'max_run'
op|'='
number|'0'
newline|'\n'
name|'run'
op|'='
number|'0'
newline|'\n'
name|'last_part'
op|'='
number|'0'
newline|'\n'
name|'for'
name|'part'
name|'in'
name|'parts'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'part'
op|'>'
name|'last_part'
op|':'
newline|'\n'
indent|'                '
name|'run'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'run'
op|'>'
name|'max_run'
op|':'
newline|'\n'
indent|'                    '
name|'max_run'
op|'='
name|'run'
newline|'\n'
dedent|''
name|'run'
op|'='
number|'0'
newline|'\n'
dedent|''
name|'last_part'
op|'='
name|'part'
newline|'\n'
dedent|''
name|'if'
name|'run'
op|'>'
name|'max_run'
op|':'
newline|'\n'
indent|'            '
name|'max_run'
op|'='
name|'run'
newline|'\n'
dedent|''
name|'return'
name|'max_run'
op|'>'
name|'len'
op|'('
name|'parts'
op|')'
op|'/'
number|'2'
newline|'\n'
nl|'\n'
DECL|member|test_rerebalance
dedent|''
name|'def'
name|'test_rerebalance'
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
number|'1'
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
string|"'zone'"
op|':'
number|'0'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
string|"'zone'"
op|':'
number|'1'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
string|"'zone'"
op|':'
number|'2'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
name|'r'
op|'='
name|'rb'
op|'.'
name|'get_ring'
op|'('
op|')'
newline|'\n'
name|'counts'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'part2dev_id'
name|'in'
name|'r'
op|'.'
name|'_replica2part2dev_id'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'dev_id'
name|'in'
name|'part2dev_id'
op|':'
newline|'\n'
indent|'                '
name|'counts'
op|'['
name|'dev_id'
op|']'
op|'='
name|'counts'
op|'.'
name|'get'
op|'('
name|'dev_id'
op|','
number|'0'
op|')'
op|'+'
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'counts'
op|','
op|'{'
number|'0'
op|':'
number|'256'
op|','
number|'1'
op|':'
number|'256'
op|','
number|'2'
op|':'
number|'256'
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
number|'3'
op|','
string|"'zone'"
op|':'
number|'3'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
string|"'port'"
op|':'
number|'10003'
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
name|'r'
op|'='
name|'rb'
op|'.'
name|'get_ring'
op|'('
op|')'
newline|'\n'
name|'counts'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'part2dev_id'
name|'in'
name|'r'
op|'.'
name|'_replica2part2dev_id'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'dev_id'
name|'in'
name|'part2dev_id'
op|':'
newline|'\n'
indent|'                '
name|'counts'
op|'['
name|'dev_id'
op|']'
op|'='
name|'counts'
op|'.'
name|'get'
op|'('
name|'dev_id'
op|','
number|'0'
op|')'
op|'+'
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'counts'
op|','
op|'{'
number|'0'
op|':'
number|'192'
op|','
number|'1'
op|':'
number|'192'
op|','
number|'2'
op|':'
number|'192'
op|','
number|'3'
op|':'
number|'192'
op|'}'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'set_dev_weight'
op|'('
number|'3'
op|','
number|'100'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'rebalance'
op|'('
op|')'
newline|'\n'
name|'r'
op|'='
name|'rb'
op|'.'
name|'get_ring'
op|'('
op|')'
newline|'\n'
name|'counts'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'part2dev_id'
name|'in'
name|'r'
op|'.'
name|'_replica2part2dev_id'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'dev_id'
name|'in'
name|'part2dev_id'
op|':'
newline|'\n'
indent|'                '
name|'counts'
op|'['
name|'dev_id'
op|']'
op|'='
name|'counts'
op|'.'
name|'get'
op|'('
name|'dev_id'
op|','
number|'0'
op|')'
op|'+'
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'counts'
op|'['
number|'3'
op|']'
op|','
number|'256'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_validate
dedent|''
name|'def'
name|'test_validate'
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
number|'1'
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
string|"'zone'"
op|':'
number|'0'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
string|"'zone'"
op|':'
number|'1'
op|','
string|"'weight'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
string|"'zone'"
op|':'
number|'2'
op|','
string|"'weight'"
op|':'
number|'2'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
name|'add_dev'
op|'('
op|'{'
string|"'id'"
op|':'
number|'3'
op|','
string|"'zone'"
op|':'
number|'3'
op|','
string|"'weight'"
op|':'
number|'2'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
string|"'port'"
op|':'
number|'10003'
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
name|'r'
op|'='
name|'rb'
op|'.'
name|'get_ring'
op|'('
op|')'
newline|'\n'
name|'counts'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'part2dev_id'
name|'in'
name|'r'
op|'.'
name|'_replica2part2dev_id'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'dev_id'
name|'in'
name|'part2dev_id'
op|':'
newline|'\n'
indent|'                '
name|'counts'
op|'['
name|'dev_id'
op|']'
op|'='
name|'counts'
op|'.'
name|'get'
op|'('
name|'dev_id'
op|','
number|'0'
op|')'
op|'+'
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'counts'
op|','
op|'{'
number|'0'
op|':'
number|'128'
op|','
number|'1'
op|':'
number|'128'
op|','
number|'2'
op|':'
number|'256'
op|','
number|'3'
op|':'
number|'256'
op|'}'
op|')'
newline|'\n'
nl|'\n'
name|'dev_usage'
op|','
name|'worst'
op|'='
name|'rb'
op|'.'
name|'validate'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'dev_usage'
name|'is'
name|'None'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'worst'
name|'is'
name|'None'
op|')'
newline|'\n'
nl|'\n'
name|'dev_usage'
op|','
name|'worst'
op|'='
name|'rb'
op|'.'
name|'validate'
op|'('
name|'stats'
op|'='
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'list'
op|'('
name|'dev_usage'
op|')'
op|','
op|'['
number|'128'
op|','
number|'128'
op|','
number|'256'
op|','
number|'256'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'int'
op|'('
name|'worst'
op|')'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
name|'rb'
op|'.'
name|'set_dev_weight'
op|'('
number|'2'
op|','
number|'0'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'rebalance'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'rb'
op|'.'
name|'validate'
op|'('
name|'stats'
op|'='
name|'True'
op|')'
op|'['
number|'1'
op|']'
op|','
number|'999.99'
op|')'
newline|'\n'
nl|'\n'
comment|'# Test not all partitions doubly accounted for'
nl|'\n'
name|'rb'
op|'.'
name|'devs'
op|'['
number|'1'
op|']'
op|'['
string|"'parts'"
op|']'
op|'-='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'Exception'
op|','
name|'rb'
op|'.'
name|'validate'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'devs'
op|'['
number|'1'
op|']'
op|'['
string|"'parts'"
op|']'
op|'+='
number|'1'
newline|'\n'
nl|'\n'
comment|'# Test duplicate device for partition'
nl|'\n'
name|'orig_dev_id'
op|'='
name|'rb'
op|'.'
name|'_replica2part2dev'
op|'['
number|'0'
op|']'
op|'['
number|'0'
op|']'
newline|'\n'
name|'rb'
op|'.'
name|'_replica2part2dev'
op|'['
number|'0'
op|']'
op|'['
number|'0'
op|']'
op|'='
name|'rb'
op|'.'
name|'_replica2part2dev'
op|'['
number|'1'
op|']'
op|'['
number|'0'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'Exception'
op|','
name|'rb'
op|'.'
name|'validate'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'_replica2part2dev'
op|'['
number|'0'
op|']'
op|'['
number|'0'
op|']'
op|'='
name|'orig_dev_id'
newline|'\n'
nl|'\n'
comment|'# Test duplicate zone for partition'
nl|'\n'
name|'rb'
op|'.'
name|'add_dev'
op|'('
op|'{'
string|"'id'"
op|':'
number|'5'
op|','
string|"'zone'"
op|':'
number|'0'
op|','
string|"'weight'"
op|':'
number|'2'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
string|"'port'"
op|':'
number|'10005'
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
name|'rb'
op|'.'
name|'validate'
op|'('
op|')'
newline|'\n'
name|'orig_replica'
op|'='
name|'orig_partition'
op|'='
name|'orig_device'
op|'='
name|'None'
newline|'\n'
name|'for'
name|'part2dev'
name|'in'
name|'rb'
op|'.'
name|'_replica2part2dev'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'p'
name|'in'
name|'xrange'
op|'('
number|'2'
op|'**'
number|'8'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'part2dev'
op|'['
name|'p'
op|']'
op|'=='
number|'5'
op|':'
newline|'\n'
indent|'                    '
name|'for'
name|'r'
name|'in'
name|'xrange'
op|'('
name|'len'
op|'('
name|'rb'
op|'.'
name|'_replica2part2dev'
op|')'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'if'
name|'rb'
op|'.'
name|'_replica2part2dev'
op|'['
name|'r'
op|']'
op|'['
name|'p'
op|']'
op|'!='
number|'5'
op|':'
newline|'\n'
indent|'                            '
name|'orig_replica'
op|'='
name|'r'
newline|'\n'
name|'orig_partition'
op|'='
name|'p'
newline|'\n'
name|'orig_device'
op|'='
name|'rb'
op|'.'
name|'_replica2part2dev'
op|'['
name|'r'
op|']'
op|'['
name|'p'
op|']'
newline|'\n'
name|'rb'
op|'.'
name|'_replica2part2dev'
op|'['
name|'r'
op|']'
op|'['
name|'p'
op|']'
op|'='
number|'0'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'if'
name|'orig_replica'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'                    '
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'orig_replica'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'Exception'
op|','
name|'rb'
op|'.'
name|'validate'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'_replica2part2dev'
op|'['
name|'orig_replica'
op|']'
op|'['
name|'orig_partition'
op|']'
op|'='
name|'orig_device'
newline|'\n'
nl|'\n'
comment|"# Tests that validate can handle 'holes' in .devs"
nl|'\n'
name|'rb'
op|'.'
name|'remove_dev'
op|'('
number|'2'
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
name|'rb'
op|'.'
name|'validate'
op|'('
name|'stats'
op|'='
name|'True'
op|')'
newline|'\n'
nl|'\n'
comment|"# Validate that zero weight devices with no partitions don't count on"
nl|'\n'
comment|"# the 'worst' value."
nl|'\n'
name|'self'
op|'.'
name|'assertNotEquals'
op|'('
name|'rb'
op|'.'
name|'validate'
op|'('
name|'stats'
op|'='
name|'True'
op|')'
op|'['
number|'1'
op|']'
op|','
number|'999.99'
op|')'
newline|'\n'
name|'rb'
op|'.'
name|'add_dev'
op|'('
op|'{'
string|"'id'"
op|':'
number|'4'
op|','
string|"'zone'"
op|':'
number|'0'
op|','
string|"'weight'"
op|':'
number|'0'
op|','
string|"'ip'"
op|':'
string|"'127.0.0.1'"
op|','
nl|'\n'
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
name|'self'
op|'.'
name|'assertNotEquals'
op|'('
name|'rb'
op|'.'
name|'validate'
op|'('
name|'stats'
op|'='
name|'True'
op|')'
op|'['
number|'1'
op|']'
op|','
number|'999.99'
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
