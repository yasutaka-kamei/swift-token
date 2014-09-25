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
name|'eventlet'
name|'import'
name|'Timeout'
newline|'\n'
name|'import'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|MessageTimeout
name|'class'
name|'MessageTimeout'
op|'('
name|'Timeout'
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
name|'seconds'
op|'='
name|'None'
op|','
name|'msg'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'Timeout'
op|'.'
name|'__init__'
op|'('
name|'self'
op|','
name|'seconds'
op|'='
name|'seconds'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'msg'
op|'='
name|'msg'
newline|'\n'
nl|'\n'
DECL|member|__str__
dedent|''
name|'def'
name|'__str__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
string|"'%s: %s'"
op|'%'
op|'('
name|'Timeout'
op|'.'
name|'__str__'
op|'('
name|'self'
op|')'
op|','
name|'self'
op|'.'
name|'msg'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|SwiftException
dedent|''
dedent|''
name|'class'
name|'SwiftException'
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
DECL|class|InvalidTimestamp
dedent|''
name|'class'
name|'InvalidTimestamp'
op|'('
name|'SwiftException'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DiskFileError
dedent|''
name|'class'
name|'DiskFileError'
op|'('
name|'SwiftException'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DiskFileNotOpen
dedent|''
name|'class'
name|'DiskFileNotOpen'
op|'('
name|'DiskFileError'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DiskFileQuarantined
dedent|''
name|'class'
name|'DiskFileQuarantined'
op|'('
name|'DiskFileError'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DiskFileCollision
dedent|''
name|'class'
name|'DiskFileCollision'
op|'('
name|'DiskFileError'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DiskFileNotExist
dedent|''
name|'class'
name|'DiskFileNotExist'
op|'('
name|'DiskFileError'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DiskFileDeleted
dedent|''
name|'class'
name|'DiskFileDeleted'
op|'('
name|'DiskFileNotExist'
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
name|'metadata'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'metadata'
op|'='
name|'metadata'
name|'or'
op|'{'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'timestamp'
op|'='
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
op|'.'
name|'Timestamp'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'metadata'
op|'.'
name|'get'
op|'('
string|"'X-Timestamp'"
op|','
number|'0'
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DiskFileExpired
dedent|''
dedent|''
name|'class'
name|'DiskFileExpired'
op|'('
name|'DiskFileDeleted'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DiskFileNoSpace
dedent|''
name|'class'
name|'DiskFileNoSpace'
op|'('
name|'DiskFileError'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DiskFileDeviceUnavailable
dedent|''
name|'class'
name|'DiskFileDeviceUnavailable'
op|'('
name|'DiskFileError'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DeviceUnavailable
dedent|''
name|'class'
name|'DeviceUnavailable'
op|'('
name|'SwiftException'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|InvalidAccountInfo
dedent|''
name|'class'
name|'InvalidAccountInfo'
op|'('
name|'SwiftException'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|PathNotDir
dedent|''
name|'class'
name|'PathNotDir'
op|'('
name|'OSError'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ChunkReadTimeout
dedent|''
name|'class'
name|'ChunkReadTimeout'
op|'('
name|'Timeout'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ChunkWriteTimeout
dedent|''
name|'class'
name|'ChunkWriteTimeout'
op|'('
name|'Timeout'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ConnectionTimeout
dedent|''
name|'class'
name|'ConnectionTimeout'
op|'('
name|'Timeout'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DriveNotMounted
dedent|''
name|'class'
name|'DriveNotMounted'
op|'('
name|'SwiftException'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|LockTimeout
dedent|''
name|'class'
name|'LockTimeout'
op|'('
name|'MessageTimeout'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|RingBuilderError
dedent|''
name|'class'
name|'RingBuilderError'
op|'('
name|'SwiftException'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|RingValidationError
dedent|''
name|'class'
name|'RingValidationError'
op|'('
name|'RingBuilderError'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|EmptyRingError
dedent|''
name|'class'
name|'EmptyRingError'
op|'('
name|'RingBuilderError'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DuplicateDeviceError
dedent|''
name|'class'
name|'DuplicateDeviceError'
op|'('
name|'RingBuilderError'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ListingIterError
dedent|''
name|'class'
name|'ListingIterError'
op|'('
name|'SwiftException'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ListingIterNotFound
dedent|''
name|'class'
name|'ListingIterNotFound'
op|'('
name|'ListingIterError'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ListingIterNotAuthorized
dedent|''
name|'class'
name|'ListingIterNotAuthorized'
op|'('
name|'ListingIterError'
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
name|'aresp'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'aresp'
op|'='
name|'aresp'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|SegmentError
dedent|''
dedent|''
name|'class'
name|'SegmentError'
op|'('
name|'SwiftException'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ReplicationException
dedent|''
name|'class'
name|'ReplicationException'
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
DECL|class|ReplicationLockTimeout
dedent|''
name|'class'
name|'ReplicationLockTimeout'
op|'('
name|'LockTimeout'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|MimeInvalid
dedent|''
name|'class'
name|'MimeInvalid'
op|'('
name|'SwiftException'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ClientException
dedent|''
name|'class'
name|'ClientException'
op|'('
name|'Exception'
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
name|'msg'
op|','
name|'http_scheme'
op|'='
string|"''"
op|','
name|'http_host'
op|'='
string|"''"
op|','
name|'http_port'
op|'='
string|"''"
op|','
nl|'\n'
name|'http_path'
op|'='
string|"''"
op|','
name|'http_query'
op|'='
string|"''"
op|','
name|'http_status'
op|'='
number|'0'
op|','
name|'http_reason'
op|'='
string|"''"
op|','
nl|'\n'
name|'http_device'
op|'='
string|"''"
op|','
name|'http_response_content'
op|'='
string|"''"
op|','
name|'http_headers'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'Exception'
op|'.'
name|'__init__'
op|'('
name|'self'
op|','
name|'msg'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'msg'
op|'='
name|'msg'
newline|'\n'
name|'self'
op|'.'
name|'http_scheme'
op|'='
name|'http_scheme'
newline|'\n'
name|'self'
op|'.'
name|'http_host'
op|'='
name|'http_host'
newline|'\n'
name|'self'
op|'.'
name|'http_port'
op|'='
name|'http_port'
newline|'\n'
name|'self'
op|'.'
name|'http_path'
op|'='
name|'http_path'
newline|'\n'
name|'self'
op|'.'
name|'http_query'
op|'='
name|'http_query'
newline|'\n'
name|'self'
op|'.'
name|'http_status'
op|'='
name|'http_status'
newline|'\n'
name|'self'
op|'.'
name|'http_reason'
op|'='
name|'http_reason'
newline|'\n'
name|'self'
op|'.'
name|'http_device'
op|'='
name|'http_device'
newline|'\n'
name|'self'
op|'.'
name|'http_response_content'
op|'='
name|'http_response_content'
newline|'\n'
name|'self'
op|'.'
name|'http_headers'
op|'='
name|'http_headers'
name|'or'
op|'{'
op|'}'
newline|'\n'
nl|'\n'
DECL|member|__str__
dedent|''
name|'def'
name|'__str__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'a'
op|'='
name|'self'
op|'.'
name|'msg'
newline|'\n'
name|'b'
op|'='
string|"''"
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'http_scheme'
op|':'
newline|'\n'
indent|'            '
name|'b'
op|'+='
string|"'%s://'"
op|'%'
name|'self'
op|'.'
name|'http_scheme'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'http_host'
op|':'
newline|'\n'
indent|'            '
name|'b'
op|'+='
name|'self'
op|'.'
name|'http_host'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'http_port'
op|':'
newline|'\n'
indent|'            '
name|'b'
op|'+='
string|"':%s'"
op|'%'
name|'self'
op|'.'
name|'http_port'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'http_path'
op|':'
newline|'\n'
indent|'            '
name|'b'
op|'+='
name|'self'
op|'.'
name|'http_path'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'http_query'
op|':'
newline|'\n'
indent|'            '
name|'b'
op|'+='
string|"'?%s'"
op|'%'
name|'self'
op|'.'
name|'http_query'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'http_status'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'b'
op|':'
newline|'\n'
indent|'                '
name|'b'
op|'='
string|"'%s %s'"
op|'%'
op|'('
name|'b'
op|','
name|'self'
op|'.'
name|'http_status'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'b'
op|'='
name|'str'
op|'('
name|'self'
op|'.'
name|'http_status'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'self'
op|'.'
name|'http_reason'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'b'
op|':'
newline|'\n'
indent|'                '
name|'b'
op|'='
string|"'%s %s'"
op|'%'
op|'('
name|'b'
op|','
name|'self'
op|'.'
name|'http_reason'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'b'
op|'='
string|"'- %s'"
op|'%'
name|'self'
op|'.'
name|'http_reason'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'self'
op|'.'
name|'http_device'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'b'
op|':'
newline|'\n'
indent|'                '
name|'b'
op|'='
string|"'%s: device %s'"
op|'%'
op|'('
name|'b'
op|','
name|'self'
op|'.'
name|'http_device'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'b'
op|'='
string|"'device %s'"
op|'%'
name|'self'
op|'.'
name|'http_device'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'self'
op|'.'
name|'http_response_content'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'len'
op|'('
name|'self'
op|'.'
name|'http_response_content'
op|')'
op|'<='
number|'60'
op|':'
newline|'\n'
indent|'                '
name|'b'
op|'+='
string|"'   %s'"
op|'%'
name|'self'
op|'.'
name|'http_response_content'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'b'
op|'+='
string|"'  [first 60 chars of response] %s'"
op|'%'
name|'self'
op|'.'
name|'http_response_content'
op|'['
op|':'
number|'60'
op|']'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'b'
name|'and'
string|"'%s: %s'"
op|'%'
op|'('
name|'a'
op|','
name|'b'
op|')'
name|'or'
name|'a'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
