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
comment|'# TODO: More tests'
nl|'\n'
name|'import'
name|'socket'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'from'
name|'StringIO'
name|'import'
name|'StringIO'
newline|'\n'
name|'from'
name|'urlparse'
name|'import'
name|'urlparse'
newline|'\n'
nl|'\n'
comment|'# TODO: mock http connection class with more control over headers'
nl|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
op|'.'
name|'proxy'
op|'.'
name|'test_server'
name|'import'
name|'fake_http_connect'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'client'
name|'as'
name|'c'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestHttpHelpers
name|'class'
name|'TestHttpHelpers'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_quote
indent|'    '
name|'def'
name|'test_quote'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'value'
op|'='
string|"'standard string'"
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
string|"'standard%20string'"
op|','
name|'c'
op|'.'
name|'quote'
op|'('
name|'value'
op|')'
op|')'
newline|'\n'
name|'value'
op|'='
string|"u'\\u0075nicode string'"
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
string|"'unicode%20string'"
op|','
name|'c'
op|'.'
name|'quote'
op|'('
name|'value'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_http_connection
dedent|''
name|'def'
name|'test_http_connection'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'url'
op|'='
string|"'http://www.test.com'"
newline|'\n'
name|'_junk'
op|','
name|'conn'
op|'='
name|'c'
op|'.'
name|'http_connection'
op|'('
name|'url'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'isinstance'
op|'('
name|'conn'
op|','
name|'c'
op|'.'
name|'HTTPConnection'
op|')'
op|')'
newline|'\n'
name|'url'
op|'='
string|"'https://www.test.com'"
newline|'\n'
name|'_junk'
op|','
name|'conn'
op|'='
name|'c'
op|'.'
name|'http_connection'
op|'('
name|'url'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'isinstance'
op|'('
name|'conn'
op|','
name|'c'
op|'.'
name|'HTTPSConnection'
op|')'
op|')'
newline|'\n'
name|'url'
op|'='
string|"'ftp://www.test.com'"
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'c'
op|'.'
name|'ClientException'
op|','
name|'c'
op|'.'
name|'http_connection'
op|','
name|'url'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestClientException
dedent|''
dedent|''
name|'class'
name|'TestClientException'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_is_exception
indent|'    '
name|'def'
name|'test_is_exception'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'issubclass'
op|'('
name|'c'
op|'.'
name|'ClientException'
op|','
name|'Exception'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_format
dedent|''
name|'def'
name|'test_format'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'exc'
op|'='
name|'c'
op|'.'
name|'ClientException'
op|'('
string|"'something failed'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'something failed'"
name|'in'
name|'str'
op|'('
name|'exc'
op|')'
op|')'
newline|'\n'
name|'test_kwargs'
op|'='
op|'('
nl|'\n'
string|"'scheme'"
op|','
nl|'\n'
string|"'host'"
op|','
nl|'\n'
string|"'port'"
op|','
nl|'\n'
string|"'path'"
op|','
nl|'\n'
string|"'query'"
op|','
nl|'\n'
string|"'status'"
op|','
nl|'\n'
string|"'reason'"
op|','
nl|'\n'
string|"'device'"
op|','
nl|'\n'
op|')'
newline|'\n'
name|'for'
name|'value'
name|'in'
name|'test_kwargs'
op|':'
newline|'\n'
indent|'            '
name|'kwargs'
op|'='
op|'{'
nl|'\n'
string|"'http_%s'"
op|'%'
name|'value'
op|':'
name|'value'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'exc'
op|'='
name|'c'
op|'.'
name|'ClientException'
op|'('
string|"'test'"
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'value'
name|'in'
name|'str'
op|'('
name|'exc'
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestJsonImport
dedent|''
dedent|''
dedent|''
name|'class'
name|'TestJsonImport'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|tearDown
indent|'    '
name|'def'
name|'tearDown'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'import'
name|'json'
newline|'\n'
dedent|''
name|'except'
name|'ImportError'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'reload'
op|'('
name|'json'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'import'
name|'simplejson'
newline|'\n'
dedent|''
name|'except'
name|'ImportError'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'reload'
op|'('
name|'simplejson'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_any
dedent|''
dedent|''
name|'def'
name|'test_any'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'hasattr'
op|'('
name|'c'
op|','
string|"'json_loads'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_no_simplejson
dedent|''
name|'def'
name|'test_no_simplejson'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# break simplejson'
nl|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'import'
name|'simplejson'
newline|'\n'
dedent|''
name|'except'
name|'ImportError'
op|':'
newline|'\n'
comment|"# not installed, so we don't have to break it for these tests"
nl|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'delattr'
op|'('
name|'simplejson'
op|','
string|"'loads'"
op|')'
newline|'\n'
name|'reload'
op|'('
name|'c'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'from'
name|'json'
name|'import'
name|'loads'
newline|'\n'
dedent|''
name|'except'
name|'ImportError'
op|':'
newline|'\n'
comment|'# this case is stested in _no_json'
nl|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'loads'
op|','
name|'c'
op|'.'
name|'json_loads'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|MockHttpTest
dedent|''
dedent|''
dedent|''
name|'class'
name|'MockHttpTest'
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
DECL|function|fake_http_connection
indent|'        '
name|'def'
name|'fake_http_connection'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'_orig_http_connection'
op|'='
name|'c'
op|'.'
name|'http_connection'
newline|'\n'
nl|'\n'
DECL|function|wrapper
name|'def'
name|'wrapper'
op|'('
name|'url'
op|','
name|'proxy'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'parsed'
op|','
name|'_conn'
op|'='
name|'_orig_http_connection'
op|'('
name|'url'
op|','
name|'proxy'
op|'='
name|'proxy'
op|')'
newline|'\n'
name|'conn'
op|'='
name|'fake_http_connect'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|function|request
name|'def'
name|'request'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'return'
newline|'\n'
dedent|''
name|'conn'
op|'.'
name|'request'
op|'='
name|'request'
newline|'\n'
nl|'\n'
name|'conn'
op|'.'
name|'has_been_read'
op|'='
name|'False'
newline|'\n'
name|'_orig_read'
op|'='
name|'conn'
op|'.'
name|'read'
newline|'\n'
nl|'\n'
DECL|function|read
name|'def'
name|'read'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'conn'
op|'.'
name|'has_been_read'
op|'='
name|'True'
newline|'\n'
name|'return'
name|'_orig_read'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
dedent|''
name|'conn'
op|'.'
name|'read'
op|'='
name|'read'
newline|'\n'
nl|'\n'
name|'return'
name|'parsed'
op|','
name|'conn'
newline|'\n'
dedent|''
name|'return'
name|'wrapper'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'fake_http_connection'
op|'='
name|'fake_http_connection'
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
name|'reload'
op|'('
name|'c'
op|')'
newline|'\n'
nl|'\n'
comment|'# TODO: following tests are placeholders, need more tests, better coverage'
nl|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestGetAuth
dedent|''
dedent|''
name|'class'
name|'TestGetAuth'
op|'('
name|'MockHttpTest'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_ok
indent|'    '
name|'def'
name|'test_ok'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'200'
op|')'
newline|'\n'
name|'url'
op|','
name|'token'
op|'='
name|'c'
op|'.'
name|'get_auth'
op|'('
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'url'
op|','
name|'None'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'token'
op|','
name|'None'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestGetAccount
dedent|''
dedent|''
name|'class'
name|'TestGetAccount'
op|'('
name|'MockHttpTest'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_no_content
indent|'    '
name|'def'
name|'test_no_content'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'204'
op|')'
newline|'\n'
name|'value'
op|'='
name|'c'
op|'.'
name|'get_account'
op|'('
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|')'
op|'['
number|'1'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
op|'['
op|']'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestHeadAccount
dedent|''
dedent|''
name|'class'
name|'TestHeadAccount'
op|'('
name|'MockHttpTest'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_ok
indent|'    '
name|'def'
name|'test_ok'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'200'
op|')'
newline|'\n'
name|'value'
op|'='
name|'c'
op|'.'
name|'head_account'
op|'('
string|"'http://www.tests.com'"
op|','
string|"'asdf'"
op|')'
newline|'\n'
comment|"# TODO: Hmm. This doesn't really test too much as it uses a fake that"
nl|'\n'
comment|'# always returns the same dict. I guess it "exercises" the code, so'
nl|'\n'
comment|"# I'll leave it for now."
nl|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'type'
op|'('
name|'value'
op|')'
op|','
name|'dict'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_server_error
dedent|''
name|'def'
name|'test_server_error'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'body'
op|'='
string|"'c'"
op|'*'
number|'65'
newline|'\n'
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'500'
op|','
name|'body'
op|'='
name|'body'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'c'
op|'.'
name|'ClientException'
op|','
name|'c'
op|'.'
name|'head_account'
op|','
nl|'\n'
string|"'http://www.tests.com'"
op|','
string|"'asdf'"
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'value'
op|'='
name|'c'
op|'.'
name|'head_account'
op|'('
string|"'http://www.tests.com'"
op|','
string|"'asdf'"
op|')'
newline|'\n'
dedent|''
name|'except'
name|'c'
op|'.'
name|'ClientException'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'            '
name|'new_body'
op|'='
string|'"[first 60 chars of response] "'
op|'+'
name|'body'
op|'['
number|'0'
op|':'
number|'60'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'e'
op|'.'
name|'__str__'
op|'('
op|')'
op|'['
op|'-'
number|'89'
op|':'
op|']'
op|','
name|'new_body'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestGetContainer
dedent|''
dedent|''
dedent|''
name|'class'
name|'TestGetContainer'
op|'('
name|'MockHttpTest'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_no_content
indent|'    '
name|'def'
name|'test_no_content'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'204'
op|')'
newline|'\n'
name|'value'
op|'='
name|'c'
op|'.'
name|'get_container'
op|'('
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|')'
op|'['
number|'1'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
op|'['
op|']'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestHeadContainer
dedent|''
dedent|''
name|'class'
name|'TestHeadContainer'
op|'('
name|'MockHttpTest'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_server_error
indent|'    '
name|'def'
name|'test_server_error'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'body'
op|'='
string|"'c'"
op|'*'
number|'60'
newline|'\n'
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'500'
op|','
name|'body'
op|'='
name|'body'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'c'
op|'.'
name|'ClientException'
op|','
name|'c'
op|'.'
name|'head_container'
op|','
nl|'\n'
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|','
nl|'\n'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'value'
op|'='
name|'c'
op|'.'
name|'head_container'
op|'('
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|')'
newline|'\n'
dedent|''
name|'except'
name|'c'
op|'.'
name|'ClientException'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'e'
op|'.'
name|'http_response_content'
op|','
name|'body'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestPutContainer
dedent|''
dedent|''
dedent|''
name|'class'
name|'TestPutContainer'
op|'('
name|'MockHttpTest'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_ok
indent|'    '
name|'def'
name|'test_ok'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'200'
op|')'
newline|'\n'
name|'value'
op|'='
name|'c'
op|'.'
name|'put_container'
op|'('
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
name|'None'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_server_error
dedent|''
name|'def'
name|'test_server_error'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'body'
op|'='
string|"'c'"
op|'*'
number|'60'
newline|'\n'
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'500'
op|','
name|'body'
op|'='
name|'body'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'c'
op|'.'
name|'ClientException'
op|','
name|'c'
op|'.'
name|'put_container'
op|','
nl|'\n'
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|','
nl|'\n'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'value'
op|'='
name|'c'
op|'.'
name|'put_container'
op|'('
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|')'
newline|'\n'
dedent|''
name|'except'
name|'c'
op|'.'
name|'ClientException'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'e'
op|'.'
name|'http_response_content'
op|','
name|'body'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestDeleteContainer
dedent|''
dedent|''
dedent|''
name|'class'
name|'TestDeleteContainer'
op|'('
name|'MockHttpTest'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_ok
indent|'    '
name|'def'
name|'test_ok'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'200'
op|')'
newline|'\n'
name|'value'
op|'='
name|'c'
op|'.'
name|'delete_container'
op|'('
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'value'
op|','
name|'None'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestGetObject
dedent|''
dedent|''
name|'class'
name|'TestGetObject'
op|'('
name|'MockHttpTest'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_server_error
indent|'    '
name|'def'
name|'test_server_error'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'500'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'c'
op|'.'
name|'ClientException'
op|','
name|'c'
op|'.'
name|'get_object'
op|','
nl|'\n'
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestHeadObject
dedent|''
dedent|''
name|'class'
name|'TestHeadObject'
op|'('
name|'MockHttpTest'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_server_error
indent|'    '
name|'def'
name|'test_server_error'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'500'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'c'
op|'.'
name|'ClientException'
op|','
name|'c'
op|'.'
name|'head_object'
op|','
nl|'\n'
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestPutObject
dedent|''
dedent|''
name|'class'
name|'TestPutObject'
op|'('
name|'MockHttpTest'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_ok
indent|'    '
name|'def'
name|'test_ok'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'200'
op|')'
newline|'\n'
name|'args'
op|'='
op|'('
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|')'
newline|'\n'
name|'value'
op|'='
name|'c'
op|'.'
name|'put_object'
op|'('
op|'*'
name|'args'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'isinstance'
op|'('
name|'value'
op|','
name|'basestring'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_server_error
dedent|''
name|'def'
name|'test_server_error'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'body'
op|'='
string|"'c'"
op|'*'
number|'60'
newline|'\n'
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'500'
op|','
name|'body'
op|'='
name|'body'
op|')'
newline|'\n'
name|'args'
op|'='
op|'('
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'c'
op|'.'
name|'ClientException'
op|','
name|'c'
op|'.'
name|'put_object'
op|','
op|'*'
name|'args'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'value'
op|'='
name|'c'
op|'.'
name|'put_object'
op|'('
op|'*'
name|'args'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'c'
op|'.'
name|'ClientException'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'e'
op|'.'
name|'http_response_content'
op|','
name|'body'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestPostObject
dedent|''
dedent|''
dedent|''
name|'class'
name|'TestPostObject'
op|'('
name|'MockHttpTest'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_ok
indent|'    '
name|'def'
name|'test_ok'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'200'
op|')'
newline|'\n'
name|'args'
op|'='
op|'('
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'value'
op|'='
name|'c'
op|'.'
name|'post_object'
op|'('
op|'*'
name|'args'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_server_error
dedent|''
name|'def'
name|'test_server_error'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'body'
op|'='
string|"'c'"
op|'*'
number|'60'
newline|'\n'
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'500'
op|','
name|'body'
op|'='
name|'body'
op|')'
newline|'\n'
name|'args'
op|'='
op|'('
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'c'
op|'.'
name|'ClientException'
op|','
name|'c'
op|'.'
name|'post_object'
op|','
op|'*'
name|'args'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'value'
op|'='
name|'c'
op|'.'
name|'post_object'
op|'('
op|'*'
name|'args'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'c'
op|'.'
name|'ClientException'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'e'
op|'.'
name|'http_response_content'
op|','
name|'body'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestDeleteObject
dedent|''
dedent|''
dedent|''
name|'class'
name|'TestDeleteObject'
op|'('
name|'MockHttpTest'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_ok
indent|'    '
name|'def'
name|'test_ok'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'200'
op|')'
newline|'\n'
name|'value'
op|'='
name|'c'
op|'.'
name|'delete_object'
op|'('
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_server_error
dedent|''
name|'def'
name|'test_server_error'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'500'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'c'
op|'.'
name|'ClientException'
op|','
name|'c'
op|'.'
name|'delete_object'
op|','
nl|'\n'
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestConnection
dedent|''
dedent|''
name|'class'
name|'TestConnection'
op|'('
name|'MockHttpTest'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_instance
indent|'    '
name|'def'
name|'test_instance'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'conn'
op|'='
name|'c'
op|'.'
name|'Connection'
op|'('
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'conn'
op|'.'
name|'retries'
op|','
number|'5'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_retry
dedent|''
name|'def'
name|'test_retry'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'500'
op|')'
newline|'\n'
nl|'\n'
DECL|function|quick_sleep
name|'def'
name|'quick_sleep'
op|'('
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'c'
op|'.'
name|'sleep'
op|'='
name|'quick_sleep'
newline|'\n'
name|'conn'
op|'='
name|'c'
op|'.'
name|'Connection'
op|'('
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'c'
op|'.'
name|'ClientException'
op|','
name|'conn'
op|'.'
name|'head_account'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'conn'
op|'.'
name|'attempts'
op|','
name|'conn'
op|'.'
name|'retries'
op|'+'
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_resp_read_on_server_error
dedent|''
name|'def'
name|'test_resp_read_on_server_error'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'500'
op|')'
newline|'\n'
name|'conn'
op|'='
name|'c'
op|'.'
name|'Connection'
op|'('
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|','
name|'retries'
op|'='
number|'0'
op|')'
newline|'\n'
nl|'\n'
DECL|function|get_auth
name|'def'
name|'get_auth'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
string|"'http://www.new.com'"
op|','
string|"'new'"
newline|'\n'
dedent|''
name|'conn'
op|'.'
name|'get_auth'
op|'='
name|'get_auth'
newline|'\n'
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|'='
name|'conn'
op|'.'
name|'get_auth'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'method_signatures'
op|'='
op|'('
nl|'\n'
op|'('
name|'conn'
op|'.'
name|'head_account'
op|','
op|'['
op|']'
op|')'
op|','
nl|'\n'
op|'('
name|'conn'
op|'.'
name|'get_account'
op|','
op|'['
op|']'
op|')'
op|','
nl|'\n'
op|'('
name|'conn'
op|'.'
name|'head_container'
op|','
op|'('
string|"'asdf'"
op|','
op|')'
op|')'
op|','
nl|'\n'
op|'('
name|'conn'
op|'.'
name|'get_container'
op|','
op|'('
string|"'asdf'"
op|','
op|')'
op|')'
op|','
nl|'\n'
op|'('
name|'conn'
op|'.'
name|'put_container'
op|','
op|'('
string|"'asdf'"
op|','
op|')'
op|')'
op|','
nl|'\n'
op|'('
name|'conn'
op|'.'
name|'delete_container'
op|','
op|'('
string|"'asdf'"
op|','
op|')'
op|')'
op|','
nl|'\n'
op|'('
name|'conn'
op|'.'
name|'head_object'
op|','
op|'('
string|"'asdf'"
op|','
string|"'asdf'"
op|')'
op|')'
op|','
nl|'\n'
op|'('
name|'conn'
op|'.'
name|'get_object'
op|','
op|'('
string|"'asdf'"
op|','
string|"'asdf'"
op|')'
op|')'
op|','
nl|'\n'
op|'('
name|'conn'
op|'.'
name|'put_object'
op|','
op|'('
string|"'asdf'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|')'
op|')'
op|','
nl|'\n'
op|'('
name|'conn'
op|'.'
name|'post_object'
op|','
op|'('
string|"'asdf'"
op|','
string|"'asdf'"
op|','
op|'{'
op|'}'
op|')'
op|')'
op|','
nl|'\n'
op|'('
name|'conn'
op|'.'
name|'delete_object'
op|','
op|'('
string|"'asdf'"
op|','
string|"'asdf'"
op|')'
op|')'
op|','
nl|'\n'
op|')'
newline|'\n'
nl|'\n'
name|'for'
name|'method'
op|','
name|'args'
name|'in'
name|'method_signatures'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'c'
op|'.'
name|'ClientException'
op|','
name|'method'
op|','
op|'*'
name|'args'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'conn'
op|'.'
name|'http_conn'
op|'['
number|'1'
op|']'
op|'.'
name|'has_been_read'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'AssertionError'
op|':'
newline|'\n'
indent|'                '
name|'msg'
op|'='
string|"'%s did not read resp on server error'"
op|'%'
name|'method'
op|'.'
name|'__name__'
newline|'\n'
name|'self'
op|'.'
name|'fail'
op|'('
name|'msg'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|','
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'e'
op|'.'
name|'__class__'
op|'('
string|'"%s - %s"'
op|'%'
op|'('
name|'method'
op|'.'
name|'__name__'
op|','
name|'e'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_reauth
dedent|''
dedent|''
dedent|''
name|'def'
name|'test_reauth'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'401'
op|')'
newline|'\n'
nl|'\n'
DECL|function|get_auth
name|'def'
name|'get_auth'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
string|"'http://www.new.com'"
op|','
string|"'new'"
newline|'\n'
nl|'\n'
DECL|function|swap_sleep
dedent|''
name|'def'
name|'swap_sleep'
op|'('
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'swap_sleep_called'
op|'='
name|'True'
newline|'\n'
name|'c'
op|'.'
name|'get_auth'
op|'='
name|'get_auth'
newline|'\n'
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'self'
op|'.'
name|'fake_http_connection'
op|'('
number|'200'
op|')'
newline|'\n'
dedent|''
name|'c'
op|'.'
name|'sleep'
op|'='
name|'swap_sleep'
newline|'\n'
name|'self'
op|'.'
name|'swap_sleep_called'
op|'='
name|'False'
newline|'\n'
nl|'\n'
name|'conn'
op|'='
name|'c'
op|'.'
name|'Connection'
op|'('
string|"'http://www.test.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|','
nl|'\n'
name|'preauthurl'
op|'='
string|"'http://www.old.com'"
op|','
nl|'\n'
name|'preauthtoken'
op|'='
string|"'old'"
op|','
nl|'\n'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'conn'
op|'.'
name|'attempts'
op|','
number|'0'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'conn'
op|'.'
name|'url'
op|','
string|"'http://www.old.com'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'conn'
op|'.'
name|'token'
op|','
string|"'old'"
op|')'
newline|'\n'
nl|'\n'
name|'value'
op|'='
name|'conn'
op|'.'
name|'head_account'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'self'
op|'.'
name|'swap_sleep_called'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'conn'
op|'.'
name|'attempts'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'conn'
op|'.'
name|'url'
op|','
string|"'http://www.new.com'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'conn'
op|'.'
name|'token'
op|','
string|"'new'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_reset_stream
dedent|''
name|'def'
name|'test_reset_stream'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|class|LocalContents
indent|'        '
name|'class'
name|'LocalContents'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__init__
indent|'            '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'tell_value'
op|'='
number|'0'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'already_read'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'seeks'
op|'='
op|'['
op|']'
newline|'\n'
name|'self'
op|'.'
name|'tell_value'
op|'='
name|'tell_value'
newline|'\n'
nl|'\n'
DECL|member|tell
dedent|''
name|'def'
name|'tell'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'self'
op|'.'
name|'tell_value'
newline|'\n'
nl|'\n'
DECL|member|seek
dedent|''
name|'def'
name|'seek'
op|'('
name|'self'
op|','
name|'position'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'seeks'
op|'.'
name|'append'
op|'('
name|'position'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'already_read'
op|'='
name|'False'
newline|'\n'
nl|'\n'
DECL|member|read
dedent|''
name|'def'
name|'read'
op|'('
name|'self'
op|','
name|'size'
op|'='
op|'-'
number|'1'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'self'
op|'.'
name|'already_read'
op|':'
newline|'\n'
indent|'                    '
name|'return'
string|"''"
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'already_read'
op|'='
name|'True'
newline|'\n'
name|'return'
string|"'abcdef'"
newline|'\n'
nl|'\n'
DECL|class|LocalConnection
dedent|''
dedent|''
dedent|''
name|'class'
name|'LocalConnection'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|putrequest
indent|'            '
name|'def'
name|'putrequest'
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
indent|'                '
name|'return'
newline|'\n'
nl|'\n'
DECL|member|putheader
dedent|''
name|'def'
name|'putheader'
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
indent|'                '
name|'return'
newline|'\n'
nl|'\n'
DECL|member|endheaders
dedent|''
name|'def'
name|'endheaders'
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
indent|'                '
name|'return'
newline|'\n'
nl|'\n'
DECL|member|send
dedent|''
name|'def'
name|'send'
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
indent|'                '
name|'raise'
name|'socket'
op|'.'
name|'error'
op|'('
string|"'oops'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|request
dedent|''
name|'def'
name|'request'
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
indent|'                '
name|'return'
newline|'\n'
nl|'\n'
DECL|member|getresponse
dedent|''
name|'def'
name|'getresponse'
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
indent|'                '
name|'self'
op|'.'
name|'status'
op|'='
number|'200'
newline|'\n'
name|'return'
name|'self'
newline|'\n'
nl|'\n'
DECL|member|getheader
dedent|''
name|'def'
name|'getheader'
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
indent|'                '
name|'return'
string|"''"
newline|'\n'
nl|'\n'
DECL|member|read
dedent|''
name|'def'
name|'read'
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
indent|'                '
name|'return'
string|"''"
newline|'\n'
nl|'\n'
DECL|function|local_http_connection
dedent|''
dedent|''
name|'def'
name|'local_http_connection'
op|'('
name|'url'
op|','
name|'proxy'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'parsed'
op|'='
name|'urlparse'
op|'('
name|'url'
op|')'
newline|'\n'
name|'return'
name|'parsed'
op|','
name|'LocalConnection'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'orig_conn'
op|'='
name|'c'
op|'.'
name|'http_connection'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'local_http_connection'
newline|'\n'
name|'conn'
op|'='
name|'c'
op|'.'
name|'Connection'
op|'('
string|"'http://www.example.com'"
op|','
string|"'asdf'"
op|','
string|"'asdf'"
op|','
nl|'\n'
name|'retries'
op|'='
number|'1'
op|','
name|'starting_backoff'
op|'='
number|'.0001'
op|')'
newline|'\n'
nl|'\n'
name|'contents'
op|'='
name|'LocalContents'
op|'('
op|')'
newline|'\n'
name|'exc'
op|'='
name|'None'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'conn'
op|'.'
name|'put_object'
op|'('
string|"'c'"
op|','
string|"'o'"
op|','
name|'contents'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'socket'
op|'.'
name|'error'
op|','
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'exc'
op|'='
name|'err'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'contents'
op|'.'
name|'seeks'
op|','
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'str'
op|'('
name|'exc'
op|')'
op|','
string|"'oops'"
op|')'
newline|'\n'
nl|'\n'
name|'contents'
op|'='
name|'LocalContents'
op|'('
name|'tell_value'
op|'='
number|'123'
op|')'
newline|'\n'
name|'exc'
op|'='
name|'None'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'conn'
op|'.'
name|'put_object'
op|'('
string|"'c'"
op|','
string|"'o'"
op|','
name|'contents'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'socket'
op|'.'
name|'error'
op|','
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'exc'
op|'='
name|'err'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'contents'
op|'.'
name|'seeks'
op|','
op|'['
number|'123'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'str'
op|'('
name|'exc'
op|')'
op|','
string|"'oops'"
op|')'
newline|'\n'
nl|'\n'
name|'contents'
op|'='
name|'LocalContents'
op|'('
op|')'
newline|'\n'
name|'contents'
op|'.'
name|'tell'
op|'='
name|'None'
newline|'\n'
name|'exc'
op|'='
name|'None'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'conn'
op|'.'
name|'put_object'
op|'('
string|"'c'"
op|','
string|"'o'"
op|','
name|'contents'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'c'
op|'.'
name|'ClientException'
op|','
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'exc'
op|'='
name|'err'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'contents'
op|'.'
name|'seeks'
op|','
op|'['
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'str'
op|'('
name|'exc'
op|')'
op|','
string|'"put_object(\'c\', \'o\', ...) failure "'
nl|'\n'
string|'"and no ability to reset contents for reupload."'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'c'
op|'.'
name|'http_connection'
op|'='
name|'orig_conn'
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
