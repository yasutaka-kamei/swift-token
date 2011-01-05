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
name|'os'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'random'
name|'import'
name|'random'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'account'
name|'import'
name|'server'
name|'as'
name|'account_server'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'db'
name|'import'
name|'AccountBroker'
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
nl|'\n'
DECL|class|AccountAuditor
name|'class'
name|'AccountAuditor'
op|'('
name|'Daemon'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Audit accounts."""'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'conf'
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
string|"'account-auditor'"
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
number|'1800'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account_passes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'account_failures'
op|'='
number|'0'
newline|'\n'
nl|'\n'
DECL|member|run_forever
dedent|''
name|'def'
name|'run_forever'
op|'('
name|'self'
op|')'
op|':'
comment|'# pragma: no cover'
newline|'\n'
indent|'        '
string|'"""Run the account audit until stopped."""'
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
name|'all_locs'
op|'='
name|'audit_location_generator'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
nl|'\n'
name|'account_server'
op|'.'
name|'DATADIR'
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
indent|'                '
name|'self'
op|'.'
name|'account_audit'
op|'('
name|'path'
op|')'
newline|'\n'
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
indent|'                    '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|"'Since %(time)s: Account audits: '"
nl|'\n'
string|"'%(passed)s passed audit, %(failed)s failed audit'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'time'"
op|':'
name|'time'
op|'.'
name|'ctime'
op|'('
name|'reported'
op|')'
op|','
nl|'\n'
string|"'passed'"
op|':'
name|'self'
op|'.'
name|'account_passes'
op|','
nl|'\n'
string|"'failed'"
op|':'
name|'self'
op|'.'
name|'account_failures'
op|'}'
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
name|'account_passes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'account_failures'
op|'='
number|'0'
newline|'\n'
dedent|''
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
DECL|member|run_once
dedent|''
dedent|''
dedent|''
name|'def'
name|'run_once'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Run the account audit once."""'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
string|'\'Begin account audit "once" mode\''
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
name|'all_locs'
op|'='
name|'audit_location_generator'
op|'('
name|'self'
op|'.'
name|'devices'
op|','
nl|'\n'
name|'account_server'
op|'.'
name|'DATADIR'
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
name|'self'
op|'.'
name|'account_audit'
op|'('
name|'path'
op|')'
newline|'\n'
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
name|'_'
op|'('
string|"'Since %(time)s: Account audits: '"
nl|'\n'
string|"'%(passed)s passed audit, %(failed)s failed audit'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'time'"
op|':'
name|'time'
op|'.'
name|'ctime'
op|'('
name|'reported'
op|')'
op|','
nl|'\n'
string|"'passed'"
op|':'
name|'self'
op|'.'
name|'account_passes'
op|','
nl|'\n'
string|"'failed'"
op|':'
name|'self'
op|'.'
name|'account_failures'
op|'}'
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
name|'account_passes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'account_failures'
op|'='
number|'0'
newline|'\n'
dedent|''
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
string|'\'Account audit "once" mode completed: %.02fs\''
op|','
name|'elapsed'
op|')'
newline|'\n'
nl|'\n'
DECL|member|account_audit
dedent|''
name|'def'
name|'account_audit'
op|'('
name|'self'
op|','
name|'path'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Audits the given account path\n\n        :param path: the path to an account db\n        """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'not'
name|'path'
op|'.'
name|'endswith'
op|'('
string|"'.db'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
newline|'\n'
dedent|''
name|'broker'
op|'='
name|'AccountBroker'
op|'('
name|'path'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'broker'
op|'.'
name|'is_deleted'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'info'
op|'='
name|'broker'
op|'.'
name|'get_info'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account_passes'
op|'+='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|"'Audit passed for %s'"
op|')'
op|'%'
name|'broker'
op|'.'
name|'db_file'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'account_failures'
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
string|"'ERROR Could not get account info %s'"
op|')'
op|','
nl|'\n'
op|'('
name|'broker'
op|'.'
name|'db_file'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
endmarker|''
end_unit
