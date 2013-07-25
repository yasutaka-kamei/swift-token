begin_unit
comment|'#!/usr/bin/python -u'
nl|'\n'
comment|'# Copyright (c) 2010-2013 OpenStack, LLC.'
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
name|'httplib'
newline|'\n'
name|'import'
name|'re'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
nl|'\n'
name|'from'
name|'swiftclient'
name|'import'
name|'get_auth'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'probe'
op|'.'
name|'common'
name|'import'
name|'kill_servers'
op|','
name|'reset_environment'
newline|'\n'
name|'from'
name|'urlparse'
name|'import'
name|'urlparse'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestAccountGetFakeResponsesMatch
name|'class'
name|'TestAccountGetFakeResponsesMatch'
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
op|'('
name|'self'
op|'.'
name|'pids'
op|','
name|'self'
op|'.'
name|'port2server'
op|','
name|'self'
op|'.'
name|'account_ring'
op|','
name|'self'
op|'.'
name|'container_ring'
op|','
nl|'\n'
name|'self'
op|'.'
name|'object_ring'
op|','
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
name|'account'
op|','
name|'self'
op|'.'
name|'configs'
op|')'
op|'='
name|'reset_environment'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|'='
name|'get_auth'
op|'('
nl|'\n'
string|"'http://127.0.0.1:8080/auth/v1.0'"
op|','
string|"'admin:admin'"
op|','
string|"'admin'"
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
name|'kill_servers'
op|'('
name|'self'
op|'.'
name|'port2server'
op|','
name|'self'
op|'.'
name|'pids'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_account_path
dedent|''
name|'def'
name|'_account_path'
op|'('
name|'self'
op|','
name|'account'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'_'
op|','
name|'_'
op|','
name|'path'
op|','
name|'_'
op|','
name|'_'
op|','
name|'_'
op|'='
name|'urlparse'
op|'('
name|'self'
op|'.'
name|'url'
op|')'
newline|'\n'
nl|'\n'
name|'basepath'
op|','
name|'_'
op|'='
name|'path'
op|'.'
name|'rsplit'
op|'('
string|"'/'"
op|','
number|'1'
op|')'
newline|'\n'
name|'return'
name|'basepath'
op|'+'
string|"'/'"
op|'+'
name|'account'
newline|'\n'
nl|'\n'
DECL|member|_get
dedent|''
name|'def'
name|'_get'
op|'('
name|'self'
op|','
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'kw'
op|'['
string|"'method'"
op|']'
op|'='
string|"'GET'"
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'_account_request'
op|'('
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_account_request
dedent|''
name|'def'
name|'_account_request'
op|'('
name|'self'
op|','
name|'account'
op|','
name|'method'
op|','
name|'headers'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'headers'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'headers'
op|'='
op|'{'
op|'}'
newline|'\n'
dedent|''
name|'headers'
op|'['
string|"'X-Auth-Token'"
op|']'
op|'='
name|'self'
op|'.'
name|'token'
newline|'\n'
nl|'\n'
name|'scheme'
op|','
name|'netloc'
op|','
name|'path'
op|','
name|'_'
op|','
name|'_'
op|','
name|'_'
op|'='
name|'urlparse'
op|'('
name|'self'
op|'.'
name|'url'
op|')'
newline|'\n'
name|'host'
op|','
name|'port'
op|'='
name|'netloc'
op|'.'
name|'split'
op|'('
string|"':'"
op|')'
newline|'\n'
name|'port'
op|'='
name|'int'
op|'('
name|'port'
op|')'
newline|'\n'
nl|'\n'
name|'conn'
op|'='
name|'httplib'
op|'.'
name|'HTTPConnection'
op|'('
name|'host'
op|','
name|'port'
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'request'
op|'('
name|'method'
op|','
name|'self'
op|'.'
name|'_account_path'
op|'('
name|'account'
op|')'
op|','
name|'headers'
op|'='
name|'headers'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'conn'
op|'.'
name|'getresponse'
op|'('
op|')'
newline|'\n'
name|'if'
name|'resp'
op|'.'
name|'status'
op|'//'
number|'100'
op|'!='
number|'2'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|'"Unexpected status %s\\n%s"'
op|'%'
nl|'\n'
op|'('
name|'resp'
op|'.'
name|'status'
op|','
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'response_headers'
op|'='
name|'dict'
op|'('
name|'resp'
op|'.'
name|'getheaders'
op|'('
op|')'
op|')'
newline|'\n'
name|'response_body'
op|'='
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
name|'return'
name|'response_headers'
op|','
name|'response_body'
newline|'\n'
nl|'\n'
DECL|member|test_main
dedent|''
name|'def'
name|'test_main'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# Two accounts: "real" and "fake". The fake one doesn\'t have any .db'
nl|'\n'
comment|'# files on disk; the real one does. The real one is empty.'
nl|'\n'
comment|'#'
nl|'\n'
comment|'# Make sure the important response fields match.'
nl|'\n'
nl|'\n'
indent|'        '
name|'real_acct'
op|'='
string|'"AUTH_real"'
newline|'\n'
name|'fake_acct'
op|'='
string|'"AUTH_fake"'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'_account_request'
op|'('
name|'real_acct'
op|','
string|"'POST'"
op|','
nl|'\n'
op|'{'
string|"'X-Account-Meta-Bert'"
op|':'
string|"'Ernie'"
op|'}'
op|')'
newline|'\n'
nl|'\n'
comment|'# text'
nl|'\n'
name|'real_headers'
op|','
name|'real_body'
op|'='
name|'self'
op|'.'
name|'_get'
op|'('
name|'real_acct'
op|')'
newline|'\n'
name|'fake_headers'
op|','
name|'fake_body'
op|'='
name|'self'
op|'.'
name|'_get'
op|'('
name|'fake_acct'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'real_body'
op|','
name|'fake_body'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'real_headers'
op|'['
string|"'content-type'"
op|']'
op|','
nl|'\n'
name|'fake_headers'
op|'['
string|"'content-type'"
op|']'
op|')'
newline|'\n'
nl|'\n'
comment|'# json'
nl|'\n'
name|'real_headers'
op|','
name|'real_body'
op|'='
name|'self'
op|'.'
name|'_get'
op|'('
nl|'\n'
name|'real_acct'
op|','
name|'headers'
op|'='
op|'{'
string|"'Accept'"
op|':'
string|"'application/json'"
op|'}'
op|')'
newline|'\n'
name|'fake_headers'
op|','
name|'fake_body'
op|'='
name|'self'
op|'.'
name|'_get'
op|'('
nl|'\n'
name|'fake_acct'
op|','
name|'headers'
op|'='
op|'{'
string|"'Accept'"
op|':'
string|"'application/json'"
op|'}'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'real_body'
op|','
name|'fake_body'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'real_headers'
op|'['
string|"'content-type'"
op|']'
op|','
nl|'\n'
name|'fake_headers'
op|'['
string|"'content-type'"
op|']'
op|')'
newline|'\n'
nl|'\n'
comment|'# xml'
nl|'\n'
name|'real_headers'
op|','
name|'real_body'
op|'='
name|'self'
op|'.'
name|'_get'
op|'('
nl|'\n'
name|'real_acct'
op|','
name|'headers'
op|'='
op|'{'
string|"'Accept'"
op|':'
string|"'application/xml'"
op|'}'
op|')'
newline|'\n'
name|'fake_headers'
op|','
name|'fake_body'
op|'='
name|'self'
op|'.'
name|'_get'
op|'('
nl|'\n'
name|'fake_acct'
op|','
name|'headers'
op|'='
op|'{'
string|"'Accept'"
op|':'
string|"'application/xml'"
op|'}'
op|')'
newline|'\n'
nl|'\n'
comment|'# the account name is in the XML response'
nl|'\n'
name|'real_body'
op|'='
name|'re'
op|'.'
name|'sub'
op|'('
string|"'AUTH_\\w{4}'"
op|','
string|"'AUTH_someaccount'"
op|','
name|'real_body'
op|')'
newline|'\n'
name|'fake_body'
op|'='
name|'re'
op|'.'
name|'sub'
op|'('
string|"'AUTH_\\w{4}'"
op|','
string|"'AUTH_someaccount'"
op|','
name|'fake_body'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'real_body'
op|','
name|'fake_body'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'real_headers'
op|'['
string|"'content-type'"
op|']'
op|','
nl|'\n'
name|'fake_headers'
op|'['
string|"'content-type'"
op|']'
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
