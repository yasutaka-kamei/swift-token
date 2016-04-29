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
name|'swift'
op|'.'
name|'account'
op|'.'
name|'backend'
name|'import'
name|'AccountBroker'
op|','
name|'DATADIR'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'db_replicator'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|AccountReplicator
name|'class'
name|'AccountReplicator'
op|'('
name|'db_replicator'
op|'.'
name|'Replicator'
op|')'
op|':'
newline|'\n'
DECL|variable|server_type
indent|'    '
name|'server_type'
op|'='
string|"'account'"
newline|'\n'
DECL|variable|brokerclass
name|'brokerclass'
op|'='
name|'AccountBroker'
newline|'\n'
DECL|variable|datadir
name|'datadir'
op|'='
name|'DATADIR'
newline|'\n'
DECL|variable|default_port
name|'default_port'
op|'='
number|'6202'
newline|'\n'
dedent|''
endmarker|''
end_unit
