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
name|'import'
name|'time'
newline|'\n'
nl|'\n'
name|'from'
name|'webob'
op|'.'
name|'request'
name|'import'
name|'Request'
newline|'\n'
name|'from'
name|'webob'
op|'.'
name|'exc'
name|'import'
name|'HTTPUnauthorized'
op|','
name|'HTTPPreconditionFailed'
newline|'\n'
name|'from'
name|'eventlet'
op|'.'
name|'timeout'
name|'import'
name|'Timeout'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'split_path'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'bufferedhttp'
name|'import'
name|'http_connect_raw'
name|'as'
name|'http_connect'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'get_logger'
op|','
name|'cache_from_env'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'memcached'
name|'import'
name|'MemcacheRing'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DevAuthMiddleware
name|'class'
name|'DevAuthMiddleware'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Auth Middleware that uses the dev auth server\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'app'
op|','
name|'conf'
op|','
name|'memcache_client'
op|'='
name|'None'
op|','
name|'logger'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'app'
op|'='
name|'app'
newline|'\n'
name|'self'
op|'.'
name|'memcache_client'
op|'='
name|'memcache_client'
newline|'\n'
name|'if'
name|'logger'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'conf'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'='
name|'logger'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'conf'
op|'='
name|'conf'
newline|'\n'
name|'self'
op|'.'
name|'auth_host'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'ip'"
op|','
string|"'127.0.0.1'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auth_port'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'port'"
op|','
number|'11000'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'ssl'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'ssl'"
op|','
string|"'false'"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
name|'in'
op|'('
string|"'true'"
op|','
string|"'on'"
op|','
string|"'1'"
op|','
string|"'yes'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'timeout'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'node_timeout'"
op|','
number|'10'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|__call__
dedent|''
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
name|'if'
name|'self'
op|'.'
name|'memcache_client'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'memcache_client'
op|'='
name|'cache_from_env'
op|'('
name|'env'
op|')'
newline|'\n'
dedent|''
name|'req'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
newline|'\n'
name|'if'
string|"'x-storage-token'"
name|'in'
name|'req'
op|'.'
name|'headers'
name|'and'
string|"'x-auth-token'"
name|'not'
name|'in'
name|'req'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'            '
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-auth-token'"
op|']'
op|'='
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-storage-token'"
op|']'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|'='
name|'split_path'
op|'('
name|'req'
op|'.'
name|'path'
op|','
number|'1'
op|','
number|'4'
op|','
name|'True'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|','
name|'e'
op|':'
newline|'\n'
indent|'            '
name|'version'
op|'='
name|'account'
op|'='
name|'container'
op|'='
name|'obj'
op|'='
name|'None'
newline|'\n'
dedent|''
name|'if'
name|'account'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPPreconditionFailed'
op|'('
name|'request'
op|'='
name|'req'
op|','
name|'body'
op|'='
string|"'Bad URL'"
op|')'
op|'('
nl|'\n'
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-auth-token'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPPreconditionFailed'
op|'('
name|'request'
op|'='
name|'req'
op|','
nl|'\n'
name|'body'
op|'='
string|"'Missing Auth Token'"
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'self'
op|'.'
name|'auth'
op|'('
name|'account'
op|','
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-auth-token'"
op|']'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPUnauthorized'
op|'('
name|'request'
op|'='
name|'req'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
comment|'# If we get here, then things should be good.'
nl|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
DECL|member|auth
dedent|''
name|'def'
name|'auth'
op|'('
name|'self'
op|','
name|'account'
op|','
name|'token'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Dev authorization implmentation\n\n        :param account: account name\n        :param token: auth token\n\n        :returns: True if authorization is successful, False otherwise\n        """'
newline|'\n'
name|'key'
op|'='
string|"'auth/%s/%s'"
op|'%'
op|'('
name|'account'
op|','
name|'token'
op|')'
newline|'\n'
name|'now'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'cached_auth_data'
op|'='
name|'self'
op|'.'
name|'memcache_client'
op|'.'
name|'get'
op|'('
name|'key'
op|')'
newline|'\n'
name|'if'
name|'cached_auth_data'
op|':'
newline|'\n'
indent|'            '
name|'start'
op|','
name|'expiration'
op|'='
name|'cached_auth_data'
newline|'\n'
name|'if'
name|'now'
op|'-'
name|'start'
op|'<='
name|'expiration'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'True'
newline|'\n'
dedent|''
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'Timeout'
op|'('
name|'self'
op|'.'
name|'timeout'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'conn'
op|'='
name|'http_connect'
op|'('
name|'self'
op|'.'
name|'auth_host'
op|','
name|'self'
op|'.'
name|'auth_port'
op|','
string|"'GET'"
op|','
nl|'\n'
string|"'/token/%s/%s'"
op|'%'
op|'('
name|'account'
op|','
name|'token'
op|')'
op|','
name|'ssl'
op|'='
name|'self'
op|'.'
name|'ssl'
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
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
name|'if'
name|'resp'
op|'.'
name|'status'
op|'=='
number|'204'
op|':'
newline|'\n'
indent|'                    '
name|'validated'
op|'='
name|'float'
op|'('
name|'resp'
op|'.'
name|'getheader'
op|'('
string|"'x-auth-ttl'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'validated'
op|'='
name|'False'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'except'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
string|"'ERROR with auth'"
op|')'
newline|'\n'
name|'return'
name|'False'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'validated'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'False'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'val'
op|'='
op|'('
name|'now'
op|','
name|'validated'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'memcache_client'
op|'.'
name|'set'
op|'('
name|'key'
op|','
name|'val'
op|','
name|'timeout'
op|'='
name|'validated'
op|')'
newline|'\n'
name|'return'
name|'True'
newline|'\n'
nl|'\n'
DECL|function|filter_factory
dedent|''
dedent|''
dedent|''
name|'def'
name|'filter_factory'
op|'('
name|'global_conf'
op|','
op|'**'
name|'local_conf'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'conf'
op|'='
name|'global_conf'
op|'.'
name|'copy'
op|'('
op|')'
newline|'\n'
name|'conf'
op|'.'
name|'update'
op|'('
name|'local_conf'
op|')'
newline|'\n'
DECL|function|auth_filter
name|'def'
name|'auth_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'DevAuthMiddleware'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'auth_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
