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
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'socket'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'hashlib'
name|'import'
name|'md5'
newline|'\n'
name|'from'
name|'random'
name|'import'
name|'choice'
op|','
name|'random'
newline|'\n'
name|'from'
name|'urllib'
name|'import'
name|'quote'
newline|'\n'
nl|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'Timeout'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'obj'
name|'import'
name|'server'
name|'as'
name|'object_server'
newline|'\n'
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
name|'exceptions'
name|'import'
name|'ConnectionTimeout'
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
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'get_logger'
op|','
name|'renamer'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'exceptions'
name|'import'
name|'AuditException'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ObjectAuditor
name|'class'
name|'ObjectAuditor'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Audit objects."""'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'server_conf'
op|','
name|'auditor_conf'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'auditor_conf'
op|','
string|"'object-auditor'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'devices'
op|'='
name|'server_conf'
op|'.'
name|'get'
op|'('
string|"'devices'"
op|','
string|"'/srv/node'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'mount_check'
op|'='
name|'server_conf'
op|'.'
name|'get'
op|'('
string|"'mount_check'"
op|','
string|"'true'"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
name|'in'
op|'('
string|"'true'"
op|','
string|"'t'"
op|','
string|"'1'"
op|','
string|"'on'"
op|','
string|"'yes'"
op|','
string|"'y'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'interval'
op|'='
name|'int'
op|'('
name|'auditor_conf'
op|'.'
name|'get'
op|'('
string|"'interval'"
op|','
number|'1800'
op|')'
op|')'
newline|'\n'
name|'swift_dir'
op|'='
name|'server_conf'
op|'.'
name|'get'
op|'('
string|"'swift_dir'"
op|','
string|"'/etc/swift'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'container_ring_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'swift_dir'
op|','
string|"'container.ring.gz'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'container_ring'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'node_timeout'
op|'='
name|'int'
op|'('
name|'auditor_conf'
op|'.'
name|'get'
op|'('
string|"'node_timeout'"
op|','
number|'10'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'conn_timeout'
op|'='
name|'float'
op|'('
name|'auditor_conf'
op|'.'
name|'get'
op|'('
string|"'conn_timeout'"
op|','
number|'0.5'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'passes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'quarantines'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'errors'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'container_passes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'container_failures'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'container_errors'
op|'='
number|'0'
newline|'\n'
nl|'\n'
DECL|member|get_container_ring
dedent|''
name|'def'
name|'get_container_ring'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Get the container ring, loading it if neccesary.\n\n        :returns: container ring\n        """'
newline|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'container_ring'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
nl|'\n'
string|"'Loading container ring from %s'"
op|'%'
name|'self'
op|'.'
name|'container_ring_path'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'container_ring'
op|'='
name|'Ring'
op|'('
name|'self'
op|'.'
name|'container_ring_path'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'container_ring'
newline|'\n'
nl|'\n'
DECL|member|audit_forever
dedent|''
name|'def'
name|'audit_forever'
op|'('
name|'self'
op|')'
op|':'
comment|'# pragma: no cover'
newline|'\n'
indent|'        '
string|'"""Run the object audit until stopped."""'
newline|'\n'
name|'reported'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'time'
op|'.'
name|'sleep'
op|'('
name|'random'
op|'('
op|')'
op|'*'
name|'self'
op|'.'
name|'interval'
op|')'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'begin'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
comment|"# read from container ring to ensure it's fresh"
nl|'\n'
name|'self'
op|'.'
name|'get_container_ring'
op|'('
op|')'
op|'.'
name|'get_nodes'
op|'('
string|"''"
op|')'
newline|'\n'
name|'for'
name|'device'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'self'
op|'.'
name|'devices'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'self'
op|'.'
name|'mount_check'
name|'and'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'ismount'
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
name|'device'
op|')'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
nl|'\n'
string|"'Skipping %s as it is not mounted'"
op|'%'
name|'device'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'object_audit'
op|'('
name|'device'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'reported'
op|'>='
number|'3600'
op|':'
comment|'# once an hour'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
nl|'\n'
string|"'Since %s: Locally: %d passed audit, %d quarantined, %d '"
nl|'\n'
string|"'errors  Remote audits with containers: %s passed audit, '"
nl|'\n'
string|"'%s failed audit, %s errors'"
op|'%'
nl|'\n'
op|'('
name|'time'
op|'.'
name|'ctime'
op|'('
name|'reported'
op|')'
op|','
name|'self'
op|'.'
name|'passes'
op|','
name|'self'
op|'.'
name|'quarantines'
op|','
nl|'\n'
name|'self'
op|'.'
name|'errors'
op|','
name|'self'
op|'.'
name|'container_passes'
op|','
nl|'\n'
name|'self'
op|'.'
name|'container_failures'
op|','
name|'self'
op|'.'
name|'container_errors'
op|')'
op|')'
newline|'\n'
name|'reported'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'passes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'quarantines'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'errors'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'container_passes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'container_failures'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'container_errors'
op|'='
number|'0'
newline|'\n'
dedent|''
name|'elapsed'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'begin'
newline|'\n'
name|'if'
name|'elapsed'
op|'<'
name|'self'
op|'.'
name|'interval'
op|':'
newline|'\n'
indent|'                '
name|'time'
op|'.'
name|'sleep'
op|'('
name|'self'
op|'.'
name|'interval'
op|'-'
name|'elapsed'
op|')'
newline|'\n'
nl|'\n'
DECL|member|audit_once
dedent|''
dedent|''
dedent|''
name|'def'
name|'audit_once'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Run the object audit once."""'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
string|'\'Begin object audit "once" mode\''
op|')'
newline|'\n'
name|'begin'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'for'
name|'device'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'self'
op|'.'
name|'devices'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'self'
op|'.'
name|'mount_check'
name|'and'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'ismount'
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
name|'device'
op|')'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
nl|'\n'
string|"'Skipping %s as it is not mounted'"
op|'%'
name|'device'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'object_audit'
op|'('
name|'device'
op|')'
newline|'\n'
dedent|''
name|'elapsed'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'begin'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
nl|'\n'
string|'\'Object audit "once" mode completed: %.02fs\''
op|'%'
name|'elapsed'
op|')'
newline|'\n'
nl|'\n'
DECL|member|object_audit
dedent|''
name|'def'
name|'object_audit'
op|'('
name|'self'
op|','
name|'device'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Walk the device, and audit any objects found."""'
newline|'\n'
name|'datadir'
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
name|'device'
op|','
name|'object_server'
op|'.'
name|'DATADIR'
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
name|'datadir'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
dedent|''
name|'name'
op|'='
name|'None'
newline|'\n'
name|'partition'
op|'='
name|'None'
newline|'\n'
name|'attempts'
op|'='
number|'100'
newline|'\n'
name|'while'
name|'not'
name|'name'
name|'and'
name|'attempts'
op|':'
newline|'\n'
indent|'            '
name|'attempts'
op|'-='
number|'1'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'partition'
op|'='
name|'choice'
op|'('
name|'os'
op|'.'
name|'listdir'
op|'('
name|'datadir'
op|')'
op|')'
newline|'\n'
name|'fpath'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'datadir'
op|','
name|'partition'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'isdir'
op|'('
name|'fpath'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'continue'
newline|'\n'
dedent|''
name|'suffix'
op|'='
name|'choice'
op|'('
name|'os'
op|'.'
name|'listdir'
op|'('
name|'fpath'
op|')'
op|')'
newline|'\n'
name|'fpath'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'fpath'
op|','
name|'suffix'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'isdir'
op|'('
name|'fpath'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'continue'
newline|'\n'
dedent|''
name|'hsh'
op|'='
name|'choice'
op|'('
name|'os'
op|'.'
name|'listdir'
op|'('
name|'fpath'
op|')'
op|')'
newline|'\n'
name|'fpath'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'fpath'
op|','
name|'hsh'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'isdir'
op|'('
name|'fpath'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'continue'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'IndexError'
op|':'
newline|'\n'
indent|'                '
name|'continue'
newline|'\n'
dedent|''
name|'for'
name|'fname'
name|'in'
name|'sorted'
op|'('
name|'os'
op|'.'
name|'listdir'
op|'('
name|'fpath'
op|')'
op|','
name|'reverse'
op|'='
name|'True'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'fname'
op|'.'
name|'endswith'
op|'('
string|"'.ts'"
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'break'
newline|'\n'
dedent|''
name|'if'
name|'fname'
op|'.'
name|'endswith'
op|'('
string|"'.data'"
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'name'
op|'='
name|'object_server'
op|'.'
name|'read_metadata'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'fpath'
op|','
name|'fname'
op|')'
op|')'
op|'['
string|"'name'"
op|']'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'if'
name|'not'
name|'name'
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
dedent|''
name|'_'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|'='
name|'name'
op|'.'
name|'split'
op|'('
string|"'/'"
op|','
number|'3'
op|')'
newline|'\n'
name|'df'
op|'='
name|'object_server'
op|'.'
name|'DiskFile'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
name|'device'
op|','
name|'partition'
op|','
name|'account'
op|','
nl|'\n'
name|'container'
op|','
name|'obj'
op|','
name|'keep_data_fp'
op|'='
name|'True'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'os'
op|'.'
name|'path'
op|'.'
name|'getsize'
op|'('
name|'df'
op|'.'
name|'data_file'
op|')'
op|'!='
name|'int'
op|'('
name|'df'
op|'.'
name|'metadata'
op|'['
string|"'Content-Length'"
op|']'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'AuditException'
op|'('
string|"'Content-Length of %s does not match '"
nl|'\n'
string|"'file size of %s'"
op|'%'
op|'('
name|'int'
op|'('
name|'df'
op|'.'
name|'metadata'
op|'['
string|"'Content-Length'"
op|']'
op|')'
op|','
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'getsize'
op|'('
name|'df'
op|'.'
name|'data_file'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'for'
name|'chunk'
name|'in'
name|'df'
op|':'
newline|'\n'
indent|'                '
name|'etag'
op|'.'
name|'update'
op|'('
name|'chunk'
op|')'
newline|'\n'
dedent|''
name|'etag'
op|'='
name|'etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'if'
name|'etag'
op|'!='
name|'df'
op|'.'
name|'metadata'
op|'['
string|"'ETag'"
op|']'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'AuditException'
op|'('
string|'"ETag of %s does not match file\'s md5 of "'
nl|'\n'
string|'"%s"'
op|'%'
op|'('
name|'df'
op|'.'
name|'metadata'
op|'['
string|"'ETag'"
op|']'
op|','
name|'etag'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'AuditException'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'quarantines'
op|'+='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
string|"'ERROR Object %s failed audit and will be '"
nl|'\n'
string|"'quarantined: %s'"
op|'%'
op|'('
name|'df'
op|'.'
name|'datadir'
op|','
name|'err'
op|')'
op|')'
newline|'\n'
name|'renamer'
op|'('
name|'df'
op|'.'
name|'datadir'
op|','
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
name|'device'
op|','
nl|'\n'
string|"'quarantined'"
op|','
string|"'objects'"
op|','
name|'os'
op|'.'
name|'path'
op|'.'
name|'basename'
op|'('
name|'df'
op|'.'
name|'datadir'
op|')'
op|')'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'except'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'errors'
op|'+='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
string|"'ERROR Trying to audit %s'"
op|'%'
name|'df'
op|'.'
name|'datadir'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'passes'
op|'+='
number|'1'
newline|'\n'
name|'found'
op|'='
name|'False'
newline|'\n'
name|'good_response'
op|'='
name|'False'
newline|'\n'
name|'results'
op|'='
op|'['
op|']'
newline|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'get_container_ring'
op|'('
op|')'
op|'.'
name|'get_nodes'
op|'('
name|'account'
op|','
name|'container'
op|')'
newline|'\n'
name|'for'
name|'node'
name|'in'
name|'nodes'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'with'
name|'ConnectionTimeout'
op|'('
name|'self'
op|'.'
name|'conn_timeout'
op|')'
op|':'
newline|'\n'
indent|'                    '
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
nl|'\n'
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'part'
op|','
string|"'GET'"
op|','
nl|'\n'
string|"'/%s/%s'"
op|'%'
op|'('
name|'account'
op|','
name|'container'
op|')'
op|','
nl|'\n'
name|'query_string'
op|'='
string|"'prefix=%s'"
op|'%'
name|'quote'
op|'('
name|'obj'
op|')'
op|')'
newline|'\n'
dedent|''
name|'with'
name|'Timeout'
op|'('
name|'self'
op|'.'
name|'node_timeout'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'resp'
op|'='
name|'conn'
op|'.'
name|'getresponse'
op|'('
op|')'
newline|'\n'
name|'body'
op|'='
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
dedent|''
name|'if'
number|'200'
op|'<='
name|'resp'
op|'.'
name|'status'
op|'<='
number|'299'
op|':'
newline|'\n'
indent|'                    '
name|'for'
name|'oname'
name|'in'
name|'body'
op|'.'
name|'split'
op|'('
string|"'\\n'"
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'if'
name|'oname'
op|'=='
name|'obj'
op|':'
newline|'\n'
indent|'                            '
name|'found'
op|'='
name|'True'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'found'
op|':'
newline|'\n'
indent|'                        '
name|'break'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'results'
op|'.'
name|'append'
op|'('
string|"'%s:%s/%s %s %s = %s'"
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
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'resp'
op|'.'
name|'status'
op|','
nl|'\n'
name|'resp'
op|'.'
name|'reason'
op|','
name|'repr'
op|'('
name|'body'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'results'
op|'.'
name|'append'
op|'('
string|"'%s:%s/%s %s %s'"
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
name|'node'
op|'['
string|"'device'"
op|']'
op|','
nl|'\n'
name|'resp'
op|'.'
name|'status'
op|','
name|'resp'
op|'.'
name|'reason'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'socket'
op|'.'
name|'error'
op|','
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'results'
op|'.'
name|'append'
op|'('
string|"'%s:%s/%s Socket Error: %s'"
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
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'err'
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ConnectionTimeout'
op|':'
newline|'\n'
indent|'                '
name|'results'
op|'.'
name|'append'
op|'('
string|"'%(ip)s:%(port)s/%(device)s ConnectionTimeout'"
op|'%'
nl|'\n'
name|'node'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Timeout'
op|':'
newline|'\n'
indent|'                '
name|'results'
op|'.'
name|'append'
op|'('
string|"'%(ip)s:%(port)s/%(device)s Timeout'"
op|'%'
name|'node'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|','
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
string|"'ERROR With remote server '"
nl|'\n'
string|"'%(ip)s:%(port)s/%(device)s'"
op|'%'
name|'node'
op|')'
newline|'\n'
name|'results'
op|'.'
name|'append'
op|'('
string|"'%s:%s/%s Exception: %s'"
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
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'err'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'found'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'container_passes'
op|'+='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
string|"'Audit passed for %s %s'"
op|'%'
op|'('
name|'name'
op|','
name|'df'
op|'.'
name|'datadir'
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'good_response'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'container_failures'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'container_errors'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
string|"'ERROR Could not find object %s %s on any of '"
nl|'\n'
string|"'the primary container servers it should be on: %s'"
op|'%'
op|'('
name|'name'
op|','
nl|'\n'
name|'df'
op|'.'
name|'datadir'
op|','
name|'results'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
endmarker|''
end_unit
