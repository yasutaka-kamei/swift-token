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
string|'"""\nInternal client library for making calls directly to the servers rather than\nthrough the proxy.\n"""'
newline|'\n'
nl|'\n'
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
op|','
name|'unquote'
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
name|'swift'
op|'.'
name|'common'
op|'.'
name|'client'
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
name|'resp'
op|'.'
name|'status'
op|'<'
number|'200'
name|'or'
name|'resp'
op|'.'
name|'status'
op|'>='
number|'300'
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
string|'"""\n    Get container listings directly from the container server.\n\n    :param node: node dictionary from the ring\n    :param part: partition the container is on\n    :param account: account name\n    :param container: container name\n    :param marker: marker query\n    :param limit: query limit\n    :param prefix: prefix query\n    :param delimeter: delimeter for the query\n    :param conn_timeout: timeout in seconds for establishing the connection\n    :param response_timeout: timeout in seconds for getting the response\n    :returns: a tuple of (response headers, a list of objects) The response\n              headers will be a dict and all header names will be lowercase. \n    """'
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
string|"'format=json'"
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
name|'resp'
op|'.'
name|'status'
op|'<'
number|'200'
name|'or'
name|'resp'
op|'.'
name|'status'
op|'>='
number|'300'
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
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
nl|'\n'
name|'node'
op|'['
string|"'port'"
op|']'
op|','
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
number|'204'
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
op|'{'
op|'}'
op|')'
op|':'
newline|'\n'
indent|'    '
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
name|'headers'
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
name|'resp'
op|'.'
name|'status'
op|'<'
number|'200'
name|'or'
name|'resp'
op|'.'
name|'status'
op|'>='
number|'300'
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
name|'resp'
op|'.'
name|'status'
op|'<'
number|'200'
name|'or'
name|'resp'
op|'.'
name|'status'
op|'>='
number|'300'
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
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Get object directly from the object server.\n\n    :param node: node dictionary from the ring\n    :param part: partition the container is on\n    :param account: account name\n    :param container: container name\n    :param obj: object name\n    :param conn_timeout: timeout in seconds for establishing the connection\n    :param response_timeout: timeout in seconds for getting the response\n    :param resp_chunk_size: if defined, chunk size of data to read.\n    :returns: a tuple of (response headers, the object\'s contents) The response\n              headers will be a dict and all header names will be lowercase. \n    """'
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
string|"'GET'"
op|','
name|'path'
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
name|'resp'
op|'.'
name|'status'
op|'<'
number|'200'
name|'or'
name|'resp'
op|'.'
name|'status'
op|'>='
number|'300'
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
DECL|function|direct_delete_object
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
op|'{'
op|'}'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Delete object directly from the object server.\n\n    :param node: node dictionary from the ring\n    :param part: partition the container is on\n    :param account: account name\n    :param container: container name\n    :param obj: object name\n    :param conn_timeout: timeout in seconds for establishing the connection\n    :param response_timeout: timeout in seconds for getting the response\n    :returns: response from server\n    """'
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
name|'headers'
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
name|'resp'
op|'.'
name|'status'
op|'<'
number|'200'
name|'or'
name|'resp'
op|'.'
name|'status'
op|'>='
number|'300'
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
name|'err'
op|'.'
name|'http_status'
op|'<'
number|'500'
name|'or'
name|'err'
op|'.'
name|'http_status'
op|'=='
number|'507'
name|'or'
name|'err'
op|'.'
name|'http_status'
op|'>'
number|'599'
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
