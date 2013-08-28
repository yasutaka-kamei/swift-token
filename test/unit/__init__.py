begin_unit
string|'""" Swift tests """'
newline|'\n'
nl|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'copy'
newline|'\n'
name|'import'
name|'logging'
newline|'\n'
name|'from'
name|'sys'
name|'import'
name|'exc_info'
newline|'\n'
name|'from'
name|'contextlib'
name|'import'
name|'contextmanager'
newline|'\n'
name|'from'
name|'collections'
name|'import'
name|'defaultdict'
newline|'\n'
name|'from'
name|'tempfile'
name|'import'
name|'NamedTemporaryFile'
newline|'\n'
name|'from'
name|'eventlet'
op|'.'
name|'green'
name|'import'
name|'socket'
newline|'\n'
name|'from'
name|'tempfile'
name|'import'
name|'mkdtemp'
newline|'\n'
name|'from'
name|'shutil'
name|'import'
name|'rmtree'
newline|'\n'
name|'from'
name|'test'
name|'import'
name|'get_config'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'config_true_value'
newline|'\n'
name|'from'
name|'hashlib'
name|'import'
name|'md5'
newline|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'sleep'
op|','
name|'Timeout'
newline|'\n'
name|'import'
name|'logging'
op|'.'
name|'handlers'
newline|'\n'
name|'from'
name|'httplib'
name|'import'
name|'HTTPException'
newline|'\n'
nl|'\n'
DECL|class|FakeRing
name|'class'
name|'FakeRing'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'replicas'
op|'='
number|'3'
op|','
name|'max_more_nodes'
op|'='
number|'0'
op|')'
op|':'
newline|'\n'
comment|'# 9 total nodes (6 more past the initial 3) is the cap, no matter if'
nl|'\n'
comment|'# this is set higher, or R^2 for R replicas'
nl|'\n'
indent|'        '
name|'self'
op|'.'
name|'replicas'
op|'='
name|'replicas'
newline|'\n'
name|'self'
op|'.'
name|'max_more_nodes'
op|'='
name|'max_more_nodes'
newline|'\n'
name|'self'
op|'.'
name|'devs'
op|'='
op|'{'
op|'}'
newline|'\n'
nl|'\n'
DECL|member|set_replicas
dedent|''
name|'def'
name|'set_replicas'
op|'('
name|'self'
op|','
name|'replicas'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'replicas'
op|'='
name|'replicas'
newline|'\n'
name|'self'
op|'.'
name|'devs'
op|'='
op|'{'
op|'}'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'property'
newline|'\n'
DECL|member|replica_count
name|'def'
name|'replica_count'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'self'
op|'.'
name|'replicas'
newline|'\n'
nl|'\n'
DECL|member|get_part
dedent|''
name|'def'
name|'get_part'
op|'('
name|'self'
op|','
name|'account'
op|','
name|'container'
op|'='
name|'None'
op|','
name|'obj'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
number|'1'
newline|'\n'
nl|'\n'
DECL|member|get_nodes
dedent|''
name|'def'
name|'get_nodes'
op|'('
name|'self'
op|','
name|'account'
op|','
name|'container'
op|'='
name|'None'
op|','
name|'obj'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'devs'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'x'
name|'in'
name|'xrange'
op|'('
name|'self'
op|'.'
name|'replicas'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'devs'
op|'.'
name|'append'
op|'('
name|'self'
op|'.'
name|'devs'
op|'.'
name|'get'
op|'('
name|'x'
op|')'
op|')'
newline|'\n'
name|'if'
name|'devs'
op|'['
name|'x'
op|']'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'devs'
op|'['
name|'x'
op|']'
op|'='
name|'devs'
op|'['
name|'x'
op|']'
op|'='
op|'{'
string|"'ip'"
op|':'
string|"'10.0.0.%s'"
op|'%'
name|'x'
op|','
nl|'\n'
string|"'port'"
op|':'
number|'1000'
op|'+'
name|'x'
op|','
nl|'\n'
string|"'device'"
op|':'
string|"'sd'"
op|'+'
op|'('
name|'chr'
op|'('
name|'ord'
op|'('
string|"'a'"
op|')'
op|'+'
name|'x'
op|')'
op|')'
op|','
nl|'\n'
string|"'zone'"
op|':'
name|'x'
op|'%'
number|'3'
op|','
nl|'\n'
string|"'region'"
op|':'
name|'x'
op|'%'
number|'2'
op|','
nl|'\n'
string|"'id'"
op|':'
name|'x'
op|'}'
newline|'\n'
dedent|''
dedent|''
name|'return'
number|'1'
op|','
name|'devs'
newline|'\n'
nl|'\n'
DECL|member|get_part_nodes
dedent|''
name|'def'
name|'get_part_nodes'
op|'('
name|'self'
op|','
name|'part'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'self'
op|'.'
name|'get_nodes'
op|'('
string|"'blah'"
op|')'
op|'['
number|'1'
op|']'
newline|'\n'
nl|'\n'
DECL|member|get_more_nodes
dedent|''
name|'def'
name|'get_more_nodes'
op|'('
name|'self'
op|','
name|'part'
op|')'
op|':'
newline|'\n'
comment|'# replicas^2 is the true cap'
nl|'\n'
indent|'        '
name|'for'
name|'x'
name|'in'
name|'xrange'
op|'('
name|'self'
op|'.'
name|'replicas'
op|','
name|'min'
op|'('
name|'self'
op|'.'
name|'replicas'
op|'+'
name|'self'
op|'.'
name|'max_more_nodes'
op|','
nl|'\n'
name|'self'
op|'.'
name|'replicas'
op|'*'
name|'self'
op|'.'
name|'replicas'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'yield'
op|'{'
string|"'ip'"
op|':'
string|"'10.0.0.%s'"
op|'%'
name|'x'
op|','
nl|'\n'
string|"'port'"
op|':'
number|'1000'
op|'+'
name|'x'
op|','
nl|'\n'
string|"'device'"
op|':'
string|"'sda'"
op|','
nl|'\n'
string|"'zone'"
op|':'
name|'x'
op|'%'
number|'3'
op|','
nl|'\n'
string|"'region'"
op|':'
name|'x'
op|'%'
number|'2'
op|','
nl|'\n'
string|"'id'"
op|':'
name|'x'
op|'}'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FakeMemcache
dedent|''
dedent|''
dedent|''
name|'class'
name|'FakeMemcache'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'store'
op|'='
op|'{'
op|'}'
newline|'\n'
nl|'\n'
DECL|member|get
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
name|'return'
name|'self'
op|'.'
name|'store'
op|'.'
name|'get'
op|'('
name|'key'
op|')'
newline|'\n'
nl|'\n'
DECL|member|keys
dedent|''
name|'def'
name|'keys'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'self'
op|'.'
name|'store'
op|'.'
name|'keys'
op|'('
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
name|'time'
op|'='
number|'0'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'store'
op|'['
name|'key'
op|']'
op|'='
name|'value'
newline|'\n'
name|'return'
name|'True'
newline|'\n'
nl|'\n'
DECL|member|incr
dedent|''
name|'def'
name|'incr'
op|'('
name|'self'
op|','
name|'key'
op|','
name|'time'
op|'='
number|'0'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'store'
op|'['
name|'key'
op|']'
op|'='
name|'self'
op|'.'
name|'store'
op|'.'
name|'setdefault'
op|'('
name|'key'
op|','
number|'0'
op|')'
op|'+'
number|'1'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'store'
op|'['
name|'key'
op|']'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'contextmanager'
newline|'\n'
DECL|member|soft_lock
name|'def'
name|'soft_lock'
op|'('
name|'self'
op|','
name|'key'
op|','
name|'timeout'
op|'='
number|'0'
op|','
name|'retries'
op|'='
number|'5'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'yield'
name|'True'
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
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'del'
name|'self'
op|'.'
name|'store'
op|'['
name|'key'
op|']'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'return'
name|'True'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|readuntil2crlfs
dedent|''
dedent|''
name|'def'
name|'readuntil2crlfs'
op|'('
name|'fd'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'rv'
op|'='
string|"''"
newline|'\n'
name|'lc'
op|'='
string|"''"
newline|'\n'
name|'crlfs'
op|'='
number|'0'
newline|'\n'
name|'while'
name|'crlfs'
op|'<'
number|'2'
op|':'
newline|'\n'
indent|'        '
name|'c'
op|'='
name|'fd'
op|'.'
name|'read'
op|'('
number|'1'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'c'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'ValueError'
op|'('
string|'"didn\'t get two CRLFs; just got %r"'
op|'%'
name|'rv'
op|')'
newline|'\n'
dedent|''
name|'rv'
op|'='
name|'rv'
op|'+'
name|'c'
newline|'\n'
name|'if'
name|'c'
op|'=='
string|"'\\r'"
name|'and'
name|'lc'
op|'!='
string|"'\\n'"
op|':'
newline|'\n'
indent|'            '
name|'crlfs'
op|'='
number|'0'
newline|'\n'
dedent|''
name|'if'
name|'lc'
op|'=='
string|"'\\r'"
name|'and'
name|'c'
op|'=='
string|"'\\n'"
op|':'
newline|'\n'
indent|'            '
name|'crlfs'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'lc'
op|'='
name|'c'
newline|'\n'
dedent|''
name|'return'
name|'rv'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|connect_tcp
dedent|''
name|'def'
name|'connect_tcp'
op|'('
name|'hostport'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'rv'
op|'='
name|'socket'
op|'.'
name|'socket'
op|'('
op|')'
newline|'\n'
name|'rv'
op|'.'
name|'connect'
op|'('
name|'hostport'
op|')'
newline|'\n'
name|'return'
name|'rv'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
op|'@'
name|'contextmanager'
newline|'\n'
DECL|function|tmpfile
name|'def'
name|'tmpfile'
op|'('
name|'content'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'with'
name|'NamedTemporaryFile'
op|'('
string|"'w'"
op|','
name|'delete'
op|'='
name|'False'
op|')'
name|'as'
name|'f'
op|':'
newline|'\n'
indent|'        '
name|'file_name'
op|'='
name|'f'
op|'.'
name|'name'
newline|'\n'
name|'f'
op|'.'
name|'write'
op|'('
name|'str'
op|'('
name|'content'
op|')'
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'yield'
name|'file_name'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'        '
name|'os'
op|'.'
name|'unlink'
op|'('
name|'file_name'
op|')'
newline|'\n'
nl|'\n'
DECL|variable|xattr_data
dedent|''
dedent|''
name|'xattr_data'
op|'='
op|'{'
op|'}'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|_get_inode
name|'def'
name|'_get_inode'
op|'('
name|'fd'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'if'
name|'not'
name|'isinstance'
op|'('
name|'fd'
op|','
name|'int'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'fd'
op|'='
name|'fd'
op|'.'
name|'fileno'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'AttributeError'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'os'
op|'.'
name|'stat'
op|'('
name|'fd'
op|')'
op|'.'
name|'st_ino'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'os'
op|'.'
name|'fstat'
op|'('
name|'fd'
op|')'
op|'.'
name|'st_ino'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|_setxattr
dedent|''
name|'def'
name|'_setxattr'
op|'('
name|'fd'
op|','
name|'k'
op|','
name|'v'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'inode'
op|'='
name|'_get_inode'
op|'('
name|'fd'
op|')'
newline|'\n'
name|'data'
op|'='
name|'xattr_data'
op|'.'
name|'get'
op|'('
name|'inode'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'data'
op|'['
name|'k'
op|']'
op|'='
name|'v'
newline|'\n'
name|'xattr_data'
op|'['
name|'inode'
op|']'
op|'='
name|'data'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|_getxattr
dedent|''
name|'def'
name|'_getxattr'
op|'('
name|'fd'
op|','
name|'k'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'inode'
op|'='
name|'_get_inode'
op|'('
name|'fd'
op|')'
newline|'\n'
name|'data'
op|'='
name|'xattr_data'
op|'.'
name|'get'
op|'('
name|'inode'
op|','
op|'{'
op|'}'
op|')'
op|'.'
name|'get'
op|'('
name|'k'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'data'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'IOError'
newline|'\n'
dedent|''
name|'return'
name|'data'
newline|'\n'
nl|'\n'
dedent|''
name|'import'
name|'xattr'
newline|'\n'
name|'xattr'
op|'.'
name|'setxattr'
op|'='
name|'_setxattr'
newline|'\n'
name|'xattr'
op|'.'
name|'getxattr'
op|'='
name|'_getxattr'
newline|'\n'
nl|'\n'
nl|'\n'
op|'@'
name|'contextmanager'
newline|'\n'
DECL|function|temptree
name|'def'
name|'temptree'
op|'('
name|'files'
op|','
name|'contents'
op|'='
string|"''"
op|')'
op|':'
newline|'\n'
comment|'# generate enough contents to fill the files'
nl|'\n'
indent|'    '
name|'c'
op|'='
name|'len'
op|'('
name|'files'
op|')'
newline|'\n'
name|'contents'
op|'='
op|'('
name|'list'
op|'('
name|'contents'
op|')'
op|'+'
op|'['
string|"''"
op|']'
op|'*'
name|'c'
op|')'
op|'['
op|':'
name|'c'
op|']'
newline|'\n'
name|'tempdir'
op|'='
name|'mkdtemp'
op|'('
op|')'
newline|'\n'
name|'for'
name|'path'
op|','
name|'content'
name|'in'
name|'zip'
op|'('
name|'files'
op|','
name|'contents'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'os'
op|'.'
name|'path'
op|'.'
name|'isabs'
op|'('
name|'path'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'path'
op|'='
string|"'.'"
op|'+'
name|'path'
newline|'\n'
dedent|''
name|'new_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'tempdir'
op|','
name|'path'
op|')'
newline|'\n'
name|'subdir'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'dirname'
op|'('
name|'new_path'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'subdir'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'os'
op|'.'
name|'makedirs'
op|'('
name|'subdir'
op|')'
newline|'\n'
dedent|''
name|'with'
name|'open'
op|'('
name|'new_path'
op|','
string|"'w'"
op|')'
name|'as'
name|'f'
op|':'
newline|'\n'
indent|'            '
name|'f'
op|'.'
name|'write'
op|'('
name|'str'
op|'('
name|'content'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'yield'
name|'tempdir'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'        '
name|'rmtree'
op|'('
name|'tempdir'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|NullLoggingHandler
dedent|''
dedent|''
name|'class'
name|'NullLoggingHandler'
op|'('
name|'logging'
op|'.'
name|'Handler'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|emit
indent|'    '
name|'def'
name|'emit'
op|'('
name|'self'
op|','
name|'record'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FakeLogger
dedent|''
dedent|''
name|'class'
name|'FakeLogger'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
comment|'# a thread safe logger'
nl|'\n'
nl|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
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
indent|'        '
name|'self'
op|'.'
name|'_clear'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'level'
op|'='
name|'logging'
op|'.'
name|'NOTSET'
newline|'\n'
name|'if'
string|"'facility'"
name|'in'
name|'kwargs'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'facility'
op|'='
name|'kwargs'
op|'['
string|"'facility'"
op|']'
newline|'\n'
nl|'\n'
DECL|member|_clear
dedent|''
dedent|''
name|'def'
name|'_clear'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'log_dict'
op|'='
name|'defaultdict'
op|'('
name|'list'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_store_in
dedent|''
name|'def'
name|'_store_in'
op|'('
name|'store_name'
op|')'
op|':'
newline|'\n'
DECL|function|stub_fn
indent|'        '
name|'def'
name|'stub_fn'
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
indent|'            '
name|'self'
op|'.'
name|'log_dict'
op|'['
name|'store_name'
op|']'
op|'.'
name|'append'
op|'('
op|'('
name|'args'
op|','
name|'kwargs'
op|')'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'stub_fn'
newline|'\n'
nl|'\n'
DECL|variable|error
dedent|''
name|'error'
op|'='
name|'_store_in'
op|'('
string|"'error'"
op|')'
newline|'\n'
DECL|variable|info
name|'info'
op|'='
name|'_store_in'
op|'('
string|"'info'"
op|')'
newline|'\n'
DECL|variable|warning
name|'warning'
op|'='
name|'_store_in'
op|'('
string|"'warning'"
op|')'
newline|'\n'
DECL|variable|debug
name|'debug'
op|'='
name|'_store_in'
op|'('
string|"'debug'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|exception
name|'def'
name|'exception'
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
indent|'        '
name|'self'
op|'.'
name|'log_dict'
op|'['
string|"'exception'"
op|']'
op|'.'
name|'append'
op|'('
op|'('
name|'args'
op|','
name|'kwargs'
op|','
name|'str'
op|'('
name|'exc_info'
op|'('
op|')'
op|'['
number|'1'
op|']'
op|')'
op|')'
op|')'
newline|'\n'
name|'print'
string|"'FakeLogger Exception: %s'"
op|'%'
name|'self'
op|'.'
name|'log_dict'
newline|'\n'
nl|'\n'
comment|'# mock out the StatsD logging methods:'
nl|'\n'
DECL|variable|increment
dedent|''
name|'increment'
op|'='
name|'_store_in'
op|'('
string|"'increment'"
op|')'
newline|'\n'
DECL|variable|decrement
name|'decrement'
op|'='
name|'_store_in'
op|'('
string|"'decrement'"
op|')'
newline|'\n'
DECL|variable|timing
name|'timing'
op|'='
name|'_store_in'
op|'('
string|"'timing'"
op|')'
newline|'\n'
DECL|variable|timing_since
name|'timing_since'
op|'='
name|'_store_in'
op|'('
string|"'timing_since'"
op|')'
newline|'\n'
DECL|variable|update_stats
name|'update_stats'
op|'='
name|'_store_in'
op|'('
string|"'update_stats'"
op|')'
newline|'\n'
DECL|variable|set_statsd_prefix
name|'set_statsd_prefix'
op|'='
name|'_store_in'
op|'('
string|"'set_statsd_prefix'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_increments
name|'def'
name|'get_increments'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
op|'['
name|'call'
op|'['
number|'0'
op|']'
op|'['
number|'0'
op|']'
name|'for'
name|'call'
name|'in'
name|'self'
op|'.'
name|'log_dict'
op|'['
string|"'increment'"
op|']'
op|']'
newline|'\n'
nl|'\n'
DECL|member|get_increment_counts
dedent|''
name|'def'
name|'get_increment_counts'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'counts'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'metric'
name|'in'
name|'self'
op|'.'
name|'get_increments'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'metric'
name|'not'
name|'in'
name|'counts'
op|':'
newline|'\n'
indent|'                '
name|'counts'
op|'['
name|'metric'
op|']'
op|'='
number|'0'
newline|'\n'
dedent|''
name|'counts'
op|'['
name|'metric'
op|']'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'return'
name|'counts'
newline|'\n'
nl|'\n'
DECL|member|setFormatter
dedent|''
name|'def'
name|'setFormatter'
op|'('
name|'self'
op|','
name|'obj'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'formatter'
op|'='
name|'obj'
newline|'\n'
nl|'\n'
DECL|member|close
dedent|''
name|'def'
name|'close'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'_clear'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|set_name
dedent|''
name|'def'
name|'set_name'
op|'('
name|'self'
op|','
name|'name'
op|')'
op|':'
newline|'\n'
comment|"# don't touch _handlers"
nl|'\n'
indent|'        '
name|'self'
op|'.'
name|'_name'
op|'='
name|'name'
newline|'\n'
nl|'\n'
DECL|member|acquire
dedent|''
name|'def'
name|'acquire'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|release
dedent|''
name|'def'
name|'release'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|createLock
dedent|''
name|'def'
name|'createLock'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|emit
dedent|''
name|'def'
name|'emit'
op|'('
name|'self'
op|','
name|'record'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|handle
dedent|''
name|'def'
name|'handle'
op|'('
name|'self'
op|','
name|'record'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|flush
dedent|''
name|'def'
name|'flush'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|handleError
dedent|''
name|'def'
name|'handleError'
op|'('
name|'self'
op|','
name|'record'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|variable|original_syslog_handler
dedent|''
dedent|''
name|'original_syslog_handler'
op|'='
name|'logging'
op|'.'
name|'handlers'
op|'.'
name|'SysLogHandler'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|fake_syslog_handler
name|'def'
name|'fake_syslog_handler'
op|'('
op|')'
op|':'
newline|'\n'
indent|'    '
name|'for'
name|'attr'
name|'in'
name|'dir'
op|'('
name|'original_syslog_handler'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'attr'
op|'.'
name|'startswith'
op|'('
string|"'LOG'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'setattr'
op|'('
name|'FakeLogger'
op|','
name|'attr'
op|','
nl|'\n'
name|'copy'
op|'.'
name|'copy'
op|'('
name|'getattr'
op|'('
name|'logging'
op|'.'
name|'handlers'
op|'.'
name|'SysLogHandler'
op|','
name|'attr'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'FakeLogger'
op|'.'
name|'priority_map'
op|'='
name|'copy'
op|'.'
name|'deepcopy'
op|'('
name|'logging'
op|'.'
name|'handlers'
op|'.'
name|'SysLogHandler'
op|'.'
name|'priority_map'
op|')'
newline|'\n'
nl|'\n'
name|'logging'
op|'.'
name|'handlers'
op|'.'
name|'SysLogHandler'
op|'='
name|'FakeLogger'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
name|'if'
name|'config_true_value'
op|'('
name|'get_config'
op|'('
string|"'unit_test'"
op|')'
op|'.'
name|'get'
op|'('
string|"'fake_syslog'"
op|','
string|"'False'"
op|')'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'fake_syslog_handler'
op|'('
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|MockTrue
dedent|''
name|'class'
name|'MockTrue'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Instances of MockTrue evaluate like True\n    Any attr accessed on an instance of MockTrue will return a MockTrue\n    instance. Any method called on an instance of MockTrue will return\n    a MockTrue instance.\n\n    >>> thing = MockTrue()\n    >>> thing\n    True\n    >>> thing == True # True == True\n    True\n    >>> thing == False # True == False\n    False\n    >>> thing != True # True != True\n    False\n    >>> thing != False # True != False\n    True\n    >>> thing.attribute\n    True\n    >>> thing.method()\n    True\n    >>> thing.attribute.method()\n    True\n    >>> thing.method().attribute\n    True\n\n    """'
newline|'\n'
nl|'\n'
DECL|member|__getattribute__
name|'def'
name|'__getattribute__'
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
indent|'        '
name|'return'
name|'self'
newline|'\n'
nl|'\n'
DECL|member|__call__
dedent|''
name|'def'
name|'__call__'
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
indent|'        '
name|'return'
name|'self'
newline|'\n'
nl|'\n'
DECL|member|__repr__
dedent|''
name|'def'
name|'__repr__'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'repr'
op|'('
name|'True'
op|')'
newline|'\n'
nl|'\n'
DECL|member|__eq__
dedent|''
name|'def'
name|'__eq__'
op|'('
name|'self'
op|','
name|'other'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'other'
name|'is'
name|'True'
newline|'\n'
nl|'\n'
DECL|member|__ne__
dedent|''
name|'def'
name|'__ne__'
op|'('
name|'self'
op|','
name|'other'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'other'
name|'is'
name|'not'
name|'True'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
dedent|''
op|'@'
name|'contextmanager'
newline|'\n'
DECL|function|mock
name|'def'
name|'mock'
op|'('
name|'update'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'returns'
op|'='
op|'['
op|']'
newline|'\n'
name|'deletes'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'key'
op|','
name|'value'
name|'in'
name|'update'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'        '
name|'imports'
op|'='
name|'key'
op|'.'
name|'split'
op|'('
string|"'.'"
op|')'
newline|'\n'
name|'attr'
op|'='
name|'imports'
op|'.'
name|'pop'
op|'('
op|'-'
number|'1'
op|')'
newline|'\n'
name|'module'
op|'='
name|'__import__'
op|'('
name|'imports'
op|'['
number|'0'
op|']'
op|','
name|'fromlist'
op|'='
name|'imports'
op|'['
number|'1'
op|':'
op|']'
op|')'
newline|'\n'
name|'for'
name|'modname'
name|'in'
name|'imports'
op|'['
number|'1'
op|':'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'module'
op|'='
name|'getattr'
op|'('
name|'module'
op|','
name|'modname'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'hasattr'
op|'('
name|'module'
op|','
name|'attr'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'returns'
op|'.'
name|'append'
op|'('
op|'('
name|'module'
op|','
name|'attr'
op|','
name|'getattr'
op|'('
name|'module'
op|','
name|'attr'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'deletes'
op|'.'
name|'append'
op|'('
op|'('
name|'module'
op|','
name|'attr'
op|')'
op|')'
newline|'\n'
dedent|''
name|'setattr'
op|'('
name|'module'
op|','
name|'attr'
op|','
name|'value'
op|')'
newline|'\n'
dedent|''
name|'yield'
name|'True'
newline|'\n'
name|'for'
name|'module'
op|','
name|'attr'
op|','
name|'value'
name|'in'
name|'returns'
op|':'
newline|'\n'
indent|'        '
name|'setattr'
op|'('
name|'module'
op|','
name|'attr'
op|','
name|'value'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'module'
op|','
name|'attr'
name|'in'
name|'deletes'
op|':'
newline|'\n'
indent|'        '
name|'delattr'
op|'('
name|'module'
op|','
name|'attr'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|fake_http_connect
dedent|''
dedent|''
name|'def'
name|'fake_http_connect'
op|'('
op|'*'
name|'code_iter'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|class|FakeConn
indent|'    '
name|'class'
name|'FakeConn'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|__init__
indent|'        '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'status'
op|','
name|'etag'
op|'='
name|'None'
op|','
name|'body'
op|'='
string|"''"
op|','
name|'timestamp'
op|'='
string|"'1'"
op|','
nl|'\n'
name|'expect_status'
op|'='
name|'None'
op|','
name|'headers'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'status'
op|'='
name|'status'
newline|'\n'
name|'if'
name|'expect_status'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'expect_status'
op|'='
name|'self'
op|'.'
name|'status'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'expect_status'
op|'='
name|'expect_status'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'reason'
op|'='
string|"'Fake'"
newline|'\n'
name|'self'
op|'.'
name|'host'
op|'='
string|"'1.2.3.4'"
newline|'\n'
name|'self'
op|'.'
name|'port'
op|'='
string|"'1234'"
newline|'\n'
name|'self'
op|'.'
name|'sent'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'received'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'etag'
op|'='
name|'etag'
newline|'\n'
name|'self'
op|'.'
name|'body'
op|'='
name|'body'
newline|'\n'
name|'self'
op|'.'
name|'headers'
op|'='
name|'headers'
name|'or'
op|'{'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'timestamp'
op|'='
name|'timestamp'
newline|'\n'
nl|'\n'
DECL|member|getresponse
dedent|''
name|'def'
name|'getresponse'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'raise_exc'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'Exception'
op|'('
string|"'test'"
op|')'
newline|'\n'
dedent|''
name|'if'
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'raise_timeout_exc'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'Timeout'
op|'('
op|')'
newline|'\n'
dedent|''
name|'return'
name|'self'
newline|'\n'
nl|'\n'
DECL|member|getexpect
dedent|''
name|'def'
name|'getexpect'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'self'
op|'.'
name|'expect_status'
op|'=='
op|'-'
number|'2'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'HTTPException'
op|'('
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'expect_status'
op|'=='
op|'-'
number|'3'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'FakeConn'
op|'('
number|'507'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'expect_status'
op|'=='
op|'-'
number|'4'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'FakeConn'
op|'('
number|'201'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'FakeConn'
op|'('
number|'100'
op|')'
newline|'\n'
nl|'\n'
DECL|member|getheaders
dedent|''
name|'def'
name|'getheaders'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'etag'
op|'='
name|'self'
op|'.'
name|'etag'
newline|'\n'
name|'if'
name|'not'
name|'etag'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'isinstance'
op|'('
name|'self'
op|'.'
name|'body'
op|','
name|'str'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'etag'
op|'='
string|'\'"\''
op|'+'
name|'md5'
op|'('
name|'self'
op|'.'
name|'body'
op|')'
op|'.'
name|'hexdigest'
op|'('
op|')'
op|'+'
string|'\'"\''
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'etag'
op|'='
string|'\'"68b329da9893e34099c7d8ad5cb9c940"\''
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'headers'
op|'='
op|'{'
string|"'content-length'"
op|':'
name|'len'
op|'('
name|'self'
op|'.'
name|'body'
op|')'
op|','
nl|'\n'
string|"'content-type'"
op|':'
string|"'x-application/test'"
op|','
nl|'\n'
string|"'x-timestamp'"
op|':'
name|'self'
op|'.'
name|'timestamp'
op|','
nl|'\n'
string|"'last-modified'"
op|':'
name|'self'
op|'.'
name|'timestamp'
op|','
nl|'\n'
string|"'x-object-meta-test'"
op|':'
string|"'testing'"
op|','
nl|'\n'
string|"'x-delete-at'"
op|':'
string|"'9876543210'"
op|','
nl|'\n'
string|"'etag'"
op|':'
name|'etag'
op|','
nl|'\n'
string|"'x-works'"
op|':'
string|"'yes'"
op|'}'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'status'
op|'//'
number|'100'
op|'=='
number|'2'
op|':'
newline|'\n'
indent|'                '
name|'headers'
op|'['
string|"'x-account-container-count'"
op|']'
op|'='
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'count'"
op|','
number|'12345'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'self'
op|'.'
name|'timestamp'
op|':'
newline|'\n'
indent|'                '
name|'del'
name|'headers'
op|'['
string|"'x-timestamp'"
op|']'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'container_ts_iter'
op|'.'
name|'next'
op|'('
op|')'
name|'is'
name|'False'
op|':'
newline|'\n'
indent|'                    '
name|'headers'
op|'['
string|"'x-container-timestamp'"
op|']'
op|'='
string|"'1'"
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'StopIteration'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
dedent|''
name|'if'
string|"'slow'"
name|'in'
name|'kwargs'
op|':'
newline|'\n'
indent|'                '
name|'headers'
op|'['
string|"'content-length'"
op|']'
op|'='
string|"'4'"
newline|'\n'
dedent|''
name|'headers'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'headers'
op|')'
newline|'\n'
name|'return'
name|'headers'
op|'.'
name|'items'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|read
dedent|''
name|'def'
name|'read'
op|'('
name|'self'
op|','
name|'amt'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
string|"'slow'"
name|'in'
name|'kwargs'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'self'
op|'.'
name|'sent'
op|'<'
number|'4'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'sent'
op|'+='
number|'1'
newline|'\n'
name|'sleep'
op|'('
number|'0.1'
op|')'
newline|'\n'
name|'return'
string|"' '"
newline|'\n'
dedent|''
dedent|''
name|'rv'
op|'='
name|'self'
op|'.'
name|'body'
op|'['
op|':'
name|'amt'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'body'
op|'='
name|'self'
op|'.'
name|'body'
op|'['
name|'amt'
op|':'
op|']'
newline|'\n'
name|'return'
name|'rv'
newline|'\n'
nl|'\n'
DECL|member|send
dedent|''
name|'def'
name|'send'
op|'('
name|'self'
op|','
name|'amt'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
string|"'slow'"
name|'in'
name|'kwargs'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'self'
op|'.'
name|'received'
op|'<'
number|'4'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'received'
op|'+='
number|'1'
newline|'\n'
name|'sleep'
op|'('
number|'0.1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|getheader
dedent|''
dedent|''
dedent|''
name|'def'
name|'getheader'
op|'('
name|'self'
op|','
name|'name'
op|','
name|'default'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'dict'
op|'('
name|'self'
op|'.'
name|'getheaders'
op|'('
op|')'
op|')'
op|'.'
name|'get'
op|'('
name|'name'
op|'.'
name|'lower'
op|'('
op|')'
op|','
name|'default'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'timestamps_iter'
op|'='
name|'iter'
op|'('
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'timestamps'"
op|')'
name|'or'
op|'['
string|"'1'"
op|']'
op|'*'
name|'len'
op|'('
name|'code_iter'
op|')'
op|')'
newline|'\n'
name|'etag_iter'
op|'='
name|'iter'
op|'('
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'etags'"
op|')'
name|'or'
op|'['
name|'None'
op|']'
op|'*'
name|'len'
op|'('
name|'code_iter'
op|')'
op|')'
newline|'\n'
name|'if'
name|'isinstance'
op|'('
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'headers'"
op|')'
op|','
name|'list'
op|')'
op|':'
newline|'\n'
DECL|variable|headers_iter
indent|'        '
name|'headers_iter'
op|'='
name|'iter'
op|'('
name|'kwargs'
op|'['
string|"'headers'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
DECL|variable|headers_iter
indent|'        '
name|'headers_iter'
op|'='
name|'iter'
op|'('
op|'['
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'headers'"
op|','
op|'{'
op|'}'
op|')'
op|']'
op|'*'
name|'len'
op|'('
name|'code_iter'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'x'
op|'='
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'missing_container'"
op|','
op|'['
name|'False'
op|']'
op|'*'
name|'len'
op|'('
name|'code_iter'
op|')'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'isinstance'
op|'('
name|'x'
op|','
op|'('
name|'tuple'
op|','
name|'list'
op|')'
op|')'
op|':'
newline|'\n'
DECL|variable|x
indent|'        '
name|'x'
op|'='
op|'['
name|'x'
op|']'
op|'*'
name|'len'
op|'('
name|'code_iter'
op|')'
newline|'\n'
dedent|''
name|'container_ts_iter'
op|'='
name|'iter'
op|'('
name|'x'
op|')'
newline|'\n'
name|'code_iter'
op|'='
name|'iter'
op|'('
name|'code_iter'
op|')'
newline|'\n'
name|'static_body'
op|'='
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'body'"
op|','
name|'None'
op|')'
newline|'\n'
name|'body_iter'
op|'='
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'body_iter'"
op|','
name|'None'
op|')'
newline|'\n'
name|'if'
name|'body_iter'
op|':'
newline|'\n'
DECL|variable|body_iter
indent|'        '
name|'body_iter'
op|'='
name|'iter'
op|'('
name|'body_iter'
op|')'
newline|'\n'
nl|'\n'
DECL|function|connect
dedent|''
name|'def'
name|'connect'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'ckwargs'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'slow_connect'"
op|','
name|'False'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'sleep'
op|'('
number|'0.1'
op|')'
newline|'\n'
dedent|''
name|'if'
string|"'give_content_type'"
name|'in'
name|'kwargs'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'len'
op|'('
name|'args'
op|')'
op|'>='
number|'7'
name|'and'
string|"'Content-Type'"
name|'in'
name|'args'
op|'['
number|'6'
op|']'
op|':'
newline|'\n'
indent|'                '
name|'kwargs'
op|'['
string|"'give_content_type'"
op|']'
op|'('
name|'args'
op|'['
number|'6'
op|']'
op|'['
string|"'Content-Type'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'kwargs'
op|'['
string|"'give_content_type'"
op|']'
op|'('
string|"''"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'if'
string|"'give_connect'"
name|'in'
name|'kwargs'
op|':'
newline|'\n'
indent|'            '
name|'kwargs'
op|'['
string|"'give_connect'"
op|']'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'ckwargs'
op|')'
newline|'\n'
dedent|''
name|'status'
op|'='
name|'code_iter'
op|'.'
name|'next'
op|'('
op|')'
newline|'\n'
name|'if'
name|'isinstance'
op|'('
name|'status'
op|','
name|'tuple'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'status'
op|','
name|'expect_status'
op|'='
name|'status'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'expect_status'
op|'='
name|'status'
newline|'\n'
dedent|''
name|'etag'
op|'='
name|'etag_iter'
op|'.'
name|'next'
op|'('
op|')'
newline|'\n'
name|'headers'
op|'='
name|'headers_iter'
op|'.'
name|'next'
op|'('
op|')'
newline|'\n'
name|'timestamp'
op|'='
name|'timestamps_iter'
op|'.'
name|'next'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'if'
name|'status'
op|'<='
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'HTTPException'
op|'('
op|')'
newline|'\n'
dedent|''
name|'if'
name|'body_iter'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'body'
op|'='
name|'static_body'
name|'or'
string|"''"
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'body'
op|'='
name|'body_iter'
op|'.'
name|'next'
op|'('
op|')'
newline|'\n'
dedent|''
name|'return'
name|'FakeConn'
op|'('
name|'status'
op|','
name|'etag'
op|','
name|'body'
op|'='
name|'body'
op|','
name|'timestamp'
op|'='
name|'timestamp'
op|','
nl|'\n'
name|'expect_status'
op|'='
name|'expect_status'
op|','
name|'headers'
op|'='
name|'headers'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'connect'
newline|'\n'
dedent|''
endmarker|''
end_unit
