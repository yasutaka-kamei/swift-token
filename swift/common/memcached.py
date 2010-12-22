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
string|'"""\nLucid comes with memcached: v1.4.2.  Protocol documentation for that\nversion is at:\n\nhttp://github.com/memcached/memcached/blob/1.4.2/doc/protocol.txt\n"""'
newline|'\n'
nl|'\n'
name|'import'
name|'cPickle'
name|'as'
name|'pickle'
newline|'\n'
name|'import'
name|'logging'
newline|'\n'
name|'import'
name|'socket'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'bisect'
name|'import'
name|'bisect'
newline|'\n'
name|'from'
name|'hashlib'
name|'import'
name|'md5'
newline|'\n'
nl|'\n'
DECL|variable|CONN_TIMEOUT
name|'CONN_TIMEOUT'
op|'='
number|'0.3'
newline|'\n'
DECL|variable|IO_TIMEOUT
name|'IO_TIMEOUT'
op|'='
number|'2.0'
newline|'\n'
DECL|variable|PICKLE_FLAG
name|'PICKLE_FLAG'
op|'='
number|'1'
newline|'\n'
DECL|variable|NODE_WEIGHT
name|'NODE_WEIGHT'
op|'='
number|'50'
newline|'\n'
DECL|variable|PICKLE_PROTOCOL
name|'PICKLE_PROTOCOL'
op|'='
number|'2'
newline|'\n'
DECL|variable|TRY_COUNT
name|'TRY_COUNT'
op|'='
number|'3'
newline|'\n'
nl|'\n'
comment|'# if ERROR_LIMIT_COUNT errors occur in ERROR_LIMIT_TIME seconds, the server'
nl|'\n'
comment|'# will be considered failed for ERROR_LIMIT_DURATION seconds.'
nl|'\n'
DECL|variable|ERROR_LIMIT_COUNT
name|'ERROR_LIMIT_COUNT'
op|'='
number|'10'
newline|'\n'
DECL|variable|ERROR_LIMIT_TIME
name|'ERROR_LIMIT_TIME'
op|'='
number|'60'
newline|'\n'
DECL|variable|ERROR_LIMIT_DURATION
name|'ERROR_LIMIT_DURATION'
op|'='
number|'300'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|md5hash
name|'def'
name|'md5hash'
op|'('
name|'key'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'return'
name|'md5'
op|'('
name|'key'
op|')'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|MemcacheRing
dedent|''
name|'class'
name|'MemcacheRing'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Simple, consistent-hashed memcache client.\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'servers'
op|','
name|'connect_timeout'
op|'='
name|'CONN_TIMEOUT'
op|','
nl|'\n'
name|'io_timeout'
op|'='
name|'IO_TIMEOUT'
op|','
name|'tries'
op|'='
name|'TRY_COUNT'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'_ring'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'_errors'
op|'='
name|'dict'
op|'('
op|'('
op|'('
name|'serv'
op|','
op|'['
op|']'
op|')'
name|'for'
name|'serv'
name|'in'
name|'servers'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_error_limited'
op|'='
name|'dict'
op|'('
op|'('
op|'('
name|'serv'
op|','
number|'0'
op|')'
name|'for'
name|'serv'
name|'in'
name|'servers'
op|')'
op|')'
newline|'\n'
name|'for'
name|'server'
name|'in'
name|'sorted'
op|'('
name|'servers'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'i'
name|'in'
name|'xrange'
op|'('
name|'NODE_WEIGHT'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'_ring'
op|'['
name|'md5hash'
op|'('
string|"'%s-%s'"
op|'%'
op|'('
name|'server'
op|','
name|'i'
op|')'
op|')'
op|']'
op|'='
name|'server'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'_tries'
op|'='
name|'tries'
name|'if'
name|'tries'
op|'<='
name|'len'
op|'('
name|'servers'
op|')'
name|'else'
name|'len'
op|'('
name|'servers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_sorted'
op|'='
name|'sorted'
op|'('
name|'self'
op|'.'
name|'_ring'
op|'.'
name|'keys'
op|'('
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_client_cache'
op|'='
name|'dict'
op|'('
op|'('
op|'('
name|'server'
op|','
op|'['
op|']'
op|')'
name|'for'
name|'server'
name|'in'
name|'servers'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_connect_timeout'
op|'='
name|'connect_timeout'
newline|'\n'
name|'self'
op|'.'
name|'_io_timeout'
op|'='
name|'io_timeout'
newline|'\n'
nl|'\n'
DECL|member|_exception_occurred
dedent|''
name|'def'
name|'_exception_occurred'
op|'('
name|'self'
op|','
name|'server'
op|','
name|'e'
op|','
name|'action'
op|'='
string|"'talking'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'isinstance'
op|'('
name|'e'
op|','
name|'socket'
op|'.'
name|'timeout'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'logging'
op|'.'
name|'error'
op|'('
name|'_'
op|'('
string|'"Timeout %(action)s to memcached: %(server)s"'
op|')'
op|','
nl|'\n'
op|'{'
string|"'action'"
op|':'
name|'action'
op|','
string|"'server'"
op|':'
name|'server'
op|'}'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'logging'
op|'.'
name|'exception'
op|'('
name|'_'
op|'('
string|'"Error %(action)s to memcached: %(server)s"'
op|')'
op|','
nl|'\n'
op|'{'
string|"'action'"
op|':'
name|'action'
op|','
string|"'server'"
op|':'
name|'server'
op|'}'
op|')'
newline|'\n'
dedent|''
name|'now'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_errors'
op|'['
name|'server'
op|']'
op|'.'
name|'append'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'self'
op|'.'
name|'_errors'
op|'['
name|'server'
op|']'
op|')'
op|'>'
name|'ERROR_LIMIT_COUNT'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_errors'
op|'['
name|'server'
op|']'
op|'='
op|'['
name|'err'
name|'for'
name|'err'
name|'in'
name|'self'
op|'.'
name|'_errors'
op|'['
name|'server'
op|']'
nl|'\n'
name|'if'
name|'err'
op|'>'
name|'now'
op|'-'
name|'ERROR_LIMIT_TIME'
op|']'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'self'
op|'.'
name|'_errors'
op|'['
name|'server'
op|']'
op|')'
op|'>'
name|'ERROR_LIMIT_COUNT'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'_error_limited'
op|'['
name|'server'
op|']'
op|'='
name|'now'
op|'+'
name|'ERROR_LIMIT_DURATION'
newline|'\n'
name|'logging'
op|'.'
name|'error'
op|'('
name|'_'
op|'('
string|"'Error limiting server %s'"
op|')'
op|','
name|'server'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_get_conns
dedent|''
dedent|''
dedent|''
name|'def'
name|'_get_conns'
op|'('
name|'self'
op|','
name|'key'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Retrieves a server conn from the pool, or connects a new one.\n        Chooses the server based on a consistent hash of "key".\n        """'
newline|'\n'
name|'pos'
op|'='
name|'bisect'
op|'('
name|'self'
op|'.'
name|'_sorted'
op|','
name|'key'
op|')'
newline|'\n'
name|'served'
op|'='
op|'['
op|']'
newline|'\n'
name|'while'
name|'len'
op|'('
name|'served'
op|')'
op|'<'
name|'self'
op|'.'
name|'_tries'
op|':'
newline|'\n'
indent|'            '
name|'pos'
op|'='
op|'('
name|'pos'
op|'+'
number|'1'
op|')'
op|'%'
name|'len'
op|'('
name|'self'
op|'.'
name|'_sorted'
op|')'
newline|'\n'
name|'server'
op|'='
name|'self'
op|'.'
name|'_ring'
op|'['
name|'self'
op|'.'
name|'_sorted'
op|'['
name|'pos'
op|']'
op|']'
newline|'\n'
name|'if'
name|'server'
name|'in'
name|'served'
op|':'
newline|'\n'
indent|'                '
name|'continue'
newline|'\n'
dedent|''
name|'served'
op|'.'
name|'append'
op|'('
name|'server'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'_error_limited'
op|'['
name|'server'
op|']'
op|'>'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'continue'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'fp'
op|','
name|'sock'
op|'='
name|'self'
op|'.'
name|'_client_cache'
op|'['
name|'server'
op|']'
op|'.'
name|'pop'
op|'('
op|')'
newline|'\n'
name|'yield'
name|'server'
op|','
name|'fp'
op|','
name|'sock'
newline|'\n'
dedent|''
name|'except'
name|'IndexError'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'host'
op|','
name|'port'
op|'='
name|'server'
op|'.'
name|'split'
op|'('
string|"':'"
op|')'
newline|'\n'
name|'sock'
op|'='
name|'socket'
op|'.'
name|'socket'
op|'('
name|'socket'
op|'.'
name|'AF_INET'
op|','
name|'socket'
op|'.'
name|'SOCK_STREAM'
op|')'
newline|'\n'
name|'sock'
op|'.'
name|'setsockopt'
op|'('
name|'socket'
op|'.'
name|'IPPROTO_TCP'
op|','
name|'socket'
op|'.'
name|'TCP_NODELAY'
op|','
number|'1'
op|')'
newline|'\n'
name|'sock'
op|'.'
name|'settimeout'
op|'('
name|'self'
op|'.'
name|'_connect_timeout'
op|')'
newline|'\n'
name|'sock'
op|'.'
name|'connect'
op|'('
op|'('
name|'host'
op|','
name|'int'
op|'('
name|'port'
op|')'
op|')'
op|')'
newline|'\n'
name|'sock'
op|'.'
name|'settimeout'
op|'('
name|'self'
op|'.'
name|'_io_timeout'
op|')'
newline|'\n'
name|'yield'
name|'server'
op|','
name|'sock'
op|'.'
name|'makefile'
op|'('
op|')'
op|','
name|'sock'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|','
name|'e'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'_exception_occurred'
op|'('
name|'server'
op|','
name|'e'
op|','
string|"'connecting'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|_return_conn
dedent|''
dedent|''
dedent|''
dedent|''
name|'def'
name|'_return_conn'
op|'('
name|'self'
op|','
name|'server'
op|','
name|'fp'
op|','
name|'sock'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'""" Returns a server connection to the pool """'
newline|'\n'
name|'self'
op|'.'
name|'_client_cache'
op|'['
name|'server'
op|']'
op|'.'
name|'append'
op|'('
op|'('
name|'fp'
op|','
name|'sock'
op|')'
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
name|'serialize'
op|'='
name|'True'
op|','
name|'timeout'
op|'='
number|'0'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Set a key/value pair in memcache\n\n        :param key: key\n        :param value: value\n        :param serialize: if True, value is pickled before sending to memcache\n        :param timeout: ttl in memcache\n        """'
newline|'\n'
name|'key'
op|'='
name|'md5hash'
op|'('
name|'key'
op|')'
newline|'\n'
name|'if'
name|'timeout'
op|'>'
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'timeout'
op|'+='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
dedent|''
name|'flags'
op|'='
number|'0'
newline|'\n'
name|'if'
name|'serialize'
op|':'
newline|'\n'
indent|'            '
name|'value'
op|'='
name|'pickle'
op|'.'
name|'dumps'
op|'('
name|'value'
op|','
name|'PICKLE_PROTOCOL'
op|')'
newline|'\n'
name|'flags'
op|'|='
name|'PICKLE_FLAG'
newline|'\n'
dedent|''
name|'for'
op|'('
name|'server'
op|','
name|'fp'
op|','
name|'sock'
op|')'
name|'in'
name|'self'
op|'.'
name|'_get_conns'
op|'('
name|'key'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'sock'
op|'.'
name|'sendall'
op|'('
string|"'set %s %d %d %s noreply\\r\\n%s\\r\\n'"
op|'%'
op|'('
name|'key'
op|','
name|'flags'
op|','
name|'timeout'
op|','
name|'len'
op|'('
name|'value'
op|')'
op|','
name|'value'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_return_conn'
op|'('
name|'server'
op|','
name|'fp'
op|','
name|'sock'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|','
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'_exception_occurred'
op|'('
name|'server'
op|','
name|'e'
op|')'
newline|'\n'
nl|'\n'
DECL|member|get
dedent|''
dedent|''
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
string|'"""\n        Gets the object specified by key.  It will also unpickle the object\n        before returning if it is pickled in memcache.\n\n        :param key: key\n        :returns: value of the key in memcache\n        """'
newline|'\n'
name|'key'
op|'='
name|'md5hash'
op|'('
name|'key'
op|')'
newline|'\n'
name|'value'
op|'='
name|'None'
newline|'\n'
name|'for'
op|'('
name|'server'
op|','
name|'fp'
op|','
name|'sock'
op|')'
name|'in'
name|'self'
op|'.'
name|'_get_conns'
op|'('
name|'key'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'sock'
op|'.'
name|'sendall'
op|'('
string|"'get %s\\r\\n'"
op|'%'
name|'key'
op|')'
newline|'\n'
name|'line'
op|'='
name|'fp'
op|'.'
name|'readline'
op|'('
op|')'
op|'.'
name|'strip'
op|'('
op|')'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'while'
name|'line'
op|'['
number|'0'
op|']'
op|'.'
name|'upper'
op|'('
op|')'
op|'!='
string|"'END'"
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'line'
op|'['
number|'0'
op|']'
op|'.'
name|'upper'
op|'('
op|')'
op|'=='
string|"'VALUE'"
name|'and'
name|'line'
op|'['
number|'1'
op|']'
op|'=='
name|'key'
op|':'
newline|'\n'
indent|'                        '
name|'size'
op|'='
name|'int'
op|'('
name|'line'
op|'['
number|'3'
op|']'
op|')'
newline|'\n'
name|'value'
op|'='
name|'fp'
op|'.'
name|'read'
op|'('
name|'size'
op|')'
newline|'\n'
name|'if'
name|'int'
op|'('
name|'line'
op|'['
number|'2'
op|']'
op|')'
op|'&'
name|'PICKLE_FLAG'
op|':'
newline|'\n'
indent|'                            '
name|'value'
op|'='
name|'pickle'
op|'.'
name|'loads'
op|'('
name|'value'
op|')'
newline|'\n'
dedent|''
name|'fp'
op|'.'
name|'readline'
op|'('
op|')'
newline|'\n'
dedent|''
name|'line'
op|'='
name|'fp'
op|'.'
name|'readline'
op|'('
op|')'
op|'.'
name|'strip'
op|'('
op|')'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'_return_conn'
op|'('
name|'server'
op|','
name|'fp'
op|','
name|'sock'
op|')'
newline|'\n'
name|'return'
name|'value'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|','
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'_exception_occurred'
op|'('
name|'server'
op|','
name|'e'
op|')'
newline|'\n'
nl|'\n'
DECL|member|incr
dedent|''
dedent|''
dedent|''
name|'def'
name|'incr'
op|'('
name|'self'
op|','
name|'key'
op|','
name|'delta'
op|'='
number|'1'
op|','
name|'timeout'
op|'='
number|'0'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Increments a key which has a numeric value by delta.\n        If the key can\'t be found, it\'s added as delta or 0 if delta < 0.\n        If passed a negative number, will use memcached\'s decr. Returns\n        the int stored in memcached\n        Note: The data memcached stores as the result of incr/decr is\n        an unsigned int.  decr\'s that result in a number below 0 are\n        stored as 0.\n\n        :param key: key\n        :param delta: amount to add to the value of key (or set as the value\n                      if the key is not found) will be cast to an int\n        :param timeout: ttl in memcache\n        """'
newline|'\n'
name|'key'
op|'='
name|'md5hash'
op|'('
name|'key'
op|')'
newline|'\n'
name|'command'
op|'='
string|"'incr'"
newline|'\n'
name|'if'
name|'delta'
op|'<'
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'command'
op|'='
string|"'decr'"
newline|'\n'
dedent|''
name|'delta'
op|'='
name|'str'
op|'('
name|'abs'
op|'('
name|'int'
op|'('
name|'delta'
op|')'
op|')'
op|')'
newline|'\n'
name|'for'
op|'('
name|'server'
op|','
name|'fp'
op|','
name|'sock'
op|')'
name|'in'
name|'self'
op|'.'
name|'_get_conns'
op|'('
name|'key'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'sock'
op|'.'
name|'sendall'
op|'('
string|"'%s %s %s\\r\\n'"
op|'%'
op|'('
name|'command'
op|','
name|'key'
op|','
name|'delta'
op|')'
op|')'
newline|'\n'
name|'line'
op|'='
name|'fp'
op|'.'
name|'readline'
op|'('
op|')'
op|'.'
name|'strip'
op|'('
op|')'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'if'
name|'line'
op|'['
number|'0'
op|']'
op|'.'
name|'upper'
op|'('
op|')'
op|'=='
string|"'NOT_FOUND'"
op|':'
newline|'\n'
indent|'                    '
name|'add_val'
op|'='
name|'delta'
newline|'\n'
name|'if'
name|'command'
op|'=='
string|"'decr'"
op|':'
newline|'\n'
indent|'                        '
name|'add_val'
op|'='
string|"'0'"
newline|'\n'
dedent|''
name|'sock'
op|'.'
name|'sendall'
op|'('
string|"'add %s %d %d %s\\r\\n%s\\r\\n'"
op|'%'
op|'('
name|'key'
op|','
number|'0'
op|','
name|'timeout'
op|','
name|'len'
op|'('
name|'add_val'
op|')'
op|','
name|'add_val'
op|')'
op|')'
newline|'\n'
name|'line'
op|'='
name|'fp'
op|'.'
name|'readline'
op|'('
op|')'
op|'.'
name|'strip'
op|'('
op|')'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'if'
name|'line'
op|'['
number|'0'
op|']'
op|'.'
name|'upper'
op|'('
op|')'
op|'=='
string|"'NOT_STORED'"
op|':'
newline|'\n'
indent|'                        '
name|'sock'
op|'.'
name|'sendall'
op|'('
string|"'%s %s %s\\r\\n'"
op|'%'
op|'('
name|'command'
op|','
name|'key'
op|','
name|'delta'
op|')'
op|')'
newline|'\n'
name|'line'
op|'='
name|'fp'
op|'.'
name|'readline'
op|'('
op|')'
op|'.'
name|'strip'
op|'('
op|')'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'ret'
op|'='
name|'int'
op|'('
name|'line'
op|'['
number|'0'
op|']'
op|'.'
name|'strip'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'ret'
op|'='
name|'int'
op|'('
name|'add_val'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'ret'
op|'='
name|'int'
op|'('
name|'line'
op|'['
number|'0'
op|']'
op|'.'
name|'strip'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'_return_conn'
op|'('
name|'server'
op|','
name|'fp'
op|','
name|'sock'
op|')'
newline|'\n'
name|'return'
name|'ret'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|','
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'_exception_occurred'
op|'('
name|'server'
op|','
name|'e'
op|')'
newline|'\n'
nl|'\n'
DECL|member|decr
dedent|''
dedent|''
dedent|''
name|'def'
name|'decr'
op|'('
name|'self'
op|','
name|'key'
op|','
name|'delta'
op|'='
number|'1'
op|','
name|'timeout'
op|'='
number|'0'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Decrements a key which has a numeric value by delta. Calls incr with\n        -delta.\n\n        :param key: key\n        :param delta: amount to subtract to the value of key (or set the\n                      value to 0 if the key is not found) will be cast to\n                      an int\n        :param timeout: ttl in memcache\n        """'
newline|'\n'
name|'self'
op|'.'
name|'incr'
op|'('
name|'key'
op|','
name|'delta'
op|'='
op|'-'
name|'delta'
op|','
name|'timeout'
op|'='
name|'timeout'
op|')'
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
string|'"""\n        Deletes a key/value pair from memcache.\n\n        :param key: key to be deleted\n        """'
newline|'\n'
name|'key'
op|'='
name|'md5hash'
op|'('
name|'key'
op|')'
newline|'\n'
name|'for'
op|'('
name|'server'
op|','
name|'fp'
op|','
name|'sock'
op|')'
name|'in'
name|'self'
op|'.'
name|'_get_conns'
op|'('
name|'key'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'sock'
op|'.'
name|'sendall'
op|'('
string|"'delete %s noreply\\r\\n'"
op|'%'
name|'key'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_return_conn'
op|'('
name|'server'
op|','
name|'fp'
op|','
name|'sock'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|','
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'_exception_occurred'
op|'('
name|'server'
op|','
name|'e'
op|')'
newline|'\n'
nl|'\n'
DECL|member|set_multi
dedent|''
dedent|''
dedent|''
name|'def'
name|'set_multi'
op|'('
name|'self'
op|','
name|'mapping'
op|','
name|'server_key'
op|','
name|'serialize'
op|'='
name|'True'
op|','
name|'timeout'
op|'='
number|'0'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Sets multiple key/value pairs in memcache.\n\n        :param mapping: dictonary of keys and values to be set in memcache\n        :param servery_key: key to use in determining which server in the ring\n                            is used\n        :param serialize: if True, value is pickled before sending to memcache\n        :param timeout: ttl for memcache\n        """'
newline|'\n'
name|'server_key'
op|'='
name|'md5hash'
op|'('
name|'server_key'
op|')'
newline|'\n'
name|'if'
name|'timeout'
op|'>'
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'timeout'
op|'+='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
dedent|''
name|'msg'
op|'='
string|"''"
newline|'\n'
name|'for'
name|'key'
op|','
name|'value'
name|'in'
name|'mapping'
op|'.'
name|'iteritems'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'key'
op|'='
name|'md5hash'
op|'('
name|'key'
op|')'
newline|'\n'
name|'flags'
op|'='
number|'0'
newline|'\n'
name|'if'
name|'serialize'
op|':'
newline|'\n'
indent|'                '
name|'value'
op|'='
name|'pickle'
op|'.'
name|'dumps'
op|'('
name|'value'
op|','
name|'PICKLE_PROTOCOL'
op|')'
newline|'\n'
name|'flags'
op|'|='
name|'PICKLE_FLAG'
newline|'\n'
dedent|''
name|'msg'
op|'+='
op|'('
string|"'set %s %d %d %s noreply\\r\\n%s\\r\\n'"
op|'%'
nl|'\n'
op|'('
name|'key'
op|','
name|'flags'
op|','
name|'timeout'
op|','
name|'len'
op|'('
name|'value'
op|')'
op|','
name|'value'
op|')'
op|')'
newline|'\n'
dedent|''
name|'for'
op|'('
name|'server'
op|','
name|'fp'
op|','
name|'sock'
op|')'
name|'in'
name|'self'
op|'.'
name|'_get_conns'
op|'('
name|'server_key'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'sock'
op|'.'
name|'sendall'
op|'('
name|'msg'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_return_conn'
op|'('
name|'server'
op|','
name|'fp'
op|','
name|'sock'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|','
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'_exception_occurred'
op|'('
name|'server'
op|','
name|'e'
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_multi
dedent|''
dedent|''
dedent|''
name|'def'
name|'get_multi'
op|'('
name|'self'
op|','
name|'keys'
op|','
name|'server_key'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Gets multiple values from memcache for the given keys.\n\n        :param keys: keys for values to be retrieved from memcache\n        :param servery_key: key to use in determining which server in the ring\n                            is used\n        :returns: list of values\n        """'
newline|'\n'
name|'server_key'
op|'='
name|'md5hash'
op|'('
name|'server_key'
op|')'
newline|'\n'
name|'keys'
op|'='
op|'['
name|'md5hash'
op|'('
name|'key'
op|')'
name|'for'
name|'key'
name|'in'
name|'keys'
op|']'
newline|'\n'
name|'for'
op|'('
name|'server'
op|','
name|'fp'
op|','
name|'sock'
op|')'
name|'in'
name|'self'
op|'.'
name|'_get_conns'
op|'('
name|'server_key'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'sock'
op|'.'
name|'sendall'
op|'('
string|"'get %s\\r\\n'"
op|'%'
string|"' '"
op|'.'
name|'join'
op|'('
name|'keys'
op|')'
op|')'
newline|'\n'
name|'line'
op|'='
name|'fp'
op|'.'
name|'readline'
op|'('
op|')'
op|'.'
name|'strip'
op|'('
op|')'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'responses'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'while'
name|'line'
op|'['
number|'0'
op|']'
op|'.'
name|'upper'
op|'('
op|')'
op|'!='
string|"'END'"
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'line'
op|'['
number|'0'
op|']'
op|'.'
name|'upper'
op|'('
op|')'
op|'=='
string|"'VALUE'"
op|':'
newline|'\n'
indent|'                        '
name|'size'
op|'='
name|'int'
op|'('
name|'line'
op|'['
number|'3'
op|']'
op|')'
newline|'\n'
name|'value'
op|'='
name|'fp'
op|'.'
name|'read'
op|'('
name|'size'
op|')'
newline|'\n'
name|'if'
name|'int'
op|'('
name|'line'
op|'['
number|'2'
op|']'
op|')'
op|'&'
name|'PICKLE_FLAG'
op|':'
newline|'\n'
indent|'                            '
name|'value'
op|'='
name|'pickle'
op|'.'
name|'loads'
op|'('
name|'value'
op|')'
newline|'\n'
dedent|''
name|'responses'
op|'['
name|'line'
op|'['
number|'1'
op|']'
op|']'
op|'='
name|'value'
newline|'\n'
name|'fp'
op|'.'
name|'readline'
op|'('
op|')'
newline|'\n'
dedent|''
name|'line'
op|'='
name|'fp'
op|'.'
name|'readline'
op|'('
op|')'
op|'.'
name|'strip'
op|'('
op|')'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
dedent|''
name|'values'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'key'
name|'in'
name|'keys'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'key'
name|'in'
name|'responses'
op|':'
newline|'\n'
indent|'                        '
name|'values'
op|'.'
name|'append'
op|'('
name|'responses'
op|'['
name|'key'
op|']'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'values'
op|'.'
name|'append'
op|'('
name|'None'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'_return_conn'
op|'('
name|'server'
op|','
name|'fp'
op|','
name|'sock'
op|')'
newline|'\n'
name|'return'
name|'values'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|','
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'_exception_occurred'
op|'('
name|'server'
op|','
name|'e'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
endmarker|''
end_unit
