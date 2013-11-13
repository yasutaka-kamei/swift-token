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
name|'from'
name|'httplib'
name|'import'
name|'HTTPException'
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
name|'from'
name|'time'
name|'import'
name|'sleep'
newline|'\n'
name|'from'
name|'urlparse'
name|'import'
name|'urlparse'
newline|'\n'
nl|'\n'
name|'from'
name|'test'
name|'import'
name|'get_config'
newline|'\n'
nl|'\n'
name|'from'
name|'swiftclient'
name|'import'
name|'get_auth'
op|','
name|'http_connection'
newline|'\n'
nl|'\n'
DECL|variable|conf
name|'conf'
op|'='
name|'get_config'
op|'('
string|"'func_test'"
op|')'
newline|'\n'
DECL|variable|web_front_end
name|'web_front_end'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'web_front_end'"
op|','
string|"'integral'"
op|')'
newline|'\n'
DECL|variable|normalized_urls
name|'normalized_urls'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'normalized_urls'"
op|','
name|'False'
op|')'
newline|'\n'
nl|'\n'
comment|'# If no conf was read, we will fall back to old school env vars'
nl|'\n'
DECL|variable|swift_test_auth
name|'swift_test_auth'
op|'='
name|'os'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'SWIFT_TEST_AUTH'"
op|')'
newline|'\n'
DECL|variable|swift_test_user
name|'swift_test_user'
op|'='
op|'['
name|'os'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'SWIFT_TEST_USER'"
op|')'
op|','
name|'None'
op|','
name|'None'
op|']'
newline|'\n'
DECL|variable|swift_test_key
name|'swift_test_key'
op|'='
op|'['
name|'os'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'SWIFT_TEST_KEY'"
op|')'
op|','
name|'None'
op|','
name|'None'
op|']'
newline|'\n'
DECL|variable|swift_test_tenant
name|'swift_test_tenant'
op|'='
op|'['
string|"''"
op|','
string|"''"
op|','
string|"''"
op|']'
newline|'\n'
DECL|variable|swift_test_perm
name|'swift_test_perm'
op|'='
op|'['
string|"''"
op|','
string|"''"
op|','
string|"''"
op|']'
newline|'\n'
nl|'\n'
name|'if'
name|'conf'
op|':'
newline|'\n'
DECL|variable|swift_test_auth_version
indent|'    '
name|'swift_test_auth_version'
op|'='
name|'str'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'auth_version'"
op|','
string|"'1'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|variable|swift_test_auth
name|'swift_test_auth'
op|'='
string|"'http'"
newline|'\n'
name|'if'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'auth_ssl'"
op|','
string|"'no'"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
name|'in'
op|'('
string|"'yes'"
op|','
string|"'true'"
op|','
string|"'on'"
op|','
string|"'1'"
op|')'
op|':'
newline|'\n'
DECL|variable|swift_test_auth
indent|'        '
name|'swift_test_auth'
op|'='
string|"'https'"
newline|'\n'
dedent|''
name|'if'
string|"'auth_prefix'"
name|'not'
name|'in'
name|'conf'
op|':'
newline|'\n'
indent|'        '
name|'conf'
op|'['
string|"'auth_prefix'"
op|']'
op|'='
string|"'/'"
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
DECL|variable|suffix
indent|'        '
name|'suffix'
op|'='
string|"'://%(auth_host)s:%(auth_port)s%(auth_prefix)s'"
op|'%'
name|'conf'
newline|'\n'
name|'swift_test_auth'
op|'+='
name|'suffix'
newline|'\n'
dedent|''
name|'except'
name|'KeyError'
op|':'
newline|'\n'
indent|'        '
name|'pass'
comment|'# skip'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'swift_test_auth_version'
op|'=='
string|'"1"'
op|':'
newline|'\n'
indent|'        '
name|'swift_test_auth'
op|'+='
string|"'v1.0'"
newline|'\n'
nl|'\n'
name|'if'
string|"'account'"
name|'in'
name|'conf'
op|':'
newline|'\n'
indent|'            '
name|'swift_test_user'
op|'['
number|'0'
op|']'
op|'='
string|"'%(account)s:%(username)s'"
op|'%'
name|'conf'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'swift_test_user'
op|'['
number|'0'
op|']'
op|'='
string|"'%(username)s'"
op|'%'
name|'conf'
newline|'\n'
dedent|''
name|'swift_test_key'
op|'['
number|'0'
op|']'
op|'='
name|'conf'
op|'['
string|"'password'"
op|']'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'swift_test_user'
op|'['
number|'1'
op|']'
op|'='
string|"'%s%s'"
op|'%'
op|'('
nl|'\n'
string|"'%s:'"
op|'%'
name|'conf'
op|'['
string|"'account2'"
op|']'
name|'if'
string|"'account2'"
name|'in'
name|'conf'
name|'else'
string|"''"
op|','
nl|'\n'
name|'conf'
op|'['
string|"'username2'"
op|']'
op|')'
newline|'\n'
name|'swift_test_key'
op|'['
number|'1'
op|']'
op|'='
name|'conf'
op|'['
string|"'password2'"
op|']'
newline|'\n'
dedent|''
name|'except'
name|'KeyError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'pass'
comment|'# old conf, no second account tests can be run'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'swift_test_user'
op|'['
number|'2'
op|']'
op|'='
string|"'%s%s'"
op|'%'
op|'('
string|"'%s:'"
op|'%'
name|'conf'
op|'['
string|"'account'"
op|']'
name|'if'
string|"'account'"
nl|'\n'
name|'in'
name|'conf'
name|'else'
string|"''"
op|','
name|'conf'
op|'['
string|"'username3'"
op|']'
op|')'
newline|'\n'
name|'swift_test_key'
op|'['
number|'2'
op|']'
op|'='
name|'conf'
op|'['
string|"'password3'"
op|']'
newline|'\n'
dedent|''
name|'except'
name|'KeyError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'pass'
comment|'# old conf, no third account tests can be run'
newline|'\n'
nl|'\n'
dedent|''
name|'for'
name|'_'
name|'in'
name|'range'
op|'('
number|'3'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'swift_test_perm'
op|'['
name|'_'
op|']'
op|'='
name|'swift_test_user'
op|'['
name|'_'
op|']'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'        '
name|'swift_test_user'
op|'['
number|'0'
op|']'
op|'='
name|'conf'
op|'['
string|"'username'"
op|']'
newline|'\n'
name|'swift_test_tenant'
op|'['
number|'0'
op|']'
op|'='
name|'conf'
op|'['
string|"'account'"
op|']'
newline|'\n'
name|'swift_test_key'
op|'['
number|'0'
op|']'
op|'='
name|'conf'
op|'['
string|"'password'"
op|']'
newline|'\n'
name|'swift_test_user'
op|'['
number|'1'
op|']'
op|'='
name|'conf'
op|'['
string|"'username2'"
op|']'
newline|'\n'
name|'swift_test_tenant'
op|'['
number|'1'
op|']'
op|'='
name|'conf'
op|'['
string|"'account2'"
op|']'
newline|'\n'
name|'swift_test_key'
op|'['
number|'1'
op|']'
op|'='
name|'conf'
op|'['
string|"'password2'"
op|']'
newline|'\n'
name|'swift_test_user'
op|'['
number|'2'
op|']'
op|'='
name|'conf'
op|'['
string|"'username3'"
op|']'
newline|'\n'
name|'swift_test_tenant'
op|'['
number|'2'
op|']'
op|'='
name|'conf'
op|'['
string|"'account'"
op|']'
newline|'\n'
name|'swift_test_key'
op|'['
number|'2'
op|']'
op|'='
name|'conf'
op|'['
string|"'password3'"
op|']'
newline|'\n'
nl|'\n'
name|'for'
name|'_'
name|'in'
name|'range'
op|'('
number|'3'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'swift_test_perm'
op|'['
name|'_'
op|']'
op|'='
name|'swift_test_tenant'
op|'['
name|'_'
op|']'
op|'+'
string|"':'"
op|'+'
name|'swift_test_user'
op|'['
name|'_'
op|']'
newline|'\n'
nl|'\n'
DECL|variable|skip
dedent|''
dedent|''
dedent|''
name|'skip'
op|'='
name|'not'
name|'all'
op|'('
op|'['
name|'swift_test_auth'
op|','
name|'swift_test_user'
op|'['
number|'0'
op|']'
op|','
name|'swift_test_key'
op|'['
number|'0'
op|']'
op|']'
op|')'
newline|'\n'
name|'if'
name|'skip'
op|':'
newline|'\n'
indent|'    '
name|'print'
op|'>>'
name|'sys'
op|'.'
name|'stderr'
op|','
string|"'SKIPPING FUNCTIONAL TESTS DUE TO NO CONFIG'"
newline|'\n'
nl|'\n'
DECL|variable|skip2
dedent|''
name|'skip2'
op|'='
name|'not'
name|'all'
op|'('
op|'['
name|'not'
name|'skip'
op|','
name|'swift_test_user'
op|'['
number|'1'
op|']'
op|','
name|'swift_test_key'
op|'['
number|'1'
op|']'
op|']'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'skip'
name|'and'
name|'skip2'
op|':'
newline|'\n'
indent|'    '
name|'print'
op|'>>'
name|'sys'
op|'.'
name|'stderr'
op|','
string|"'SKIPPING SECOND ACCOUNT FUNCTIONAL TESTS DUE TO NO CONFIG FOR THEM'"
newline|'\n'
nl|'\n'
DECL|variable|skip3
dedent|''
name|'skip3'
op|'='
name|'not'
name|'all'
op|'('
op|'['
name|'not'
name|'skip'
op|','
name|'swift_test_user'
op|'['
number|'2'
op|']'
op|','
name|'swift_test_key'
op|'['
number|'2'
op|']'
op|']'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'skip'
name|'and'
name|'skip3'
op|':'
newline|'\n'
indent|'    '
name|'print'
op|'>>'
name|'sys'
op|'.'
name|'stderr'
op|','
string|"'SKIPPING THIRD ACCOUNT FUNCTIONAL TESTS DUE TO NO CONFIG FOR THEM'"
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|AuthError
dedent|''
name|'class'
name|'AuthError'
op|'('
name|'Exception'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|InternalServerError
dedent|''
name|'class'
name|'InternalServerError'
op|'('
name|'Exception'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|variable|url
dedent|''
name|'url'
op|'='
op|'['
name|'None'
op|','
name|'None'
op|','
name|'None'
op|']'
newline|'\n'
DECL|variable|token
name|'token'
op|'='
op|'['
name|'None'
op|','
name|'None'
op|','
name|'None'
op|']'
newline|'\n'
DECL|variable|parsed
name|'parsed'
op|'='
op|'['
name|'None'
op|','
name|'None'
op|','
name|'None'
op|']'
newline|'\n'
DECL|variable|conn
name|'conn'
op|'='
op|'['
name|'None'
op|','
name|'None'
op|','
name|'None'
op|']'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|retry
name|'def'
name|'retry'
op|'('
name|'func'
op|','
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    You can use the kwargs to override:\n      \'retries\' (default: 5)\n      \'use_account\' (default: 1) - which user\'s token to pass\n      \'url_account\' (default: matches \'use_account\') - which user\'s storage URL\n      \'resource\' (default: url[url_account] - URL to connect to; retry()\n          will interpolate the variable :storage_url: if present\n    """'
newline|'\n'
name|'global'
name|'url'
op|','
name|'token'
op|','
name|'parsed'
op|','
name|'conn'
newline|'\n'
name|'retries'
op|'='
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'retries'"
op|','
number|'5'
op|')'
newline|'\n'
name|'attempts'
op|','
name|'backoff'
op|'='
number|'0'
op|','
number|'1'
newline|'\n'
nl|'\n'
comment|"# use account #1 by default; turn user's 1-indexed account into 0-indexed"
nl|'\n'
name|'use_account'
op|'='
name|'kwargs'
op|'.'
name|'pop'
op|'('
string|"'use_account'"
op|','
number|'1'
op|')'
op|'-'
number|'1'
newline|'\n'
nl|'\n'
comment|'# access our own account by default'
nl|'\n'
name|'url_account'
op|'='
name|'kwargs'
op|'.'
name|'pop'
op|'('
string|"'url_account'"
op|','
name|'use_account'
op|'+'
number|'1'
op|')'
op|'-'
number|'1'
newline|'\n'
nl|'\n'
name|'while'
name|'attempts'
op|'<='
name|'retries'
op|':'
newline|'\n'
indent|'        '
name|'attempts'
op|'+='
number|'1'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'not'
name|'url'
op|'['
name|'use_account'
op|']'
name|'or'
name|'not'
name|'token'
op|'['
name|'use_account'
op|']'
op|':'
newline|'\n'
indent|'                '
name|'url'
op|'['
name|'use_account'
op|']'
op|','
name|'token'
op|'['
name|'use_account'
op|']'
op|'='
name|'get_auth'
op|'('
name|'swift_test_auth'
op|','
name|'swift_test_user'
op|'['
name|'use_account'
op|']'
op|','
nl|'\n'
name|'swift_test_key'
op|'['
name|'use_account'
op|']'
op|','
nl|'\n'
name|'snet'
op|'='
name|'False'
op|','
nl|'\n'
name|'tenant_name'
op|'='
name|'swift_test_tenant'
op|'['
name|'use_account'
op|']'
op|','
nl|'\n'
name|'auth_version'
op|'='
name|'swift_test_auth_version'
op|','
nl|'\n'
name|'os_options'
op|'='
op|'{'
op|'}'
op|')'
newline|'\n'
name|'parsed'
op|'['
name|'use_account'
op|']'
op|'='
name|'conn'
op|'['
name|'use_account'
op|']'
op|'='
name|'None'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'parsed'
op|'['
name|'use_account'
op|']'
name|'or'
name|'not'
name|'conn'
op|'['
name|'use_account'
op|']'
op|':'
newline|'\n'
indent|'                '
name|'parsed'
op|'['
name|'use_account'
op|']'
op|','
name|'conn'
op|'['
name|'use_account'
op|']'
op|'='
name|'http_connection'
op|'('
name|'url'
op|'['
name|'use_account'
op|']'
op|')'
newline|'\n'
nl|'\n'
comment|'# default resource is the account url[url_account]'
nl|'\n'
dedent|''
name|'resource'
op|'='
name|'kwargs'
op|'.'
name|'pop'
op|'('
string|"'resource'"
op|','
string|"'%(storage_url)s'"
op|')'
newline|'\n'
name|'template_vars'
op|'='
op|'{'
string|"'storage_url'"
op|':'
name|'url'
op|'['
name|'url_account'
op|']'
op|'}'
newline|'\n'
name|'parsed_result'
op|'='
name|'urlparse'
op|'('
name|'resource'
op|'%'
name|'template_vars'
op|')'
newline|'\n'
name|'return'
name|'func'
op|'('
name|'url'
op|'['
name|'url_account'
op|']'
op|','
name|'token'
op|'['
name|'use_account'
op|']'
op|','
nl|'\n'
name|'parsed_result'
op|','
name|'conn'
op|'['
name|'url_account'
op|']'
op|','
nl|'\n'
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'socket'
op|'.'
name|'error'
op|','
name|'HTTPException'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'attempts'
op|'>'
name|'retries'
op|':'
newline|'\n'
indent|'                '
name|'raise'
newline|'\n'
dedent|''
name|'parsed'
op|'['
name|'use_account'
op|']'
op|'='
name|'conn'
op|'['
name|'use_account'
op|']'
op|'='
name|'None'
newline|'\n'
dedent|''
name|'except'
name|'AuthError'
op|':'
newline|'\n'
indent|'            '
name|'url'
op|'['
name|'use_account'
op|']'
op|'='
name|'token'
op|'['
name|'use_account'
op|']'
op|'='
name|'None'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'except'
name|'InternalServerError'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'if'
name|'attempts'
op|'<='
name|'retries'
op|':'
newline|'\n'
indent|'            '
name|'sleep'
op|'('
name|'backoff'
op|')'
newline|'\n'
name|'backoff'
op|'*='
number|'2'
newline|'\n'
dedent|''
dedent|''
name|'raise'
name|'Exception'
op|'('
string|"'No result after %s retries.'"
op|'%'
name|'retries'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|check_response
dedent|''
name|'def'
name|'check_response'
op|'('
name|'conn'
op|')'
op|':'
newline|'\n'
indent|'    '
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
op|'=='
number|'401'
op|':'
newline|'\n'
indent|'        '
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'raise'
name|'AuthError'
op|'('
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'resp'
op|'.'
name|'status'
op|'//'
number|'100'
op|'=='
number|'5'
op|':'
newline|'\n'
indent|'        '
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'raise'
name|'InternalServerError'
op|'('
op|')'
newline|'\n'
dedent|''
name|'return'
name|'resp'
newline|'\n'
dedent|''
endmarker|''
end_unit
