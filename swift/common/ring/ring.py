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
name|'cPickle'
name|'as'
name|'pickle'
newline|'\n'
name|'from'
name|'gzip'
name|'import'
name|'GzipFile'
newline|'\n'
name|'from'
name|'os'
op|'.'
name|'path'
name|'import'
name|'getmtime'
newline|'\n'
name|'from'
name|'struct'
name|'import'
name|'unpack_from'
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'hash_path'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|RingData
name|'class'
name|'RingData'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Partitioned consistent hashing ring data (used for serialization)."""'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'replica2part2dev_id'
op|','
name|'devs'
op|','
name|'part_shift'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'devs'
op|'='
name|'devs'
newline|'\n'
name|'self'
op|'.'
name|'_replica2part2dev_id'
op|'='
name|'replica2part2dev_id'
newline|'\n'
name|'self'
op|'.'
name|'_part_shift'
op|'='
name|'part_shift'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|Ring
dedent|''
dedent|''
name|'class'
name|'Ring'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Partitioned consistent hashing ring.\n\n    :param pickle_gz_path: path to ring file\n    :param reload_time: time interval in seconds to check for a ring change\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'pickle_gz_path'
op|','
name|'reload_time'
op|'='
number|'15'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'pickle_gz_path'
op|'='
name|'pickle_gz_path'
newline|'\n'
name|'self'
op|'.'
name|'reload_time'
op|'='
name|'reload_time'
newline|'\n'
name|'self'
op|'.'
name|'_reload'
op|'('
name|'force'
op|'='
name|'True'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_reload
dedent|''
name|'def'
name|'_reload'
op|'('
name|'self'
op|','
name|'force'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'_rtime'
op|'='
name|'time'
op|'('
op|')'
op|'+'
name|'self'
op|'.'
name|'reload_time'
newline|'\n'
name|'if'
name|'force'
name|'or'
name|'self'
op|'.'
name|'has_changed'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'ring_data'
op|'='
name|'pickle'
op|'.'
name|'load'
op|'('
name|'GzipFile'
op|'('
name|'self'
op|'.'
name|'pickle_gz_path'
op|','
string|"'rb'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_mtime'
op|'='
name|'getmtime'
op|'('
name|'self'
op|'.'
name|'pickle_gz_path'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'devs'
op|'='
name|'ring_data'
op|'.'
name|'devs'
newline|'\n'
name|'self'
op|'.'
name|'zone2devs'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'dev'
name|'in'
name|'self'
op|'.'
name|'devs'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'not'
name|'dev'
op|':'
newline|'\n'
indent|'                    '
name|'continue'
newline|'\n'
dedent|''
name|'if'
name|'dev'
op|'['
string|"'zone'"
op|']'
name|'in'
name|'self'
op|'.'
name|'zone2devs'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'zone2devs'
op|'['
name|'dev'
op|'['
string|"'zone'"
op|']'
op|']'
op|'.'
name|'append'
op|'('
name|'dev'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'zone2devs'
op|'['
name|'dev'
op|'['
string|"'zone'"
op|']'
op|']'
op|'='
op|'['
name|'dev'
op|']'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'_replica2part2dev_id'
op|'='
name|'ring_data'
op|'.'
name|'_replica2part2dev_id'
newline|'\n'
name|'self'
op|'.'
name|'_part_shift'
op|'='
name|'ring_data'
op|'.'
name|'_part_shift'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
op|'@'
name|'property'
newline|'\n'
DECL|member|replica_count
name|'def'
name|'replica_count'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Number of replicas used in the ring."""'
newline|'\n'
name|'return'
name|'len'
op|'('
name|'self'
op|'.'
name|'_replica2part2dev_id'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'property'
newline|'\n'
DECL|member|partition_count
name|'def'
name|'partition_count'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Number of partitions in the ring."""'
newline|'\n'
name|'return'
name|'len'
op|'('
name|'self'
op|'.'
name|'_replica2part2dev_id'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|has_changed
dedent|''
name|'def'
name|'has_changed'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Check to see if the ring on disk is different than the current one in\n        memory.\n\n        :returns: True if the ring on disk has changed, False otherwise\n        """'
newline|'\n'
name|'return'
name|'getmtime'
op|'('
name|'self'
op|'.'
name|'pickle_gz_path'
op|')'
op|'!='
name|'self'
op|'.'
name|'_mtime'
newline|'\n'
nl|'\n'
DECL|member|get_part_nodes
dedent|''
name|'def'
name|'get_part_nodes'
op|'('
name|'self'
op|','
name|'part'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Get the nodes that are responsible for the partition.\n\n        :param part: partition to get nodes for\n        :returns: list of node dicts\n\n        See :func:`get_nodes` for a description of the node dicts.\n        """'
newline|'\n'
name|'if'
name|'time'
op|'('
op|')'
op|'>'
name|'self'
op|'.'
name|'_rtime'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_reload'
op|'('
op|')'
newline|'\n'
dedent|''
name|'return'
op|'['
name|'self'
op|'.'
name|'devs'
op|'['
name|'r'
op|'['
name|'part'
op|']'
op|']'
name|'for'
name|'r'
name|'in'
name|'self'
op|'.'
name|'_replica2part2dev_id'
op|']'
newline|'\n'
nl|'\n'
DECL|member|get_nodes
dedent|''
name|'def'
name|'get_nodes'
op|'('
name|'self'
op|','
name|'account'
op|','
name|'container'
op|'='
name|'None'
op|','
name|'obj'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Get the partition and nodes for an account/container/object.\n\n        :param account: account name\n        :param container: container name\n        :param obj: object name\n        :returns: a tuple of (partition, list of node dicts)\n\n        Each node dict will have at least the following keys:\n\n        ======  ===============================================================\n        id      unique integer identifier amongst devices\n        weight  a float of the relative weight of this device as compared to\n                others; this indicates how many partitions the builder will try\n                to assign to this device\n        zone    integer indicating which zone the device is in; a given\n                partition will not be assigned to multiple devices within the\n                same zone ip the ip address of the device\n        port    the tcp port of the device\n        device  the device\'s name on disk (sdb1, for example)\n        meta    general use \'extra\' field; for example: the online date, the\n                hardware description\n        ======  ===============================================================\n        """'
newline|'\n'
name|'key'
op|'='
name|'hash_path'
op|'('
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|','
name|'raw_digest'
op|'='
name|'True'
op|')'
newline|'\n'
name|'if'
name|'time'
op|'('
op|')'
op|'>'
name|'self'
op|'.'
name|'_rtime'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_reload'
op|'('
op|')'
newline|'\n'
dedent|''
name|'part'
op|'='
name|'unpack_from'
op|'('
string|"'>I'"
op|','
name|'key'
op|')'
op|'['
number|'0'
op|']'
op|'>>'
name|'self'
op|'.'
name|'_part_shift'
newline|'\n'
name|'return'
name|'part'
op|','
op|'['
name|'self'
op|'.'
name|'devs'
op|'['
name|'r'
op|'['
name|'part'
op|']'
op|']'
name|'for'
name|'r'
name|'in'
name|'self'
op|'.'
name|'_replica2part2dev_id'
op|']'
newline|'\n'
nl|'\n'
DECL|member|get_more_nodes
dedent|''
name|'def'
name|'get_more_nodes'
op|'('
name|'self'
op|','
name|'part'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Generator to get extra nodes for a partition for hinted handoff.\n\n        :param part: partition to get handoff nodes for\n        :returns: generator of node dicts\n\n        See :func:`get_nodes` for a description of the node dicts.\n        """'
newline|'\n'
name|'if'
name|'time'
op|'('
op|')'
op|'>'
name|'self'
op|'.'
name|'_rtime'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_reload'
op|'('
op|')'
newline|'\n'
dedent|''
name|'zones'
op|'='
name|'sorted'
op|'('
name|'self'
op|'.'
name|'zone2devs'
op|'.'
name|'keys'
op|'('
op|')'
op|')'
newline|'\n'
name|'for'
name|'part2dev_id'
name|'in'
name|'self'
op|'.'
name|'_replica2part2dev_id'
op|':'
newline|'\n'
indent|'            '
name|'zones'
op|'.'
name|'remove'
op|'('
name|'self'
op|'.'
name|'devs'
op|'['
name|'part2dev_id'
op|'['
name|'part'
op|']'
op|']'
op|'['
string|"'zone'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'while'
name|'zones'
op|':'
newline|'\n'
indent|'            '
name|'zone'
op|'='
name|'zones'
op|'.'
name|'pop'
op|'('
name|'part'
op|'%'
name|'len'
op|'('
name|'zones'
op|')'
op|')'
newline|'\n'
name|'yield'
name|'self'
op|'.'
name|'zone2devs'
op|'['
name|'zone'
op|']'
op|'['
name|'part'
op|'%'
name|'len'
op|'('
name|'self'
op|'.'
name|'zone2devs'
op|'['
name|'zone'
op|']'
op|')'
op|']'
newline|'\n'
dedent|''
dedent|''
dedent|''
endmarker|''
end_unit
