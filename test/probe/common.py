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
name|'from'
name|'os'
name|'import'
name|'environ'
op|','
name|'kill'
newline|'\n'
name|'from'
name|'signal'
name|'import'
name|'SIGTERM'
newline|'\n'
name|'from'
name|'subprocess'
name|'import'
name|'call'
op|','
name|'Popen'
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'sleep'
newline|'\n'
name|'from'
name|'ConfigParser'
name|'import'
name|'ConfigParser'
newline|'\n'
nl|'\n'
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
name|'client'
name|'import'
name|'get_auth'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'ring'
name|'import'
name|'Ring'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|variable|SUPER_ADMIN_KEY
name|'SUPER_ADMIN_KEY'
op|'='
name|'None'
newline|'\n'
DECL|variable|AUTH_TYPE
name|'AUTH_TYPE'
op|'='
name|'None'
newline|'\n'
nl|'\n'
DECL|variable|c
name|'c'
op|'='
name|'ConfigParser'
op|'('
op|')'
newline|'\n'
DECL|variable|AUTH_SERVER_CONF_FILE
name|'AUTH_SERVER_CONF_FILE'
op|'='
name|'environ'
op|'.'
name|'get'
op|'('
string|"'SWIFT_AUTH_SERVER_CONF_FILE'"
op|','
nl|'\n'
string|"'/etc/swift/auth-server.conf'"
op|')'
newline|'\n'
name|'if'
name|'c'
op|'.'
name|'read'
op|'('
name|'AUTH_SERVER_CONF_FILE'
op|')'
op|':'
newline|'\n'
DECL|variable|conf
indent|'    '
name|'conf'
op|'='
name|'dict'
op|'('
name|'c'
op|'.'
name|'items'
op|'('
string|"'app:auth-server'"
op|')'
op|')'
newline|'\n'
DECL|variable|SUPER_ADMIN_KEY
name|'SUPER_ADMIN_KEY'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'super_admin_key'"
op|','
string|"'devauth'"
op|')'
newline|'\n'
DECL|variable|AUTH_TYPE
name|'AUTH_TYPE'
op|'='
string|"'devauth'"
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
DECL|variable|PROXY_SERVER_CONF_FILE
indent|'    '
name|'PROXY_SERVER_CONF_FILE'
op|'='
name|'environ'
op|'.'
name|'get'
op|'('
string|"'SWIFT_PROXY_SERVER_CONF_FILE'"
op|','
nl|'\n'
string|"'/etc/swift/proxy-server.conf'"
op|')'
newline|'\n'
name|'if'
name|'c'
op|'.'
name|'read'
op|'('
name|'PROXY_SERVER_CONF_FILE'
op|')'
op|':'
newline|'\n'
DECL|variable|conf
indent|'        '
name|'conf'
op|'='
name|'dict'
op|'('
name|'c'
op|'.'
name|'items'
op|'('
string|"'filter:swauth'"
op|')'
op|')'
newline|'\n'
DECL|variable|SUPER_ADMIN_KEY
name|'SUPER_ADMIN_KEY'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'super_admin_key'"
op|','
string|"'swauthkey'"
op|')'
newline|'\n'
DECL|variable|AUTH_TYPE
name|'AUTH_TYPE'
op|'='
string|"'swauth'"
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'        '
name|'exit'
op|'('
string|"'Unable to read config file: %s'"
op|'%'
name|'AUTH_SERVER_CONF_FILE'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|kill_pids
dedent|''
dedent|''
name|'def'
name|'kill_pids'
op|'('
name|'pids'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'for'
name|'pid'
name|'in'
name|'pids'
op|'.'
name|'values'
op|'('
op|')'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'kill'
op|'('
name|'pid'
op|','
name|'SIGTERM'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|reset_environment
dedent|''
dedent|''
dedent|''
name|'def'
name|'reset_environment'
op|'('
op|')'
op|':'
newline|'\n'
indent|'    '
name|'call'
op|'('
op|'['
string|"'resetswift'"
op|']'
op|')'
newline|'\n'
name|'pids'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'AUTH_TYPE'
op|'=='
string|"'devauth'"
op|':'
newline|'\n'
indent|'            '
name|'pids'
op|'['
string|"'auth'"
op|']'
op|'='
name|'Popen'
op|'('
op|'['
string|"'swift-auth-server'"
op|','
nl|'\n'
string|"'/etc/swift/auth-server.conf'"
op|']'
op|')'
op|'.'
name|'pid'
newline|'\n'
dedent|''
name|'pids'
op|'['
string|"'proxy'"
op|']'
op|'='
name|'Popen'
op|'('
op|'['
string|"'swift-proxy-server'"
op|','
nl|'\n'
string|"'/etc/swift/proxy-server.conf'"
op|']'
op|')'
op|'.'
name|'pid'
newline|'\n'
name|'port2server'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'s'
op|','
name|'p'
name|'in'
op|'('
op|'('
string|"'account'"
op|','
number|'6002'
op|')'
op|','
op|'('
string|"'container'"
op|','
number|'6001'
op|')'
op|','
op|'('
string|"'object'"
op|','
number|'6000'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'n'
name|'in'
name|'xrange'
op|'('
number|'1'
op|','
number|'5'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'pids'
op|'['
string|"'%s%d'"
op|'%'
op|'('
name|'s'
op|','
name|'n'
op|')'
op|']'
op|'='
name|'Popen'
op|'('
op|'['
string|"'swift-%s-server'"
op|'%'
name|'s'
op|','
nl|'\n'
string|"'/etc/swift/%s-server/%d.conf'"
op|'%'
op|'('
name|'s'
op|','
name|'n'
op|')'
op|']'
op|')'
op|'.'
name|'pid'
newline|'\n'
name|'port2server'
op|'['
name|'p'
op|'+'
op|'('
name|'n'
op|'*'
number|'10'
op|')'
op|']'
op|'='
string|"'%s%d'"
op|'%'
op|'('
name|'s'
op|','
name|'n'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'account_ring'
op|'='
name|'Ring'
op|'('
string|"'/etc/swift/account.ring.gz'"
op|')'
newline|'\n'
name|'container_ring'
op|'='
name|'Ring'
op|'('
string|"'/etc/swift/container.ring.gz'"
op|')'
newline|'\n'
name|'object_ring'
op|'='
name|'Ring'
op|'('
string|"'/etc/swift/object.ring.gz'"
op|')'
newline|'\n'
name|'sleep'
op|'('
number|'5'
op|')'
newline|'\n'
name|'if'
name|'AUTH_TYPE'
op|'=='
string|"'devauth'"
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'='
name|'http_connect'
op|'('
string|"'127.0.0.1'"
op|','
string|"'11000'"
op|','
string|"'POST'"
op|','
nl|'\n'
string|"'/recreate_accounts'"
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Auth-Admin-User'"
op|':'
string|"'.super_admin'"
op|','
nl|'\n'
string|"'X-Auth-Admin-Key'"
op|':'
name|'SUPER_ADMIN_KEY'
op|'}'
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
op|'!='
number|'200'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'Exception'
op|'('
string|"'Recreating accounts failed. (%d)'"
op|'%'
nl|'\n'
name|'resp'
op|'.'
name|'status'
op|')'
newline|'\n'
dedent|''
name|'url'
op|','
name|'token'
op|'='
name|'get_auth'
op|'('
string|"'http://127.0.0.1:11000/auth'"
op|','
string|"'test:tester'"
op|','
nl|'\n'
string|"'testing'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'AUTH_TYPE'
op|'=='
string|"'swauth'"
op|':'
newline|'\n'
indent|'            '
name|'call'
op|'('
op|'['
string|"'recreateaccounts'"
op|']'
op|')'
newline|'\n'
name|'url'
op|','
name|'token'
op|'='
name|'get_auth'
op|'('
string|"'http://127.0.0.1:8080/auth/v1.0'"
op|','
nl|'\n'
string|"'test:tester'"
op|','
string|"'testing'"
op|')'
newline|'\n'
dedent|''
name|'account'
op|'='
name|'url'
op|'.'
name|'split'
op|'('
string|"'/'"
op|')'
op|'['
op|'-'
number|'1'
op|']'
newline|'\n'
dedent|''
name|'except'
name|'BaseException'
op|','
name|'err'
op|':'
newline|'\n'
indent|'        '
name|'kill_pids'
op|'('
name|'pids'
op|')'
newline|'\n'
name|'raise'
name|'err'
newline|'\n'
dedent|''
name|'return'
name|'pids'
op|','
name|'port2server'
op|','
name|'account_ring'
op|','
name|'container_ring'
op|','
name|'object_ring'
op|','
name|'url'
op|','
name|'token'
op|','
name|'account'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_to_final_state
dedent|''
name|'def'
name|'get_to_final_state'
op|'('
op|')'
op|':'
newline|'\n'
indent|'    '
name|'ps'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'job'
name|'in'
op|'('
string|"'account-replicator'"
op|','
string|"'container-replicator'"
op|','
nl|'\n'
string|"'object-replicator'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'n'
name|'in'
name|'xrange'
op|'('
number|'1'
op|','
number|'5'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'ps'
op|'.'
name|'append'
op|'('
name|'Popen'
op|'('
op|'['
string|"'swift-%s'"
op|'%'
name|'job'
op|','
nl|'\n'
string|"'/etc/swift/%s-server/%d.conf'"
op|'%'
nl|'\n'
op|'('
name|'job'
op|'.'
name|'split'
op|'('
string|"'-'"
op|')'
op|'['
number|'0'
op|']'
op|','
name|'n'
op|')'
op|','
nl|'\n'
string|"'once'"
op|']'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'for'
name|'p'
name|'in'
name|'ps'
op|':'
newline|'\n'
indent|'        '
name|'p'
op|'.'
name|'wait'
op|'('
op|')'
newline|'\n'
dedent|''
name|'ps'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'job'
name|'in'
op|'('
string|"'container-updater'"
op|','
string|"'object-updater'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'n'
name|'in'
name|'xrange'
op|'('
number|'1'
op|','
number|'5'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'ps'
op|'.'
name|'append'
op|'('
name|'Popen'
op|'('
op|'['
string|"'swift-%s'"
op|'%'
name|'job'
op|','
nl|'\n'
string|"'/etc/swift/%s-server/%d.conf'"
op|'%'
nl|'\n'
op|'('
name|'job'
op|'.'
name|'split'
op|'('
string|"'-'"
op|')'
op|'['
number|'0'
op|']'
op|','
name|'n'
op|')'
op|','
nl|'\n'
string|"'once'"
op|']'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'for'
name|'p'
name|'in'
name|'ps'
op|':'
newline|'\n'
indent|'        '
name|'p'
op|'.'
name|'wait'
op|'('
op|')'
newline|'\n'
dedent|''
name|'ps'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'job'
name|'in'
op|'('
string|"'account-replicator'"
op|','
string|"'container-replicator'"
op|','
nl|'\n'
string|"'object-replicator'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'n'
name|'in'
name|'xrange'
op|'('
number|'1'
op|','
number|'5'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'ps'
op|'.'
name|'append'
op|'('
name|'Popen'
op|'('
op|'['
string|"'swift-%s'"
op|'%'
name|'job'
op|','
nl|'\n'
string|"'/etc/swift/%s-server/%d.conf'"
op|'%'
nl|'\n'
op|'('
name|'job'
op|'.'
name|'split'
op|'('
string|"'-'"
op|')'
op|'['
number|'0'
op|']'
op|','
name|'n'
op|')'
op|','
nl|'\n'
string|"'once'"
op|']'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'for'
name|'p'
name|'in'
name|'ps'
op|':'
newline|'\n'
indent|'        '
name|'p'
op|'.'
name|'wait'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
