begin_unit
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
name|'common'
op|'.'
name|'ring'
op|'.'
name|'utils'
name|'import'
name|'build_tier_tree'
op|','
name|'tiers_for_dev'
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
string|"'zone'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'192.168.1.1'"
op|','
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
string|"'zone'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'192.168.1.1'"
op|','
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
string|"'zone'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'192.168.1.1'"
op|','
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
string|"'zone'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'192.168.1.2'"
op|','
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
string|"'zone'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'192.168.1.2'"
op|','
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
string|"'zone'"
op|':'
number|'1'
op|','
string|"'ip'"
op|':'
string|"'192.168.1.2'"
op|','
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
string|"'zone'"
op|':'
number|'2'
op|','
string|"'ip'"
op|':'
string|"'192.168.2.1'"
op|','
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
string|"'zone'"
op|':'
number|'2'
op|','
string|"'ip'"
op|':'
string|"'192.168.2.1'"
op|','
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
string|"'zone'"
op|':'
number|'2'
op|','
string|"'ip'"
op|':'
string|"'192.168.2.1'"
op|','
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
string|"'zone'"
op|':'
number|'2'
op|','
string|"'ip'"
op|':'
string|"'192.168.2.2'"
op|','
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
string|"'zone'"
op|':'
number|'2'
op|','
string|"'ip'"
op|':'
string|"'192.168.2.2'"
op|','
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
string|"'zone'"
op|':'
number|'2'
op|','
string|"'ip'"
op|':'
string|"'192.168.2.2'"
op|','
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
op|'('
number|'1'
op|','
string|"'192.168.1.1:6000'"
op|')'
op|','
op|'('
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
number|'7'
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
number|'2'
op|','
op|')'
op|','
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
nl|'\n'
name|'set'
op|'('
op|'['
op|'('
number|'1'
op|','
string|"'192.168.1.2:6000'"
op|')'
op|','
nl|'\n'
op|'('
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
number|'2'
op|','
op|')'
op|']'
op|','
nl|'\n'
name|'set'
op|'('
op|'['
op|'('
number|'2'
op|','
string|"'192.168.2.2:6000'"
op|')'
op|','
nl|'\n'
op|'('
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
string|"'192.168.1.1:6000'"
op|','
number|'0'
op|')'
op|','
nl|'\n'
op|'('
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
string|"'192.168.1.2:6000'"
op|','
number|'3'
op|')'
op|','
nl|'\n'
op|'('
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
number|'2'
op|','
string|"'192.168.2.1:6000'"
op|','
number|'6'
op|')'
op|','
nl|'\n'
op|'('
number|'2'
op|','
string|"'192.168.2.1:6000'"
op|','
number|'7'
op|')'
op|','
nl|'\n'
op|'('
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
number|'2'
op|','
string|"'192.168.2.2:6000'"
op|','
number|'9'
op|')'
op|','
nl|'\n'
op|'('
number|'2'
op|','
string|"'192.168.2.2:6000'"
op|','
number|'10'
op|')'
op|','
nl|'\n'
op|'('
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
