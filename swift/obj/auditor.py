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
name|'import'
name|'time'
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
name|'diskfile'
newline|'\n'
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
name|'utils'
name|'import'
name|'get_logger'
op|','
name|'audit_location_generator'
op|','
name|'ratelimit_sleep'
op|','
name|'config_true_value'
op|','
name|'dump_recon_cache'
op|','
name|'list_from_csv'
op|','
name|'json'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'exceptions'
name|'import'
name|'AuditException'
op|','
name|'DiskFileError'
op|','
name|'DiskFileNotExist'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'daemon'
name|'import'
name|'Daemon'
newline|'\n'
nl|'\n'
DECL|variable|SLEEP_BETWEEN_AUDITS
name|'SLEEP_BETWEEN_AUDITS'
op|'='
number|'30'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|AuditorWorker
name|'class'
name|'AuditorWorker'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Walk through file system to audit object"""'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'conf'
op|','
name|'logger'
op|','
name|'zero_byte_only_at_fps'
op|'='
number|'0'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'conf'
op|'='
name|'conf'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'='
name|'logger'
newline|'\n'
name|'self'
op|'.'
name|'devices'
op|'='
name|'conf'
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
name|'config_true_value'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'mount_check'"
op|','
string|"'true'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'max_files_per_second'
op|'='
name|'float'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'files_per_second'"
op|','
number|'20'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'max_bytes_per_second'
op|'='
name|'float'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'bytes_per_second'"
op|','
nl|'\n'
number|'10000000'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auditor_type'
op|'='
string|"'ALL'"
newline|'\n'
name|'self'
op|'.'
name|'zero_byte_only_at_fps'
op|'='
name|'zero_byte_only_at_fps'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'zero_byte_only_at_fps'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'max_files_per_second'
op|'='
name|'float'
op|'('
name|'self'
op|'.'
name|'zero_byte_only_at_fps'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'auditor_type'
op|'='
string|"'ZBF'"
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'log_time'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'log_time'"
op|','
number|'3600'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'files_running_time'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'bytes_running_time'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'bytes_processed'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'total_bytes_processed'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'total_files_processed'
op|'='
number|'0'
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
name|'recon_cache_path'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'recon_cache_path'"
op|','
nl|'\n'
string|"'/var/cache/swift'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'rcache'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'recon_cache_path'
op|','
string|'"object.recon"'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'stats_sizes'
op|'='
name|'sorted'
op|'('
nl|'\n'
op|'['
name|'int'
op|'('
name|'s'
op|')'
name|'for'
name|'s'
name|'in'
name|'list_from_csv'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'object_size_stats'"
op|')'
op|')'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'stats_buckets'
op|'='
name|'dict'
op|'('
nl|'\n'
op|'['
op|'('
name|'s'
op|','
number|'0'
op|')'
name|'for'
name|'s'
name|'in'
name|'self'
op|'.'
name|'stats_sizes'
op|'+'
op|'['
string|"'OVER'"
op|']'
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|audit_all_objects
dedent|''
name|'def'
name|'audit_all_objects'
op|'('
name|'self'
op|','
name|'mode'
op|'='
string|"'once'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|'\'Begin object audit "%s" mode (%s)\''
op|'%'
nl|'\n'
op|'('
name|'mode'
op|','
name|'self'
op|'.'
name|'auditor_type'
op|')'
op|')'
op|')'
newline|'\n'
name|'begin'
op|'='
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
name|'total_bytes_processed'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'total_files_processed'
op|'='
number|'0'
newline|'\n'
name|'total_quarantines'
op|'='
number|'0'
newline|'\n'
name|'total_errors'
op|'='
number|'0'
newline|'\n'
name|'time_auditing'
op|'='
number|'0'
newline|'\n'
name|'all_locs'
op|'='
name|'audit_location_generator'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
nl|'\n'
name|'object_server'
op|'.'
name|'DATADIR'
op|','
string|"'.data'"
op|','
nl|'\n'
name|'mount_check'
op|'='
name|'self'
op|'.'
name|'mount_check'
op|','
nl|'\n'
name|'logger'
op|'='
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'for'
name|'path'
op|','
name|'device'
op|','
name|'partition'
name|'in'
name|'all_locs'
op|':'
newline|'\n'
indent|'            '
name|'loop_time'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'object_audit'
op|'('
name|'path'
op|','
name|'device'
op|','
name|'partition'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'timing_since'
op|'('
string|"'timing'"
op|','
name|'loop_time'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'files_running_time'
op|'='
name|'ratelimit_sleep'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'files_running_time'
op|','
name|'self'
op|'.'
name|'max_files_per_second'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'total_files_processed'
op|'+='
number|'1'
newline|'\n'
name|'now'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'if'
name|'now'
op|'-'
name|'reported'
op|'>='
name|'self'
op|'.'
name|'log_time'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
nl|'\n'
string|"'Object audit (%(type)s). '"
nl|'\n'
string|"'Since %(start_time)s: Locally: %(passes)d passed, '"
nl|'\n'
string|"'%(quars)d quarantined, %(errors)d errors '"
nl|'\n'
string|"'files/sec: %(frate).2f , bytes/sec: %(brate).2f, '"
nl|'\n'
string|"'Total time: %(total).2f, Auditing time: %(audit).2f, '"
nl|'\n'
string|"'Rate: %(audit_rate).2f'"
op|')'
op|'%'
op|'{'
nl|'\n'
string|"'type'"
op|':'
name|'self'
op|'.'
name|'auditor_type'
op|','
nl|'\n'
string|"'start_time'"
op|':'
name|'time'
op|'.'
name|'ctime'
op|'('
name|'reported'
op|')'
op|','
nl|'\n'
string|"'passes'"
op|':'
name|'self'
op|'.'
name|'passes'
op|','
string|"'quars'"
op|':'
name|'self'
op|'.'
name|'quarantines'
op|','
nl|'\n'
string|"'errors'"
op|':'
name|'self'
op|'.'
name|'errors'
op|','
nl|'\n'
string|"'frate'"
op|':'
name|'self'
op|'.'
name|'passes'
op|'/'
op|'('
name|'now'
op|'-'
name|'reported'
op|')'
op|','
nl|'\n'
string|"'brate'"
op|':'
name|'self'
op|'.'
name|'bytes_processed'
op|'/'
op|'('
name|'now'
op|'-'
name|'reported'
op|')'
op|','
nl|'\n'
string|"'total'"
op|':'
op|'('
name|'now'
op|'-'
name|'begin'
op|')'
op|','
string|"'audit'"
op|':'
name|'time_auditing'
op|','
nl|'\n'
string|"'audit_rate'"
op|':'
name|'time_auditing'
op|'/'
op|'('
name|'now'
op|'-'
name|'begin'
op|')'
op|'}'
op|')'
newline|'\n'
name|'dump_recon_cache'
op|'('
op|'{'
string|"'object_auditor_stats_%s'"
op|'%'
nl|'\n'
name|'self'
op|'.'
name|'auditor_type'
op|':'
op|'{'
nl|'\n'
string|"'errors'"
op|':'
name|'self'
op|'.'
name|'errors'
op|','
nl|'\n'
string|"'passes'"
op|':'
name|'self'
op|'.'
name|'passes'
op|','
nl|'\n'
string|"'quarantined'"
op|':'
name|'self'
op|'.'
name|'quarantines'
op|','
nl|'\n'
string|"'bytes_processed'"
op|':'
name|'self'
op|'.'
name|'bytes_processed'
op|','
nl|'\n'
string|"'start_time'"
op|':'
name|'reported'
op|','
nl|'\n'
string|"'audit_time'"
op|':'
name|'time_auditing'
op|'}'
op|'}'
op|','
nl|'\n'
name|'self'
op|'.'
name|'rcache'
op|','
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'reported'
op|'='
name|'now'
newline|'\n'
name|'total_quarantines'
op|'+='
name|'self'
op|'.'
name|'quarantines'
newline|'\n'
name|'total_errors'
op|'+='
name|'self'
op|'.'
name|'errors'
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
name|'bytes_processed'
op|'='
number|'0'
newline|'\n'
dedent|''
name|'time_auditing'
op|'+='
op|'('
name|'now'
op|'-'
name|'loop_time'
op|')'
newline|'\n'
comment|'# Avoid divide by zero during very short runs'
nl|'\n'
dedent|''
name|'elapsed'
op|'='
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'begin'
op|')'
name|'or'
number|'0.000001'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
nl|'\n'
string|'\'Object audit (%(type)s) "%(mode)s" mode \''
nl|'\n'
string|"'completed: %(elapsed).02fs. Total quarantined: %(quars)d, '"
nl|'\n'
string|"'Total errors: %(errors)d, Total files/sec: %(frate).2f , '"
nl|'\n'
string|"'Total bytes/sec: %(brate).2f, Auditing time: %(audit).2f, '"
nl|'\n'
string|"'Rate: %(audit_rate).2f'"
op|')'
op|'%'
op|'{'
nl|'\n'
string|"'type'"
op|':'
name|'self'
op|'.'
name|'auditor_type'
op|','
string|"'mode'"
op|':'
name|'mode'
op|','
string|"'elapsed'"
op|':'
name|'elapsed'
op|','
nl|'\n'
string|"'quars'"
op|':'
name|'total_quarantines'
op|','
string|"'errors'"
op|':'
name|'total_errors'
op|','
nl|'\n'
string|"'frate'"
op|':'
name|'self'
op|'.'
name|'total_files_processed'
op|'/'
name|'elapsed'
op|','
nl|'\n'
string|"'brate'"
op|':'
name|'self'
op|'.'
name|'total_bytes_processed'
op|'/'
name|'elapsed'
op|','
nl|'\n'
string|"'audit'"
op|':'
name|'time_auditing'
op|','
string|"'audit_rate'"
op|':'
name|'time_auditing'
op|'/'
name|'elapsed'
op|'}'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'stats_sizes'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Object audit stats: %s'"
op|')'
op|'%'
name|'json'
op|'.'
name|'dumps'
op|'('
name|'self'
op|'.'
name|'stats_buckets'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|record_stats
dedent|''
dedent|''
name|'def'
name|'record_stats'
op|'('
name|'self'
op|','
name|'obj_size'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Based on config\'s object_size_stats will keep track of how many objects\n        fall into the specified ranges. For example with the following:\n\n        object_size_stats = 10, 100, 1024\n\n        and your system has 3 objects of sizes: 5, 20, and 10000 bytes the log\n        will look like: {"10": 1, "100": 1, "1024": 0, "OVER": 1}\n        """'
newline|'\n'
name|'for'
name|'size'
name|'in'
name|'self'
op|'.'
name|'stats_sizes'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'obj_size'
op|'<='
name|'size'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'stats_buckets'
op|'['
name|'size'
op|']'
op|'+='
number|'1'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'stats_buckets'
op|'['
string|'"OVER"'
op|']'
op|'+='
number|'1'
newline|'\n'
nl|'\n'
DECL|member|object_audit
dedent|''
dedent|''
name|'def'
name|'object_audit'
op|'('
name|'self'
op|','
name|'path'
op|','
name|'device'
op|','
name|'partition'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Audits the given object path.\n\n        :param path: a path to an object\n        :param device: the device the path is on\n        :param partition: the partition the path is on\n        """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'name'
op|'='
name|'diskfile'
op|'.'
name|'read_metadata'
op|'('
name|'path'
op|')'
op|'['
string|"'name'"
op|']'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'Timeout'
op|')'
name|'as'
name|'exc'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'AuditException'
op|'('
string|"'Error when reading metadata: %s'"
op|'%'
name|'exc'
op|')'
newline|'\n'
dedent|''
name|'_junk'
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
name|'diskfile'
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
nl|'\n'
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|','
name|'self'
op|'.'
name|'logger'
op|','
nl|'\n'
name|'keep_data_fp'
op|'='
name|'True'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'obj_size'
op|'='
name|'df'
op|'.'
name|'get_data_file_size'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'DiskFileError'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
name|'AuditException'
op|'('
name|'str'
op|'('
name|'e'
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'DiskFileNotExist'
op|':'
newline|'\n'
indent|'                    '
name|'return'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'stats_sizes'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'record_stats'
op|'('
name|'obj_size'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'zero_byte_only_at_fps'
name|'and'
name|'obj_size'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'passes'
op|'+='
number|'1'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'for'
name|'chunk'
name|'in'
name|'df'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'bytes_running_time'
op|'='
name|'ratelimit_sleep'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'bytes_running_time'
op|','
name|'self'
op|'.'
name|'max_bytes_per_second'
op|','
nl|'\n'
name|'incr_by'
op|'='
name|'len'
op|'('
name|'chunk'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'bytes_processed'
op|'+='
name|'len'
op|'('
name|'chunk'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'total_bytes_processed'
op|'+='
name|'len'
op|'('
name|'chunk'
op|')'
newline|'\n'
dedent|''
name|'df'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
name|'if'
name|'df'
op|'.'
name|'quarantined_dir'
op|':'
newline|'\n'
indent|'                    '
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
nl|'\n'
name|'_'
op|'('
string|'"ERROR Object %(path)s failed audit and will be "'
nl|'\n'
string|'"quarantined: ETag and file\'s md5 do not match"'
op|')'
op|','
nl|'\n'
op|'{'
string|"'path'"
op|':'
name|'path'
op|'}'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'                '
name|'df'
op|'.'
name|'close'
op|'('
name|'verify_file'
op|'='
name|'False'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'AuditException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|"'quarantines'"
op|')'
newline|'\n'
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
name|'_'
op|'('
string|"'ERROR Object %(obj)s failed audit and will '"
nl|'\n'
string|"'be quarantined: %(err)s'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'obj'"
op|':'
name|'path'
op|','
string|"'err'"
op|':'
name|'err'
op|'}'
op|')'
newline|'\n'
name|'diskfile'
op|'.'
name|'quarantine_renamer'
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
name|'devices'
op|','
name|'device'
op|')'
op|','
name|'path'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'Timeout'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|"'errors'"
op|')'
newline|'\n'
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
name|'_'
op|'('
string|"'ERROR Trying to audit %s'"
op|')'
op|','
name|'path'
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
nl|'\n'
nl|'\n'
DECL|class|ObjectAuditor
dedent|''
dedent|''
name|'class'
name|'ObjectAuditor'
op|'('
name|'Daemon'
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
name|'conf'
op|','
op|'**'
name|'options'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'conf'
op|'='
name|'conf'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'conf'
op|','
name|'log_route'
op|'='
string|"'object-auditor'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'conf_zero_byte_fps'
op|'='
name|'int'
op|'('
nl|'\n'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'zero_byte_files_per_second'"
op|','
number|'50'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_sleep
dedent|''
name|'def'
name|'_sleep'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'time'
op|'.'
name|'sleep'
op|'('
name|'SLEEP_BETWEEN_AUDITS'
op|')'
newline|'\n'
nl|'\n'
DECL|member|run_forever
dedent|''
name|'def'
name|'run_forever'
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
string|'"""Run the object audit until stopped."""'
newline|'\n'
comment|'# zero byte only command line option'
nl|'\n'
name|'zbo_fps'
op|'='
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'zero_byte_fps'"
op|','
number|'0'
op|')'
newline|'\n'
name|'if'
name|'zbo_fps'
op|':'
newline|'\n'
comment|'# only start parent'
nl|'\n'
indent|'            '
name|'parent'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'parent'
op|'='
name|'os'
op|'.'
name|'fork'
op|'('
op|')'
comment|'# child gets parent = 0'
newline|'\n'
dedent|''
name|'kwargs'
op|'='
op|'{'
string|"'mode'"
op|':'
string|"'forever'"
op|'}'
newline|'\n'
name|'if'
name|'parent'
op|':'
newline|'\n'
indent|'            '
name|'kwargs'
op|'['
string|"'zero_byte_fps'"
op|']'
op|'='
name|'zbo_fps'
name|'or'
name|'self'
op|'.'
name|'conf_zero_byte_fps'
newline|'\n'
dedent|''
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'run_once'
op|'('
op|'**'
name|'kwargs'
op|')'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'Timeout'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
name|'_'
op|'('
string|"'ERROR auditing'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'_sleep'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|run_once
dedent|''
dedent|''
name|'def'
name|'run_once'
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
string|'"""Run the object audit once."""'
newline|'\n'
name|'mode'
op|'='
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'mode'"
op|','
string|"'once'"
op|')'
newline|'\n'
name|'zero_byte_only_at_fps'
op|'='
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'zero_byte_fps'"
op|','
number|'0'
op|')'
newline|'\n'
name|'worker'
op|'='
name|'AuditorWorker'
op|'('
name|'self'
op|'.'
name|'conf'
op|','
name|'self'
op|'.'
name|'logger'
op|','
nl|'\n'
name|'zero_byte_only_at_fps'
op|'='
name|'zero_byte_only_at_fps'
op|')'
newline|'\n'
name|'worker'
op|'.'
name|'audit_all_objects'
op|'('
name|'mode'
op|'='
name|'mode'
op|')'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
