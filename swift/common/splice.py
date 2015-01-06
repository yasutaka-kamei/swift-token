begin_unit
comment|'# Copyright (c) 2014 OpenStack Foundation'
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
string|"'''\nBindings to the `tee` and `splice` system calls\n'''"
newline|'\n'
nl|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'operator'
newline|'\n'
nl|'\n'
name|'import'
name|'ctypes'
newline|'\n'
name|'import'
name|'ctypes'
op|'.'
name|'util'
newline|'\n'
nl|'\n'
DECL|variable|__all__
name|'__all__'
op|'='
op|'['
string|"'tee'"
op|','
string|"'splice'"
op|']'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|variable|c_loff_t
name|'c_loff_t'
op|'='
name|'ctypes'
op|'.'
name|'c_long'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|Tee
name|'class'
name|'Tee'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|"'''Binding to `tee`'''"
newline|'\n'
nl|'\n'
DECL|variable|__slots__
name|'__slots__'
op|'='
string|"'_c_tee'"
op|','
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'libc'
op|'='
name|'ctypes'
op|'.'
name|'CDLL'
op|'('
name|'ctypes'
op|'.'
name|'util'
op|'.'
name|'find_library'
op|'('
string|"'c'"
op|')'
op|','
name|'use_errno'
op|'='
name|'True'
op|')'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'c_tee'
op|'='
name|'libc'
op|'.'
name|'tee'
newline|'\n'
dedent|''
name|'except'
name|'AttributeError'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_c_tee'
op|'='
name|'None'
newline|'\n'
name|'return'
newline|'\n'
nl|'\n'
dedent|''
name|'c_tee'
op|'.'
name|'argtypes'
op|'='
op|'['
nl|'\n'
name|'ctypes'
op|'.'
name|'c_int'
op|','
nl|'\n'
name|'ctypes'
op|'.'
name|'c_int'
op|','
nl|'\n'
name|'ctypes'
op|'.'
name|'c_size_t'
op|','
nl|'\n'
name|'ctypes'
op|'.'
name|'c_uint'
nl|'\n'
op|']'
newline|'\n'
nl|'\n'
name|'c_tee'
op|'.'
name|'restype'
op|'='
name|'ctypes'
op|'.'
name|'c_ssize_t'
newline|'\n'
nl|'\n'
DECL|function|errcheck
name|'def'
name|'errcheck'
op|'('
name|'result'
op|','
name|'func'
op|','
name|'arguments'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'result'
op|'=='
op|'-'
number|'1'
op|':'
newline|'\n'
indent|'                '
name|'errno'
op|'='
name|'ctypes'
op|'.'
name|'set_errno'
op|'('
number|'0'
op|')'
newline|'\n'
nl|'\n'
name|'raise'
name|'IOError'
op|'('
name|'errno'
op|','
string|"'tee: %s'"
op|'%'
name|'os'
op|'.'
name|'strerror'
op|'('
name|'errno'
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'result'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'c_tee'
op|'.'
name|'errcheck'
op|'='
name|'errcheck'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'_c_tee'
op|'='
name|'c_tee'
newline|'\n'
nl|'\n'
DECL|member|__call__
dedent|''
name|'def'
name|'__call__'
op|'('
name|'self'
op|','
name|'fd_in'
op|','
name|'fd_out'
op|','
name|'len_'
op|','
name|'flags'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''See `man 2 tee`\n\n        File-descriptors can be file-like objects with a `fileno` method, or\n        integers.\n\n        Flags can be an integer value, or a list of flags (exposed on\n        `splice`).\n\n        This function returns the number of bytes transferred (i.e. the actual\n        result of the call to `tee`).\n\n        Upon other errors, an `IOError` is raised with the proper `errno` set.\n        '''"
newline|'\n'
nl|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'available'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'EnvironmentError'
op|'('
string|"'tee not available'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'not'
name|'isinstance'
op|'('
name|'flags'
op|','
op|'('
name|'int'
op|','
name|'long'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'c_flags'
op|'='
name|'reduce'
op|'('
name|'operator'
op|'.'
name|'or_'
op|','
name|'flags'
op|','
number|'0'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'c_flags'
op|'='
name|'flags'
newline|'\n'
nl|'\n'
dedent|''
name|'c_fd_in'
op|'='
name|'getattr'
op|'('
name|'fd_in'
op|','
string|"'fileno'"
op|','
name|'lambda'
op|':'
name|'fd_in'
op|')'
op|'('
op|')'
newline|'\n'
name|'c_fd_out'
op|'='
name|'getattr'
op|'('
name|'fd_out'
op|','
string|"'fileno'"
op|','
name|'lambda'
op|':'
name|'fd_out'
op|')'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'return'
name|'self'
op|'.'
name|'_c_tee'
op|'('
name|'c_fd_in'
op|','
name|'c_fd_out'
op|','
name|'len_'
op|','
name|'c_flags'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'property'
newline|'\n'
DECL|member|available
name|'def'
name|'available'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''Availability of `tee`'''"
newline|'\n'
nl|'\n'
name|'return'
name|'self'
op|'.'
name|'_c_tee'
name|'is'
name|'not'
name|'None'
newline|'\n'
nl|'\n'
DECL|variable|tee
dedent|''
dedent|''
name|'tee'
op|'='
name|'Tee'
op|'('
op|')'
newline|'\n'
name|'del'
name|'Tee'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|Splice
name|'class'
name|'Splice'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|"'''Binding to `splice`'''"
newline|'\n'
nl|'\n'
comment|'# From `bits/fcntl-linux.h`'
nl|'\n'
DECL|variable|SPLICE_F_MOVE
name|'SPLICE_F_MOVE'
op|'='
number|'1'
newline|'\n'
DECL|variable|SPLICE_F_NONBLOCK
name|'SPLICE_F_NONBLOCK'
op|'='
number|'2'
newline|'\n'
DECL|variable|SPLICE_F_MORE
name|'SPLICE_F_MORE'
op|'='
number|'4'
newline|'\n'
DECL|variable|SPLICE_F_GIFT
name|'SPLICE_F_GIFT'
op|'='
number|'8'
newline|'\n'
nl|'\n'
DECL|variable|__slots__
name|'__slots__'
op|'='
string|"'_c_splice'"
op|','
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'libc'
op|'='
name|'ctypes'
op|'.'
name|'CDLL'
op|'('
name|'ctypes'
op|'.'
name|'util'
op|'.'
name|'find_library'
op|'('
string|"'c'"
op|')'
op|','
name|'use_errno'
op|'='
name|'True'
op|')'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'c_splice'
op|'='
name|'libc'
op|'.'
name|'splice'
newline|'\n'
dedent|''
name|'except'
name|'AttributeError'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_c_splice'
op|'='
name|'None'
newline|'\n'
name|'return'
newline|'\n'
nl|'\n'
dedent|''
name|'c_loff_t_p'
op|'='
name|'ctypes'
op|'.'
name|'POINTER'
op|'('
name|'c_loff_t'
op|')'
newline|'\n'
nl|'\n'
name|'c_splice'
op|'.'
name|'argtypes'
op|'='
op|'['
nl|'\n'
name|'ctypes'
op|'.'
name|'c_int'
op|','
name|'c_loff_t_p'
op|','
nl|'\n'
name|'ctypes'
op|'.'
name|'c_int'
op|','
name|'c_loff_t_p'
op|','
nl|'\n'
name|'ctypes'
op|'.'
name|'c_size_t'
op|','
nl|'\n'
name|'ctypes'
op|'.'
name|'c_uint'
nl|'\n'
op|']'
newline|'\n'
nl|'\n'
name|'c_splice'
op|'.'
name|'restype'
op|'='
name|'ctypes'
op|'.'
name|'c_ssize_t'
newline|'\n'
nl|'\n'
DECL|function|errcheck
name|'def'
name|'errcheck'
op|'('
name|'result'
op|','
name|'func'
op|','
name|'arguments'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'result'
op|'=='
op|'-'
number|'1'
op|':'
newline|'\n'
indent|'                '
name|'errno'
op|'='
name|'ctypes'
op|'.'
name|'set_errno'
op|'('
number|'0'
op|')'
newline|'\n'
nl|'\n'
name|'raise'
name|'IOError'
op|'('
name|'errno'
op|','
string|"'splice: %s'"
op|'%'
name|'os'
op|'.'
name|'strerror'
op|'('
name|'errno'
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'off_in'
op|'='
name|'arguments'
op|'['
number|'1'
op|']'
newline|'\n'
name|'off_out'
op|'='
name|'arguments'
op|'['
number|'3'
op|']'
newline|'\n'
nl|'\n'
name|'return'
op|'('
nl|'\n'
name|'result'
op|','
nl|'\n'
name|'off_in'
op|'.'
name|'contents'
op|'.'
name|'value'
name|'if'
name|'off_in'
name|'is'
name|'not'
name|'None'
name|'else'
name|'None'
op|','
nl|'\n'
name|'off_out'
op|'.'
name|'contents'
op|'.'
name|'value'
name|'if'
name|'off_out'
name|'is'
name|'not'
name|'None'
name|'else'
name|'None'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'c_splice'
op|'.'
name|'errcheck'
op|'='
name|'errcheck'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'_c_splice'
op|'='
name|'c_splice'
newline|'\n'
nl|'\n'
DECL|member|__call__
dedent|''
name|'def'
name|'__call__'
op|'('
name|'self'
op|','
name|'fd_in'
op|','
name|'off_in'
op|','
name|'fd_out'
op|','
name|'off_out'
op|','
name|'len_'
op|','
name|'flags'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''See `man 2 splice`\n\n        File-descriptors can be file-like objects with a `fileno` method, or\n        integers.\n\n        Flags can be an integer value, or a list of flags (exposed on this\n        object).\n\n        Returns a tuple of the result of the `splice` call, the output value of\n        `off_in` and the output value of `off_out` (or `None` for any of these\n        output values, if applicable).\n\n        Upon other errors, an `IOError` is raised with the proper `errno` set.\n\n        Note: if you want to pass `NULL` as value for `off_in` or `off_out` to\n        the system call, you must pass `None`, *not* 0!\n        '''"
newline|'\n'
nl|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'available'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'EnvironmentError'
op|'('
string|"'splice not available'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'not'
name|'isinstance'
op|'('
name|'flags'
op|','
op|'('
name|'int'
op|','
name|'long'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'c_flags'
op|'='
name|'reduce'
op|'('
name|'operator'
op|'.'
name|'or_'
op|','
name|'flags'
op|','
number|'0'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'c_flags'
op|'='
name|'flags'
newline|'\n'
nl|'\n'
dedent|''
name|'c_fd_in'
op|'='
name|'getattr'
op|'('
name|'fd_in'
op|','
string|"'fileno'"
op|','
name|'lambda'
op|':'
name|'fd_in'
op|')'
op|'('
op|')'
newline|'\n'
name|'c_fd_out'
op|'='
name|'getattr'
op|'('
name|'fd_out'
op|','
string|"'fileno'"
op|','
name|'lambda'
op|':'
name|'fd_out'
op|')'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'c_off_in'
op|'='
name|'ctypes'
op|'.'
name|'pointer'
op|'('
name|'c_loff_t'
op|'('
name|'off_in'
op|')'
op|')'
name|'if'
name|'off_in'
name|'is'
name|'not'
name|'None'
name|'else'
name|'None'
newline|'\n'
name|'c_off_out'
op|'='
name|'ctypes'
op|'.'
name|'pointer'
op|'('
name|'c_loff_t'
op|'('
name|'off_out'
op|')'
op|')'
name|'if'
name|'off_out'
name|'is'
name|'not'
name|'None'
name|'else'
name|'None'
newline|'\n'
nl|'\n'
name|'return'
name|'self'
op|'.'
name|'_c_splice'
op|'('
nl|'\n'
name|'c_fd_in'
op|','
name|'c_off_in'
op|','
name|'c_fd_out'
op|','
name|'c_off_out'
op|','
name|'len_'
op|','
name|'c_flags'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'property'
newline|'\n'
DECL|member|available
name|'def'
name|'available'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''Availability of `splice`'''"
newline|'\n'
nl|'\n'
name|'return'
name|'self'
op|'.'
name|'_c_splice'
name|'is'
name|'not'
name|'None'
newline|'\n'
nl|'\n'
DECL|variable|splice
dedent|''
dedent|''
name|'splice'
op|'='
name|'Splice'
op|'('
op|')'
newline|'\n'
name|'del'
name|'Splice'
newline|'\n'
endmarker|''
end_unit