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
string|'""" Tests for swift.common.utils """'
newline|'\n'
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
name|'mimetools'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'socket'
newline|'\n'
name|'import'
name|'sys'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'from'
name|'getpass'
name|'import'
name|'getuser'
newline|'\n'
name|'from'
name|'shutil'
name|'import'
name|'rmtree'
newline|'\n'
name|'from'
name|'StringIO'
name|'import'
name|'StringIO'
newline|'\n'
name|'from'
name|'collections'
name|'import'
name|'defaultdict'
newline|'\n'
name|'from'
name|'urllib'
name|'import'
name|'quote'
newline|'\n'
nl|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'sleep'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'Request'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'wsgi'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestWSGI
name|'class'
name|'TestWSGI'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'""" Tests for swift.common.wsgi """'
newline|'\n'
nl|'\n'
DECL|member|test_monkey_patch_mimetools
name|'def'
name|'test_monkey_patch_mimetools'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'sio'
op|'='
name|'StringIO'
op|'('
string|"'blah'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mimetools'
op|'.'
name|'Message'
op|'('
name|'sio'
op|')'
op|'.'
name|'type'
op|','
string|"'text/plain'"
op|')'
newline|'\n'
name|'sio'
op|'='
name|'StringIO'
op|'('
string|"'blah'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mimetools'
op|'.'
name|'Message'
op|'('
name|'sio'
op|')'
op|'.'
name|'plisttext'
op|','
string|"''"
op|')'
newline|'\n'
name|'sio'
op|'='
name|'StringIO'
op|'('
string|"'blah'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mimetools'
op|'.'
name|'Message'
op|'('
name|'sio'
op|')'
op|'.'
name|'maintype'
op|','
string|"'text'"
op|')'
newline|'\n'
name|'sio'
op|'='
name|'StringIO'
op|'('
string|"'blah'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mimetools'
op|'.'
name|'Message'
op|'('
name|'sio'
op|')'
op|'.'
name|'subtype'
op|','
string|"'plain'"
op|')'
newline|'\n'
name|'sio'
op|'='
name|'StringIO'
op|'('
string|"'Content-Type: text/html; charset=ISO-8859-4'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mimetools'
op|'.'
name|'Message'
op|'('
name|'sio'
op|')'
op|'.'
name|'type'
op|','
string|"'text/html'"
op|')'
newline|'\n'
name|'sio'
op|'='
name|'StringIO'
op|'('
string|"'Content-Type: text/html; charset=ISO-8859-4'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mimetools'
op|'.'
name|'Message'
op|'('
name|'sio'
op|')'
op|'.'
name|'plisttext'
op|','
nl|'\n'
string|"'; charset=ISO-8859-4'"
op|')'
newline|'\n'
name|'sio'
op|'='
name|'StringIO'
op|'('
string|"'Content-Type: text/html; charset=ISO-8859-4'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mimetools'
op|'.'
name|'Message'
op|'('
name|'sio'
op|')'
op|'.'
name|'maintype'
op|','
string|"'text'"
op|')'
newline|'\n'
name|'sio'
op|'='
name|'StringIO'
op|'('
string|"'Content-Type: text/html; charset=ISO-8859-4'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mimetools'
op|'.'
name|'Message'
op|'('
name|'sio'
op|')'
op|'.'
name|'subtype'
op|','
string|"'html'"
op|')'
newline|'\n'
nl|'\n'
name|'wsgi'
op|'.'
name|'monkey_patch_mimetools'
op|'('
op|')'
newline|'\n'
name|'sio'
op|'='
name|'StringIO'
op|'('
string|"'blah'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mimetools'
op|'.'
name|'Message'
op|'('
name|'sio'
op|')'
op|'.'
name|'type'
op|','
name|'None'
op|')'
newline|'\n'
name|'sio'
op|'='
name|'StringIO'
op|'('
string|"'blah'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mimetools'
op|'.'
name|'Message'
op|'('
name|'sio'
op|')'
op|'.'
name|'plisttext'
op|','
string|"''"
op|')'
newline|'\n'
name|'sio'
op|'='
name|'StringIO'
op|'('
string|"'blah'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mimetools'
op|'.'
name|'Message'
op|'('
name|'sio'
op|')'
op|'.'
name|'maintype'
op|','
name|'None'
op|')'
newline|'\n'
name|'sio'
op|'='
name|'StringIO'
op|'('
string|"'blah'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mimetools'
op|'.'
name|'Message'
op|'('
name|'sio'
op|')'
op|'.'
name|'subtype'
op|','
name|'None'
op|')'
newline|'\n'
name|'sio'
op|'='
name|'StringIO'
op|'('
string|"'Content-Type: text/html; charset=ISO-8859-4'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mimetools'
op|'.'
name|'Message'
op|'('
name|'sio'
op|')'
op|'.'
name|'type'
op|','
string|"'text/html'"
op|')'
newline|'\n'
name|'sio'
op|'='
name|'StringIO'
op|'('
string|"'Content-Type: text/html; charset=ISO-8859-4'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mimetools'
op|'.'
name|'Message'
op|'('
name|'sio'
op|')'
op|'.'
name|'plisttext'
op|','
nl|'\n'
string|"'; charset=ISO-8859-4'"
op|')'
newline|'\n'
name|'sio'
op|'='
name|'StringIO'
op|'('
string|"'Content-Type: text/html; charset=ISO-8859-4'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mimetools'
op|'.'
name|'Message'
op|'('
name|'sio'
op|')'
op|'.'
name|'maintype'
op|','
string|"'text'"
op|')'
newline|'\n'
name|'sio'
op|'='
name|'StringIO'
op|'('
string|"'Content-Type: text/html; charset=ISO-8859-4'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mimetools'
op|'.'
name|'Message'
op|'('
name|'sio'
op|')'
op|'.'
name|'subtype'
op|','
string|"'html'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_socket
dedent|''
name|'def'
name|'test_get_socket'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# stubs'
nl|'\n'
indent|'        '
name|'conf'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'ssl_conf'
op|'='
op|'{'
nl|'\n'
string|"'cert_file'"
op|':'
string|"''"
op|','
nl|'\n'
string|"'key_file'"
op|':'
string|"''"
op|','
nl|'\n'
op|'}'
newline|'\n'
nl|'\n'
comment|'# mocks'
nl|'\n'
DECL|class|MockSocket
name|'class'
name|'MockSocket'
op|'('
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'            '
name|'def'
name|'__init__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'opts'
op|'='
name|'defaultdict'
op|'('
name|'dict'
op|')'
newline|'\n'
nl|'\n'
DECL|member|setsockopt
dedent|''
name|'def'
name|'setsockopt'
op|'('
name|'self'
op|','
name|'level'
op|','
name|'optname'
op|','
name|'value'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'opts'
op|'['
name|'level'
op|']'
op|'['
name|'optname'
op|']'
op|'='
name|'value'
newline|'\n'
nl|'\n'
DECL|function|mock_listen
dedent|''
dedent|''
name|'def'
name|'mock_listen'
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
name|'MockSocket'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|class|MockSsl
dedent|''
name|'class'
name|'MockSsl'
op|'('
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'            '
name|'def'
name|'__init__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'wrap_socket_called'
op|'='
op|'['
op|']'
newline|'\n'
nl|'\n'
DECL|member|wrap_socket
dedent|''
name|'def'
name|'wrap_socket'
op|'('
name|'self'
op|','
name|'sock'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'wrap_socket_called'
op|'.'
name|'append'
op|'('
name|'kwargs'
op|')'
newline|'\n'
name|'return'
name|'sock'
newline|'\n'
nl|'\n'
comment|'# patch'
nl|'\n'
dedent|''
dedent|''
name|'old_listen'
op|'='
name|'wsgi'
op|'.'
name|'listen'
newline|'\n'
name|'old_ssl'
op|'='
name|'wsgi'
op|'.'
name|'ssl'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'wsgi'
op|'.'
name|'listen'
op|'='
name|'mock_listen'
newline|'\n'
name|'wsgi'
op|'.'
name|'ssl'
op|'='
name|'MockSsl'
op|'('
op|')'
newline|'\n'
comment|'# test'
nl|'\n'
DECL|variable|sock
name|'sock'
op|'='
name|'wsgi'
op|'.'
name|'get_socket'
op|'('
name|'conf'
op|')'
newline|'\n'
comment|'# assert'
nl|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'isinstance'
op|'('
name|'sock'
op|','
name|'MockSocket'
op|')'
op|')'
newline|'\n'
DECL|variable|expected_socket_opts
name|'expected_socket_opts'
op|'='
op|'{'
nl|'\n'
name|'socket'
op|'.'
name|'SOL_SOCKET'
op|':'
op|'{'
nl|'\n'
name|'socket'
op|'.'
name|'SO_REUSEADDR'
op|':'
number|'1'
op|','
nl|'\n'
name|'socket'
op|'.'
name|'SO_KEEPALIVE'
op|':'
number|'1'
op|','
nl|'\n'
op|'}'
op|','
nl|'\n'
name|'socket'
op|'.'
name|'IPPROTO_TCP'
op|':'
op|'{'
nl|'\n'
name|'socket'
op|'.'
name|'TCP_KEEPIDLE'
op|':'
number|'600'
op|','
nl|'\n'
op|'}'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'sock'
op|'.'
name|'opts'
op|','
name|'expected_socket_opts'
op|')'
newline|'\n'
comment|'# test ssl'
nl|'\n'
DECL|variable|sock
name|'sock'
op|'='
name|'wsgi'
op|'.'
name|'get_socket'
op|'('
name|'ssl_conf'
op|')'
newline|'\n'
DECL|variable|expected_kwargs
name|'expected_kwargs'
op|'='
op|'{'
nl|'\n'
string|"'certfile'"
op|':'
string|"''"
op|','
nl|'\n'
string|"'keyfile'"
op|':'
string|"''"
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'wsgi'
op|'.'
name|'ssl'
op|'.'
name|'wrap_socket_called'
op|','
op|'['
name|'expected_kwargs'
op|']'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'wsgi'
op|'.'
name|'listen'
op|'='
name|'old_listen'
newline|'\n'
name|'wsgi'
op|'.'
name|'ssl'
op|'='
name|'old_ssl'
newline|'\n'
nl|'\n'
DECL|member|test_address_in_use
dedent|''
dedent|''
name|'def'
name|'test_address_in_use'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# stubs'
nl|'\n'
indent|'        '
name|'conf'
op|'='
op|'{'
op|'}'
newline|'\n'
nl|'\n'
comment|'# mocks'
nl|'\n'
DECL|function|mock_listen
name|'def'
name|'mock_listen'
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
name|'raise'
name|'socket'
op|'.'
name|'error'
op|'('
name|'errno'
op|'.'
name|'EADDRINUSE'
op|')'
newline|'\n'
nl|'\n'
DECL|function|value_error_listen
dedent|''
name|'def'
name|'value_error_listen'
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
name|'raise'
name|'ValueError'
op|'('
string|"'fake'"
op|')'
newline|'\n'
nl|'\n'
DECL|function|mock_sleep
dedent|''
name|'def'
name|'mock_sleep'
op|'('
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
nl|'\n'
DECL|class|MockTime
dedent|''
name|'class'
name|'MockTime'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
string|'"""Fast clock advances 10 seconds after every call to time\n            """'
newline|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'current_time'
op|'='
name|'old_time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|time
dedent|''
name|'def'
name|'time'
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
name|'rv'
op|'='
name|'self'
op|'.'
name|'current_time'
newline|'\n'
comment|'# advance for next call'
nl|'\n'
name|'self'
op|'.'
name|'current_time'
op|'+='
number|'10'
newline|'\n'
name|'return'
name|'rv'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'old_listen'
op|'='
name|'wsgi'
op|'.'
name|'listen'
newline|'\n'
name|'old_sleep'
op|'='
name|'wsgi'
op|'.'
name|'sleep'
newline|'\n'
name|'old_time'
op|'='
name|'wsgi'
op|'.'
name|'time'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'wsgi'
op|'.'
name|'listen'
op|'='
name|'mock_listen'
newline|'\n'
name|'wsgi'
op|'.'
name|'sleep'
op|'='
name|'mock_sleep'
newline|'\n'
name|'wsgi'
op|'.'
name|'time'
op|'='
name|'MockTime'
op|'('
op|')'
newline|'\n'
comment|'# test error'
nl|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'Exception'
op|','
name|'wsgi'
op|'.'
name|'get_socket'
op|','
name|'conf'
op|')'
newline|'\n'
comment|'# different error'
nl|'\n'
name|'wsgi'
op|'.'
name|'listen'
op|'='
name|'value_error_listen'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'ValueError'
op|','
name|'wsgi'
op|'.'
name|'get_socket'
op|','
name|'conf'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'wsgi'
op|'.'
name|'listen'
op|'='
name|'old_listen'
newline|'\n'
name|'wsgi'
op|'.'
name|'sleep'
op|'='
name|'old_sleep'
newline|'\n'
name|'wsgi'
op|'.'
name|'time'
op|'='
name|'old_time'
newline|'\n'
nl|'\n'
DECL|member|test_pre_auth_wsgi_input
dedent|''
dedent|''
name|'def'
name|'test_pre_auth_wsgi_input'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'oldenv'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'newenv'
op|'='
name|'wsgi'
op|'.'
name|'make_pre_authed_env'
op|'('
name|'oldenv'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'wsgi.input'"
name|'in'
name|'newenv'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'newenv'
op|'['
string|"'wsgi.input'"
op|']'
op|'.'
name|'read'
op|'('
op|')'
op|','
string|"''"
op|')'
newline|'\n'
nl|'\n'
name|'oldenv'
op|'='
op|'{'
string|"'wsgi.input'"
op|':'
name|'StringIO'
op|'('
string|"'original wsgi.input'"
op|')'
op|'}'
newline|'\n'
name|'newenv'
op|'='
name|'wsgi'
op|'.'
name|'make_pre_authed_env'
op|'('
name|'oldenv'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'wsgi.input'"
name|'in'
name|'newenv'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'newenv'
op|'['
string|"'wsgi.input'"
op|']'
op|'.'
name|'read'
op|'('
op|')'
op|','
string|"''"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_pre_auth_req
dedent|''
name|'def'
name|'test_pre_auth_req'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
DECL|class|FakeReq
indent|'        '
name|'class'
name|'FakeReq'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'            '
op|'@'
name|'classmethod'
newline|'\n'
DECL|member|fake_blank
name|'def'
name|'fake_blank'
op|'('
name|'cls'
op|','
name|'path'
op|','
name|'environ'
op|'='
op|'{'
op|'}'
op|','
name|'body'
op|'='
string|"''"
op|','
name|'headers'
op|'='
op|'{'
op|'}'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'environ'
op|'['
string|"'swift.authorize'"
op|']'
op|'('
string|"'test'"
op|')'
op|','
name|'None'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertFalse'
op|'('
string|"'HTTP_X_TRANS_ID'"
name|'in'
name|'environ'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'was_blank'
op|'='
name|'Request'
op|'.'
name|'blank'
newline|'\n'
name|'Request'
op|'.'
name|'blank'
op|'='
name|'FakeReq'
op|'.'
name|'fake_blank'
newline|'\n'
name|'wsgi'
op|'.'
name|'make_pre_authed_request'
op|'('
op|'{'
string|"'HTTP_X_TRANS_ID'"
op|':'
string|"'1234'"
op|'}'
op|','
nl|'\n'
string|"'PUT'"
op|','
string|"'/'"
op|','
name|'body'
op|'='
string|"'tester'"
op|','
name|'headers'
op|'='
op|'{'
op|'}'
op|')'
newline|'\n'
name|'wsgi'
op|'.'
name|'make_pre_authed_request'
op|'('
op|'{'
string|"'HTTP_X_TRANS_ID'"
op|':'
string|"'1234'"
op|'}'
op|','
nl|'\n'
string|"'PUT'"
op|','
string|"'/'"
op|','
name|'headers'
op|'='
op|'{'
op|'}'
op|')'
newline|'\n'
name|'Request'
op|'.'
name|'blank'
op|'='
name|'was_blank'
newline|'\n'
nl|'\n'
DECL|member|test_pre_auth_req_with_quoted_path
dedent|''
name|'def'
name|'test_pre_auth_req_with_quoted_path'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'r'
op|'='
name|'wsgi'
op|'.'
name|'make_pre_authed_request'
op|'('
nl|'\n'
op|'{'
string|"'HTTP_X_TRANS_ID'"
op|':'
string|"'1234'"
op|'}'
op|','
string|"'PUT'"
op|','
name|'path'
op|'='
name|'quote'
op|'('
string|"'/a space'"
op|')'
op|','
nl|'\n'
name|'body'
op|'='
string|"'tester'"
op|','
name|'headers'
op|'='
op|'{'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'r'
op|'.'
name|'path'
op|','
name|'quote'
op|'('
string|"'/a space'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_pre_auth_req_drops_query
dedent|''
name|'def'
name|'test_pre_auth_req_drops_query'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'r'
op|'='
name|'wsgi'
op|'.'
name|'make_pre_authed_request'
op|'('
nl|'\n'
op|'{'
string|"'QUERY_STRING'"
op|':'
string|"'original'"
op|'}'
op|','
string|"'GET'"
op|','
string|"'path'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'r'
op|'.'
name|'query_string'
op|','
string|"'original'"
op|')'
newline|'\n'
name|'r'
op|'='
name|'wsgi'
op|'.'
name|'make_pre_authed_request'
op|'('
nl|'\n'
op|'{'
string|"'QUERY_STRING'"
op|':'
string|"'original'"
op|'}'
op|','
string|"'GET'"
op|','
string|"'path?replacement'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'r'
op|'.'
name|'query_string'
op|','
string|"'replacement'"
op|')'
newline|'\n'
name|'r'
op|'='
name|'wsgi'
op|'.'
name|'make_pre_authed_request'
op|'('
nl|'\n'
op|'{'
string|"'QUERY_STRING'"
op|':'
string|"'original'"
op|'}'
op|','
string|"'GET'"
op|','
string|"'path?'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'r'
op|'.'
name|'query_string'
op|','
string|"''"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_pre_auth_req_with_body
dedent|''
name|'def'
name|'test_pre_auth_req_with_body'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'r'
op|'='
name|'wsgi'
op|'.'
name|'make_pre_authed_request'
op|'('
nl|'\n'
op|'{'
string|"'QUERY_STRING'"
op|':'
string|"'original'"
op|'}'
op|','
string|"'GET'"
op|','
string|"'path'"
op|','
string|"'the body'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'r'
op|'.'
name|'body'
op|','
string|"'the body'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_pre_auth_creates_script_name
dedent|''
name|'def'
name|'test_pre_auth_creates_script_name'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'e'
op|'='
name|'wsgi'
op|'.'
name|'make_pre_authed_env'
op|'('
op|'{'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'SCRIPT_NAME'"
name|'in'
name|'e'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_pre_auth_copies_script_name
dedent|''
name|'def'
name|'test_pre_auth_copies_script_name'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'e'
op|'='
name|'wsgi'
op|'.'
name|'make_pre_authed_env'
op|'('
op|'{'
string|"'SCRIPT_NAME'"
op|':'
string|"'/script_name'"
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'e'
op|'['
string|"'SCRIPT_NAME'"
op|']'
op|','
string|"'/script_name'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_pre_auth_copies_script_name_unless_path_overridden
dedent|''
name|'def'
name|'test_pre_auth_copies_script_name_unless_path_overridden'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'e'
op|'='
name|'wsgi'
op|'.'
name|'make_pre_authed_env'
op|'('
op|'{'
string|"'SCRIPT_NAME'"
op|':'
string|"'/script_name'"
op|'}'
op|','
nl|'\n'
name|'path'
op|'='
string|"'/override'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'e'
op|'['
string|"'SCRIPT_NAME'"
op|']'
op|','
string|"''"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'e'
op|'['
string|"'PATH_INFO'"
op|']'
op|','
string|"'/override'"
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
