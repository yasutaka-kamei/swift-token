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
name|'import'
name|'os'
newline|'\n'
name|'from'
name|'ConfigParser'
name|'import'
name|'ConfigParser'
op|','
name|'NoSectionError'
op|','
name|'NoOptionError'
newline|'\n'
nl|'\n'
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
DECL|class|MemcacheMiddleware
name|'class'
name|'MemcacheMiddleware'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Caching middleware that manages caching in swift.\n    """'
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
name|'memcache_servers'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'memcache_servers'"
op|')'
newline|'\n'
name|'serialization_format'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'memcache_serialization_support'"
op|')'
newline|'\n'
name|'max_conns'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'max_connections'"
op|','
number|'2'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'memcache_servers'
name|'or'
name|'serialization_format'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
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
string|"'memcache.conf'"
op|')'
newline|'\n'
name|'memcache_conf'
op|'='
name|'ConfigParser'
op|'('
op|')'
newline|'\n'
name|'if'
name|'memcache_conf'
op|'.'
name|'read'
op|'('
name|'path'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'not'
name|'self'
op|'.'
name|'memcache_servers'
op|':'
newline|'\n'
indent|'                    '
name|'try'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'memcache_servers'
op|'='
name|'memcache_conf'
op|'.'
name|'get'
op|'('
string|"'memcache'"
op|','
string|"'memcache_servers'"
op|')'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'NoSectionError'
op|','
name|'NoOptionError'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'pass'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'serialization_format'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                    '
name|'try'
op|':'
newline|'\n'
indent|'                        '
name|'serialization_format'
op|'='
name|'memcache_conf'
op|'.'
name|'get'
op|'('
string|"'memcache'"
op|','
nl|'\n'
string|"'memcache_serialization_support'"
op|')'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'NoSectionError'
op|','
name|'NoOptionError'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'pass'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
name|'if'
name|'not'
name|'self'
op|'.'
name|'memcache_servers'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'memcache_servers'
op|'='
string|"'127.0.0.1:11211'"
newline|'\n'
dedent|''
name|'if'
name|'serialization_format'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'serialization_format'
op|'='
number|'2'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'serialization_format'
op|'='
name|'int'
op|'('
name|'serialization_format'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'memcache'
op|'='
name|'MemcacheRing'
op|'('
nl|'\n'
op|'['
name|'s'
op|'.'
name|'strip'
op|'('
op|')'
name|'for'
name|'s'
name|'in'
name|'self'
op|'.'
name|'memcache_servers'
op|'.'
name|'split'
op|'('
string|"','"
op|')'
name|'if'
name|'s'
op|'.'
name|'strip'
op|'('
op|')'
op|']'
op|','
nl|'\n'
name|'allow_pickle'
op|'='
op|'('
name|'serialization_format'
op|'=='
number|'0'
op|')'
op|','
nl|'\n'
name|'allow_unpickle'
op|'='
op|'('
name|'serialization_format'
op|'<='
number|'1'
op|')'
op|','
nl|'\n'
name|'max_conns'
op|'='
name|'max_conns'
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
name|'env'
op|'['
string|"'swift.cache'"
op|']'
op|'='
name|'self'
op|'.'
name|'memcache'
newline|'\n'
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
name|'MemcacheMiddleware'
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
