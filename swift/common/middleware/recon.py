begin_unit
comment|'# Copyright (c) 2010-2011 OpenStack, LLC.'
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
name|'errno'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
nl|'\n'
name|'from'
name|'webob'
name|'import'
name|'Request'
op|','
name|'Response'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'split_path'
op|','
name|'get_logger'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'constraints'
name|'import'
name|'check_mount'
newline|'\n'
name|'from'
name|'resource'
name|'import'
name|'getpagesize'
newline|'\n'
name|'from'
name|'hashlib'
name|'import'
name|'md5'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'    '
name|'import'
name|'simplejson'
name|'as'
name|'json'
newline|'\n'
dedent|''
name|'except'
name|'ImportError'
op|':'
newline|'\n'
indent|'    '
name|'import'
name|'json'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ReconMiddleware
dedent|''
name|'class'
name|'ReconMiddleware'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Recon middleware used for monitoring.\n\n    /recon/load|mem|async... will return various system metrics.\n\n    Needs to be added to the pipeline and a requires a filter\n    declaration in the object-server.conf:\n\n    [filter:recon]\n    use = egg:swift#recon\n    recon_cache_path = /var/cache/swift\n    """'
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
name|'app'
op|'='
name|'app'
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
string|"'/srv/node/'"
op|')'
newline|'\n'
name|'swift_dir'
op|'='
name|'conf'
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
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'conf'
op|','
name|'log_route'
op|'='
string|"'recon'"
op|')'
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
string|"'/var/cache/swift'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'object_recon_cache'
op|'='
string|'"%s/object.recon"'
op|'%'
name|'self'
op|'.'
name|'recon_cache_path'
newline|'\n'
name|'self'
op|'.'
name|'account_ring_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'swift_dir'
op|','
string|"'account.ring.gz'"
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
name|'object_ring_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'swift_dir'
op|','
string|"'object.ring.gz'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'rings'
op|'='
op|'['
name|'self'
op|'.'
name|'account_ring_path'
op|','
name|'self'
op|'.'
name|'container_ring_path'
op|','
name|'self'
op|'.'
name|'object_ring_path'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'mount_check'
op|'='
name|'conf'
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
nl|'\n'
DECL|member|get_mounted
dedent|''
name|'def'
name|'get_mounted'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get ALL mounted fs from /proc/mounts"""'
newline|'\n'
name|'mounts'
op|'='
op|'['
op|']'
newline|'\n'
name|'with'
name|'open'
op|'('
string|"'/proc/mounts'"
op|','
string|"'r'"
op|')'
name|'as'
name|'procmounts'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'line'
name|'in'
name|'procmounts'
op|':'
newline|'\n'
indent|'                '
name|'mount'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'mount'
op|'['
string|"'device'"
op|']'
op|','
name|'mount'
op|'['
string|"'path'"
op|']'
op|','
name|'opt1'
op|','
name|'opt2'
op|','
name|'opt3'
op|','
name|'opt4'
op|'='
name|'line'
op|'.'
name|'rstrip'
op|'('
op|')'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'mounts'
op|'.'
name|'append'
op|'('
name|'mount'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'mounts'
newline|'\n'
nl|'\n'
DECL|member|get_load
dedent|''
name|'def'
name|'get_load'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get info from /proc/loadavg"""'
newline|'\n'
name|'loadavg'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'onemin'
op|','
name|'fivemin'
op|','
name|'ftmin'
op|','
name|'tasks'
op|','
name|'procs'
op|'='
name|'open'
op|'('
string|"'/proc/loadavg'"
op|','
string|"'r'"
op|')'
op|'.'
name|'readline'
op|'('
op|')'
op|'.'
name|'rstrip'
op|'('
op|')'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'loadavg'
op|'['
string|"'1m'"
op|']'
op|'='
name|'float'
op|'('
name|'onemin'
op|')'
newline|'\n'
name|'loadavg'
op|'['
string|"'5m'"
op|']'
op|'='
name|'float'
op|'('
name|'fivemin'
op|')'
newline|'\n'
name|'loadavg'
op|'['
string|"'15m'"
op|']'
op|'='
name|'float'
op|'('
name|'ftmin'
op|')'
newline|'\n'
name|'loadavg'
op|'['
string|"'tasks'"
op|']'
op|'='
name|'tasks'
newline|'\n'
name|'loadavg'
op|'['
string|"'processes'"
op|']'
op|'='
name|'int'
op|'('
name|'procs'
op|')'
newline|'\n'
name|'return'
name|'loadavg'
newline|'\n'
nl|'\n'
DECL|member|get_mem
dedent|''
name|'def'
name|'get_mem'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get info from /proc/meminfo"""'
newline|'\n'
name|'meminfo'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'with'
name|'open'
op|'('
string|"'/proc/meminfo'"
op|','
string|"'r'"
op|')'
name|'as'
name|'memlines'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'i'
name|'in'
name|'memlines'
op|':'
newline|'\n'
indent|'                '
name|'entry'
op|'='
name|'i'
op|'.'
name|'rstrip'
op|'('
op|')'
op|'.'
name|'split'
op|'('
string|'":"'
op|')'
newline|'\n'
name|'meminfo'
op|'['
name|'entry'
op|'['
number|'0'
op|']'
op|']'
op|'='
name|'entry'
op|'['
number|'1'
op|']'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'meminfo'
newline|'\n'
nl|'\n'
DECL|member|get_async_info
dedent|''
name|'def'
name|'get_async_info'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get # of async pendings"""'
newline|'\n'
name|'asyncinfo'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'with'
name|'open'
op|'('
name|'self'
op|'.'
name|'object_recon_cache'
op|','
string|"'r'"
op|')'
name|'as'
name|'f'
op|':'
newline|'\n'
indent|'            '
name|'recondata'
op|'='
name|'json'
op|'.'
name|'load'
op|'('
name|'f'
op|')'
newline|'\n'
name|'if'
string|"'async_pending'"
name|'in'
name|'recondata'
op|':'
newline|'\n'
indent|'                '
name|'asyncinfo'
op|'['
string|"'async_pending'"
op|']'
op|'='
name|'recondata'
op|'['
string|"'async_pending'"
op|']'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'notice'
op|'('
name|'_'
op|'('
string|"'NOTICE: Async pendings not in recon data.'"
op|')'
op|')'
newline|'\n'
name|'asyncinfo'
op|'['
string|"'async_pending'"
op|']'
op|'='
op|'-'
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'asyncinfo'
newline|'\n'
nl|'\n'
DECL|member|get_replication_info
dedent|''
name|'def'
name|'get_replication_info'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""grab last object replication time"""'
newline|'\n'
name|'repinfo'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'with'
name|'open'
op|'('
name|'self'
op|'.'
name|'object_recon_cache'
op|','
string|"'r'"
op|')'
name|'as'
name|'f'
op|':'
newline|'\n'
indent|'            '
name|'recondata'
op|'='
name|'json'
op|'.'
name|'load'
op|'('
name|'f'
op|')'
newline|'\n'
name|'if'
string|"'object_replication_time'"
name|'in'
name|'recondata'
op|':'
newline|'\n'
indent|'                '
name|'repinfo'
op|'['
string|"'object_replication_time'"
op|']'
op|'='
name|'recondata'
op|'['
string|"'object_replication_time'"
op|']'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'notice'
op|'('
name|'_'
op|'('
string|"'NOTICE: obj replication time not in recon data'"
op|')'
op|')'
newline|'\n'
name|'repinfo'
op|'['
string|"'object_replication_time'"
op|']'
op|'='
op|'-'
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'repinfo'
newline|'\n'
nl|'\n'
DECL|member|get_device_info
dedent|''
name|'def'
name|'get_device_info'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""place holder, grab dev info"""'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'devices'
newline|'\n'
nl|'\n'
DECL|member|get_unmounted
dedent|''
name|'def'
name|'get_unmounted'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""list unmounted (failed?) devices"""'
newline|'\n'
name|'mountlist'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'entry'
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
name|'mpoint'
op|'='
op|'{'
string|"'device'"
op|':'
name|'entry'
op|','
string|'"mounted"'
op|':'
name|'check_mount'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
name|'entry'
op|')'
op|'}'
newline|'\n'
name|'if'
name|'not'
name|'mpoint'
op|'['
string|"'mounted'"
op|']'
op|':'
newline|'\n'
indent|'                '
name|'mountlist'
op|'.'
name|'append'
op|'('
name|'mpoint'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'mountlist'
newline|'\n'
nl|'\n'
DECL|member|get_diskusage
dedent|''
name|'def'
name|'get_diskusage'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get disk utilization statistics"""'
newline|'\n'
name|'devices'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'entry'
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
name|'check_mount'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
name|'entry'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'path'
op|'='
string|'"%s/%s"'
op|'%'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
name|'entry'
op|')'
newline|'\n'
name|'disk'
op|'='
name|'os'
op|'.'
name|'statvfs'
op|'('
name|'path'
op|')'
newline|'\n'
name|'capacity'
op|'='
name|'disk'
op|'.'
name|'f_bsize'
op|'*'
name|'disk'
op|'.'
name|'f_blocks'
newline|'\n'
name|'available'
op|'='
name|'disk'
op|'.'
name|'f_bsize'
op|'*'
name|'disk'
op|'.'
name|'f_bavail'
newline|'\n'
name|'used'
op|'='
name|'disk'
op|'.'
name|'f_bsize'
op|'*'
op|'('
name|'disk'
op|'.'
name|'f_blocks'
op|'-'
name|'disk'
op|'.'
name|'f_bavail'
op|')'
newline|'\n'
name|'devices'
op|'.'
name|'append'
op|'('
op|'{'
string|"'device'"
op|':'
name|'entry'
op|','
string|"'mounted'"
op|':'
name|'True'
op|','
string|"'size'"
op|':'
name|'capacity'
op|','
string|"'used'"
op|':'
name|'used'
op|','
string|"'avail'"
op|':'
name|'available'
op|'}'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'devices'
op|'.'
name|'append'
op|'('
op|'{'
string|"'device'"
op|':'
name|'entry'
op|','
string|"'mounted'"
op|':'
name|'False'
op|','
string|"'size'"
op|':'
string|"''"
op|','
string|"'used'"
op|':'
string|"''"
op|','
string|"'avail'"
op|':'
string|"''"
op|'}'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'devices'
newline|'\n'
nl|'\n'
DECL|member|get_ring_md5
dedent|''
name|'def'
name|'get_ring_md5'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get all ring md5sum\'s"""'
newline|'\n'
name|'sums'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'ringfile'
name|'in'
name|'self'
op|'.'
name|'rings'
op|':'
newline|'\n'
indent|'            '
name|'md5sum'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
name|'with'
name|'open'
op|'('
name|'ringfile'
op|','
string|"'rb'"
op|')'
name|'as'
name|'f'
op|':'
newline|'\n'
indent|'                '
name|'block'
op|'='
name|'f'
op|'.'
name|'read'
op|'('
number|'4096'
op|')'
newline|'\n'
name|'while'
name|'block'
op|':'
newline|'\n'
indent|'                    '
name|'md5sum'
op|'.'
name|'update'
op|'('
name|'block'
op|')'
newline|'\n'
name|'block'
op|'='
name|'f'
op|'.'
name|'read'
op|'('
number|'4096'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'sums'
op|'['
name|'ringfile'
op|']'
op|'='
name|'md5sum'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
dedent|''
name|'return'
name|'sums'
newline|'\n'
nl|'\n'
DECL|member|get_quarantine_count
dedent|''
name|'def'
name|'get_quarantine_count'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""get obj/container/account quarantine counts"""'
newline|'\n'
name|'qcounts'
op|'='
op|'{'
string|'"objects"'
op|':'
number|'0'
op|','
string|'"containers"'
op|':'
number|'0'
op|','
string|'"accounts"'
op|':'
number|'0'
op|'}'
newline|'\n'
name|'qdir'
op|'='
string|'"quarantined"'
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
name|'for'
name|'qtype'
name|'in'
name|'qcounts'
op|':'
newline|'\n'
indent|'                '
name|'qtgt'
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
name|'qdir'
op|','
name|'qtype'
op|')'
newline|'\n'
name|'if'
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'qtgt'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'linkcount'
op|'='
name|'os'
op|'.'
name|'lstat'
op|'('
name|'qtgt'
op|')'
op|'.'
name|'st_nlink'
newline|'\n'
name|'if'
name|'linkcount'
op|'>'
number|'2'
op|':'
newline|'\n'
indent|'                        '
name|'qcounts'
op|'['
name|'qtype'
op|']'
op|'+='
name|'linkcount'
op|'-'
number|'2'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
name|'return'
name|'qcounts'
newline|'\n'
nl|'\n'
DECL|member|get_socket_info
dedent|''
name|'def'
name|'get_socket_info'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        get info from /proc/net/sockstat and sockstat6\n\n        Note: The mem value is actually kernel pages, but we return bytes\n        allocated based on the systems page size.\n        """'
newline|'\n'
name|'sockstat'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'open'
op|'('
string|"'/proc/net/sockstat'"
op|')'
name|'as'
name|'proc_sockstat'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'entry'
name|'in'
name|'proc_sockstat'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'entry'
op|'.'
name|'startswith'
op|'('
string|'"TCP: inuse"'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'tcpstats'
op|'='
name|'entry'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'sockstat'
op|'['
string|"'tcp_in_use'"
op|']'
op|'='
name|'int'
op|'('
name|'tcpstats'
op|'['
number|'2'
op|']'
op|')'
newline|'\n'
name|'sockstat'
op|'['
string|"'orphan'"
op|']'
op|'='
name|'int'
op|'('
name|'tcpstats'
op|'['
number|'4'
op|']'
op|')'
newline|'\n'
name|'sockstat'
op|'['
string|"'time_wait'"
op|']'
op|'='
name|'int'
op|'('
name|'tcpstats'
op|'['
number|'6'
op|']'
op|')'
newline|'\n'
name|'sockstat'
op|'['
string|"'tcp_mem_allocated_bytes'"
op|']'
op|'='
name|'int'
op|'('
name|'tcpstats'
op|'['
number|'10'
op|']'
op|')'
op|'*'
name|'getpagesize'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
name|'except'
name|'IOError'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'e'
op|'.'
name|'errno'
op|'!='
name|'errno'
op|'.'
name|'ENOENT'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
newline|'\n'
dedent|''
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'open'
op|'('
string|"'/proc/net/sockstat6'"
op|')'
name|'as'
name|'proc_sockstat6'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'entry'
name|'in'
name|'proc_sockstat6'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'entry'
op|'.'
name|'startswith'
op|'('
string|'"TCP6: inuse"'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'sockstat'
op|'['
string|"'tcp6_in_use'"
op|']'
op|'='
name|'int'
op|'('
name|'entry'
op|'.'
name|'split'
op|'('
op|')'
op|'['
number|'2'
op|']'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
name|'except'
name|'IOError'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'e'
op|'.'
name|'errno'
op|'!='
name|'errno'
op|'.'
name|'ENOENT'
op|':'
newline|'\n'
indent|'                '
name|'raise'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'sockstat'
newline|'\n'
nl|'\n'
DECL|member|GET
dedent|''
name|'def'
name|'GET'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'error'
op|'='
name|'False'
newline|'\n'
name|'root'
op|','
name|'type'
op|'='
name|'split_path'
op|'('
name|'req'
op|'.'
name|'path'
op|','
number|'1'
op|','
number|'2'
op|','
name|'False'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'type'
op|'=='
string|'"mem"'
op|':'
newline|'\n'
indent|'                '
name|'content'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
name|'self'
op|'.'
name|'get_mem'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'type'
op|'=='
string|'"load"'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'content'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
name|'self'
op|'.'
name|'get_load'
op|'('
op|')'
op|','
name|'sort_keys'
op|'='
name|'True'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'IOError'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'                    '
name|'error'
op|'='
name|'True'
newline|'\n'
name|'content'
op|'='
string|'"load - %s"'
op|'%'
name|'e'
newline|'\n'
dedent|''
dedent|''
name|'elif'
name|'type'
op|'=='
string|'"async"'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'content'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
name|'self'
op|'.'
name|'get_async_info'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'IOError'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'                    '
name|'error'
op|'='
name|'True'
newline|'\n'
name|'content'
op|'='
string|'"async - %s"'
op|'%'
name|'e'
newline|'\n'
dedent|''
dedent|''
name|'elif'
name|'type'
op|'=='
string|'"replication"'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'content'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
name|'self'
op|'.'
name|'get_replication_info'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'IOError'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'                    '
name|'error'
op|'='
name|'True'
newline|'\n'
name|'content'
op|'='
string|'"replication - %s"'
op|'%'
name|'e'
newline|'\n'
dedent|''
dedent|''
name|'elif'
name|'type'
op|'=='
string|'"mounted"'
op|':'
newline|'\n'
indent|'                '
name|'content'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
name|'self'
op|'.'
name|'get_mounted'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'type'
op|'=='
string|'"unmounted"'
op|':'
newline|'\n'
indent|'                '
name|'content'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
name|'self'
op|'.'
name|'get_unmounted'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'type'
op|'=='
string|'"diskusage"'
op|':'
newline|'\n'
indent|'                '
name|'content'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
name|'self'
op|'.'
name|'get_diskusage'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'type'
op|'=='
string|'"ringmd5"'
op|':'
newline|'\n'
indent|'                '
name|'content'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
name|'self'
op|'.'
name|'get_ring_md5'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'type'
op|'=='
string|'"quarantined"'
op|':'
newline|'\n'
indent|'                '
name|'content'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
name|'self'
op|'.'
name|'get_quarantine_count'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'type'
op|'=='
string|'"sockstat"'
op|':'
newline|'\n'
indent|'                '
name|'content'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
name|'self'
op|'.'
name|'get_socket_info'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'content'
op|'='
string|'"Invalid path: %s"'
op|'%'
name|'req'
op|'.'
name|'path'
newline|'\n'
name|'return'
name|'Response'
op|'('
name|'request'
op|'='
name|'req'
op|','
name|'status'
op|'='
string|'"400 Bad Request"'
op|','
name|'body'
op|'='
name|'content'
op|','
name|'content_type'
op|'='
string|'"text/plain"'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'ValueError'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'            '
name|'error'
op|'='
name|'True'
newline|'\n'
name|'content'
op|'='
string|'"ValueError: %s"'
op|'%'
name|'e'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'not'
name|'error'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'Response'
op|'('
name|'request'
op|'='
name|'req'
op|','
name|'body'
op|'='
name|'content'
op|','
name|'content_type'
op|'='
string|'"application/json"'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'msg'
op|'='
string|"'CRITICAL recon - %s'"
op|'%'
name|'str'
op|'('
name|'content'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'critical'
op|'('
name|'msg'
op|')'
newline|'\n'
name|'body'
op|'='
string|'"Internal server error."'
newline|'\n'
name|'return'
name|'Response'
op|'('
name|'request'
op|'='
name|'req'
op|','
name|'status'
op|'='
string|'"500 Server Error"'
op|','
name|'body'
op|'='
name|'body'
op|','
name|'content_type'
op|'='
string|'"text/plain"'
op|')'
newline|'\n'
nl|'\n'
DECL|member|__call__
dedent|''
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
name|'req'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
newline|'\n'
name|'if'
name|'req'
op|'.'
name|'path'
op|'.'
name|'startswith'
op|'('
string|"'/recon/'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'GET'
op|'('
name|'req'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
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
DECL|function|recon_filter
name|'def'
name|'recon_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'ReconMiddleware'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'recon_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
