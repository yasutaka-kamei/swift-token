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
name|'unittest'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'middleware'
name|'import'
name|'acl'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestACL
name|'class'
name|'TestACL'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_clean_acl
indent|'    '
name|'def'
name|'test_clean_acl'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'value'
op|'='
name|'acl'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.r:*'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.r:*'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'acl'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.r:specific.host'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.r:specific.host'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'acl'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.r:.ending.with'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.r:.ending.with'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'acl'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.r:*.ending.with'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.r:.ending.with'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'acl'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.r:-*.ending.with'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.r:-.ending.with'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'acl'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.r:one,.r:two'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.r:one,.r:two'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'acl'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.r:*,.r:-specific.host'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.r:*,.r:-specific.host'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'acl'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.r:*,.r:-.ending.with'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.r:*,.r:-.ending.with'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'acl'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.r:one,.r:-two'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.r:one,.r:-two'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'acl'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.r:one,.r:-two,account,account:user'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.r:one,.r:-two,account,account:user'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'acl'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'TEST_account'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'TEST_account'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'acl'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.ref:*'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.r:*'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'acl'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.referer:*'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.r:*'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'acl'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
string|"'.referrer:*'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.r:*'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'acl'
op|'.'
name|'clean_acl'
op|'('
string|"'header'"
op|','
nl|'\n'
string|"' .r : one , ,, .r:two , .r : - three '"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
string|"'.r:one,.r:two,.r:-three'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'acl'
op|'.'
name|'clean_acl'
op|','
string|"'header'"
op|','
string|"'.unknown:test'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'acl'
op|'.'
name|'clean_acl'
op|','
string|"'header'"
op|','
string|"'.r:'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'acl'
op|'.'
name|'clean_acl'
op|','
string|"'header'"
op|','
string|"'.r:*.'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'acl'
op|'.'
name|'clean_acl'
op|','
string|"'header'"
op|','
string|"'.r : * . '"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'acl'
op|'.'
name|'clean_acl'
op|','
string|"'header'"
op|','
string|"'.r:-*.'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'acl'
op|'.'
name|'clean_acl'
op|','
string|"'header'"
op|','
string|"'.r : - * . '"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'acl'
op|'.'
name|'clean_acl'
op|','
string|"'header'"
op|','
string|"' .r : '"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'acl'
op|'.'
name|'clean_acl'
op|','
string|"'header'"
op|','
string|"'user , .r : '"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'acl'
op|'.'
name|'clean_acl'
op|','
string|"'header'"
op|','
string|"'.r:-'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'acl'
op|'.'
name|'clean_acl'
op|','
string|"'header'"
op|','
string|"' .r : - '"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'acl'
op|'.'
name|'clean_acl'
op|','
string|"'header'"
op|','
nl|'\n'
string|"'user , .r : - '"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'acl'
op|'.'
name|'clean_acl'
op|','
string|"'write-header'"
op|','
string|"'.r:r'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_parse_acl
dedent|''
name|'def'
name|'test_parse_acl'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'acl'
op|'.'
name|'parse_acl'
op|'('
name|'None'
op|')'
op|','
op|'('
op|'['
op|']'
op|','
op|'['
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'acl'
op|'.'
name|'parse_acl'
op|'('
string|"''"
op|')'
op|','
op|'('
op|'['
op|']'
op|','
op|'['
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'acl'
op|'.'
name|'parse_acl'
op|'('
string|"'.r:ref1'"
op|')'
op|','
op|'('
op|'['
string|"'ref1'"
op|']'
op|','
op|'['
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'acl'
op|'.'
name|'parse_acl'
op|'('
string|"'.r:-ref1'"
op|')'
op|','
op|'('
op|'['
string|"'-ref1'"
op|']'
op|','
op|'['
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'acl'
op|'.'
name|'parse_acl'
op|'('
string|"'account:user'"
op|')'
op|','
nl|'\n'
op|'('
op|'['
op|']'
op|','
op|'['
string|"'account:user'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'acl'
op|'.'
name|'parse_acl'
op|'('
string|"'account'"
op|')'
op|','
op|'('
op|'['
op|']'
op|','
op|'['
string|"'account'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'acl'
op|'.'
name|'parse_acl'
op|'('
string|"'acc1,acc2:usr2,.r:ref3,.r:-ref4'"
op|')'
op|','
nl|'\n'
op|'('
op|'['
string|"'ref3'"
op|','
string|"'-ref4'"
op|']'
op|','
op|'['
string|"'acc1'"
op|','
string|"'acc2:usr2'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'acl'
op|'.'
name|'parse_acl'
op|'('
nl|'\n'
string|"'acc1,acc2:usr2,.r:ref3,acc3,acc4:usr4,.r:ref5,.r:-ref6'"
op|')'
op|','
nl|'\n'
op|'('
op|'['
string|"'ref3'"
op|','
string|"'ref5'"
op|','
string|"'-ref6'"
op|']'
op|','
nl|'\n'
op|'['
string|"'acc1'"
op|','
string|"'acc2:usr2'"
op|','
string|"'acc3'"
op|','
string|"'acc4:usr4'"
op|']'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_referrer_allowed
dedent|''
name|'def'
name|'test_referrer_allowed'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'assert_'
op|'('
name|'not'
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
string|"'host'"
op|','
name|'None'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'not'
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
string|"'host'"
op|','
op|'['
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
name|'None'
op|','
op|'['
string|"'*'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
string|"''"
op|','
op|'['
string|"'*'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'not'
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
name|'None'
op|','
op|'['
string|"'specific.host'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'not'
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
string|"''"
op|','
op|'['
string|"'specific.host'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
string|"'http://www.example.com/index.html'"
op|','
nl|'\n'
op|'['
string|"'.example.com'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
nl|'\n'
string|"'http://user@www.example.com/index.html'"
op|','
op|'['
string|"'.example.com'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
nl|'\n'
string|"'http://user:pass@www.example.com/index.html'"
op|','
op|'['
string|"'.example.com'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
nl|'\n'
string|"'http://www.example.com:8080/index.html'"
op|','
op|'['
string|"'.example.com'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
nl|'\n'
string|"'http://user@www.example.com:8080/index.html'"
op|','
op|'['
string|"'.example.com'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
nl|'\n'
string|"'http://user:pass@www.example.com:8080/index.html'"
op|','
nl|'\n'
op|'['
string|"'.example.com'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
nl|'\n'
string|"'http://user:pass@www.example.com:8080'"
op|','
op|'['
string|"'.example.com'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
string|"'http://www.example.com'"
op|','
nl|'\n'
op|'['
string|"'.example.com'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'not'
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
string|"'http://thief.example.com'"
op|','
nl|'\n'
op|'['
string|"'.example.com'"
op|','
string|"'-thief.example.com'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'not'
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
string|"'http://thief.example.com'"
op|','
nl|'\n'
op|'['
string|"'*'"
op|','
string|"'-thief.example.com'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
string|"'http://www.example.com'"
op|','
nl|'\n'
op|'['
string|"'.other.com'"
op|','
string|"'www.example.com'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
string|"'http://www.example.com'"
op|','
nl|'\n'
op|'['
string|"'-.example.com'"
op|','
string|"'www.example.com'"
op|']'
op|')'
op|')'
newline|'\n'
comment|'# This is considered a relative uri to the request uri, a mode not'
nl|'\n'
comment|'# currently supported.'
nl|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'not'
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
string|"'www.example.com'"
op|','
nl|'\n'
op|'['
string|"'.example.com'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'not'
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
string|"'../index.html'"
op|','
nl|'\n'
op|'['
string|"'.example.com'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'acl'
op|'.'
name|'referrer_allowed'
op|'('
string|"'www.example.com'"
op|','
op|'['
string|"'*'"
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
