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
name|'import'
name|'cPickle'
name|'as'
name|'pickle'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'signal'
newline|'\n'
name|'import'
name|'sys'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'swift'
name|'import'
name|'gettext_'
name|'as'
name|'_'
newline|'\n'
name|'from'
name|'random'
name|'import'
name|'random'
newline|'\n'
nl|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'patcher'
op|','
name|'Timeout'
newline|'\n'
nl|'\n'
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
op|','
name|'write_pickle'
op|','
name|'dump_recon_cache'
op|','
name|'config_true_value'
op|','
name|'ismount'
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
name|'from'
name|'swift'
op|'.'
name|'obj'
op|'.'
name|'diskfile'
name|'import'
name|'get_tmp_dir'
op|','
name|'get_async_dir'
op|','
name|'ASYNCDIR_BASE'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'http'
name|'import'
name|'is_success'
op|','
name|'HTTP_NOT_FOUND'
op|','
name|'HTTP_INTERNAL_SERVER_ERROR'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ObjectUpdater
name|'class'
name|'ObjectUpdater'
op|'('
name|'Daemon'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Update object information in container listings."""'
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
op|'='
name|'None'
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
name|'or'
name|'get_logger'
op|'('
name|'conf'
op|','
name|'log_route'
op|'='
string|"'object-updater'"
op|')'
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
name|'interval'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'interval'"
op|','
number|'300'
op|')'
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
name|'concurrency'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'concurrency'"
op|','
number|'1'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'slowdown'
op|'='
name|'float'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'slowdown'"
op|','
number|'0.01'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'node_timeout'
op|'='
name|'int'
op|'('
name|'conf'
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
name|'conf'
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
name|'successes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'failures'
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
string|"'object.recon'"
op|')'
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
string|'"""Get the container ring.  Load it, if it hasn\'t been yet."""'
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
name|'container_ring'
op|'='
name|'Ring'
op|'('
name|'self'
op|'.'
name|'swift_dir'
op|','
name|'ring_name'
op|'='
string|"'container'"
op|')'
newline|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'container_ring'
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
string|'"""Run the updater continuously."""'
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
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|"'Begin object update sweep'"
op|')'
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
name|'pids'
op|'='
op|'['
op|']'
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
name|'increment'
op|'('
string|"'errors'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'warn'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Skipping %s as it is not mounted'"
op|')'
op|','
name|'device'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'while'
name|'len'
op|'('
name|'pids'
op|')'
op|'>='
name|'self'
op|'.'
name|'concurrency'
op|':'
newline|'\n'
indent|'                    '
name|'pids'
op|'.'
name|'remove'
op|'('
name|'os'
op|'.'
name|'wait'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
dedent|''
name|'pid'
op|'='
name|'os'
op|'.'
name|'fork'
op|'('
op|')'
newline|'\n'
name|'if'
name|'pid'
op|':'
newline|'\n'
indent|'                    '
name|'pids'
op|'.'
name|'append'
op|'('
name|'pid'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'signal'
op|'.'
name|'signal'
op|'('
name|'signal'
op|'.'
name|'SIGTERM'
op|','
name|'signal'
op|'.'
name|'SIG_DFL'
op|')'
newline|'\n'
name|'patcher'
op|'.'
name|'monkey_patch'
op|'('
name|'all'
op|'='
name|'False'
op|','
name|'socket'
op|'='
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'successes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'failures'
op|'='
number|'0'
newline|'\n'
name|'forkbegin'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'object_sweep'
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
newline|'\n'
name|'elapsed'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'forkbegin'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Object update sweep of %(device)s'"
nl|'\n'
string|"' completed: %(elapsed).02fs, %(success)s successes'"
nl|'\n'
string|"', %(fail)s failures'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'device'"
op|':'
name|'device'
op|','
string|"'elapsed'"
op|':'
name|'elapsed'
op|','
nl|'\n'
string|"'success'"
op|':'
name|'self'
op|'.'
name|'successes'
op|','
string|"'fail'"
op|':'
name|'self'
op|'.'
name|'failures'
op|'}'
op|')'
newline|'\n'
name|'sys'
op|'.'
name|'exit'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
name|'while'
name|'pids'
op|':'
newline|'\n'
indent|'                '
name|'pids'
op|'.'
name|'remove'
op|'('
name|'os'
op|'.'
name|'wait'
op|'('
op|')'
op|'['
number|'0'
op|']'
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
name|'_'
op|'('
string|"'Object update sweep completed: %.02fs'"
op|')'
op|','
nl|'\n'
name|'elapsed'
op|')'
newline|'\n'
name|'dump_recon_cache'
op|'('
op|'{'
string|"'object_updater_sweep'"
op|':'
name|'elapsed'
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
DECL|member|run_once
dedent|''
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
string|'"""Run the updater once."""'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|"'Begin object update single threaded sweep'"
op|')'
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
name|'self'
op|'.'
name|'successes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'failures'
op|'='
number|'0'
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
name|'increment'
op|'('
string|"'errors'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'warn'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Skipping %s as it is not mounted'"
op|')'
op|','
name|'device'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'object_sweep'
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
name|'_'
op|'('
string|"'Object update single threaded sweep completed: '"
nl|'\n'
string|"'%(elapsed).02fs, %(success)s successes, %(fail)s failures'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'elapsed'"
op|':'
name|'elapsed'
op|','
string|"'success'"
op|':'
name|'self'
op|'.'
name|'successes'
op|','
nl|'\n'
string|"'fail'"
op|':'
name|'self'
op|'.'
name|'failures'
op|'}'
op|')'
newline|'\n'
name|'dump_recon_cache'
op|'('
op|'{'
string|"'object_updater_sweep'"
op|':'
name|'elapsed'
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
nl|'\n'
DECL|member|object_sweep
dedent|''
name|'def'
name|'object_sweep'
op|'('
name|'self'
op|','
name|'device'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        If there are async pendings on the device, walk each one and update.\n\n        :param device: path to device\n        """'
newline|'\n'
name|'start_time'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
comment|'# loop through async pending dirs for all policies'
nl|'\n'
name|'for'
name|'asyncdir'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'device'
op|')'
op|':'
newline|'\n'
comment|'# skip stuff like "accounts", "containers", etc.'
nl|'\n'
indent|'            '
name|'if'
name|'not'
op|'('
name|'asyncdir'
op|'=='
name|'ASYNCDIR_BASE'
name|'or'
nl|'\n'
name|'asyncdir'
op|'.'
name|'startswith'
op|'('
name|'ASYNCDIR_BASE'
op|'+'
string|"'-'"
op|')'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'continue'
newline|'\n'
nl|'\n'
comment|'# we only care about directories'
nl|'\n'
dedent|''
name|'async_pending'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'device'
op|','
name|'asyncdir'
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
name|'async_pending'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'continue'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'asyncdir'
op|'=='
name|'ASYNCDIR_BASE'
op|':'
newline|'\n'
indent|'                '
name|'policy_idx'
op|'='
number|'0'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'_junk'
op|','
name|'policy_idx'
op|'='
name|'asyncdir'
op|'.'
name|'split'
op|'('
string|"'-'"
op|','
number|'1'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'policy_idx'
op|'='
name|'int'
op|'('
name|'policy_idx'
op|')'
newline|'\n'
name|'get_async_dir'
op|'('
name|'policy_idx'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'warn'
op|'('
name|'_'
op|'('
string|"'Directory %s does not map to a '"
nl|'\n'
string|"'valid policy'"
op|')'
op|'%'
name|'asyncdir'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'for'
name|'prefix'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'async_pending'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'prefix_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'async_pending'
op|','
name|'prefix'
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
name|'prefix_path'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'continue'
newline|'\n'
dedent|''
name|'last_obj_hash'
op|'='
name|'None'
newline|'\n'
name|'for'
name|'update'
name|'in'
name|'sorted'
op|'('
name|'os'
op|'.'
name|'listdir'
op|'('
name|'prefix_path'
op|')'
op|','
name|'reverse'
op|'='
name|'True'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'update_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'prefix_path'
op|','
name|'update'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'isfile'
op|'('
name|'update_path'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'continue'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'                        '
name|'obj_hash'
op|','
name|'timestamp'
op|'='
name|'update'
op|'.'
name|'split'
op|'('
string|"'-'"
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'                        '
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
name|'logger'
op|'.'
name|'error'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'ERROR async pending file with unexpected '"
nl|'\n'
string|"'name %s'"
op|')'
nl|'\n'
op|'%'
op|'('
name|'update_path'
op|')'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'if'
name|'obj_hash'
op|'=='
name|'last_obj_hash'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|'"unlinks"'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'unlink'
op|'('
name|'update_path'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'process_object_update'
op|'('
name|'update_path'
op|','
name|'device'
op|','
nl|'\n'
name|'policy_idx'
op|')'
newline|'\n'
name|'last_obj_hash'
op|'='
name|'obj_hash'
newline|'\n'
dedent|''
name|'time'
op|'.'
name|'sleep'
op|'('
name|'self'
op|'.'
name|'slowdown'
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'os'
op|'.'
name|'rmdir'
op|'('
name|'prefix_path'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'OSError'
op|':'
newline|'\n'
indent|'                    '
name|'pass'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'logger'
op|'.'
name|'timing_since'
op|'('
string|"'timing'"
op|','
name|'start_time'
op|')'
newline|'\n'
nl|'\n'
DECL|member|process_object_update
dedent|''
dedent|''
name|'def'
name|'process_object_update'
op|'('
name|'self'
op|','
name|'update_path'
op|','
name|'device'
op|','
name|'policy_idx'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Process the object information to be updated and update.\n\n        :param update_path: path to pickled object update file\n        :param device: path to device\n        :param policy_idx: storage policy index of object update\n        """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'update'
op|'='
name|'pickle'
op|'.'
name|'load'
op|'('
name|'open'
op|'('
name|'update_path'
op|','
string|"'rb'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'ERROR Pickle problem, quarantining %s'"
op|')'
op|','
name|'update_path'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|"'quarantines'"
op|')'
newline|'\n'
name|'renamer'
op|'('
name|'update_path'
op|','
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
nl|'\n'
name|'device'
op|','
string|"'quarantined'"
op|','
string|"'objects'"
op|','
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'basename'
op|'('
name|'update_path'
op|')'
op|')'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'successes'
op|'='
name|'update'
op|'.'
name|'get'
op|'('
string|"'successes'"
op|','
op|'['
op|']'
op|')'
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
nl|'\n'
name|'update'
op|'['
string|"'account'"
op|']'
op|','
name|'update'
op|'['
string|"'container'"
op|']'
op|')'
newline|'\n'
name|'obj'
op|'='
string|"'/%s/%s/%s'"
op|'%'
op|'('
name|'update'
op|'['
string|"'account'"
op|']'
op|','
name|'update'
op|'['
string|"'container'"
op|']'
op|','
name|'update'
op|'['
string|"'obj'"
op|']'
op|')'
newline|'\n'
name|'success'
op|'='
name|'True'
newline|'\n'
name|'new_successes'
op|'='
name|'False'
newline|'\n'
name|'for'
name|'node'
name|'in'
name|'nodes'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'node'
op|'['
string|"'id'"
op|']'
name|'not'
name|'in'
name|'successes'
op|':'
newline|'\n'
indent|'                '
name|'headers'
op|'='
name|'update'
op|'['
string|"'headers'"
op|']'
op|'.'
name|'copy'
op|'('
op|')'
newline|'\n'
name|'headers'
op|'.'
name|'setdefault'
op|'('
string|"'X-Backend-Storage-Policy-Index'"
op|','
nl|'\n'
name|'str'
op|'('
name|'policy_idx'
op|')'
op|')'
newline|'\n'
name|'status'
op|'='
name|'self'
op|'.'
name|'object_update'
op|'('
name|'node'
op|','
name|'part'
op|','
name|'update'
op|'['
string|"'op'"
op|']'
op|','
name|'obj'
op|','
nl|'\n'
name|'headers'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'is_success'
op|'('
name|'status'
op|')'
name|'and'
name|'status'
op|'!='
name|'HTTP_NOT_FOUND'
op|':'
newline|'\n'
indent|'                    '
name|'success'
op|'='
name|'False'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'successes'
op|'.'
name|'append'
op|'('
name|'node'
op|'['
string|"'id'"
op|']'
op|')'
newline|'\n'
name|'new_successes'
op|'='
name|'True'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'if'
name|'success'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'successes'
op|'+='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|"'successes'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
string|"'Update sent for %(obj)s %(path)s'"
op|','
nl|'\n'
op|'{'
string|"'obj'"
op|':'
name|'obj'
op|','
string|"'path'"
op|':'
name|'update_path'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|'"unlinks"'
op|')'
newline|'\n'
name|'os'
op|'.'
name|'unlink'
op|'('
name|'update_path'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'failures'
op|'+='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|"'failures'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
string|"'Update failed for %(obj)s %(path)s'"
op|','
nl|'\n'
op|'{'
string|"'obj'"
op|':'
name|'obj'
op|','
string|"'path'"
op|':'
name|'update_path'
op|'}'
op|')'
newline|'\n'
name|'if'
name|'new_successes'
op|':'
newline|'\n'
indent|'                '
name|'update'
op|'['
string|"'successes'"
op|']'
op|'='
name|'successes'
newline|'\n'
name|'write_pickle'
op|'('
name|'update'
op|','
name|'update_path'
op|','
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
nl|'\n'
name|'device'
op|','
name|'get_tmp_dir'
op|'('
name|'policy_idx'
op|')'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|object_update
dedent|''
dedent|''
dedent|''
name|'def'
name|'object_update'
op|'('
name|'self'
op|','
name|'node'
op|','
name|'part'
op|','
name|'op'
op|','
name|'obj'
op|','
name|'headers'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Perform the object update to the container\n\n        :param node: node dictionary from the container ring\n        :param part: partition that holds the container\n        :param op: operation performed (ex: \'POST\' or \'DELETE\')\n        :param obj: object name being updated\n        :param headers: headers to send with the update\n        """'
newline|'\n'
name|'headers_out'
op|'='
name|'headers'
op|'.'
name|'copy'
op|'('
op|')'
newline|'\n'
name|'headers_out'
op|'['
string|"'user-agent'"
op|']'
op|'='
string|"'object-updater %s'"
op|'%'
name|'os'
op|'.'
name|'getpid'
op|'('
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'ConnectionTimeout'
op|'('
name|'self'
op|'.'
name|'conn_timeout'
op|')'
op|':'
newline|'\n'
indent|'                '
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
name|'node'
op|'['
string|"'device'"
op|']'
op|','
nl|'\n'
name|'part'
op|','
name|'op'
op|','
name|'obj'
op|','
name|'headers_out'
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
indent|'                '
name|'resp'
op|'='
name|'conn'
op|'.'
name|'getresponse'
op|'('
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'return'
name|'resp'
op|'.'
name|'status'
newline|'\n'
dedent|''
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
name|'exception'
op|'('
name|'_'
op|'('
string|"'ERROR with remote server '"
nl|'\n'
string|"'%(ip)s:%(port)s/%(device)s'"
op|')'
op|','
name|'node'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'HTTP_INTERNAL_SERVER_ERROR'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
