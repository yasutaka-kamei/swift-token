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
name|'array'
newline|'\n'
name|'import'
name|'cPickle'
name|'as'
name|'pickle'
newline|'\n'
name|'from'
name|'collections'
name|'import'
name|'defaultdict'
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
name|'import'
name|'struct'
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'from'
name|'io'
name|'import'
name|'BufferedReader'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'hash_path'
op|','
name|'validate_configuration'
op|','
name|'json'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'ring'
op|'.'
name|'utils'
name|'import'
name|'tiers_for_dev'
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
dedent|''
op|'@'
name|'classmethod'
newline|'\n'
DECL|member|deserialize_v1
name|'def'
name|'deserialize_v1'
op|'('
name|'cls'
op|','
name|'gz_file'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'json_len'
op|','
op|'='
name|'struct'
op|'.'
name|'unpack'
op|'('
string|"'!I'"
op|','
name|'gz_file'
op|'.'
name|'read'
op|'('
number|'4'
op|')'
op|')'
newline|'\n'
name|'ring_dict'
op|'='
name|'json'
op|'.'
name|'loads'
op|'('
name|'gz_file'
op|'.'
name|'read'
op|'('
name|'json_len'
op|')'
op|')'
newline|'\n'
name|'ring_dict'
op|'['
string|"'replica2part2dev_id'"
op|']'
op|'='
op|'['
op|']'
newline|'\n'
name|'partition_count'
op|'='
number|'1'
op|'<<'
op|'('
number|'32'
op|'-'
name|'ring_dict'
op|'['
string|"'part_shift'"
op|']'
op|')'
newline|'\n'
name|'for'
name|'x'
name|'in'
name|'xrange'
op|'('
name|'ring_dict'
op|'['
string|"'replica_count'"
op|']'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'ring_dict'
op|'['
string|"'replica2part2dev_id'"
op|']'
op|'.'
name|'append'
op|'('
nl|'\n'
name|'array'
op|'.'
name|'array'
op|'('
string|"'H'"
op|','
name|'gz_file'
op|'.'
name|'read'
op|'('
number|'2'
op|'*'
name|'partition_count'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'ring_dict'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'classmethod'
newline|'\n'
DECL|member|load
name|'def'
name|'load'
op|'('
name|'cls'
op|','
name|'filename'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Load ring data from a file.\n\n        :param filename: Path to a file serialized by the save() method.\n        :returns: A RingData instance containing the loaded data.\n        """'
newline|'\n'
name|'gz_file'
op|'='
name|'GzipFile'
op|'('
name|'filename'
op|','
string|"'rb'"
op|')'
newline|'\n'
comment|"# Python 2.6 GzipFile doesn't support BufferedIO"
nl|'\n'
name|'if'
name|'hasattr'
op|'('
name|'gz_file'
op|','
string|"'_checkReadable'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'gz_file'
op|'='
name|'BufferedReader'
op|'('
name|'gz_file'
op|')'
newline|'\n'
nl|'\n'
comment|'# See if the file is in the new format'
nl|'\n'
dedent|''
name|'magic'
op|'='
name|'gz_file'
op|'.'
name|'read'
op|'('
number|'4'
op|')'
newline|'\n'
name|'if'
name|'magic'
op|'=='
string|"'R1NG'"
op|':'
newline|'\n'
indent|'            '
name|'version'
op|','
op|'='
name|'struct'
op|'.'
name|'unpack'
op|'('
string|"'!H'"
op|','
name|'gz_file'
op|'.'
name|'read'
op|'('
number|'2'
op|')'
op|')'
newline|'\n'
name|'if'
name|'version'
op|'=='
number|'1'
op|':'
newline|'\n'
indent|'                '
name|'ring_data'
op|'='
name|'cls'
op|'.'
name|'deserialize_v1'
op|'('
name|'gz_file'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'Exception'
op|'('
string|"'Unknown ring format version %d'"
op|'%'
name|'version'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
comment|'# Assume old-style pickled ring'
nl|'\n'
indent|'            '
name|'gz_file'
op|'.'
name|'seek'
op|'('
number|'0'
op|')'
newline|'\n'
name|'ring_data'
op|'='
name|'pickle'
op|'.'
name|'load'
op|'('
name|'gz_file'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'hasattr'
op|'('
name|'ring_data'
op|','
string|"'devs'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'ring_data'
op|'='
name|'RingData'
op|'('
name|'ring_data'
op|'['
string|"'replica2part2dev_id'"
op|']'
op|','
nl|'\n'
name|'ring_data'
op|'['
string|"'devs'"
op|']'
op|','
name|'ring_data'
op|'['
string|"'part_shift'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'ring_data'
newline|'\n'
nl|'\n'
DECL|member|serialize_v1
dedent|''
name|'def'
name|'serialize_v1'
op|'('
name|'self'
op|','
name|'file_obj'
op|')'
op|':'
newline|'\n'
comment|'# Write out new-style serialization magic and version:'
nl|'\n'
indent|'        '
name|'file_obj'
op|'.'
name|'write'
op|'('
name|'struct'
op|'.'
name|'pack'
op|'('
string|"'!4sH'"
op|','
string|"'R1NG'"
op|','
number|'1'
op|')'
op|')'
newline|'\n'
name|'ring'
op|'='
name|'self'
op|'.'
name|'to_dict'
op|'('
op|')'
newline|'\n'
name|'json_encoder'
op|'='
name|'json'
op|'.'
name|'JSONEncoder'
op|'('
name|'sort_keys'
op|'='
name|'True'
op|')'
newline|'\n'
name|'json_text'
op|'='
name|'json_encoder'
op|'.'
name|'encode'
op|'('
nl|'\n'
op|'{'
string|"'devs'"
op|':'
name|'ring'
op|'['
string|"'devs'"
op|']'
op|','
string|"'part_shift'"
op|':'
name|'ring'
op|'['
string|"'part_shift'"
op|']'
op|','
nl|'\n'
string|"'replica_count'"
op|':'
name|'len'
op|'('
name|'ring'
op|'['
string|"'replica2part2dev_id'"
op|']'
op|')'
op|'}'
op|')'
newline|'\n'
name|'json_len'
op|'='
name|'len'
op|'('
name|'json_text'
op|')'
newline|'\n'
name|'file_obj'
op|'.'
name|'write'
op|'('
name|'struct'
op|'.'
name|'pack'
op|'('
string|"'!I'"
op|','
name|'json_len'
op|')'
op|')'
newline|'\n'
name|'file_obj'
op|'.'
name|'write'
op|'('
name|'json_text'
op|')'
newline|'\n'
name|'for'
name|'part2dev_id'
name|'in'
name|'ring'
op|'['
string|"'replica2part2dev_id'"
op|']'
op|':'
newline|'\n'
indent|'            '
name|'file_obj'
op|'.'
name|'write'
op|'('
name|'part2dev_id'
op|'.'
name|'tostring'
op|'('
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|save
dedent|''
dedent|''
name|'def'
name|'save'
op|'('
name|'self'
op|','
name|'filename'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Serialize this RingData instance to disk.\n\n        :param filename: File into which this instance should be serialized.\n        """'
newline|'\n'
comment|'# Override the timestamp so that the same ring data creates'
nl|'\n'
comment|'# the same bytes on disk. This makes a checksum comparison a'
nl|'\n'
comment|'# good way to see if two rings are identical.'
nl|'\n'
comment|'#'
nl|'\n'
comment|'# This only works on Python 2.7; on 2.6, we always get the'
nl|'\n'
comment|'# current time in the gzip output.'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'gz_file'
op|'='
name|'GzipFile'
op|'('
name|'filename'
op|','
string|"'wb'"
op|','
name|'mtime'
op|'='
number|'1300507380.0'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'TypeError'
op|':'
newline|'\n'
indent|'            '
name|'gz_file'
op|'='
name|'GzipFile'
op|'('
name|'filename'
op|','
string|"'wb'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'serialize_v1'
op|'('
name|'gz_file'
op|')'
newline|'\n'
name|'gz_file'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|to_dict
dedent|''
name|'def'
name|'to_dict'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
op|'{'
string|"'devs'"
op|':'
name|'self'
op|'.'
name|'devs'
op|','
nl|'\n'
string|"'replica2part2dev_id'"
op|':'
name|'self'
op|'.'
name|'_replica2part2dev_id'
op|','
nl|'\n'
string|"'part_shift'"
op|':'
name|'self'
op|'.'
name|'_part_shift'
op|'}'
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
string|'"""\n    Partitioned consistent hashing ring.\n\n    :param serialized_path: path to serialized RingData instance\n    :param reload_time: time interval in seconds to check for a ring change\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'serialized_path'
op|','
name|'reload_time'
op|'='
number|'15'
op|','
name|'ring_name'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
comment|"# can't use the ring unless HASH_PATH_SUFFIX is set"
nl|'\n'
indent|'        '
name|'validate_configuration'
op|'('
op|')'
newline|'\n'
name|'if'
name|'ring_name'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'serialized_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'serialized_path'
op|','
nl|'\n'
name|'ring_name'
op|'+'
string|"'.ring.gz'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'serialized_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'serialized_path'
op|')'
newline|'\n'
dedent|''
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
name|'RingData'
op|'.'
name|'load'
op|'('
name|'self'
op|'.'
name|'serialized_path'
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
name|'serialized_path'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_devs'
op|'='
name|'ring_data'
op|'.'
name|'devs'
newline|'\n'
nl|'\n'
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
name|'self'
op|'.'
name|'_rebuild_tier_data'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|_rebuild_tier_data
dedent|''
dedent|''
name|'def'
name|'_rebuild_tier_data'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'tier2devs'
op|'='
name|'defaultdict'
op|'('
name|'list'
op|')'
newline|'\n'
name|'for'
name|'dev'
name|'in'
name|'self'
op|'.'
name|'_devs'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'not'
name|'dev'
op|':'
newline|'\n'
indent|'                '
name|'continue'
newline|'\n'
dedent|''
name|'for'
name|'tier'
name|'in'
name|'tiers_for_dev'
op|'('
name|'dev'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'tier2devs'
op|'['
name|'tier'
op|']'
op|'.'
name|'append'
op|'('
name|'dev'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'tiers_by_length'
op|'='
name|'defaultdict'
op|'('
name|'list'
op|')'
newline|'\n'
name|'for'
name|'tier'
name|'in'
name|'self'
op|'.'
name|'tier2devs'
op|'.'
name|'keys'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'tiers_by_length'
op|'['
name|'len'
op|'('
name|'tier'
op|')'
op|']'
op|'.'
name|'append'
op|'('
name|'tier'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'tiers_by_length'
op|'='
name|'sorted'
op|'('
name|'tiers_by_length'
op|'.'
name|'values'
op|'('
op|')'
op|','
nl|'\n'
name|'key'
op|'='
name|'lambda'
name|'x'
op|':'
name|'len'
op|'('
name|'x'
op|'['
number|'0'
op|']'
op|')'
op|')'
newline|'\n'
name|'for'
name|'tiers'
name|'in'
name|'self'
op|'.'
name|'tiers_by_length'
op|':'
newline|'\n'
indent|'            '
name|'tiers'
op|'.'
name|'sort'
op|'('
op|')'
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
string|'"""Number of replicas (full or partial) used in the ring."""'
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
dedent|''
op|'@'
name|'property'
newline|'\n'
DECL|member|devs
name|'def'
name|'devs'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""devices in the ring"""'
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
name|'self'
op|'.'
name|'_devs'
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
name|'serialized_path'
op|')'
op|'!='
name|'self'
op|'.'
name|'_mtime'
newline|'\n'
nl|'\n'
DECL|member|_get_part_nodes
dedent|''
name|'def'
name|'_get_part_nodes'
op|'('
name|'self'
op|','
name|'part'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'seen_ids'
op|'='
name|'set'
op|'('
op|')'
newline|'\n'
name|'return'
op|'['
name|'self'
op|'.'
name|'_devs'
op|'['
name|'r'
op|'['
name|'part'
op|']'
op|']'
name|'for'
name|'r'
name|'in'
nl|'\n'
op|'('
name|'rpd'
name|'for'
name|'rpd'
name|'in'
name|'self'
op|'.'
name|'_replica2part2dev_id'
name|'if'
name|'len'
op|'('
name|'rpd'
op|')'
op|'>'
name|'part'
op|')'
nl|'\n'
name|'if'
name|'not'
op|'('
name|'r'
op|'['
name|'part'
op|']'
name|'in'
name|'seen_ids'
name|'or'
name|'seen_ids'
op|'.'
name|'add'
op|'('
name|'r'
op|'['
name|'part'
op|']'
op|')'
op|')'
op|']'
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
string|'"""\n        Get the nodes that are responsible for the partition. If one\n        node is responsible for more than one replica of the same\n        partition, it will only appear in the output once.\n\n        :param part: partition to get nodes for\n        :returns: list of node dicts\n\n        See :func:`get_nodes` for a description of the node dicts.\n        """'
newline|'\n'
nl|'\n'
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
name|'self'
op|'.'
name|'_get_part_nodes'
op|'('
name|'part'
op|')'
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
string|'"""\n        Get the partition and nodes for an account/container/object.\n        If a node is responsible for more than one replica, it will\n        only appear in the output once.\n\n        :param account: account name\n        :param container: container name\n        :param obj: object name\n        :returns: a tuple of (partition, list of node dicts)\n\n        Each node dict will have at least the following keys:\n\n        ======  ===============================================================\n        id      unique integer identifier amongst devices\n        weight  a float of the relative weight of this device as compared to\n                others; this indicates how many partitions the builder will try\n                to assign to this device\n        zone    integer indicating which zone the device is in; a given\n                partition will not be assigned to multiple devices within the\n                same zone\n        ip      the ip address of the device\n        port    the tcp port of the device\n        device  the device\'s name on disk (sdb1, for example)\n        meta    general use \'extra\' field; for example: the online date, the\n                hardware description\n        ======  ===============================================================\n        """'
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
name|'struct'
op|'.'
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
name|'self'
op|'.'
name|'_get_part_nodes'
op|'('
name|'part'
op|')'
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
name|'used_tiers'
op|'='
name|'set'
op|'('
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
name|'if'
name|'len'
op|'('
name|'part2dev_id'
op|')'
op|'>'
name|'part'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'tier'
name|'in'
name|'tiers_for_dev'
op|'('
name|'self'
op|'.'
name|'_devs'
op|'['
name|'part2dev_id'
op|'['
name|'part'
op|']'
op|']'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'used_tiers'
op|'.'
name|'add'
op|'('
name|'tier'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
dedent|''
name|'for'
name|'level'
name|'in'
name|'self'
op|'.'
name|'tiers_by_length'
op|':'
newline|'\n'
indent|'            '
name|'tiers'
op|'='
name|'list'
op|'('
name|'level'
op|')'
newline|'\n'
name|'while'
name|'tiers'
op|':'
newline|'\n'
indent|'                '
name|'tier'
op|'='
name|'tiers'
op|'.'
name|'pop'
op|'('
name|'part'
op|'%'
name|'len'
op|'('
name|'tiers'
op|')'
op|')'
newline|'\n'
name|'if'
name|'tier'
name|'in'
name|'used_tiers'
op|':'
newline|'\n'
indent|'                    '
name|'continue'
newline|'\n'
dedent|''
name|'for'
name|'i'
name|'in'
name|'xrange'
op|'('
name|'len'
op|'('
name|'self'
op|'.'
name|'tier2devs'
op|'['
name|'tier'
op|']'
op|')'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'dev'
op|'='
name|'self'
op|'.'
name|'tier2devs'
op|'['
name|'tier'
op|']'
op|'['
op|'('
name|'part'
op|'+'
name|'i'
op|')'
op|'%'
nl|'\n'
name|'len'
op|'('
name|'self'
op|'.'
name|'tier2devs'
op|'['
name|'tier'
op|']'
op|')'
op|']'
newline|'\n'
name|'if'
name|'not'
name|'dev'
op|'.'
name|'get'
op|'('
string|"'weight'"
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'continue'
newline|'\n'
dedent|''
name|'yield'
name|'dev'
newline|'\n'
name|'used_tiers'
op|'.'
name|'update'
op|'('
name|'tiers_for_dev'
op|'('
name|'dev'
op|')'
op|')'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
dedent|''
endmarker|''
end_unit
