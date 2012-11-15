begin_unit
comment|'# Copyright (c) 2010-2012 OpenStack, LLC.'
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
string|'"""\nInternal client library for making calls directly to the servers rather than\nthrough the proxy.\n"""'
newline|'\n'
nl|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'socket'
newline|'\n'
name|'from'
name|'httplib'
name|'import'
name|'HTTPException'
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'urllib'
name|'import'
name|'quote'
name|'as'
name|'_quote'
newline|'\n'
nl|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'sleep'
op|','
name|'Timeout'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'bufferedhttp'
name|'import'
name|'http_connect'
newline|'\n'
name|'from'
name|'swiftclient'
name|'import'
name|'ClientException'
op|','
name|'json_loads'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'normalize_timestamp'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'http'
name|'import'
name|'HTTP_NO_CONTENT'
op|','
name|'HTTP_INSUFFICIENT_STORAGE'
op|','
name|'is_success'
op|','
name|'is_server_error'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'HeaderKeyDict'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|quote
name|'def'
name|'quote'
op|'('
name|'value'
op|','
name|'safe'
op|'='
string|"'/'"
op|')'
op|':'
newline|'\n'
indent|'    '
name|'if'
name|'isinstance'
op|'('
name|'value'
op|','
name|'unicode'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'value'
op|'='
name|'value'
op|'.'
name|'encode'
op|'('
string|"'utf8'"
op|')'
newline|'\n'
dedent|''
name|'return'
name|'_quote'
op|'('
name|'value'
op|','
name|'safe'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|gen_headers
dedent|''
name|'def'
name|'gen_headers'
op|'('
name|'hdrs_in'
op|'='
name|'None'
op|','
name|'add_ts'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'hdrs_out'
op|'='
name|'HeaderKeyDict'
op|'('
name|'hdrs_in'
op|')'
name|'if'
name|'hdrs_in'
name|'else'
name|'HeaderKeyDict'
op|'('
op|')'
newline|'\n'
name|'if'
name|'add_ts'
op|':'
newline|'\n'
indent|'        '
name|'hdrs_out'
op|'['
string|"'X-Timestamp'"
op|']'
op|'='
name|'normalize_timestamp'
op|'('
name|'time'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'hdrs_out'
op|'['
string|"'User-Agent'"
op|']'
op|'='
string|"'direct-client %s'"
op|'%'
name|'os'
op|'.'
name|'getpid'
op|'('
op|')'
newline|'\n'
name|'return'
name|'hdrs_out'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|direct_get_account
dedent|''
name|'def'
name|'direct_get_account'
op|'('
name|'node'
op|','
name|'part'
op|','
name|'account'
op|','
name|'marker'
op|'='
name|'None'
op|','
name|'limit'
op|'='
name|'None'
op|','
nl|'\n'
name|'prefix'
op|'='
name|'None'
op|','
name|'delimiter'
op|'='
name|'None'
op|','
name|'conn_timeout'
op|'='
number|'5'
op|','
nl|'\n'
name|'response_timeout'
op|'='
number|'15'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Get listings directly from the account server.\n\n    :param node: node dictionary from the ring\n    :param part: partition the account is on\n    :param account: account name\n    :param marker: marker query\n    :param limit: query limit\n    :param prefix: prefix query\n    :param delimeter: delimeter for the query\n    :param conn_timeout: timeout in seconds for establishing the connection\n    :param response_timeout: timeout in seconds for getting the response\n    :returns: a tuple of (response headers, a list of containers) The response\n              headers will be a dict and all header names will be lowercase.\n    """'
newline|'\n'
name|'path'
op|'='
string|"'/'"
op|'+'
name|'account'
newline|'\n'
name|'qs'
op|'='
string|"'format=json'"
newline|'\n'
name|'if'
name|'marker'
op|':'
newline|'\n'
indent|'        '
name|'qs'
op|'+='
string|"'&marker=%s'"
op|'%'
name|'quote'
op|'('
name|'marker'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'limit'
op|':'
newline|'\n'
indent|'        '
name|'qs'
op|'+='
string|"'&limit=%d'"
op|'%'
name|'limit'
newline|'\n'
dedent|''
name|'if'
name|'prefix'
op|':'
newline|'\n'
indent|'        '
name|'qs'
op|'+='
string|"'&prefix=%s'"
op|'%'
name|'quote'
op|'('
name|'prefix'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'delimiter'
op|':'
newline|'\n'
indent|'        '
name|'qs'
op|'+='
string|"'&delimiter=%s'"
op|'%'
name|'quote'
op|'('
name|'delimiter'
op|')'
newline|'\n'
dedent|''
name|'with'
name|'Timeout'
op|'('
name|'conn_timeout'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'conn'
op|'='
name|'http_connect'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
nl|'\n'
string|"'GET'"
op|','
name|'path'
op|','
name|'query_string'
op|'='
name|'qs'
op|','
nl|'\n'
name|'headers'
op|'='
name|'gen_headers'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'with'
name|'Timeout'
op|'('
name|'response_timeout'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'resp'
op|'='
name|'conn'
op|'.'
name|'getresponse'
op|'('
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'is_success'
op|'('
name|'resp'
op|'.'
name|'status'
op|')'
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
name|'ClientException'
op|'('
nl|'\n'
string|"'Account server %s:%s direct GET %s gave status %s'"
op|'%'
nl|'\n'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
nl|'\n'
name|'repr'
op|'('
string|"'/%s/%s%s'"
op|'%'
op|'('
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
name|'path'
op|')'
op|')'
op|','
nl|'\n'
name|'resp'
op|'.'
name|'status'
op|')'
op|','
nl|'\n'
name|'http_host'
op|'='
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'http_port'
op|'='
name|'node'
op|'['
string|"'port'"
op|']'
op|','
nl|'\n'
name|'http_device'
op|'='
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'http_status'
op|'='
name|'resp'
op|'.'
name|'status'
op|','
nl|'\n'
name|'http_reason'
op|'='
name|'resp'
op|'.'
name|'reason'
op|')'
newline|'\n'
dedent|''
name|'resp_headers'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'header'
op|','
name|'value'
name|'in'
name|'resp'
op|'.'
name|'getheaders'
op|'('
op|')'
op|':'
newline|'\n'
indent|'        '
name|'resp_headers'
op|'['
name|'header'
op|'.'
name|'lower'
op|'('
op|')'
op|']'
op|'='
name|'value'
newline|'\n'
dedent|''
name|'if'
name|'resp'
op|'.'
name|'status'
op|'=='
name|'HTTP_NO_CONTENT'
op|':'
newline|'\n'
indent|'        '
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'return'
name|'resp_headers'
op|','
op|'['
op|']'
newline|'\n'
dedent|''
name|'return'
name|'resp_headers'
op|','
name|'json_loads'
op|'('
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|direct_head_container
dedent|''
name|'def'
name|'direct_head_container'
op|'('
name|'node'
op|','
name|'part'
op|','
name|'account'
op|','
name|'container'
op|','
name|'conn_timeout'
op|'='
number|'5'
op|','
nl|'\n'
name|'response_timeout'
op|'='
number|'15'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Request container information directly from the container server.\n\n    :param node: node dictionary from the ring\n    :param part: partition the container is on\n    :param account: account name\n    :param container: container name\n    :param conn_timeout: timeout in seconds for establishing the connection\n    :param response_timeout: timeout in seconds for getting the response\n    :returns: a dict containing the response\'s headers (all header names will\n              be lowercase)\n    """'
newline|'\n'
name|'path'
op|'='
string|"'/%s/%s'"
op|'%'
op|'('
name|'account'
op|','
name|'container'
op|')'
newline|'\n'
name|'with'
name|'Timeout'
op|'('
name|'conn_timeout'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'conn'
op|'='
name|'http_connect'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
nl|'\n'
string|"'HEAD'"
op|','
name|'path'
op|','
name|'headers'
op|'='
name|'gen_headers'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'with'
name|'Timeout'
op|'('
name|'response_timeout'
op|')'
op|':'
newline|'\n'
indent|'        '
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
dedent|''
name|'if'
name|'not'
name|'is_success'
op|'('
name|'resp'
op|'.'
name|'status'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ClientException'
op|'('
nl|'\n'
string|"'Container server %s:%s direct HEAD %s gave status %s'"
op|'%'
nl|'\n'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
nl|'\n'
name|'repr'
op|'('
string|"'/%s/%s%s'"
op|'%'
op|'('
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
name|'path'
op|')'
op|')'
op|','
nl|'\n'
name|'resp'
op|'.'
name|'status'
op|')'
op|','
nl|'\n'
name|'http_host'
op|'='
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'http_port'
op|'='
name|'node'
op|'['
string|"'port'"
op|']'
op|','
nl|'\n'
name|'http_device'
op|'='
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'http_status'
op|'='
name|'resp'
op|'.'
name|'status'
op|','
nl|'\n'
name|'http_reason'
op|'='
name|'resp'
op|'.'
name|'reason'
op|')'
newline|'\n'
dedent|''
name|'resp_headers'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'header'
op|','
name|'value'
name|'in'
name|'resp'
op|'.'
name|'getheaders'
op|'('
op|')'
op|':'
newline|'\n'
indent|'        '
name|'resp_headers'
op|'['
name|'header'
op|'.'
name|'lower'
op|'('
op|')'
op|']'
op|'='
name|'value'
newline|'\n'
dedent|''
name|'return'
name|'resp_headers'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|direct_get_container
dedent|''
name|'def'
name|'direct_get_container'
op|'('
name|'node'
op|','
name|'part'
op|','
name|'account'
op|','
name|'container'
op|','
name|'marker'
op|'='
name|'None'
op|','
nl|'\n'
name|'limit'
op|'='
name|'None'
op|','
name|'prefix'
op|'='
name|'None'
op|','
name|'delimiter'
op|'='
name|'None'
op|','
nl|'\n'
name|'conn_timeout'
op|'='
number|'5'
op|','
name|'response_timeout'
op|'='
number|'15'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Get container listings directly from the container server.\n\n    :param node: node dictionary from the ring\n    :param part: partition the container is on\n    :param account: account name\n    :param container: container name\n    :param marker: marker query\n    :param limit: query limit\n    :param prefix: prefix query\n    :param delimeter: delimeter for the query\n    :param conn_timeout: timeout in seconds for establishing the connection\n    :param response_timeout: timeout in seconds for getting the response\n    :returns: a tuple of (response headers, a list of objects) The response\n              headers will be a dict and all header names will be lowercase.\n    """'
newline|'\n'
name|'path'
op|'='
string|"'/%s/%s'"
op|'%'
op|'('
name|'account'
op|','
name|'container'
op|')'
newline|'\n'
name|'qs'
op|'='
string|"'format=json'"
newline|'\n'
name|'if'
name|'marker'
op|':'
newline|'\n'
indent|'        '
name|'qs'
op|'+='
string|"'&marker=%s'"
op|'%'
name|'quote'
op|'('
name|'marker'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'limit'
op|':'
newline|'\n'
indent|'        '
name|'qs'
op|'+='
string|"'&limit=%d'"
op|'%'
name|'limit'
newline|'\n'
dedent|''
name|'if'
name|'prefix'
op|':'
newline|'\n'
indent|'        '
name|'qs'
op|'+='
string|"'&prefix=%s'"
op|'%'
name|'quote'
op|'('
name|'prefix'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'delimiter'
op|':'
newline|'\n'
indent|'        '
name|'qs'
op|'+='
string|"'&delimiter=%s'"
op|'%'
name|'quote'
op|'('
name|'delimiter'
op|')'
newline|'\n'
dedent|''
name|'with'
name|'Timeout'
op|'('
name|'conn_timeout'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'conn'
op|'='
name|'http_connect'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
nl|'\n'
string|"'GET'"
op|','
name|'path'
op|','
name|'query_string'
op|'='
name|'qs'
op|','
nl|'\n'
name|'headers'
op|'='
name|'gen_headers'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'with'
name|'Timeout'
op|'('
name|'response_timeout'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'resp'
op|'='
name|'conn'
op|'.'
name|'getresponse'
op|'('
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'is_success'
op|'('
name|'resp'
op|'.'
name|'status'
op|')'
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
name|'ClientException'
op|'('
nl|'\n'
string|"'Container server %s:%s direct GET %s gave stats %s'"
op|'%'
nl|'\n'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
nl|'\n'
name|'repr'
op|'('
string|"'/%s/%s%s'"
op|'%'
op|'('
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
name|'path'
op|')'
op|')'
op|','
nl|'\n'
name|'resp'
op|'.'
name|'status'
op|')'
op|','
nl|'\n'
name|'http_host'
op|'='
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'http_port'
op|'='
name|'node'
op|'['
string|"'port'"
op|']'
op|','
nl|'\n'
name|'http_device'
op|'='
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'http_status'
op|'='
name|'resp'
op|'.'
name|'status'
op|','
nl|'\n'
name|'http_reason'
op|'='
name|'resp'
op|'.'
name|'reason'
op|')'
newline|'\n'
dedent|''
name|'resp_headers'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'header'
op|','
name|'value'
name|'in'
name|'resp'
op|'.'
name|'getheaders'
op|'('
op|')'
op|':'
newline|'\n'
indent|'        '
name|'resp_headers'
op|'['
name|'header'
op|'.'
name|'lower'
op|'('
op|')'
op|']'
op|'='
name|'value'
newline|'\n'
dedent|''
name|'if'
name|'resp'
op|'.'
name|'status'
op|'=='
name|'HTTP_NO_CONTENT'
op|':'
newline|'\n'
indent|'        '
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'return'
name|'resp_headers'
op|','
op|'['
op|']'
newline|'\n'
dedent|''
name|'return'
name|'resp_headers'
op|','
name|'json_loads'
op|'('
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|direct_delete_container
dedent|''
name|'def'
name|'direct_delete_container'
op|'('
name|'node'
op|','
name|'part'
op|','
name|'account'
op|','
name|'container'
op|','
name|'conn_timeout'
op|'='
number|'5'
op|','
nl|'\n'
name|'response_timeout'
op|'='
number|'15'
op|','
name|'headers'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'if'
name|'headers'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
op|'}'
newline|'\n'
nl|'\n'
dedent|''
name|'path'
op|'='
string|"'/%s/%s'"
op|'%'
op|'('
name|'account'
op|','
name|'container'
op|')'
newline|'\n'
name|'with'
name|'Timeout'
op|'('
name|'conn_timeout'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'conn'
op|'='
name|'http_connect'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
nl|'\n'
string|"'DELETE'"
op|','
name|'path'
op|','
nl|'\n'
name|'headers'
op|'='
name|'gen_headers'
op|'('
name|'headers'
op|','
name|'True'
op|')'
op|')'
newline|'\n'
dedent|''
name|'with'
name|'Timeout'
op|'('
name|'response_timeout'
op|')'
op|':'
newline|'\n'
indent|'        '
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
dedent|''
name|'if'
name|'not'
name|'is_success'
op|'('
name|'resp'
op|'.'
name|'status'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ClientException'
op|'('
nl|'\n'
string|"'Container server %s:%s direct DELETE %s gave status %s'"
op|'%'
nl|'\n'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
nl|'\n'
name|'repr'
op|'('
string|"'/%s/%s%s'"
op|'%'
op|'('
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
name|'path'
op|')'
op|')'
op|','
name|'resp'
op|'.'
name|'status'
op|')'
op|','
nl|'\n'
name|'http_host'
op|'='
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'http_port'
op|'='
name|'node'
op|'['
string|"'port'"
op|']'
op|','
nl|'\n'
name|'http_device'
op|'='
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'http_status'
op|'='
name|'resp'
op|'.'
name|'status'
op|','
nl|'\n'
name|'http_reason'
op|'='
name|'resp'
op|'.'
name|'reason'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|direct_head_object
dedent|''
dedent|''
name|'def'
name|'direct_head_object'
op|'('
name|'node'
op|','
name|'part'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|','
name|'conn_timeout'
op|'='
number|'5'
op|','
nl|'\n'
name|'response_timeout'
op|'='
number|'15'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Request object information directly from the object server.\n\n    :param node: node dictionary from the ring\n    :param part: partition the container is on\n    :param account: account name\n    :param container: container name\n    :param obj: object name\n    :param conn_timeout: timeout in seconds for establishing the connection\n    :param response_timeout: timeout in seconds for getting the response\n    :returns: a dict containing the response\'s headers (all header names will\n              be lowercase)\n    """'
newline|'\n'
name|'path'
op|'='
string|"'/%s/%s/%s'"
op|'%'
op|'('
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
name|'with'
name|'Timeout'
op|'('
name|'conn_timeout'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'conn'
op|'='
name|'http_connect'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
nl|'\n'
string|"'HEAD'"
op|','
name|'path'
op|','
name|'headers'
op|'='
name|'gen_headers'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'with'
name|'Timeout'
op|'('
name|'response_timeout'
op|')'
op|':'
newline|'\n'
indent|'        '
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
dedent|''
name|'if'
name|'not'
name|'is_success'
op|'('
name|'resp'
op|'.'
name|'status'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ClientException'
op|'('
nl|'\n'
string|"'Object server %s:%s direct HEAD %s gave status %s'"
op|'%'
nl|'\n'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
nl|'\n'
name|'repr'
op|'('
string|"'/%s/%s%s'"
op|'%'
op|'('
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
name|'path'
op|')'
op|')'
op|','
nl|'\n'
name|'resp'
op|'.'
name|'status'
op|')'
op|','
nl|'\n'
name|'http_host'
op|'='
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'http_port'
op|'='
name|'node'
op|'['
string|"'port'"
op|']'
op|','
nl|'\n'
name|'http_device'
op|'='
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'http_status'
op|'='
name|'resp'
op|'.'
name|'status'
op|','
nl|'\n'
name|'http_reason'
op|'='
name|'resp'
op|'.'
name|'reason'
op|')'
newline|'\n'
dedent|''
name|'resp_headers'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'header'
op|','
name|'value'
name|'in'
name|'resp'
op|'.'
name|'getheaders'
op|'('
op|')'
op|':'
newline|'\n'
indent|'        '
name|'resp_headers'
op|'['
name|'header'
op|'.'
name|'lower'
op|'('
op|')'
op|']'
op|'='
name|'value'
newline|'\n'
dedent|''
name|'return'
name|'resp_headers'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|direct_get_object
dedent|''
name|'def'
name|'direct_get_object'
op|'('
name|'node'
op|','
name|'part'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|','
name|'conn_timeout'
op|'='
number|'5'
op|','
nl|'\n'
name|'response_timeout'
op|'='
number|'15'
op|','
name|'resp_chunk_size'
op|'='
name|'None'
op|','
name|'headers'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Get object directly from the object server.\n\n    :param node: node dictionary from the ring\n    :param part: partition the container is on\n    :param account: account name\n    :param container: container name\n    :param obj: object name\n    :param conn_timeout: timeout in seconds for establishing the connection\n    :param response_timeout: timeout in seconds for getting the response\n    :param resp_chunk_size: if defined, chunk size of data to read.\n    :param headers: dict to be passed into HTTPConnection headers\n    :returns: a tuple of (response headers, the object\'s contents) The response\n              headers will be a dict and all header names will be lowercase.\n    """'
newline|'\n'
name|'if'
name|'headers'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
op|'}'
newline|'\n'
nl|'\n'
dedent|''
name|'path'
op|'='
string|"'/%s/%s/%s'"
op|'%'
op|'('
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
name|'with'
name|'Timeout'
op|'('
name|'conn_timeout'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'conn'
op|'='
name|'http_connect'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
nl|'\n'
string|"'GET'"
op|','
name|'path'
op|','
name|'headers'
op|'='
name|'gen_headers'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
dedent|''
name|'with'
name|'Timeout'
op|'('
name|'response_timeout'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'resp'
op|'='
name|'conn'
op|'.'
name|'getresponse'
op|'('
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'is_success'
op|'('
name|'resp'
op|'.'
name|'status'
op|')'
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
name|'ClientException'
op|'('
nl|'\n'
string|"'Object server %s:%s direct GET %s gave status %s'"
op|'%'
nl|'\n'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
nl|'\n'
name|'repr'
op|'('
string|"'/%s/%s%s'"
op|'%'
op|'('
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
name|'path'
op|')'
op|')'
op|','
name|'resp'
op|'.'
name|'status'
op|')'
op|','
nl|'\n'
name|'http_host'
op|'='
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'http_port'
op|'='
name|'node'
op|'['
string|"'port'"
op|']'
op|','
nl|'\n'
name|'http_device'
op|'='
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'http_status'
op|'='
name|'resp'
op|'.'
name|'status'
op|','
nl|'\n'
name|'http_reason'
op|'='
name|'resp'
op|'.'
name|'reason'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'resp_chunk_size'
op|':'
newline|'\n'
nl|'\n'
DECL|function|_object_body
indent|'        '
name|'def'
name|'_object_body'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'buf'
op|'='
name|'resp'
op|'.'
name|'read'
op|'('
name|'resp_chunk_size'
op|')'
newline|'\n'
name|'while'
name|'buf'
op|':'
newline|'\n'
indent|'                '
name|'yield'
name|'buf'
newline|'\n'
name|'buf'
op|'='
name|'resp'
op|'.'
name|'read'
op|'('
name|'resp_chunk_size'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'object_body'
op|'='
name|'_object_body'
op|'('
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'        '
name|'object_body'
op|'='
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
dedent|''
name|'resp_headers'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'header'
op|','
name|'value'
name|'in'
name|'resp'
op|'.'
name|'getheaders'
op|'('
op|')'
op|':'
newline|'\n'
indent|'        '
name|'resp_headers'
op|'['
name|'header'
op|'.'
name|'lower'
op|'('
op|')'
op|']'
op|'='
name|'value'
newline|'\n'
dedent|''
name|'return'
name|'resp_headers'
op|','
name|'object_body'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|direct_put_object
dedent|''
name|'def'
name|'direct_put_object'
op|'('
name|'node'
op|','
name|'part'
op|','
name|'account'
op|','
name|'container'
op|','
name|'name'
op|','
name|'contents'
op|','
nl|'\n'
name|'content_length'
op|'='
name|'None'
op|','
name|'etag'
op|'='
name|'None'
op|','
name|'content_type'
op|'='
name|'None'
op|','
nl|'\n'
name|'headers'
op|'='
name|'None'
op|','
name|'conn_timeout'
op|'='
number|'5'
op|','
name|'response_timeout'
op|'='
number|'15'
op|','
nl|'\n'
name|'resp_chunk_size'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Put object directly from the object server.\n\n    :param node: node dictionary from the ring\n    :param part: partition the container is on\n    :param account: account name\n    :param container: container name\n    :param name: object name\n    :param contents: an iterable or string to read object data from\n    :param content_length: value to send as content-length header\n    :param etag: etag of contents\n    :param content_type: value to send as content-type header\n    :param headers: additional headers to include in the request\n    :param conn_timeout: timeout in seconds for establishing the connection\n    :param response_timeout: timeout in seconds for getting the response\n    :param chunk_size: if defined, chunk size of data to send.\n    :returns: etag from the server response\n    """'
newline|'\n'
comment|'# TODO: Add chunked puts'
nl|'\n'
name|'path'
op|'='
string|"'/%s/%s/%s'"
op|'%'
op|'('
name|'account'
op|','
name|'container'
op|','
name|'name'
op|')'
newline|'\n'
name|'if'
name|'headers'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
op|'}'
newline|'\n'
dedent|''
name|'if'
name|'etag'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'['
string|"'ETag'"
op|']'
op|'='
name|'etag'
op|'.'
name|'strip'
op|'('
string|'\'"\''
op|')'
newline|'\n'
dedent|''
name|'if'
name|'content_length'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'['
string|"'Content-Length'"
op|']'
op|'='
name|'str'
op|'('
name|'content_length'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'content_type'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'['
string|"'Content-Type'"
op|']'
op|'='
name|'content_type'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'['
string|"'Content-Type'"
op|']'
op|'='
string|"'application/octet-stream'"
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'contents'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'['
string|"'Content-Length'"
op|']'
op|'='
string|"'0'"
newline|'\n'
dedent|''
name|'if'
name|'isinstance'
op|'('
name|'contents'
op|','
name|'basestring'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'contents'
op|'='
op|'['
name|'contents'
op|']'
newline|'\n'
dedent|''
name|'with'
name|'Timeout'
op|'('
name|'conn_timeout'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'conn'
op|'='
name|'http_connect'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
nl|'\n'
string|"'PUT'"
op|','
name|'path'
op|','
name|'headers'
op|'='
name|'gen_headers'
op|'('
name|'headers'
op|','
name|'True'
op|')'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'chunk'
name|'in'
name|'contents'
op|':'
newline|'\n'
indent|'        '
name|'conn'
op|'.'
name|'send'
op|'('
name|'chunk'
op|')'
newline|'\n'
dedent|''
name|'with'
name|'Timeout'
op|'('
name|'response_timeout'
op|')'
op|':'
newline|'\n'
indent|'        '
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
dedent|''
name|'if'
name|'not'
name|'is_success'
op|'('
name|'resp'
op|'.'
name|'status'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ClientException'
op|'('
nl|'\n'
string|"'Object server %s:%s direct PUT %s gave status %s'"
op|'%'
nl|'\n'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
nl|'\n'
name|'repr'
op|'('
string|"'/%s/%s%s'"
op|'%'
op|'('
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
name|'path'
op|')'
op|')'
op|','
nl|'\n'
name|'resp'
op|'.'
name|'status'
op|')'
op|','
nl|'\n'
name|'http_host'
op|'='
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'http_port'
op|'='
name|'node'
op|'['
string|"'port'"
op|']'
op|','
nl|'\n'
name|'http_device'
op|'='
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'http_status'
op|'='
name|'resp'
op|'.'
name|'status'
op|','
nl|'\n'
name|'http_reason'
op|'='
name|'resp'
op|'.'
name|'reason'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'resp'
op|'.'
name|'getheader'
op|'('
string|"'etag'"
op|')'
op|'.'
name|'strip'
op|'('
string|'\'"\''
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|direct_post_object
dedent|''
name|'def'
name|'direct_post_object'
op|'('
name|'node'
op|','
name|'part'
op|','
name|'account'
op|','
name|'container'
op|','
name|'name'
op|','
name|'headers'
op|','
nl|'\n'
name|'conn_timeout'
op|'='
number|'5'
op|','
name|'response_timeout'
op|'='
number|'15'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Direct update to object metadata on object server.\n\n    :param node: node dictionary from the ring\n    :param part: partition the container is on\n    :param account: account name\n    :param container: container name\n    :param name: object name\n    :param headers: headers to store as metadata\n    :param conn_timeout: timeout in seconds for establishing the connection\n    :param response_timeout: timeout in seconds for getting the response\n    :raises ClientException: HTTP POST request failed\n    """'
newline|'\n'
name|'path'
op|'='
string|"'/%s/%s/%s'"
op|'%'
op|'('
name|'account'
op|','
name|'container'
op|','
name|'name'
op|')'
newline|'\n'
name|'with'
name|'Timeout'
op|'('
name|'conn_timeout'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'conn'
op|'='
name|'http_connect'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
nl|'\n'
string|"'POST'"
op|','
name|'path'
op|','
name|'headers'
op|'='
name|'gen_headers'
op|'('
name|'headers'
op|','
name|'True'
op|')'
op|')'
newline|'\n'
dedent|''
name|'with'
name|'Timeout'
op|'('
name|'response_timeout'
op|')'
op|':'
newline|'\n'
indent|'        '
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
dedent|''
name|'if'
name|'not'
name|'is_success'
op|'('
name|'resp'
op|'.'
name|'status'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ClientException'
op|'('
nl|'\n'
string|"'Object server %s:%s direct POST %s gave status %s'"
op|'%'
nl|'\n'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
nl|'\n'
name|'repr'
op|'('
string|"'/%s/%s%s'"
op|'%'
op|'('
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
name|'path'
op|')'
op|')'
op|','
nl|'\n'
name|'resp'
op|'.'
name|'status'
op|')'
op|','
nl|'\n'
name|'http_host'
op|'='
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'http_port'
op|'='
name|'node'
op|'['
string|"'port'"
op|']'
op|','
nl|'\n'
name|'http_device'
op|'='
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'http_status'
op|'='
name|'resp'
op|'.'
name|'status'
op|','
nl|'\n'
name|'http_reason'
op|'='
name|'resp'
op|'.'
name|'reason'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|direct_delete_object
dedent|''
dedent|''
name|'def'
name|'direct_delete_object'
op|'('
name|'node'
op|','
name|'part'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|','
nl|'\n'
name|'conn_timeout'
op|'='
number|'5'
op|','
name|'response_timeout'
op|'='
number|'15'
op|','
name|'headers'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Delete object directly from the object server.\n\n    :param node: node dictionary from the ring\n    :param part: partition the container is on\n    :param account: account name\n    :param container: container name\n    :param obj: object name\n    :param conn_timeout: timeout in seconds for establishing the connection\n    :param response_timeout: timeout in seconds for getting the response\n    :returns: response from server\n    """'
newline|'\n'
name|'if'
name|'headers'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
op|'}'
newline|'\n'
nl|'\n'
dedent|''
name|'path'
op|'='
string|"'/%s/%s/%s'"
op|'%'
op|'('
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
name|'with'
name|'Timeout'
op|'('
name|'conn_timeout'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'conn'
op|'='
name|'http_connect'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
nl|'\n'
string|"'DELETE'"
op|','
name|'path'
op|','
name|'headers'
op|'='
name|'gen_headers'
op|'('
name|'headers'
op|','
name|'True'
op|')'
op|')'
newline|'\n'
dedent|''
name|'with'
name|'Timeout'
op|'('
name|'response_timeout'
op|')'
op|':'
newline|'\n'
indent|'        '
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
dedent|''
name|'if'
name|'not'
name|'is_success'
op|'('
name|'resp'
op|'.'
name|'status'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ClientException'
op|'('
nl|'\n'
string|"'Object server %s:%s direct DELETE %s gave status %s'"
op|'%'
nl|'\n'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
nl|'\n'
name|'repr'
op|'('
string|"'/%s/%s%s'"
op|'%'
op|'('
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
name|'path'
op|')'
op|')'
op|','
nl|'\n'
name|'resp'
op|'.'
name|'status'
op|')'
op|','
nl|'\n'
name|'http_host'
op|'='
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'http_port'
op|'='
name|'node'
op|'['
string|"'port'"
op|']'
op|','
nl|'\n'
name|'http_device'
op|'='
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'http_status'
op|'='
name|'resp'
op|'.'
name|'status'
op|','
nl|'\n'
name|'http_reason'
op|'='
name|'resp'
op|'.'
name|'reason'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|retry
dedent|''
dedent|''
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
string|'"""\n    Helper function to retry a given function a number of times.\n\n    :param func: callable to be called\n    :param retries: number of retries\n    :param error_log: logger for errors\n    :param args: arguments to send to func\n    :param kwargs: keyward arguments to send to func (if retries or\n                   error_log are sent, they will be deleted from kwargs\n                   before sending on to func)\n    :returns: restult of func\n    """'
newline|'\n'
name|'retries'
op|'='
number|'5'
newline|'\n'
name|'if'
string|"'retries'"
name|'in'
name|'kwargs'
op|':'
newline|'\n'
indent|'        '
name|'retries'
op|'='
name|'kwargs'
op|'['
string|"'retries'"
op|']'
newline|'\n'
name|'del'
name|'kwargs'
op|'['
string|"'retries'"
op|']'
newline|'\n'
dedent|''
name|'error_log'
op|'='
name|'None'
newline|'\n'
name|'if'
string|"'error_log'"
name|'in'
name|'kwargs'
op|':'
newline|'\n'
indent|'        '
name|'error_log'
op|'='
name|'kwargs'
op|'['
string|"'error_log'"
op|']'
newline|'\n'
name|'del'
name|'kwargs'
op|'['
string|"'error_log'"
op|']'
newline|'\n'
dedent|''
name|'attempts'
op|'='
number|'0'
newline|'\n'
name|'backoff'
op|'='
number|'1'
newline|'\n'
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
name|'return'
name|'attempts'
op|','
name|'func'
op|'('
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
op|','
name|'Timeout'
op|')'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'error_log'
op|':'
newline|'\n'
indent|'                '
name|'error_log'
op|'('
name|'err'
op|')'
newline|'\n'
dedent|''
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
dedent|''
name|'except'
name|'ClientException'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'error_log'
op|':'
newline|'\n'
indent|'                '
name|'error_log'
op|'('
name|'err'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'attempts'
op|'>'
name|'retries'
name|'or'
name|'not'
name|'is_server_error'
op|'('
name|'err'
op|'.'
name|'http_status'
op|')'
name|'or'
name|'err'
op|'.'
name|'http_status'
op|'=='
name|'HTTP_INSUFFICIENT_STORAGE'
op|':'
newline|'\n'
indent|'                '
name|'raise'
newline|'\n'
dedent|''
dedent|''
name|'sleep'
op|'('
name|'backoff'
op|')'
newline|'\n'
name|'backoff'
op|'*='
number|'2'
newline|'\n'
comment|"# Shouldn't actually get down here, but just in case."
nl|'\n'
dedent|''
name|'if'
name|'args'
name|'and'
string|"'ip'"
name|'in'
name|'args'
op|'['
number|'0'
op|']'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ClientException'
op|'('
string|"'Raise too many retries'"
op|','
nl|'\n'
name|'http_host'
op|'='
name|'args'
op|'['
nl|'\n'
number|'0'
op|']'
op|'['
string|"'ip'"
op|']'
op|','
name|'http_port'
op|'='
name|'args'
op|'['
number|'0'
op|']'
op|'['
string|"'port'"
op|']'
op|','
nl|'\n'
name|'http_device'
op|'='
name|'args'
op|'['
number|'0'
op|']'
op|'['
string|"'device'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'ClientException'
op|'('
string|"'Raise too many retries'"
op|')'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
