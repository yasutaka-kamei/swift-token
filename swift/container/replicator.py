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
name|'os'
newline|'\n'
name|'import'
name|'itertools'
newline|'\n'
name|'import'
name|'json'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'collections'
name|'import'
name|'defaultdict'
newline|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'Timeout'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'container'
op|'.'
name|'sync_store'
name|'import'
name|'ContainerSyncStore'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'container'
op|'.'
name|'backend'
name|'import'
name|'ContainerBroker'
op|','
name|'DATADIR'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'container'
op|'.'
name|'reconciler'
name|'import'
op|'('
nl|'\n'
name|'MISPLACED_OBJECTS_ACCOUNT'
op|','
name|'incorrect_policy_index'
op|','
nl|'\n'
name|'get_reconciler_container_name'
op|','
name|'get_row_to_q_entry_translator'
op|')'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'db_replicator'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'storage_policy'
name|'import'
name|'POLICIES'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'exceptions'
name|'import'
name|'DeviceUnavailable'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'http'
name|'import'
name|'is_success'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'db'
name|'import'
name|'DatabaseAlreadyExists'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
op|'('
name|'Timestamp'
op|','
name|'hash_path'
op|','
nl|'\n'
name|'storage_directory'
op|','
name|'quorum_size'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ContainerReplicator
name|'class'
name|'ContainerReplicator'
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
string|"'container'"
newline|'\n'
DECL|variable|brokerclass
name|'brokerclass'
op|'='
name|'ContainerBroker'
newline|'\n'
DECL|variable|datadir
name|'datadir'
op|'='
name|'DATADIR'
newline|'\n'
DECL|variable|default_port
name|'default_port'
op|'='
number|'6201'
newline|'\n'
nl|'\n'
DECL|member|report_up_to_date
name|'def'
name|'report_up_to_date'
op|'('
name|'self'
op|','
name|'full_info'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'reported_key_map'
op|'='
op|'{'
nl|'\n'
string|"'reported_put_timestamp'"
op|':'
string|"'put_timestamp'"
op|','
nl|'\n'
string|"'reported_delete_timestamp'"
op|':'
string|"'delete_timestamp'"
op|','
nl|'\n'
string|"'reported_bytes_used'"
op|':'
string|"'bytes_used'"
op|','
nl|'\n'
string|"'reported_object_count'"
op|':'
string|"'count'"
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'for'
name|'reported'
op|','
name|'value_key'
name|'in'
name|'reported_key_map'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'full_info'
op|'['
name|'reported'
op|']'
op|'!='
name|'full_info'
op|'['
name|'value_key'
op|']'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'False'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'True'
newline|'\n'
nl|'\n'
DECL|member|_gather_sync_args
dedent|''
name|'def'
name|'_gather_sync_args'
op|'('
name|'self'
op|','
name|'replication_info'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'parent'
op|'='
name|'super'
op|'('
name|'ContainerReplicator'
op|','
name|'self'
op|')'
newline|'\n'
name|'sync_args'
op|'='
name|'parent'
op|'.'
name|'_gather_sync_args'
op|'('
name|'replication_info'
op|')'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'POLICIES'
op|')'
op|'>'
number|'1'
op|':'
newline|'\n'
indent|'            '
name|'sync_args'
op|'+='
name|'tuple'
op|'('
name|'replication_info'
op|'['
name|'k'
op|']'
name|'for'
name|'k'
name|'in'
nl|'\n'
op|'('
string|"'status_changed_at'"
op|','
string|"'count'"
op|','
nl|'\n'
string|"'storage_policy_index'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'sync_args'
newline|'\n'
nl|'\n'
DECL|member|_handle_sync_response
dedent|''
name|'def'
name|'_handle_sync_response'
op|'('
name|'self'
op|','
name|'node'
op|','
name|'response'
op|','
name|'info'
op|','
name|'broker'
op|','
name|'http'
op|','
nl|'\n'
name|'different_region'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'parent'
op|'='
name|'super'
op|'('
name|'ContainerReplicator'
op|','
name|'self'
op|')'
newline|'\n'
name|'if'
name|'is_success'
op|'('
name|'response'
op|'.'
name|'status'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'remote_info'
op|'='
name|'json'
op|'.'
name|'loads'
op|'('
name|'response'
op|'.'
name|'data'
op|')'
newline|'\n'
name|'if'
name|'incorrect_policy_index'
op|'('
name|'info'
op|','
name|'remote_info'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'status_changed_at'
op|'='
name|'Timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
newline|'\n'
name|'broker'
op|'.'
name|'set_storage_policy_index'
op|'('
nl|'\n'
name|'remote_info'
op|'['
string|"'storage_policy_index'"
op|']'
op|','
nl|'\n'
name|'timestamp'
op|'='
name|'status_changed_at'
op|'.'
name|'internal'
op|')'
newline|'\n'
dedent|''
name|'sync_timestamps'
op|'='
op|'('
string|"'created_at'"
op|','
string|"'put_timestamp'"
op|','
nl|'\n'
string|"'delete_timestamp'"
op|')'
newline|'\n'
name|'if'
name|'any'
op|'('
name|'info'
op|'['
name|'key'
op|']'
op|'!='
name|'remote_info'
op|'['
name|'key'
op|']'
name|'for'
name|'key'
name|'in'
name|'sync_timestamps'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'broker'
op|'.'
name|'merge_timestamps'
op|'('
op|'*'
op|'('
name|'remote_info'
op|'['
name|'key'
op|']'
name|'for'
name|'key'
name|'in'
nl|'\n'
name|'sync_timestamps'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'rv'
op|'='
name|'parent'
op|'.'
name|'_handle_sync_response'
op|'('
nl|'\n'
name|'node'
op|','
name|'response'
op|','
name|'info'
op|','
name|'broker'
op|','
name|'http'
op|','
name|'different_region'
op|')'
newline|'\n'
name|'return'
name|'rv'
newline|'\n'
nl|'\n'
DECL|member|find_local_handoff_for_part
dedent|''
name|'def'
name|'find_local_handoff_for_part'
op|'('
name|'self'
op|','
name|'part'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Look through devices in the ring for the first handoff device that was\n        identified during job creation as available on this node.\n\n        :returns: a node entry from the ring\n        """'
newline|'\n'
name|'nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_part_nodes'
op|'('
name|'part'
op|')'
newline|'\n'
name|'more_nodes'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_more_nodes'
op|'('
name|'part'
op|')'
newline|'\n'
nl|'\n'
name|'for'
name|'node'
name|'in'
name|'itertools'
op|'.'
name|'chain'
op|'('
name|'nodes'
op|','
name|'more_nodes'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'node'
op|'['
string|"'id'"
op|']'
name|'in'
name|'self'
op|'.'
name|'_local_device_ids'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'node'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'None'
newline|'\n'
nl|'\n'
DECL|member|get_reconciler_broker
dedent|''
name|'def'
name|'get_reconciler_broker'
op|'('
name|'self'
op|','
name|'timestamp'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Get a local instance of the reconciler container broker that is\n        appropriate to enqueue the given timestamp.\n\n        :param timestamp: the timestamp of the row to be enqueued\n\n        :returns: a local reconciler broker\n        """'
newline|'\n'
name|'container'
op|'='
name|'get_reconciler_container_name'
op|'('
name|'timestamp'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'reconciler_containers'
name|'and'
name|'container'
name|'in'
name|'self'
op|'.'
name|'reconciler_containers'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'reconciler_containers'
op|'['
name|'container'
op|']'
op|'['
number|'1'
op|']'
newline|'\n'
dedent|''
name|'account'
op|'='
name|'MISPLACED_OBJECTS_ACCOUNT'
newline|'\n'
name|'part'
op|'='
name|'self'
op|'.'
name|'ring'
op|'.'
name|'get_part'
op|'('
name|'account'
op|','
name|'container'
op|')'
newline|'\n'
name|'node'
op|'='
name|'self'
op|'.'
name|'find_local_handoff_for_part'
op|'('
name|'part'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'node'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'DeviceUnavailable'
op|'('
nl|'\n'
string|"'No mounted devices found suitable to Handoff reconciler '"
nl|'\n'
string|"'container %s in partition %s'"
op|'%'
op|'('
name|'container'
op|','
name|'part'
op|')'
op|')'
newline|'\n'
dedent|''
name|'hsh'
op|'='
name|'hash_path'
op|'('
name|'account'
op|','
name|'container'
op|')'
newline|'\n'
name|'db_dir'
op|'='
name|'storage_directory'
op|'('
name|'DATADIR'
op|','
name|'part'
op|','
name|'hsh'
op|')'
newline|'\n'
name|'db_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'root'
op|','
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'db_dir'
op|','
name|'hsh'
op|'+'
string|"'.db'"
op|')'
newline|'\n'
name|'broker'
op|'='
name|'ContainerBroker'
op|'('
name|'db_path'
op|','
name|'account'
op|'='
name|'account'
op|','
name|'container'
op|'='
name|'container'
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
name|'broker'
op|'.'
name|'db_file'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'broker'
op|'.'
name|'initialize'
op|'('
name|'timestamp'
op|','
number|'0'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'DatabaseAlreadyExists'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'self'
op|'.'
name|'reconciler_containers'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'reconciler_containers'
op|'['
name|'container'
op|']'
op|'='
name|'part'
op|','
name|'broker'
op|','
name|'node'
op|'['
string|"'id'"
op|']'
newline|'\n'
dedent|''
name|'return'
name|'broker'
newline|'\n'
nl|'\n'
DECL|member|feed_reconciler
dedent|''
name|'def'
name|'feed_reconciler'
op|'('
name|'self'
op|','
name|'container'
op|','
name|'item_list'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Add queue entries for rows in item_list to the local reconciler\n        container database.\n\n        :param container: the name of the reconciler container\n        :param item_list: the list of rows to enqueue\n\n        :returns: True if successfully enqueued\n        """'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'reconciler'
op|'='
name|'self'
op|'.'
name|'get_reconciler_broker'
op|'('
name|'container'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'DeviceUnavailable'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'warning'
op|'('
string|"'DeviceUnavailable: %s'"
op|','
name|'e'
op|')'
newline|'\n'
name|'return'
name|'False'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
string|"'Adding %d objects to the reconciler at %s'"
op|','
nl|'\n'
name|'len'
op|'('
name|'item_list'
op|')'
op|','
name|'reconciler'
op|'.'
name|'db_file'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'reconciler'
op|'.'
name|'merge_items'
op|'('
name|'item_list'
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
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
string|"'UNHANDLED EXCEPTION: trying to merge '"
nl|'\n'
string|"'%d items to reconciler container %s'"
op|','
nl|'\n'
name|'len'
op|'('
name|'item_list'
op|')'
op|','
name|'reconciler'
op|'.'
name|'db_file'
op|')'
newline|'\n'
name|'return'
name|'False'
newline|'\n'
dedent|''
name|'return'
name|'True'
newline|'\n'
nl|'\n'
DECL|member|dump_to_reconciler
dedent|''
name|'def'
name|'dump_to_reconciler'
op|'('
name|'self'
op|','
name|'broker'
op|','
name|'point'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Look for object rows for objects updates in the wrong storage policy\n        in broker with a ``ROWID`` greater than the rowid given as point.\n\n        :param broker: the container broker with misplaced objects\n        :param point: the last verified ``reconciler_sync_point``\n\n        :returns: the last successful enqueued rowid\n        """'
newline|'\n'
name|'max_sync'
op|'='
name|'broker'
op|'.'
name|'get_max_row'
op|'('
op|')'
newline|'\n'
name|'misplaced'
op|'='
name|'broker'
op|'.'
name|'get_misplaced_since'
op|'('
name|'point'
op|','
name|'self'
op|'.'
name|'per_diff'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'misplaced'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'max_sync'
newline|'\n'
dedent|''
name|'translator'
op|'='
name|'get_row_to_q_entry_translator'
op|'('
name|'broker'
op|')'
newline|'\n'
name|'errors'
op|'='
name|'False'
newline|'\n'
name|'low_sync'
op|'='
name|'point'
newline|'\n'
name|'while'
name|'misplaced'
op|':'
newline|'\n'
indent|'            '
name|'batches'
op|'='
name|'defaultdict'
op|'('
name|'list'
op|')'
newline|'\n'
name|'for'
name|'item'
name|'in'
name|'misplaced'
op|':'
newline|'\n'
indent|'                '
name|'container'
op|'='
name|'get_reconciler_container_name'
op|'('
name|'item'
op|'['
string|"'created_at'"
op|']'
op|')'
newline|'\n'
name|'batches'
op|'['
name|'container'
op|']'
op|'.'
name|'append'
op|'('
name|'translator'
op|'('
name|'item'
op|')'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'container'
op|','
name|'item_list'
name|'in'
name|'batches'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'success'
op|'='
name|'self'
op|'.'
name|'feed_reconciler'
op|'('
name|'container'
op|','
name|'item_list'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'success'
op|':'
newline|'\n'
indent|'                    '
name|'errors'
op|'='
name|'True'
newline|'\n'
dedent|''
dedent|''
name|'point'
op|'='
name|'misplaced'
op|'['
op|'-'
number|'1'
op|']'
op|'['
string|"'ROWID'"
op|']'
newline|'\n'
name|'if'
name|'not'
name|'errors'
op|':'
newline|'\n'
indent|'                '
name|'low_sync'
op|'='
name|'point'
newline|'\n'
dedent|''
name|'misplaced'
op|'='
name|'broker'
op|'.'
name|'get_misplaced_since'
op|'('
name|'point'
op|','
name|'self'
op|'.'
name|'per_diff'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'low_sync'
newline|'\n'
nl|'\n'
DECL|member|_post_replicate_hook
dedent|''
name|'def'
name|'_post_replicate_hook'
op|'('
name|'self'
op|','
name|'broker'
op|','
name|'info'
op|','
name|'responses'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'info'
op|'['
string|"'account'"
op|']'
op|'=='
name|'MISPLACED_OBJECTS_ACCOUNT'
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
nl|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'sync_store'
op|'.'
name|'update_sync_store'
op|'('
name|'broker'
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
string|"'Failed to update sync_store %s'"
op|'%'
nl|'\n'
name|'broker'
op|'.'
name|'db_file'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'point'
op|'='
name|'broker'
op|'.'
name|'get_reconciler_sync'
op|'('
op|')'
newline|'\n'
name|'if'
name|'not'
name|'broker'
op|'.'
name|'has_multiple_policies'
op|'('
op|')'
name|'and'
name|'info'
op|'['
string|"'max_row'"
op|']'
op|'!='
name|'point'
op|':'
newline|'\n'
indent|'            '
name|'broker'
op|'.'
name|'update_reconciler_sync'
op|'('
name|'info'
op|'['
string|"'max_row'"
op|']'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'max_sync'
op|'='
name|'self'
op|'.'
name|'dump_to_reconciler'
op|'('
name|'broker'
op|','
name|'point'
op|')'
newline|'\n'
name|'success'
op|'='
name|'responses'
op|'.'
name|'count'
op|'('
name|'True'
op|')'
op|'>='
name|'quorum_size'
op|'('
name|'len'
op|'('
name|'responses'
op|')'
op|')'
newline|'\n'
name|'if'
name|'max_sync'
op|'>'
name|'point'
name|'and'
name|'success'
op|':'
newline|'\n'
comment|'# to be safe, only slide up the sync point with a quorum on'
nl|'\n'
comment|'# replication'
nl|'\n'
indent|'            '
name|'broker'
op|'.'
name|'update_reconciler_sync'
op|'('
name|'max_sync'
op|')'
newline|'\n'
nl|'\n'
DECL|member|delete_db
dedent|''
dedent|''
name|'def'
name|'delete_db'
op|'('
name|'self'
op|','
name|'broker'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Ensure that reconciler databases are only cleaned up at the end of the\n        replication run.\n        """'
newline|'\n'
name|'if'
op|'('
name|'self'
op|'.'
name|'reconciler_cleanups'
name|'is'
name|'not'
name|'None'
name|'and'
nl|'\n'
name|'broker'
op|'.'
name|'account'
op|'=='
name|'MISPLACED_OBJECTS_ACCOUNT'
op|')'
op|':'
newline|'\n'
comment|"# this container shouldn't be here, make sure it's cleaned up"
nl|'\n'
indent|'            '
name|'self'
op|'.'
name|'reconciler_cleanups'
op|'['
name|'broker'
op|'.'
name|'container'
op|']'
op|'='
name|'broker'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
comment|'# DB is going to get deleted. Be preemptive about it'
nl|'\n'
indent|'            '
name|'self'
op|'.'
name|'sync_store'
op|'.'
name|'remove_synced_container'
op|'('
name|'broker'
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
string|"'Failed to remove sync_store entry %s'"
op|'%'
nl|'\n'
name|'broker'
op|'.'
name|'db_file'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'super'
op|'('
name|'ContainerReplicator'
op|','
name|'self'
op|')'
op|'.'
name|'delete_db'
op|'('
name|'broker'
op|')'
newline|'\n'
nl|'\n'
DECL|member|replicate_reconcilers
dedent|''
name|'def'
name|'replicate_reconcilers'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Ensure any items merged to reconciler containers during replication\n        are pushed out to correct nodes and any reconciler containers that do\n        not belong on this node are removed.\n        """'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
string|"'Replicating %d reconciler containers'"
op|','
nl|'\n'
name|'len'
op|'('
name|'self'
op|'.'
name|'reconciler_containers'
op|')'
op|')'
newline|'\n'
name|'for'
name|'part'
op|','
name|'reconciler'
op|','
name|'node_id'
name|'in'
name|'self'
op|'.'
name|'reconciler_containers'
op|'.'
name|'values'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'cpool'
op|'.'
name|'spawn_n'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'_replicate_object'
op|','
name|'part'
op|','
name|'reconciler'
op|'.'
name|'db_file'
op|','
name|'node_id'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'cpool'
op|'.'
name|'waitall'
op|'('
op|')'
newline|'\n'
comment|'# wipe out the cache do disable bypass in delete_db'
nl|'\n'
name|'cleanups'
op|'='
name|'self'
op|'.'
name|'reconciler_cleanups'
newline|'\n'
name|'self'
op|'.'
name|'reconciler_cleanups'
op|'='
name|'self'
op|'.'
name|'reconciler_containers'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
string|"'Cleaning up %d reconciler containers'"
op|','
nl|'\n'
name|'len'
op|'('
name|'cleanups'
op|')'
op|')'
newline|'\n'
name|'for'
name|'reconciler'
name|'in'
name|'cleanups'
op|'.'
name|'values'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'cpool'
op|'.'
name|'spawn_n'
op|'('
name|'self'
op|'.'
name|'delete_db'
op|','
name|'reconciler'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'cpool'
op|'.'
name|'waitall'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
string|"'Finished reconciler replication'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|run_once
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
name|'self'
op|'.'
name|'reconciler_containers'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'reconciler_cleanups'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'sync_store'
op|'='
name|'ContainerSyncStore'
op|'('
name|'self'
op|'.'
name|'root'
op|','
nl|'\n'
name|'self'
op|'.'
name|'logger'
op|','
nl|'\n'
name|'self'
op|'.'
name|'mount_check'
op|')'
newline|'\n'
name|'rv'
op|'='
name|'super'
op|'('
name|'ContainerReplicator'
op|','
name|'self'
op|')'
op|'.'
name|'run_once'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
name|'if'
name|'any'
op|'('
op|'['
name|'self'
op|'.'
name|'reconciler_containers'
op|','
name|'self'
op|'.'
name|'reconciler_cleanups'
op|']'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'replicate_reconcilers'
op|'('
op|')'
newline|'\n'
dedent|''
name|'return'
name|'rv'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ContainerReplicatorRpc
dedent|''
dedent|''
name|'class'
name|'ContainerReplicatorRpc'
op|'('
name|'db_replicator'
op|'.'
name|'ReplicatorRpc'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|_parse_sync_args
indent|'    '
name|'def'
name|'_parse_sync_args'
op|'('
name|'self'
op|','
name|'args'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'parent'
op|'='
name|'super'
op|'('
name|'ContainerReplicatorRpc'
op|','
name|'self'
op|')'
newline|'\n'
name|'remote_info'
op|'='
name|'parent'
op|'.'
name|'_parse_sync_args'
op|'('
name|'args'
op|')'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'args'
op|')'
op|'>'
number|'9'
op|':'
newline|'\n'
indent|'            '
name|'remote_info'
op|'['
string|"'status_changed_at'"
op|']'
op|'='
name|'args'
op|'['
number|'7'
op|']'
newline|'\n'
name|'remote_info'
op|'['
string|"'count'"
op|']'
op|'='
name|'args'
op|'['
number|'8'
op|']'
newline|'\n'
name|'remote_info'
op|'['
string|"'storage_policy_index'"
op|']'
op|'='
name|'args'
op|'['
number|'9'
op|']'
newline|'\n'
dedent|''
name|'return'
name|'remote_info'
newline|'\n'
nl|'\n'
DECL|member|_get_synced_replication_info
dedent|''
name|'def'
name|'_get_synced_replication_info'
op|'('
name|'self'
op|','
name|'broker'
op|','
name|'remote_info'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Sync the remote_info storage_policy_index if needed and return the\n        newly synced replication info.\n\n        :param broker: the database broker\n        :param remote_info: the remote replication info\n\n        :returns: local broker replication info\n        """'
newline|'\n'
name|'info'
op|'='
name|'broker'
op|'.'
name|'get_replication_info'
op|'('
op|')'
newline|'\n'
name|'if'
name|'incorrect_policy_index'
op|'('
name|'info'
op|','
name|'remote_info'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'status_changed_at'
op|'='
name|'Timestamp'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
op|'.'
name|'internal'
newline|'\n'
name|'broker'
op|'.'
name|'set_storage_policy_index'
op|'('
nl|'\n'
name|'remote_info'
op|'['
string|"'storage_policy_index'"
op|']'
op|','
nl|'\n'
name|'timestamp'
op|'='
name|'status_changed_at'
op|')'
newline|'\n'
name|'info'
op|'='
name|'broker'
op|'.'
name|'get_replication_info'
op|'('
op|')'
newline|'\n'
dedent|''
name|'return'
name|'info'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
