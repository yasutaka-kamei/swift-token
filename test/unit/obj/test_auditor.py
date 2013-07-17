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
name|'test'
name|'import'
name|'unit'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
name|'import'
name|'mock'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'shutil'
name|'import'
name|'rmtree'
newline|'\n'
name|'from'
name|'hashlib'
name|'import'
name|'md5'
newline|'\n'
name|'from'
name|'tempfile'
name|'import'
name|'mkdtemp'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
name|'import'
name|'FakeLogger'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'obj'
name|'import'
name|'auditor'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'obj'
op|'.'
name|'diskfile'
name|'import'
name|'DiskFile'
op|','
name|'write_metadata'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'obj'
op|'.'
name|'server'
name|'import'
name|'DATADIR'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'hash_path'
op|','
name|'mkdirs'
op|','
name|'normalize_timestamp'
op|','
name|'storage_directory'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'obj'
op|'.'
name|'base'
name|'import'
name|'invalidate_hash'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestAuditor
name|'class'
name|'TestAuditor'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|setUp
indent|'    '
name|'def'
name|'setUp'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'testdir'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'mkdtemp'
op|'('
op|')'
op|','
string|"'tmp_test_object_auditor'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'devices'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
string|"'node'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'='
name|'FakeLogger'
op|'('
op|')'
newline|'\n'
name|'rmtree'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
name|'ignore_errors'
op|'='
number|'1'
op|')'
newline|'\n'
name|'mkdirs'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'objects'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|','
string|"'objects'"
op|')'
newline|'\n'
nl|'\n'
name|'os'
op|'.'
name|'mkdir'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sdb'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'objects_2'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sdb'"
op|','
string|"'objects'"
op|')'
newline|'\n'
nl|'\n'
name|'os'
op|'.'
name|'mkdir'
op|'('
name|'self'
op|'.'
name|'objects'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'parts'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'part'
name|'in'
op|'['
string|"'0'"
op|','
string|"'1'"
op|','
string|"'2'"
op|','
string|"'3'"
op|']'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'parts'
op|'['
name|'part'
op|']'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'objects'
op|','
name|'part'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'mkdir'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'objects'
op|','
name|'part'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'conf'
op|'='
name|'dict'
op|'('
nl|'\n'
name|'devices'
op|'='
name|'self'
op|'.'
name|'devices'
op|','
nl|'\n'
name|'mount_check'
op|'='
string|"'false'"
op|','
nl|'\n'
name|'object_size_stats'
op|'='
string|"'10,100,1024,10240'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'disk_file'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|','
string|"'0'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|','
nl|'\n'
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
nl|'\n'
DECL|member|tearDown
dedent|''
name|'def'
name|'tearDown'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'rmtree'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'dirname'
op|'('
name|'self'
op|'.'
name|'testdir'
op|')'
op|','
name|'ignore_errors'
op|'='
number|'1'
op|')'
newline|'\n'
name|'unit'
op|'.'
name|'xattr_data'
op|'='
op|'{'
op|'}'
newline|'\n'
nl|'\n'
DECL|member|test_object_audit_extra_data
dedent|''
name|'def'
name|'test_object_audit_extra_data'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'auditor'
op|'='
name|'auditor'
op|'.'
name|'AuditorWorker'
op|'('
name|'self'
op|'.'
name|'conf'
op|','
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'data'
op|'='
string|"'0'"
op|'*'
number|'1024'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'writer'
op|'('
op|')'
name|'as'
name|'writer'
op|':'
newline|'\n'
indent|'            '
name|'writer'
op|'.'
name|'write'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'timestamp'
op|'='
name|'str'
op|'('
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
name|'metadata'
op|'='
op|'{'
nl|'\n'
string|"'ETag'"
op|':'
name|'etag'
op|','
nl|'\n'
string|"'X-Timestamp'"
op|':'
name|'timestamp'
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
name|'str'
op|'('
name|'os'
op|'.'
name|'fstat'
op|'('
name|'writer'
op|'.'
name|'fd'
op|')'
op|'.'
name|'st_size'
op|')'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'writer'
op|'.'
name|'put'
op|'('
name|'metadata'
op|')'
newline|'\n'
name|'pre_quarantines'
op|'='
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'object_audit'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'datadir'
op|','
name|'timestamp'
op|'+'
string|"'.data'"
op|')'
op|','
nl|'\n'
string|"'sda'"
op|','
string|"'0'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
op|','
name|'pre_quarantines'
op|')'
newline|'\n'
nl|'\n'
name|'os'
op|'.'
name|'write'
op|'('
name|'writer'
op|'.'
name|'fd'
op|','
string|"'extra_data'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'object_audit'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'datadir'
op|','
name|'timestamp'
op|'+'
string|"'.data'"
op|')'
op|','
nl|'\n'
string|"'sda'"
op|','
string|"'0'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
op|','
name|'pre_quarantines'
op|'+'
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_object_audit_diff_data
dedent|''
dedent|''
name|'def'
name|'test_object_audit_diff_data'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'auditor'
op|'='
name|'auditor'
op|'.'
name|'AuditorWorker'
op|'('
name|'self'
op|'.'
name|'conf'
op|','
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'data'
op|'='
string|"'0'"
op|'*'
number|'1024'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'timestamp'
op|'='
name|'str'
op|'('
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'writer'
op|'('
op|')'
name|'as'
name|'writer'
op|':'
newline|'\n'
indent|'            '
name|'writer'
op|'.'
name|'write'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'='
op|'{'
nl|'\n'
string|"'ETag'"
op|':'
name|'etag'
op|','
nl|'\n'
string|"'X-Timestamp'"
op|':'
name|'timestamp'
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
name|'str'
op|'('
name|'os'
op|'.'
name|'fstat'
op|'('
name|'writer'
op|'.'
name|'fd'
op|')'
op|'.'
name|'st_size'
op|')'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'writer'
op|'.'
name|'put'
op|'('
name|'metadata'
op|')'
newline|'\n'
name|'pre_quarantines'
op|'='
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
newline|'\n'
nl|'\n'
comment|'# remake so it will have metadata'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'disk_file'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|','
string|"'0'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|','
nl|'\n'
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'object_audit'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'datadir'
op|','
name|'timestamp'
op|'+'
string|"'.data'"
op|')'
op|','
nl|'\n'
string|"'sda'"
op|','
string|"'0'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
op|','
name|'pre_quarantines'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
string|"'1'"
op|'+'
string|"'0'"
op|'*'
number|'1023'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'['
string|"'ETag'"
op|']'
op|'='
name|'etag'
newline|'\n'
nl|'\n'
name|'with'
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'writer'
op|'('
op|')'
name|'as'
name|'writer'
op|':'
newline|'\n'
indent|'            '
name|'writer'
op|'.'
name|'write'
op|'('
name|'data'
op|')'
newline|'\n'
name|'writer'
op|'.'
name|'put'
op|'('
name|'metadata'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'object_audit'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'datadir'
op|','
name|'timestamp'
op|'+'
string|"'.data'"
op|')'
op|','
nl|'\n'
string|"'sda'"
op|','
string|"'0'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
op|','
name|'pre_quarantines'
op|'+'
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_object_audit_no_meta
dedent|''
name|'def'
name|'test_object_audit_no_meta'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'timestamp'
op|'='
name|'str'
op|'('
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
name|'path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'datadir'
op|','
name|'timestamp'
op|'+'
string|"'.data'"
op|')'
newline|'\n'
name|'mkdirs'
op|'('
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'datadir'
op|')'
newline|'\n'
name|'fp'
op|'='
name|'open'
op|'('
name|'path'
op|','
string|"'w'"
op|')'
newline|'\n'
name|'fp'
op|'.'
name|'write'
op|'('
string|"'0'"
op|'*'
number|'1024'
op|')'
newline|'\n'
name|'fp'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
name|'invalidate_hash'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'dirname'
op|'('
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'datadir'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auditor'
op|'='
name|'auditor'
op|'.'
name|'AuditorWorker'
op|'('
name|'self'
op|'.'
name|'conf'
op|','
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'pre_quarantines'
op|'='
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
newline|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'object_audit'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'datadir'
op|','
name|'timestamp'
op|'+'
string|"'.data'"
op|')'
op|','
nl|'\n'
string|"'sda'"
op|','
string|"'0'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
op|','
name|'pre_quarantines'
op|'+'
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_generic_exception_handling
dedent|''
name|'def'
name|'test_generic_exception_handling'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'auditor'
op|'='
name|'auditor'
op|'.'
name|'AuditorWorker'
op|'('
name|'self'
op|'.'
name|'conf'
op|','
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'timestamp'
op|'='
name|'str'
op|'('
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
name|'pre_errors'
op|'='
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'errors'
newline|'\n'
name|'data'
op|'='
string|"'0'"
op|'*'
number|'1024'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'writer'
op|'('
op|')'
name|'as'
name|'writer'
op|':'
newline|'\n'
indent|'            '
name|'writer'
op|'.'
name|'write'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'='
op|'{'
nl|'\n'
string|"'ETag'"
op|':'
name|'etag'
op|','
nl|'\n'
string|"'X-Timestamp'"
op|':'
name|'timestamp'
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
name|'str'
op|'('
name|'os'
op|'.'
name|'fstat'
op|'('
name|'writer'
op|'.'
name|'fd'
op|')'
op|'.'
name|'st_size'
op|')'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'writer'
op|'.'
name|'put'
op|'('
name|'metadata'
op|')'
newline|'\n'
dedent|''
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'swift.obj.diskfile.DiskFile'"
op|','
nl|'\n'
name|'lambda'
op|'*'
name|'_'
op|':'
number|'1'
op|'/'
number|'0'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'audit_all_objects'
op|'('
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'errors'
op|','
name|'pre_errors'
op|'+'
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_object_run_once_pass
dedent|''
name|'def'
name|'test_object_run_once_pass'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'auditor'
op|'='
name|'auditor'
op|'.'
name|'AuditorWorker'
op|'('
name|'self'
op|'.'
name|'conf'
op|','
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'log_time'
op|'='
number|'0'
newline|'\n'
name|'timestamp'
op|'='
name|'str'
op|'('
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
name|'pre_quarantines'
op|'='
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
newline|'\n'
name|'data'
op|'='
string|"'0'"
op|'*'
number|'1024'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'writer'
op|'('
op|')'
name|'as'
name|'writer'
op|':'
newline|'\n'
indent|'            '
name|'writer'
op|'.'
name|'write'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'='
op|'{'
nl|'\n'
string|"'ETag'"
op|':'
name|'etag'
op|','
nl|'\n'
string|"'X-Timestamp'"
op|':'
name|'timestamp'
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
name|'str'
op|'('
name|'os'
op|'.'
name|'fstat'
op|'('
name|'writer'
op|'.'
name|'fd'
op|')'
op|'.'
name|'st_size'
op|')'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'writer'
op|'.'
name|'put'
op|'('
name|'metadata'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'audit_all_objects'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
op|','
name|'pre_quarantines'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'stats_buckets'
op|'['
number|'1024'
op|']'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'stats_buckets'
op|'['
number|'10240'
op|']'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_object_run_once_no_sda
dedent|''
name|'def'
name|'test_object_run_once_no_sda'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'auditor'
op|'='
name|'auditor'
op|'.'
name|'AuditorWorker'
op|'('
name|'self'
op|'.'
name|'conf'
op|','
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'timestamp'
op|'='
name|'str'
op|'('
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
name|'pre_quarantines'
op|'='
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
newline|'\n'
name|'data'
op|'='
string|"'0'"
op|'*'
number|'1024'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'writer'
op|'('
op|')'
name|'as'
name|'writer'
op|':'
newline|'\n'
indent|'            '
name|'writer'
op|'.'
name|'write'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'='
op|'{'
nl|'\n'
string|"'ETag'"
op|':'
name|'etag'
op|','
nl|'\n'
string|"'X-Timestamp'"
op|':'
name|'timestamp'
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
name|'str'
op|'('
name|'os'
op|'.'
name|'fstat'
op|'('
name|'writer'
op|'.'
name|'fd'
op|')'
op|'.'
name|'st_size'
op|')'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'writer'
op|'.'
name|'put'
op|'('
name|'metadata'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'write'
op|'('
name|'writer'
op|'.'
name|'fd'
op|','
string|"'extra_data'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'audit_all_objects'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
op|','
name|'pre_quarantines'
op|'+'
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_object_run_once_multi_devices
dedent|''
name|'def'
name|'test_object_run_once_multi_devices'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'auditor'
op|'='
name|'auditor'
op|'.'
name|'AuditorWorker'
op|'('
name|'self'
op|'.'
name|'conf'
op|','
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'timestamp'
op|'='
name|'str'
op|'('
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
name|'pre_quarantines'
op|'='
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
newline|'\n'
name|'data'
op|'='
string|"'0'"
op|'*'
number|'10'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'writer'
op|'('
op|')'
name|'as'
name|'writer'
op|':'
newline|'\n'
indent|'            '
name|'writer'
op|'.'
name|'write'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'='
op|'{'
nl|'\n'
string|"'ETag'"
op|':'
name|'etag'
op|','
nl|'\n'
string|"'X-Timestamp'"
op|':'
name|'timestamp'
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
name|'str'
op|'('
name|'os'
op|'.'
name|'fstat'
op|'('
name|'writer'
op|'.'
name|'fd'
op|')'
op|'.'
name|'st_size'
op|')'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'writer'
op|'.'
name|'put'
op|'('
name|'metadata'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'audit_all_objects'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'disk_file'
op|'='
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sdb'"
op|','
string|"'0'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
nl|'\n'
string|"'ob'"
op|','
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'data'
op|'='
string|"'1'"
op|'*'
number|'10'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'writer'
op|'('
op|')'
name|'as'
name|'writer'
op|':'
newline|'\n'
indent|'            '
name|'writer'
op|'.'
name|'write'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'='
op|'{'
nl|'\n'
string|"'ETag'"
op|':'
name|'etag'
op|','
nl|'\n'
string|"'X-Timestamp'"
op|':'
name|'timestamp'
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
name|'str'
op|'('
name|'os'
op|'.'
name|'fstat'
op|'('
name|'writer'
op|'.'
name|'fd'
op|')'
op|'.'
name|'st_size'
op|')'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'writer'
op|'.'
name|'put'
op|'('
name|'metadata'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'write'
op|'('
name|'writer'
op|'.'
name|'fd'
op|','
string|"'extra_data'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'audit_all_objects'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'quarantines'
op|','
name|'pre_quarantines'
op|'+'
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_object_run_fast_track_non_zero
dedent|''
name|'def'
name|'test_object_run_fast_track_non_zero'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'auditor'
op|'='
name|'auditor'
op|'.'
name|'ObjectAuditor'
op|'('
name|'self'
op|'.'
name|'conf'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'log_time'
op|'='
number|'0'
newline|'\n'
name|'data'
op|'='
string|"'0'"
op|'*'
number|'1024'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'writer'
op|'('
op|')'
name|'as'
name|'writer'
op|':'
newline|'\n'
indent|'            '
name|'writer'
op|'.'
name|'write'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
name|'data'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'='
op|'{'
nl|'\n'
string|"'ETag'"
op|':'
name|'etag'
op|','
nl|'\n'
string|"'X-Timestamp'"
op|':'
name|'str'
op|'('
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|')'
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
name|'str'
op|'('
name|'os'
op|'.'
name|'fstat'
op|'('
name|'writer'
op|'.'
name|'fd'
op|')'
op|'.'
name|'st_size'
op|')'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'writer'
op|'.'
name|'put'
op|'('
name|'metadata'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'etag'
op|'.'
name|'update'
op|'('
string|"'1'"
op|'+'
string|"'0'"
op|'*'
number|'1023'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'['
string|"'ETag'"
op|']'
op|'='
name|'etag'
newline|'\n'
name|'write_metadata'
op|'('
name|'writer'
op|'.'
name|'fd'
op|','
name|'metadata'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'quarantine_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
nl|'\n'
string|"'sda'"
op|','
string|"'quarantined'"
op|','
string|"'objects'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'run_once'
op|'('
name|'zero_byte_fps'
op|'='
number|'50'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'isdir'
op|'('
name|'quarantine_path'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'isdir'
op|'('
name|'quarantine_path'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|setup_bad_zero_byte
dedent|''
name|'def'
name|'setup_bad_zero_byte'
op|'('
name|'self'
op|','
name|'with_ts'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'auditor'
op|'='
name|'auditor'
op|'.'
name|'ObjectAuditor'
op|'('
name|'self'
op|'.'
name|'conf'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'log_time'
op|'='
number|'0'
newline|'\n'
name|'ts_file_path'
op|'='
string|"''"
newline|'\n'
name|'if'
name|'with_ts'
op|':'
newline|'\n'
nl|'\n'
indent|'            '
name|'name_hash'
op|'='
name|'hash_path'
op|'('
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'dir_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
string|"'sda'"
op|','
nl|'\n'
name|'storage_directory'
op|'('
name|'DATADIR'
op|','
string|"'0'"
op|','
name|'name_hash'
op|')'
op|')'
newline|'\n'
name|'ts_file_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'dir_path'
op|','
string|"'99999.ts'"
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
name|'dir_path'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'mkdirs'
op|'('
name|'dir_path'
op|')'
newline|'\n'
dedent|''
name|'fp'
op|'='
name|'open'
op|'('
name|'ts_file_path'
op|','
string|"'w'"
op|')'
newline|'\n'
name|'fp'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'writer'
op|'('
op|')'
name|'as'
name|'writer'
op|':'
newline|'\n'
indent|'            '
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'='
op|'{'
nl|'\n'
string|"'ETag'"
op|':'
name|'etag'
op|','
nl|'\n'
string|"'X-Timestamp'"
op|':'
name|'str'
op|'('
name|'normalize_timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|')'
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
number|'10'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'writer'
op|'.'
name|'put'
op|'('
name|'metadata'
op|')'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'metadata'
op|'['
string|"'ETag'"
op|']'
op|'='
name|'etag'
newline|'\n'
name|'write_metadata'
op|'('
name|'writer'
op|'.'
name|'fd'
op|','
name|'metadata'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'data_file'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'data_file'
newline|'\n'
dedent|''
name|'return'
name|'ts_file_path'
newline|'\n'
nl|'\n'
DECL|member|test_object_run_fast_track_all
dedent|''
name|'def'
name|'test_object_run_fast_track_all'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'setup_bad_zero_byte'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'quarantine_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
nl|'\n'
string|"'sda'"
op|','
string|"'quarantined'"
op|','
string|"'objects'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'isdir'
op|'('
name|'quarantine_path'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_object_run_fast_track_zero
dedent|''
name|'def'
name|'test_object_run_fast_track_zero'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'setup_bad_zero_byte'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'run_once'
op|'('
name|'zero_byte_fps'
op|'='
number|'50'
op|')'
newline|'\n'
name|'quarantine_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
nl|'\n'
string|"'sda'"
op|','
string|"'quarantined'"
op|','
string|"'objects'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'isdir'
op|'('
name|'quarantine_path'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_with_tombstone
dedent|''
name|'def'
name|'test_with_tombstone'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'ts_file_path'
op|'='
name|'self'
op|'.'
name|'setup_bad_zero_byte'
op|'('
name|'with_ts'
op|'='
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'run_once'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'ts_file_path'
op|'.'
name|'endswith'
op|'('
string|"'ts'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'ts_file_path'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_sleeper
dedent|''
name|'def'
name|'test_sleeper'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'auditor'
op|'.'
name|'SLEEP_BETWEEN_AUDITS'
op|'='
number|'0.10'
newline|'\n'
name|'my_auditor'
op|'='
name|'auditor'
op|'.'
name|'ObjectAuditor'
op|'('
name|'self'
op|'.'
name|'conf'
op|')'
newline|'\n'
name|'start'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'my_auditor'
op|'.'
name|'_sleep'
op|'('
op|')'
newline|'\n'
name|'delta_t'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'start'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'delta_t'
op|'>'
number|'0.08'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'delta_t'
op|'<'
number|'0.12'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_object_run_fast_track_zero_check_closed
dedent|''
name|'def'
name|'test_object_run_fast_track_zero_check_closed'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'rat'
op|'='
op|'['
name|'False'
op|']'
newline|'\n'
nl|'\n'
DECL|class|FakeFile
name|'class'
name|'FakeFile'
op|'('
name|'DiskFile'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|close
indent|'            '
name|'def'
name|'close'
op|'('
name|'self'
op|','
name|'verify_file'
op|'='
name|'True'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'rat'
op|'['
number|'0'
op|']'
op|'='
name|'True'
newline|'\n'
name|'DiskFile'
op|'.'
name|'close'
op|'('
name|'self'
op|','
name|'verify_file'
op|'='
name|'verify_file'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'setup_bad_zero_byte'
op|'('
op|')'
newline|'\n'
name|'was_df'
op|'='
name|'auditor'
op|'.'
name|'diskfile'
op|'.'
name|'DiskFile'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'auditor'
op|'.'
name|'diskfile'
op|'.'
name|'DiskFile'
op|'='
name|'FakeFile'
newline|'\n'
name|'self'
op|'.'
name|'auditor'
op|'.'
name|'run_once'
op|'('
name|'zero_byte_fps'
op|'='
number|'50'
op|')'
newline|'\n'
DECL|variable|quarantine_path
name|'quarantine_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
nl|'\n'
string|"'sda'"
op|','
string|"'quarantined'"
op|','
string|"'objects'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'isdir'
op|'('
name|'quarantine_path'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'rat'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'auditor'
op|'.'
name|'diskfile'
op|'.'
name|'DiskFile'
op|'='
name|'was_df'
newline|'\n'
nl|'\n'
DECL|member|test_run_forever
dedent|''
dedent|''
name|'def'
name|'test_run_forever'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|class|StopForever
indent|'        '
name|'class'
name|'StopForever'
op|'('
name|'Exception'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
nl|'\n'
DECL|class|ObjectAuditorMock
dedent|''
name|'class'
name|'ObjectAuditorMock'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|variable|check_args
indent|'            '
name|'check_args'
op|'='
op|'('
op|')'
newline|'\n'
DECL|variable|check_kwargs
name|'check_kwargs'
op|'='
op|'{'
op|'}'
newline|'\n'
DECL|variable|fork_called
name|'fork_called'
op|'='
number|'0'
newline|'\n'
DECL|variable|fork_res
name|'fork_res'
op|'='
number|'0'
newline|'\n'
nl|'\n'
DECL|member|mock_run
name|'def'
name|'mock_run'
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
indent|'                '
name|'self'
op|'.'
name|'check_args'
op|'='
name|'args'
newline|'\n'
name|'self'
op|'.'
name|'check_kwargs'
op|'='
name|'kwargs'
newline|'\n'
nl|'\n'
DECL|member|mock_sleep
dedent|''
name|'def'
name|'mock_sleep'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'StopForever'
op|'('
string|"'stop'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|mock_fork
dedent|''
name|'def'
name|'mock_fork'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'fork_called'
op|'+='
number|'1'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'fork_res'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'my_auditor'
op|'='
name|'auditor'
op|'.'
name|'ObjectAuditor'
op|'('
name|'dict'
op|'('
name|'devices'
op|'='
name|'self'
op|'.'
name|'devices'
op|','
nl|'\n'
name|'mount_check'
op|'='
string|"'false'"
op|','
nl|'\n'
name|'zero_byte_files_per_second'
op|'='
number|'89'
op|')'
op|')'
newline|'\n'
name|'mocker'
op|'='
name|'ObjectAuditorMock'
op|'('
op|')'
newline|'\n'
name|'my_auditor'
op|'.'
name|'run_once'
op|'='
name|'mocker'
op|'.'
name|'mock_run'
newline|'\n'
name|'my_auditor'
op|'.'
name|'_sleep'
op|'='
name|'mocker'
op|'.'
name|'mock_sleep'
newline|'\n'
name|'was_fork'
op|'='
name|'os'
op|'.'
name|'fork'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'os'
op|'.'
name|'fork'
op|'='
name|'mocker'
op|'.'
name|'mock_fork'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'StopForever'
op|','
nl|'\n'
name|'my_auditor'
op|'.'
name|'run_forever'
op|','
name|'zero_byte_fps'
op|'='
number|'50'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mocker'
op|'.'
name|'check_kwargs'
op|'['
string|"'zero_byte_fps'"
op|']'
op|','
number|'50'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mocker'
op|'.'
name|'fork_called'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'StopForever'
op|','
name|'my_auditor'
op|'.'
name|'run_forever'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mocker'
op|'.'
name|'fork_called'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mocker'
op|'.'
name|'check_args'
op|','
op|'('
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'mocker'
op|'.'
name|'fork_res'
op|'='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'StopForever'
op|','
name|'my_auditor'
op|'.'
name|'run_forever'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mocker'
op|'.'
name|'fork_called'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'mocker'
op|'.'
name|'check_kwargs'
op|'['
string|"'zero_byte_fps'"
op|']'
op|','
number|'89'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'os'
op|'.'
name|'fork'
op|'='
name|'was_fork'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
dedent|''
name|'if'
name|'__name__'
op|'=='
string|"'__main__'"
op|':'
newline|'\n'
indent|'    '
name|'unittest'
op|'.'
name|'main'
op|'('
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
