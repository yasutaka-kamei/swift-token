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
name|'from'
name|'__future__'
name|'import'
name|'with_statement'
newline|'\n'
name|'import'
name|'logging'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'sys'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'from'
name|'contextlib'
name|'import'
name|'contextmanager'
newline|'\n'
nl|'\n'
name|'import'
name|'eventlet'
newline|'\n'
name|'from'
name|'webob'
name|'import'
name|'Request'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'middleware'
name|'import'
name|'auth'
newline|'\n'
nl|'\n'
comment|'# mocks'
nl|'\n'
name|'logging'
op|'.'
name|'getLogger'
op|'('
op|')'
op|'.'
name|'addHandler'
op|'('
name|'logging'
op|'.'
name|'StreamHandler'
op|'('
name|'sys'
op|'.'
name|'stdout'
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FakeMemcache
name|'class'
name|'FakeMemcache'
op|'('
name|'object'
op|')'
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
name|'store'
op|'='
op|'{'
op|'}'
newline|'\n'
nl|'\n'
DECL|member|get
dedent|''
name|'def'
name|'get'
op|'('
name|'self'
op|','
name|'key'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'self'
op|'.'
name|'store'
op|'.'
name|'get'
op|'('
name|'key'
op|')'
newline|'\n'
nl|'\n'
DECL|member|set
dedent|''
name|'def'
name|'set'
op|'('
name|'self'
op|','
name|'key'
op|','
name|'value'
op|','
name|'timeout'
op|'='
number|'0'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'store'
op|'['
name|'key'
op|']'
op|'='
name|'value'
newline|'\n'
name|'return'
name|'True'
newline|'\n'
nl|'\n'
DECL|member|incr
dedent|''
name|'def'
name|'incr'
op|'('
name|'self'
op|','
name|'key'
op|','
name|'timeout'
op|'='
number|'0'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'store'
op|'['
name|'key'
op|']'
op|'='
name|'self'
op|'.'
name|'store'
op|'.'
name|'setdefault'
op|'('
name|'key'
op|','
number|'0'
op|')'
op|'+'
number|'1'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'store'
op|'['
name|'key'
op|']'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'contextmanager'
newline|'\n'
DECL|member|soft_lock
name|'def'
name|'soft_lock'
op|'('
name|'self'
op|','
name|'key'
op|','
name|'timeout'
op|'='
number|'0'
op|','
name|'retries'
op|'='
number|'5'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'yield'
name|'True'
newline|'\n'
nl|'\n'
DECL|member|delete
dedent|''
name|'def'
name|'delete'
op|'('
name|'self'
op|','
name|'key'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'del'
name|'self'
op|'.'
name|'store'
op|'['
name|'key'
op|']'
newline|'\n'
dedent|''
name|'except'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'return'
name|'True'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|mock_http_connect
dedent|''
dedent|''
name|'def'
name|'mock_http_connect'
op|'('
name|'response'
op|','
name|'headers'
op|'='
name|'None'
op|','
name|'with_exc'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
DECL|class|FakeConn
indent|'    '
name|'class'
name|'FakeConn'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'        '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'status'
op|','
name|'headers'
op|','
name|'with_exc'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'status'
op|'='
name|'status'
newline|'\n'
name|'self'
op|'.'
name|'reason'
op|'='
string|"'Fake'"
newline|'\n'
name|'self'
op|'.'
name|'host'
op|'='
string|"'1.2.3.4'"
newline|'\n'
name|'self'
op|'.'
name|'port'
op|'='
string|"'1234'"
newline|'\n'
name|'self'
op|'.'
name|'with_exc'
op|'='
name|'with_exc'
newline|'\n'
name|'self'
op|'.'
name|'headers'
op|'='
name|'headers'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'headers'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'headers'
op|'='
op|'{'
op|'}'
newline|'\n'
DECL|member|getresponse
dedent|''
dedent|''
name|'def'
name|'getresponse'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'self'
op|'.'
name|'with_exc'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'Exception'
op|'('
string|"'test'"
op|')'
newline|'\n'
dedent|''
name|'return'
name|'self'
newline|'\n'
DECL|member|getheader
dedent|''
name|'def'
name|'getheader'
op|'('
name|'self'
op|','
name|'header'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'headers'
op|'['
name|'header'
op|']'
newline|'\n'
DECL|member|read
dedent|''
name|'def'
name|'read'
op|'('
name|'self'
op|','
name|'amt'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
string|"''"
newline|'\n'
DECL|member|close
dedent|''
name|'def'
name|'close'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'lambda'
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|':'
name|'FakeConn'
op|'('
name|'response'
op|','
name|'headers'
op|','
name|'with_exc'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|Logger
dedent|''
name|'class'
name|'Logger'
op|'('
name|'object'
op|')'
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
name|'error_value'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'exception_value'
op|'='
name|'None'
newline|'\n'
DECL|member|error
dedent|''
name|'def'
name|'error'
op|'('
name|'self'
op|','
name|'msg'
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
name|'error_value'
op|'='
op|'('
name|'msg'
op|','
name|'args'
op|','
name|'kwargs'
op|')'
newline|'\n'
DECL|member|exception
dedent|''
name|'def'
name|'exception'
op|'('
name|'self'
op|','
name|'msg'
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
name|'_'
op|','
name|'exc'
op|','
name|'_'
op|'='
name|'sys'
op|'.'
name|'exc_info'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'exception_value'
op|'='
op|'('
name|'msg'
op|','
nl|'\n'
string|"'%s %s'"
op|'%'
op|'('
name|'exc'
op|'.'
name|'__class__'
op|'.'
name|'__name__'
op|','
name|'str'
op|'('
name|'exc'
op|')'
op|')'
op|','
name|'args'
op|','
name|'kwargs'
op|')'
newline|'\n'
comment|'# tests'
nl|'\n'
nl|'\n'
DECL|class|FakeApp
dedent|''
dedent|''
name|'class'
name|'FakeApp'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|__call__
indent|'    '
name|'def'
name|'__call__'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
op|'['
string|"'204 No Content'"
op|']'
newline|'\n'
nl|'\n'
DECL|function|start_response
dedent|''
dedent|''
name|'def'
name|'start_response'
op|'('
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
DECL|class|TestAuth
dedent|''
name|'class'
name|'TestAuth'
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
name|'test_auth'
op|'='
name|'auth'
op|'.'
name|'filter_factory'
op|'('
op|'{'
op|'}'
op|')'
op|'('
name|'FakeApp'
op|'('
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_auth_fail
dedent|''
name|'def'
name|'test_auth_fail'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'old_http_connect'
op|'='
name|'auth'
op|'.'
name|'http_connect'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'auth'
op|'.'
name|'http_connect'
op|'='
name|'mock_http_connect'
op|'('
number|'404'
op|')'
newline|'\n'
name|'result'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'('
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'HTTP_X_AUTH_TOKEN'"
op|':'
string|"'AUTH_t'"
op|','
string|"'swift.cache'"
op|':'
name|'FakeMemcache'
op|'('
op|')'
op|'}'
op|','
nl|'\n'
name|'lambda'
name|'x'
op|','
name|'y'
op|':'
name|'None'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'result'
op|'.'
name|'startswith'
op|'('
string|"'401'"
op|')'
op|','
name|'result'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'auth'
op|'.'
name|'http_connect'
op|'='
name|'old_http_connect'
newline|'\n'
nl|'\n'
DECL|member|test_auth_success
dedent|''
dedent|''
name|'def'
name|'test_auth_success'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'old_http_connect'
op|'='
name|'auth'
op|'.'
name|'http_connect'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'auth'
op|'.'
name|'http_connect'
op|'='
name|'mock_http_connect'
op|'('
number|'204'
op|','
nl|'\n'
op|'{'
string|"'x-auth-ttl'"
op|':'
string|"'1234'"
op|','
string|"'x-auth-groups'"
op|':'
string|"'act:usr,act,AUTH_cfa'"
op|'}'
op|')'
newline|'\n'
name|'result'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'('
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'HTTP_X_AUTH_TOKEN'"
op|':'
string|"'AUTH_t'"
op|','
string|"'swift.cache'"
op|':'
name|'FakeMemcache'
op|'('
op|')'
op|'}'
op|','
nl|'\n'
name|'lambda'
name|'x'
op|','
name|'y'
op|':'
name|'None'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'result'
op|'.'
name|'startswith'
op|'('
string|"'204'"
op|')'
op|','
name|'result'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'auth'
op|'.'
name|'http_connect'
op|'='
name|'old_http_connect'
newline|'\n'
nl|'\n'
DECL|member|test_auth_memcache
dedent|''
dedent|''
name|'def'
name|'test_auth_memcache'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'old_http_connect'
op|'='
name|'auth'
op|'.'
name|'http_connect'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'fake_memcache'
op|'='
name|'FakeMemcache'
op|'('
op|')'
newline|'\n'
name|'auth'
op|'.'
name|'http_connect'
op|'='
name|'mock_http_connect'
op|'('
number|'204'
op|','
nl|'\n'
op|'{'
string|"'x-auth-ttl'"
op|':'
string|"'1234'"
op|','
string|"'x-auth-groups'"
op|':'
string|"'act:usr,act,AUTH_cfa'"
op|'}'
op|')'
newline|'\n'
name|'result'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'('
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'HTTP_X_AUTH_TOKEN'"
op|':'
string|"'AUTH_t'"
op|','
string|"'swift.cache'"
op|':'
name|'fake_memcache'
op|'}'
op|','
nl|'\n'
name|'lambda'
name|'x'
op|','
name|'y'
op|':'
name|'None'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'result'
op|'.'
name|'startswith'
op|'('
string|"'204'"
op|')'
op|','
name|'result'
op|')'
newline|'\n'
name|'auth'
op|'.'
name|'http_connect'
op|'='
name|'mock_http_connect'
op|'('
number|'404'
op|')'
newline|'\n'
comment|'# Should still be in memcache'
nl|'\n'
name|'result'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'('
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'HTTP_X_AUTH_TOKEN'"
op|':'
string|"'AUTH_t'"
op|','
string|"'swift.cache'"
op|':'
name|'fake_memcache'
op|'}'
op|','
nl|'\n'
name|'lambda'
name|'x'
op|','
name|'y'
op|':'
name|'None'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'result'
op|'.'
name|'startswith'
op|'('
string|"'204'"
op|')'
op|','
name|'result'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'auth'
op|'.'
name|'http_connect'
op|'='
name|'old_http_connect'
newline|'\n'
nl|'\n'
DECL|member|test_auth_just_expired
dedent|''
dedent|''
name|'def'
name|'test_auth_just_expired'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'old_http_connect'
op|'='
name|'auth'
op|'.'
name|'http_connect'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'fake_memcache'
op|'='
name|'FakeMemcache'
op|'('
op|')'
newline|'\n'
name|'auth'
op|'.'
name|'http_connect'
op|'='
name|'mock_http_connect'
op|'('
number|'204'
op|','
nl|'\n'
op|'{'
string|"'x-auth-ttl'"
op|':'
string|"'0'"
op|','
string|"'x-auth-groups'"
op|':'
string|"'act:usr,act,AUTH_cfa'"
op|'}'
op|')'
newline|'\n'
name|'result'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'('
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'HTTP_X_AUTH_TOKEN'"
op|':'
string|"'AUTH_t'"
op|','
string|"'swift.cache'"
op|':'
name|'fake_memcache'
op|'}'
op|','
nl|'\n'
name|'lambda'
name|'x'
op|','
name|'y'
op|':'
name|'None'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'result'
op|'.'
name|'startswith'
op|'('
string|"'204'"
op|')'
op|','
name|'result'
op|')'
newline|'\n'
name|'auth'
op|'.'
name|'http_connect'
op|'='
name|'mock_http_connect'
op|'('
number|'404'
op|')'
newline|'\n'
comment|'# Should still be in memcache, but expired'
nl|'\n'
name|'result'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'('
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'HTTP_X_AUTH_TOKEN'"
op|':'
string|"'AUTH_t'"
op|','
string|"'swift.cache'"
op|':'
name|'fake_memcache'
op|'}'
op|','
nl|'\n'
name|'lambda'
name|'x'
op|','
name|'y'
op|':'
name|'None'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'result'
op|'.'
name|'startswith'
op|'('
string|"'401'"
op|')'
op|','
name|'result'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'auth'
op|'.'
name|'http_connect'
op|'='
name|'old_http_connect'
newline|'\n'
nl|'\n'
DECL|member|test_middleware_success
dedent|''
dedent|''
name|'def'
name|'test_middleware_success'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'old_http_connect'
op|'='
name|'auth'
op|'.'
name|'http_connect'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'auth'
op|'.'
name|'http_connect'
op|'='
name|'mock_http_connect'
op|'('
number|'204'
op|','
nl|'\n'
op|'{'
string|"'x-auth-ttl'"
op|':'
string|"'1234'"
op|','
string|"'x-auth-groups'"
op|':'
string|"'act:usr,act,AUTH_cfa'"
op|'}'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v/a/c/o'"
op|','
name|'headers'
op|'='
op|'{'
string|"'x-auth-token'"
op|':'
string|"'AUTH_t'"
op|'}'
op|')'
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.cache'"
op|']'
op|'='
name|'FakeMemcache'
op|'('
op|')'
newline|'\n'
name|'result'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'result'
op|'.'
name|'startswith'
op|'('
string|"'204'"
op|')'
op|','
name|'result'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'req'
op|'.'
name|'remote_user'
op|','
string|"'act:usr,act,AUTH_cfa'"
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'auth'
op|'.'
name|'http_connect'
op|'='
name|'old_http_connect'
newline|'\n'
nl|'\n'
DECL|member|test_middleware_no_header
dedent|''
dedent|''
name|'def'
name|'test_middleware_no_header'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'old_http_connect'
op|'='
name|'auth'
op|'.'
name|'http_connect'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'auth'
op|'.'
name|'http_connect'
op|'='
name|'mock_http_connect'
op|'('
number|'204'
op|','
nl|'\n'
op|'{'
string|"'x-auth-ttl'"
op|':'
string|"'1234'"
op|','
string|"'x-auth-groups'"
op|':'
string|"'act:usr,act,AUTH_cfa'"
op|'}'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v/a/c/o'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.cache'"
op|']'
op|'='
name|'FakeMemcache'
op|'('
op|')'
newline|'\n'
name|'result'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'result'
op|'.'
name|'startswith'
op|'('
string|"'204'"
op|')'
op|','
name|'result'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'not'
name|'req'
op|'.'
name|'remote_user'
op|','
name|'req'
op|'.'
name|'remote_user'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'auth'
op|'.'
name|'http_connect'
op|'='
name|'old_http_connect'
newline|'\n'
nl|'\n'
DECL|member|test_middleware_storage_token
dedent|''
dedent|''
name|'def'
name|'test_middleware_storage_token'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'old_http_connect'
op|'='
name|'auth'
op|'.'
name|'http_connect'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'auth'
op|'.'
name|'http_connect'
op|'='
name|'mock_http_connect'
op|'('
number|'204'
op|','
nl|'\n'
op|'{'
string|"'x-auth-ttl'"
op|':'
string|"'1234'"
op|','
string|"'x-auth-groups'"
op|':'
string|"'act:usr,act,AUTH_cfa'"
op|'}'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v/a/c/o'"
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'x-storage-token'"
op|':'
string|"'AUTH_t'"
op|'}'
op|')'
newline|'\n'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.cache'"
op|']'
op|'='
name|'FakeMemcache'
op|'('
op|')'
newline|'\n'
name|'result'
op|'='
string|"''"
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'result'
op|'.'
name|'startswith'
op|'('
string|"'204'"
op|')'
op|','
name|'result'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'req'
op|'.'
name|'remote_user'
op|','
string|"'act:usr,act,AUTH_cfa'"
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'auth'
op|'.'
name|'http_connect'
op|'='
name|'old_http_connect'
newline|'\n'
nl|'\n'
DECL|member|test_authorize_bad_path
dedent|''
dedent|''
name|'def'
name|'test_authorize_bad_path'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/badpath'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'str'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'.'
name|'authorize'
op|'('
name|'req'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'startswith'
op|'('
string|"'401'"
op|')'
op|','
name|'resp'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/badpath'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'remote_user'
op|'='
string|"'act:usr,act,AUTH_cfa'"
newline|'\n'
name|'resp'
op|'='
name|'str'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'.'
name|'authorize'
op|'('
name|'req'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'startswith'
op|'('
string|"'403'"
op|')'
op|','
name|'resp'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_authorize_account_access
dedent|''
name|'def'
name|'test_authorize_account_access'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/AUTH_cfa'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'remote_user'
op|'='
string|"'act:usr,act,AUTH_cfa'"
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'.'
name|'authorize'
op|'('
name|'req'
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/AUTH_cfa'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'remote_user'
op|'='
string|"'act:usr,act'"
newline|'\n'
name|'resp'
op|'='
name|'str'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'.'
name|'authorize'
op|'('
name|'req'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'startswith'
op|'('
string|"'403'"
op|')'
op|','
name|'resp'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_authorize_acl_group_access
dedent|''
name|'def'
name|'test_authorize_acl_group_access'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/AUTH_cfa'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'remote_user'
op|'='
string|"'act:usr,act'"
newline|'\n'
name|'resp'
op|'='
name|'str'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'.'
name|'authorize'
op|'('
name|'req'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'startswith'
op|'('
string|"'403'"
op|')'
op|','
name|'resp'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/AUTH_cfa'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'remote_user'
op|'='
string|"'act:usr,act'"
newline|'\n'
name|'req'
op|'.'
name|'acl'
op|'='
string|"'act'"
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'.'
name|'authorize'
op|'('
name|'req'
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/AUTH_cfa'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'remote_user'
op|'='
string|"'act:usr,act'"
newline|'\n'
name|'req'
op|'.'
name|'acl'
op|'='
string|"'act:usr'"
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'.'
name|'authorize'
op|'('
name|'req'
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/AUTH_cfa'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'remote_user'
op|'='
string|"'act:usr,act'"
newline|'\n'
name|'req'
op|'.'
name|'acl'
op|'='
string|"'act2'"
newline|'\n'
name|'resp'
op|'='
name|'str'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'.'
name|'authorize'
op|'('
name|'req'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'startswith'
op|'('
string|"'403'"
op|')'
op|','
name|'resp'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/AUTH_cfa'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'remote_user'
op|'='
string|"'act:usr,act'"
newline|'\n'
name|'req'
op|'.'
name|'acl'
op|'='
string|"'act:usr2'"
newline|'\n'
name|'resp'
op|'='
name|'str'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'.'
name|'authorize'
op|'('
name|'req'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'startswith'
op|'('
string|"'403'"
op|')'
op|','
name|'resp'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_deny_cross_reseller
dedent|''
name|'def'
name|'test_deny_cross_reseller'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# Tests that cross-reseller is denied, even if ACLs/group names match'
nl|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/OTHER_cfa'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'remote_user'
op|'='
string|"'act:usr,act,AUTH_cfa'"
newline|'\n'
name|'req'
op|'.'
name|'acl'
op|'='
string|"'act'"
newline|'\n'
name|'resp'
op|'='
name|'str'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'.'
name|'authorize'
op|'('
name|'req'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'startswith'
op|'('
string|"'403'"
op|')'
op|','
name|'resp'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_authorize_acl_referrer_access
dedent|''
name|'def'
name|'test_authorize_acl_referrer_access'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/AUTH_cfa'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'remote_user'
op|'='
string|"'act:usr,act'"
newline|'\n'
name|'resp'
op|'='
name|'str'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'.'
name|'authorize'
op|'('
name|'req'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'startswith'
op|'('
string|"'403'"
op|')'
op|','
name|'resp'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/AUTH_cfa'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'remote_user'
op|'='
string|"'act:usr,act'"
newline|'\n'
name|'req'
op|'.'
name|'acl'
op|'='
string|"'.r:*'"
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'.'
name|'authorize'
op|'('
name|'req'
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/AUTH_cfa'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'remote_user'
op|'='
string|"'act:usr,act'"
newline|'\n'
name|'req'
op|'.'
name|'acl'
op|'='
string|"'.r:.example.com'"
newline|'\n'
name|'resp'
op|'='
name|'str'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'.'
name|'authorize'
op|'('
name|'req'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'startswith'
op|'('
string|"'403'"
op|')'
op|','
name|'resp'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/AUTH_cfa'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'remote_user'
op|'='
string|"'act:usr,act'"
newline|'\n'
name|'req'
op|'.'
name|'referer'
op|'='
string|"'http://www.example.com/index.html'"
newline|'\n'
name|'req'
op|'.'
name|'acl'
op|'='
string|"'.r:.example.com'"
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'.'
name|'authorize'
op|'('
name|'req'
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/AUTH_cfa'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'str'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'.'
name|'authorize'
op|'('
name|'req'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'startswith'
op|'('
string|"'401'"
op|')'
op|','
name|'resp'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/AUTH_cfa'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'acl'
op|'='
string|"'.r:*'"
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'.'
name|'authorize'
op|'('
name|'req'
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/AUTH_cfa'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'acl'
op|'='
string|"'.r:.example.com'"
newline|'\n'
name|'resp'
op|'='
name|'str'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'.'
name|'authorize'
op|'('
name|'req'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'resp'
op|'.'
name|'startswith'
op|'('
string|"'401'"
op|')'
op|','
name|'resp'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/AUTH_cfa'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'referer'
op|'='
string|"'http://www.example.com/index.html'"
newline|'\n'
name|'req'
op|'.'
name|'acl'
op|'='
string|"'.r:.example.com'"
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'test_auth'
op|'.'
name|'authorize'
op|'('
name|'req'
op|')'
op|','
name|'None'
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
