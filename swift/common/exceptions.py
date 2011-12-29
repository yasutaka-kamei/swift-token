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
name|'from'
name|'eventlet'
name|'import'
name|'Timeout'
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
DECL|class|AuditException
dedent|''
dedent|''
name|'class'
name|'AuditException'
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
DECL|class|DiskFileError
dedent|''
name|'class'
name|'DiskFileError'
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
DECL|class|DiskFileNotExist
dedent|''
name|'class'
name|'DiskFileNotExist'
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
DECL|class|AuthException
dedent|''
name|'class'
name|'AuthException'
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
name|'Exception'
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
name|'Exception'
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
name|'Exception'
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
dedent|''
dedent|''
endmarker|''
end_unit
