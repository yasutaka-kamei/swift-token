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
comment|'# TODO: More tests'
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
name|'client'
name|'as'
name|'c'
newline|'\n'
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
name|'_'
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
name|'_'
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
comment|'# that was easy'
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
DECL|member|test_no_json
dedent|''
dedent|''
name|'def'
name|'test_no_json'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# first break simplejson'
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
comment|'# that was easy'
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
nl|'\n'
comment|'# then break json'
nl|'\n'
dedent|''
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
comment|'# that was easy'
nl|'\n'
indent|'            '
name|'_orig_dumps'
op|'='
name|'None'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'_orig_dumps'
op|'='
name|'json'
op|'.'
name|'dumps'
newline|'\n'
name|'delattr'
op|'('
name|'json'
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
name|'if'
name|'_orig_dumps'
op|':'
newline|'\n'
comment|'# thank goodness'
nl|'\n'
indent|'            '
name|'data'
op|'='
op|'{'
nl|'\n'
string|"'string'"
op|':'
string|"'value'"
op|','
nl|'\n'
string|"'int'"
op|':'
number|'0'
op|','
nl|'\n'
string|"'bool'"
op|':'
name|'True'
op|','
nl|'\n'
string|"'none'"
op|':'
name|'None'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'json_string'
op|'='
name|'_orig_dumps'
op|'('
name|'data'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
comment|'# wow, I guess we really need this thing...'
nl|'\n'
indent|'            '
name|'data'
op|'='
op|'['
string|"'value1'"
op|','
string|"'value2'"
op|']'
newline|'\n'
name|'json_string'
op|'='
string|'"[\'value1\', \'value2\']"'
newline|'\n'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'data'
op|','
name|'c'
op|'.'
name|'json_loads'
op|'('
name|'json_string'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'AttributeError'
op|','
name|'c'
op|'.'
name|'json_loads'
op|','
name|'self'
op|')'
newline|'\n'
nl|'\n'
DECL|class|MockHttpTest
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
comment|'# Yoink!'
nl|'\n'
indent|'        '
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
comment|'# TODO: mock http connection class with more control over headers'
nl|'\n'
DECL|function|fake_http_connection
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
DECL|function|wrapper
name|'def'
name|'wrapper'
op|'('
name|'url'
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
comment|'# TODO: following tests cases are placeholders, need more tests, better coverage'
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
name|'head_account'
op|','
nl|'\n'
string|"'http://www.tests.com'"
op|','
string|"'asdf'"
op|')'
newline|'\n'
nl|'\n'
DECL|class|TestGetContainer
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
nl|'\n'
DECL|class|TestPutContainer
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
DECL|class|TestDeleteContainer
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
name|'value'
op|'='
name|'c'
op|'.'
name|'put_object'
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
name|'put_object'
op|','
nl|'\n'
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
nl|'\n'
DECL|class|TestPostObject
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
name|'value'
op|'='
name|'c'
op|'.'
name|'post_object'
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
name|'post_object'
op|','
nl|'\n'
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
nl|'\n'
DECL|class|TestDeleteObject
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
