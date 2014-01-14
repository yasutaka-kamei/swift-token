begin_unit
comment|'# Copyright (c) 2013 OpenStack Foundation'
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
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'container_sync_realms'
name|'import'
name|'ContainerSyncRealms'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'HTTPBadRequest'
op|','
name|'HTTPUnauthorized'
op|','
name|'wsgify'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
op|'('
nl|'\n'
name|'config_true_value'
op|','
name|'get_logger'
op|','
name|'register_swift_info'
op|','
name|'streq_const_time'
op|')'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'base'
name|'import'
name|'get_container_info'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ContainerSync
name|'class'
name|'ContainerSync'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    WSGI middleware that validates an incoming container sync request\n    using the container-sync-realms.conf style of container sync.\n    """'
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
name|'conf'
op|'='
name|'conf'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'conf'
op|','
name|'log_route'
op|'='
string|"'container_sync'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'realms_conf'
op|'='
name|'ContainerSyncRealms'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
nl|'\n'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'swift_dir'"
op|','
string|"'/etc/swift'"
op|')'
op|','
nl|'\n'
string|"'container-sync-realms.conf'"
op|')'
op|','
nl|'\n'
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'allow_full_urls'
op|'='
name|'config_true_value'
op|'('
nl|'\n'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'allow_full_urls'"
op|','
string|"'true'"
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'wsgify'
newline|'\n'
DECL|member|__call__
name|'def'
name|'__call__'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'not'
name|'self'
op|'.'
name|'allow_full_urls'
op|':'
newline|'\n'
indent|'            '
name|'sync_to'
op|'='
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-container-sync-to'"
op|')'
newline|'\n'
name|'if'
name|'sync_to'
name|'and'
name|'not'
name|'sync_to'
op|'.'
name|'startswith'
op|'('
string|"'//'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'HTTPBadRequest'
op|'('
nl|'\n'
name|'body'
op|'='
string|"'Full URLs are not allowed for X-Container-Sync-To '"
nl|'\n'
string|"'values. Only realm values of the format '"
nl|'\n'
string|"'//realm/cluster/account/container are allowed.\\n'"
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'auth'
op|'='
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-container-sync-auth'"
op|')'
newline|'\n'
name|'if'
name|'auth'
op|':'
newline|'\n'
indent|'            '
name|'valid'
op|'='
name|'False'
newline|'\n'
name|'auth'
op|'='
name|'auth'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'auth'
op|')'
op|'!='
number|'3'
op|':'
newline|'\n'
indent|'                '
name|'req'
op|'.'
name|'environ'
op|'.'
name|'setdefault'
op|'('
string|"'swift.log_info'"
op|','
op|'['
op|']'
op|')'
op|'.'
name|'append'
op|'('
nl|'\n'
string|"'cs:not-3-args'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'realm'
op|','
name|'nonce'
op|','
name|'sig'
op|'='
name|'auth'
newline|'\n'
name|'realm_key'
op|'='
name|'self'
op|'.'
name|'realms_conf'
op|'.'
name|'key'
op|'('
name|'realm'
op|')'
newline|'\n'
name|'realm_key2'
op|'='
name|'self'
op|'.'
name|'realms_conf'
op|'.'
name|'key2'
op|'('
name|'realm'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'realm_key'
op|':'
newline|'\n'
indent|'                    '
name|'req'
op|'.'
name|'environ'
op|'.'
name|'setdefault'
op|'('
string|"'swift.log_info'"
op|','
op|'['
op|']'
op|')'
op|'.'
name|'append'
op|'('
nl|'\n'
string|"'cs:no-local-realm-key'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'info'
op|'='
name|'get_container_info'
op|'('
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|','
name|'self'
op|'.'
name|'app'
op|','
name|'swift_source'
op|'='
string|"'CS'"
op|')'
newline|'\n'
name|'user_key'
op|'='
name|'info'
op|'.'
name|'get'
op|'('
string|"'sync_key'"
op|')'
newline|'\n'
name|'if'
name|'not'
name|'user_key'
op|':'
newline|'\n'
indent|'                        '
name|'req'
op|'.'
name|'environ'
op|'.'
name|'setdefault'
op|'('
string|"'swift.log_info'"
op|','
op|'['
op|']'
op|')'
op|'.'
name|'append'
op|'('
nl|'\n'
string|"'cs:no-local-user-key'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'expected'
op|'='
name|'self'
op|'.'
name|'realms_conf'
op|'.'
name|'get_sig'
op|'('
nl|'\n'
name|'req'
op|'.'
name|'method'
op|','
name|'req'
op|'.'
name|'path'
op|','
nl|'\n'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-timestamp'"
op|','
string|"'0'"
op|')'
op|','
name|'nonce'
op|','
nl|'\n'
name|'realm_key'
op|','
name|'user_key'
op|')'
newline|'\n'
name|'expected2'
op|'='
name|'self'
op|'.'
name|'realms_conf'
op|'.'
name|'get_sig'
op|'('
nl|'\n'
name|'req'
op|'.'
name|'method'
op|','
name|'req'
op|'.'
name|'path'
op|','
nl|'\n'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-timestamp'"
op|','
string|"'0'"
op|')'
op|','
name|'nonce'
op|','
nl|'\n'
name|'realm_key2'
op|','
name|'user_key'
op|')'
name|'if'
name|'realm_key2'
name|'else'
name|'expected'
newline|'\n'
name|'if'
name|'not'
name|'streq_const_time'
op|'('
name|'sig'
op|','
name|'expected'
op|')'
name|'and'
name|'not'
name|'streq_const_time'
op|'('
name|'sig'
op|','
name|'expected2'
op|')'
op|':'
newline|'\n'
indent|'                            '
name|'req'
op|'.'
name|'environ'
op|'.'
name|'setdefault'
op|'('
nl|'\n'
string|"'swift.log_info'"
op|','
op|'['
op|']'
op|')'
op|'.'
name|'append'
op|'('
string|"'cs:invalid-sig'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                            '
name|'req'
op|'.'
name|'environ'
op|'.'
name|'setdefault'
op|'('
nl|'\n'
string|"'swift.log_info'"
op|','
op|'['
op|']'
op|')'
op|'.'
name|'append'
op|'('
string|"'cs:valid'"
op|')'
newline|'\n'
name|'valid'
op|'='
name|'True'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
name|'if'
name|'not'
name|'valid'
op|':'
newline|'\n'
indent|'                '
name|'exc'
op|'='
name|'HTTPUnauthorized'
op|'('
nl|'\n'
name|'body'
op|'='
string|"'X-Container-Sync-Auth header not valid; '"
nl|'\n'
string|"'contact cluster operator for support.'"
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'content-type'"
op|':'
string|"'text/plain'"
op|'}'
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
name|'exc'
op|'.'
name|'headers'
op|'['
string|"'www-authenticate'"
op|']'
op|'='
string|"' '"
op|'.'
name|'join'
op|'('
op|'['
nl|'\n'
string|"'SwiftContainerSync'"
op|','
nl|'\n'
name|'exc'
op|'.'
name|'www_authenticate'
op|'('
op|')'
op|'.'
name|'split'
op|'('
name|'None'
op|','
number|'1'
op|')'
op|'['
number|'1'
op|']'
op|']'
op|')'
newline|'\n'
name|'raise'
name|'exc'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.authorize_override'"
op|']'
op|'='
name|'True'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'req'
op|'.'
name|'path'
op|'=='
string|"'/info'"
op|':'
newline|'\n'
comment|'# Ensure /info requests get the freshest results'
nl|'\n'
indent|'            '
name|'dct'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'realm'
name|'in'
name|'self'
op|'.'
name|'realms_conf'
op|'.'
name|'realms'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'clusters'
op|'='
name|'self'
op|'.'
name|'realms_conf'
op|'.'
name|'clusters'
op|'('
name|'realm'
op|')'
newline|'\n'
name|'if'
name|'clusters'
op|':'
newline|'\n'
indent|'                    '
name|'dct'
op|'['
name|'realm'
op|']'
op|'='
op|'{'
string|"'clusters'"
op|':'
name|'dict'
op|'('
op|'('
name|'c'
op|','
op|'{'
op|'}'
op|')'
name|'for'
name|'c'
name|'in'
name|'clusters'
op|')'
op|'}'
newline|'\n'
dedent|''
dedent|''
name|'register_swift_info'
op|'('
string|"'container_sync'"
op|','
name|'realms'
op|'='
name|'dct'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'app'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|filter_factory
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
name|'register_swift_info'
op|'('
string|"'container_sync'"
op|')'
newline|'\n'
nl|'\n'
DECL|function|cache_filter
name|'def'
name|'cache_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'ContainerSync'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'cache_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
