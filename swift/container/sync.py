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
name|'time'
name|'import'
name|'ctime'
op|','
name|'time'
newline|'\n'
name|'from'
name|'random'
name|'import'
name|'random'
op|','
name|'shuffle'
newline|'\n'
name|'from'
name|'struct'
name|'import'
name|'unpack_from'
newline|'\n'
nl|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'sleep'
op|','
name|'Timeout'
newline|'\n'
nl|'\n'
name|'import'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'db'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'container'
name|'import'
name|'server'
name|'as'
name|'container_server'
newline|'\n'
name|'from'
name|'swiftclient'
name|'import'
name|'ClientException'
op|','
name|'delete_object'
op|','
name|'put_object'
op|','
name|'quote'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'direct_client'
name|'import'
name|'direct_get_object'
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
name|'db'
name|'import'
name|'ContainerBroker'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'audit_location_generator'
op|','
name|'get_logger'
op|','
name|'hash_path'
op|','
name|'config_true_value'
op|','
name|'validate_sync_to'
op|','
name|'whataremyips'
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
name|'common'
op|'.'
name|'http'
name|'import'
name|'HTTP_UNAUTHORIZED'
op|','
name|'HTTP_NOT_FOUND'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|_Iter2FileLikeObject
name|'class'
name|'_Iter2FileLikeObject'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Returns an iterator\'s contents via :func:`read`, making it look like a file\n    object.\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'iterator'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'iterator'
op|'='
name|'iterator'
newline|'\n'
name|'self'
op|'.'
name|'_chunk'
op|'='
string|"''"
newline|'\n'
nl|'\n'
DECL|member|read
dedent|''
name|'def'
name|'read'
op|'('
name|'self'
op|','
name|'size'
op|'='
op|'-'
number|'1'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        read([size]) -> read at most size bytes, returned as a string.\n\n        If the size argument is negative or omitted, read until EOF is reached.\n        Notice that when in non-blocking mode, less data than what was\n        requested may be returned, even if no size parameter was given.\n        """'
newline|'\n'
name|'if'
name|'size'
op|'<'
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'chunk'
op|'='
name|'self'
op|'.'
name|'_chunk'
newline|'\n'
name|'self'
op|'.'
name|'_chunk'
op|'='
string|"''"
newline|'\n'
name|'return'
name|'chunk'
op|'+'
string|"''"
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'iterator'
op|')'
newline|'\n'
dedent|''
name|'chunk'
op|'='
name|'self'
op|'.'
name|'_chunk'
newline|'\n'
name|'self'
op|'.'
name|'_chunk'
op|'='
string|"''"
newline|'\n'
name|'if'
name|'chunk'
name|'and'
name|'len'
op|'('
name|'chunk'
op|')'
op|'<='
name|'size'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'chunk'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'chunk'
op|'+='
name|'self'
op|'.'
name|'iterator'
op|'.'
name|'next'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'StopIteration'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'if'
name|'len'
op|'('
name|'chunk'
op|')'
op|'<='
name|'size'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'chunk'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'_chunk'
op|'='
name|'chunk'
op|'['
name|'size'
op|':'
op|']'
newline|'\n'
name|'return'
name|'chunk'
op|'['
op|':'
name|'size'
op|']'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ContainerSync
dedent|''
dedent|''
name|'class'
name|'ContainerSync'
op|'('
name|'Daemon'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Daemon to sync syncable containers.\n\n    This is done by scanning the local devices for container databases and\n    checking for x-container-sync-to and x-container-sync-key metadata values.\n    If they exist, newer rows since the last sync will trigger PUTs or DELETEs\n    to the other container.\n\n    .. note::\n\n        Container sync will sync object POSTs only if the proxy server is set\n        to use "object_post_as_copy = true" which is the default. So-called\n        fast object posts, "object_post_as_copy = false" do not update the\n        container listings and therefore can\'t be detected for synchronization.\n\n    The actual syncing is slightly more complicated to make use of the three\n    (or number-of-replicas) main nodes for a container without each trying to\n    do the exact same work but also without missing work if one node happens to\n    be down.\n\n    Two sync points are kept per container database. All rows between the two\n    sync points trigger updates. Any rows newer than both sync points cause\n    updates depending on the node\'s position for the container (primary nodes\n    do one third, etc. depending on the replica count of course). After a sync\n    run, the first sync point is set to the newest ROWID known and the second\n    sync point is set to newest ROWID for which all updates have been sent.\n\n    An example may help. Assume replica count is 3 and perfectly matching\n    ROWIDs starting at 1.\n\n        First sync run, database has 6 rows:\n\n            * SyncPoint1 starts as -1.\n            * SyncPoint2 starts as -1.\n            * No rows between points, so no "all updates" rows.\n            * Six rows newer than SyncPoint1, so a third of the rows are sent\n              by node 1, another third by node 2, remaining third by node 3.\n            * SyncPoint1 is set as 6 (the newest ROWID known).\n            * SyncPoint2 is left as -1 since no "all updates" rows were synced.\n\n        Next sync run, database has 12 rows:\n\n            * SyncPoint1 starts as 6.\n            * SyncPoint2 starts as -1.\n            * The rows between -1 and 6 all trigger updates (most of which\n              should short-circuit on the remote end as having already been\n              done).\n            * Six more rows newer than SyncPoint1, so a third of the rows are\n              sent by node 1, another third by node 2, remaining third by node\n              3.\n            * SyncPoint1 is set as 12 (the newest ROWID known).\n            * SyncPoint2 is set as 6 (the newest "all updates" ROWID).\n\n    In this way, under normal circumstances each node sends its share of\n    updates each run and just sends a batch of older updates to ensure nothing\n    was missed.\n\n    :param conf: The dict of configuration values from the [container-sync]\n                 section of the container-server.conf\n    :param container_ring: If None, the <swift_dir>/container.ring.gz will be\n                           loaded. This is overridden by unit tests.\n    :param object_ring: If None, the <swift_dir>/object.ring.gz will be loaded.\n                        This is overridden by unit tests.\n    """'
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
name|'container_ring'
op|'='
name|'None'
op|','
name|'object_ring'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
comment|'#: The dict of configuration values from the [container-sync] section'
nl|'\n'
comment|'#: of the container-server.conf.'
nl|'\n'
indent|'        '
name|'self'
op|'.'
name|'conf'
op|'='
name|'conf'
newline|'\n'
comment|'#: Logger to use for container-sync log lines.'
nl|'\n'
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
string|"'container-sync'"
op|')'
newline|'\n'
comment|'#: Path to the local device mount points.'
nl|'\n'
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
comment|'#: Indicates whether mount points should be verified as actual mount'
nl|'\n'
comment|'#: points (normally true, false for tests and SAIO).'
nl|'\n'
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
comment|'#: Minimum time between full scans. This is to keep the daemon from'
nl|'\n'
comment|'#: running wild on near empty systems.'
nl|'\n'
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
comment|'#: Maximum amount of time to spend syncing a container before moving on'
nl|'\n'
comment|"#: to the next one. If a conatiner sync hasn't finished in this time,"
nl|'\n'
comment|"#: it'll just be resumed next scan."
nl|'\n'
name|'self'
op|'.'
name|'container_time'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'container_time'"
op|','
number|'60'
op|')'
op|')'
newline|'\n'
comment|"#: The list of hosts we're allowed to send syncs to."
nl|'\n'
name|'self'
op|'.'
name|'allowed_sync_hosts'
op|'='
op|'['
nl|'\n'
name|'h'
op|'.'
name|'strip'
op|'('
op|')'
nl|'\n'
name|'for'
name|'h'
name|'in'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'allowed_sync_hosts'"
op|','
string|"'127.0.0.1'"
op|')'
op|'.'
name|'split'
op|'('
string|"','"
op|')'
nl|'\n'
name|'if'
name|'h'
op|'.'
name|'strip'
op|'('
op|')'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'proxy'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'sync_proxy'"
op|')'
newline|'\n'
comment|'#: Number of containers with sync turned on that were successfully'
nl|'\n'
comment|'#: synced.'
nl|'\n'
name|'self'
op|'.'
name|'container_syncs'
op|'='
number|'0'
newline|'\n'
comment|'#: Number of successful DELETEs triggered.'
nl|'\n'
name|'self'
op|'.'
name|'container_deletes'
op|'='
number|'0'
newline|'\n'
comment|'#: Number of successful PUTs triggered.'
nl|'\n'
name|'self'
op|'.'
name|'container_puts'
op|'='
number|'0'
newline|'\n'
comment|"#: Number of containers that didn't have sync turned on."
nl|'\n'
name|'self'
op|'.'
name|'container_skips'
op|'='
number|'0'
newline|'\n'
comment|'#: Number of containers that had a failure of some type.'
nl|'\n'
name|'self'
op|'.'
name|'container_failures'
op|'='
number|'0'
newline|'\n'
comment|'#: Time of last stats report.'
nl|'\n'
name|'self'
op|'.'
name|'reported'
op|'='
name|'time'
op|'('
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
comment|'#: swift.common.ring.Ring for locating containers.'
nl|'\n'
name|'self'
op|'.'
name|'container_ring'
op|'='
name|'container_ring'
name|'or'
name|'Ring'
op|'('
name|'swift_dir'
op|','
nl|'\n'
name|'ring_name'
op|'='
string|"'container'"
op|')'
newline|'\n'
comment|'#: swift.common.ring.Ring for locating objects.'
nl|'\n'
name|'self'
op|'.'
name|'object_ring'
op|'='
name|'object_ring'
name|'or'
name|'Ring'
op|'('
name|'swift_dir'
op|','
name|'ring_name'
op|'='
string|"'object'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_myips'
op|'='
name|'whataremyips'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_myport'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'bind_port'"
op|','
number|'6001'
op|')'
op|')'
newline|'\n'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'db'
op|'.'
name|'DB_PREALLOCATION'
op|'='
name|'config_true_value'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'db_preallocation'"
op|','
string|"'f'"
op|')'
op|')'
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
newline|'\n'
indent|'        '
string|'"""\n        Runs container sync scans until stopped.\n        """'
newline|'\n'
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
name|'container_server'
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
name|'container_sync'
op|'('
name|'path'
op|')'
newline|'\n'
name|'if'
name|'time'
op|'('
op|')'
op|'-'
name|'self'
op|'.'
name|'reported'
op|'>='
number|'3600'
op|':'
comment|'# once an hour'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'report'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
name|'elapsed'
op|'='
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
string|'"""\n        Runs a single container sync scan.\n        """'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|'\'Begin container sync "once" mode\''
op|')'
op|')'
newline|'\n'
name|'begin'
op|'='
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
name|'container_server'
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
name|'container_sync'
op|'('
name|'path'
op|')'
newline|'\n'
name|'if'
name|'time'
op|'('
op|')'
op|'-'
name|'self'
op|'.'
name|'reported'
op|'>='
number|'3600'
op|':'
comment|'# once an hour'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'report'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'report'
op|'('
op|')'
newline|'\n'
name|'elapsed'
op|'='
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
string|'\'Container sync "once" mode completed: %.02fs\''
op|')'
op|','
name|'elapsed'
op|')'
newline|'\n'
nl|'\n'
DECL|member|report
dedent|''
name|'def'
name|'report'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Writes a report of the stats to the logger and resets the stats for the\n        next report.\n        """'
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
string|"'Since %(time)s: %(sync)s synced [%(delete)s deletes, %(put)s '"
nl|'\n'
string|"'puts], %(skip)s skipped, %(fail)s failed'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'time'"
op|':'
name|'ctime'
op|'('
name|'self'
op|'.'
name|'reported'
op|')'
op|','
nl|'\n'
string|"'sync'"
op|':'
name|'self'
op|'.'
name|'container_syncs'
op|','
nl|'\n'
string|"'delete'"
op|':'
name|'self'
op|'.'
name|'container_deletes'
op|','
nl|'\n'
string|"'put'"
op|':'
name|'self'
op|'.'
name|'container_puts'
op|','
nl|'\n'
string|"'skip'"
op|':'
name|'self'
op|'.'
name|'container_skips'
op|','
nl|'\n'
string|"'fail'"
op|':'
name|'self'
op|'.'
name|'container_failures'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'reported'
op|'='
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'container_syncs'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'container_deletes'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'container_puts'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'container_skips'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'container_failures'
op|'='
number|'0'
newline|'\n'
nl|'\n'
DECL|member|container_sync
dedent|''
name|'def'
name|'container_sync'
op|'('
name|'self'
op|','
name|'path'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Checks the given path for a container database, determines if syncing\n        is turned on for that database and, if so, sends any updates to the\n        other container.\n\n        :param path: the path to a container db\n        """'
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
name|'ContainerBroker'
op|'('
name|'path'
op|')'
newline|'\n'
name|'info'
op|'='
name|'broker'
op|'.'
name|'get_info'
op|'('
op|')'
newline|'\n'
name|'x'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'container_ring'
op|'.'
name|'get_nodes'
op|'('
name|'info'
op|'['
string|"'account'"
op|']'
op|','
nl|'\n'
name|'info'
op|'['
string|"'container'"
op|']'
op|')'
newline|'\n'
name|'for'
name|'ordinal'
op|','
name|'node'
name|'in'
name|'enumerate'
op|'('
name|'nodes'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'node'
op|'['
string|"'ip'"
op|']'
name|'in'
name|'self'
op|'.'
name|'_myips'
name|'and'
name|'node'
op|'['
string|"'port'"
op|']'
op|'=='
name|'self'
op|'.'
name|'_myport'
op|':'
newline|'\n'
indent|'                    '
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'return'
newline|'\n'
dedent|''
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
name|'sync_to'
op|'='
name|'None'
newline|'\n'
name|'sync_key'
op|'='
name|'None'
newline|'\n'
name|'sync_point1'
op|'='
name|'info'
op|'['
string|"'x_container_sync_point1'"
op|']'
newline|'\n'
name|'sync_point2'
op|'='
name|'info'
op|'['
string|"'x_container_sync_point2'"
op|']'
newline|'\n'
name|'for'
name|'key'
op|','
op|'('
name|'value'
op|','
name|'timestamp'
op|')'
name|'in'
name|'broker'
op|'.'
name|'metadata'
op|'.'
name|'iteritems'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'key'
op|'.'
name|'lower'
op|'('
op|')'
op|'=='
string|"'x-container-sync-to'"
op|':'
newline|'\n'
indent|'                        '
name|'sync_to'
op|'='
name|'value'
newline|'\n'
dedent|''
name|'elif'
name|'key'
op|'.'
name|'lower'
op|'('
op|')'
op|'=='
string|"'x-container-sync-key'"
op|':'
newline|'\n'
indent|'                        '
name|'sync_key'
op|'='
name|'value'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'not'
name|'sync_to'
name|'or'
name|'not'
name|'sync_key'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'container_skips'
op|'+='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|"'skips'"
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'sync_to'
op|'='
name|'sync_to'
op|'.'
name|'rstrip'
op|'('
string|"'/'"
op|')'
newline|'\n'
name|'err'
op|'='
name|'validate_sync_to'
op|'('
name|'sync_to'
op|','
name|'self'
op|'.'
name|'allowed_sync_hosts'
op|')'
newline|'\n'
name|'if'
name|'err'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'ERROR %(db_file)s: %(validate_sync_to_err)s'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'db_file'"
op|':'
name|'broker'
op|'.'
name|'db_file'
op|','
nl|'\n'
string|"'validate_sync_to_err'"
op|':'
name|'err'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'container_failures'
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
name|'return'
newline|'\n'
dedent|''
name|'stop_at'
op|'='
name|'time'
op|'('
op|')'
op|'+'
name|'self'
op|'.'
name|'container_time'
newline|'\n'
name|'while'
name|'time'
op|'('
op|')'
op|'<'
name|'stop_at'
name|'and'
name|'sync_point2'
op|'<'
name|'sync_point1'
op|':'
newline|'\n'
indent|'                    '
name|'rows'
op|'='
name|'broker'
op|'.'
name|'get_items_since'
op|'('
name|'sync_point2'
op|','
number|'1'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'rows'
op|':'
newline|'\n'
indent|'                        '
name|'break'
newline|'\n'
dedent|''
name|'row'
op|'='
name|'rows'
op|'['
number|'0'
op|']'
newline|'\n'
name|'if'
name|'row'
op|'['
string|"'ROWID'"
op|']'
op|'>'
name|'sync_point1'
op|':'
newline|'\n'
indent|'                        '
name|'break'
newline|'\n'
dedent|''
name|'key'
op|'='
name|'hash_path'
op|'('
name|'info'
op|'['
string|"'account'"
op|']'
op|','
name|'info'
op|'['
string|"'container'"
op|']'
op|','
nl|'\n'
name|'row'
op|'['
string|"'name'"
op|']'
op|','
name|'raw_digest'
op|'='
name|'True'
op|')'
newline|'\n'
comment|'# This node will only intially sync out one third of the'
nl|'\n'
comment|'# objects (if 3 replicas, 1/4 if 4, etc.). This section'
nl|'\n'
comment|'# will attempt to sync previously skipped rows in case the'
nl|'\n'
comment|"# other nodes didn't succeed."
nl|'\n'
name|'if'
name|'unpack_from'
op|'('
string|"'>I'"
op|','
name|'key'
op|')'
op|'['
number|'0'
op|']'
op|'%'
name|'len'
op|'('
name|'nodes'
op|')'
op|'!='
name|'ordinal'
op|':'
newline|'\n'
indent|'                        '
name|'if'
name|'not'
name|'self'
op|'.'
name|'container_sync_row'
op|'('
name|'row'
op|','
name|'sync_to'
op|','
name|'sync_key'
op|','
nl|'\n'
name|'broker'
op|','
name|'info'
op|')'
op|':'
newline|'\n'
indent|'                            '
name|'return'
newline|'\n'
dedent|''
dedent|''
name|'sync_point2'
op|'='
name|'row'
op|'['
string|"'ROWID'"
op|']'
newline|'\n'
name|'broker'
op|'.'
name|'set_x_container_sync_points'
op|'('
name|'None'
op|','
name|'sync_point2'
op|')'
newline|'\n'
dedent|''
name|'while'
name|'time'
op|'('
op|')'
op|'<'
name|'stop_at'
op|':'
newline|'\n'
indent|'                    '
name|'rows'
op|'='
name|'broker'
op|'.'
name|'get_items_since'
op|'('
name|'sync_point1'
op|','
number|'1'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'rows'
op|':'
newline|'\n'
indent|'                        '
name|'break'
newline|'\n'
dedent|''
name|'row'
op|'='
name|'rows'
op|'['
number|'0'
op|']'
newline|'\n'
name|'key'
op|'='
name|'hash_path'
op|'('
name|'info'
op|'['
string|"'account'"
op|']'
op|','
name|'info'
op|'['
string|"'container'"
op|']'
op|','
nl|'\n'
name|'row'
op|'['
string|"'name'"
op|']'
op|','
name|'raw_digest'
op|'='
name|'True'
op|')'
newline|'\n'
comment|'# This node will only intially sync out one third of the'
nl|'\n'
comment|"# objects (if 3 replicas, 1/4 if 4, etc.). It'll come back"
nl|'\n'
comment|'# around to the section above and attempt to sync'
nl|'\n'
comment|"# previously skipped rows in case the other nodes didn't"
nl|'\n'
comment|'# succeed.'
nl|'\n'
name|'if'
name|'unpack_from'
op|'('
string|"'>I'"
op|','
name|'key'
op|')'
op|'['
number|'0'
op|']'
op|'%'
name|'len'
op|'('
name|'nodes'
op|')'
op|'=='
name|'ordinal'
op|':'
newline|'\n'
indent|'                        '
name|'if'
name|'not'
name|'self'
op|'.'
name|'container_sync_row'
op|'('
name|'row'
op|','
name|'sync_to'
op|','
name|'sync_key'
op|','
nl|'\n'
name|'broker'
op|','
name|'info'
op|')'
op|':'
newline|'\n'
indent|'                            '
name|'return'
newline|'\n'
dedent|''
dedent|''
name|'sync_point1'
op|'='
name|'row'
op|'['
string|"'ROWID'"
op|']'
newline|'\n'
name|'broker'
op|'.'
name|'set_x_container_sync_points'
op|'('
name|'sync_point1'
op|','
name|'None'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'container_syncs'
op|'+='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|"'syncs'"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'Timeout'
op|')'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'container_failures'
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
name|'exception'
op|'('
name|'_'
op|'('
string|"'ERROR Syncing %s'"
op|')'
op|','
op|'('
name|'broker'
op|'.'
name|'db_file'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|container_sync_row
dedent|''
dedent|''
name|'def'
name|'container_sync_row'
op|'('
name|'self'
op|','
name|'row'
op|','
name|'sync_to'
op|','
name|'sync_key'
op|','
name|'broker'
op|','
name|'info'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Sends the update the row indicates to the sync_to container.\n\n        :param row: The updated row in the local database triggering the sync\n                    update.\n        :param sync_to: The URL to the remote container.\n        :param sync_key: The X-Container-Sync-Key to use when sending requests\n                         to the other container.\n        :param broker: The local container database broker.\n        :param info: The get_info result from the local container database\n                     broker.\n        :returns: True on success\n        """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'start_time'
op|'='
name|'time'
op|'('
op|')'
newline|'\n'
name|'if'
name|'row'
op|'['
string|"'deleted'"
op|']'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'delete_object'
op|'('
name|'sync_to'
op|','
name|'name'
op|'='
name|'row'
op|'['
string|"'name'"
op|']'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'x-timestamp'"
op|':'
name|'row'
op|'['
string|"'created_at'"
op|']'
op|','
nl|'\n'
string|"'x-container-sync-key'"
op|':'
name|'sync_key'
op|'}'
op|','
nl|'\n'
name|'proxy'
op|'='
name|'self'
op|'.'
name|'proxy'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ClientException'
op|','
name|'err'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'err'
op|'.'
name|'http_status'
op|'!='
name|'HTTP_NOT_FOUND'
op|':'
newline|'\n'
indent|'                        '
name|'raise'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'container_deletes'
op|'+='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|"'deletes'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'timing_since'
op|'('
string|"'deletes.timing'"
op|','
name|'start_time'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'object_ring'
op|'.'
name|'get_nodes'
op|'('
nl|'\n'
name|'info'
op|'['
string|"'account'"
op|']'
op|','
name|'info'
op|'['
string|"'container'"
op|']'
op|','
nl|'\n'
name|'row'
op|'['
string|"'name'"
op|']'
op|')'
newline|'\n'
name|'shuffle'
op|'('
name|'nodes'
op|')'
newline|'\n'
name|'exc'
op|'='
name|'None'
newline|'\n'
name|'looking_for_timestamp'
op|'='
name|'float'
op|'('
name|'row'
op|'['
string|"'created_at'"
op|']'
op|')'
newline|'\n'
name|'timestamp'
op|'='
op|'-'
number|'1'
newline|'\n'
name|'headers'
op|'='
name|'body'
op|'='
name|'None'
newline|'\n'
name|'for'
name|'node'
name|'in'
name|'nodes'
op|':'
newline|'\n'
indent|'                    '
name|'try'
op|':'
newline|'\n'
indent|'                        '
name|'these_headers'
op|','
name|'this_body'
op|'='
name|'direct_get_object'
op|'('
nl|'\n'
name|'node'
op|','
name|'part'
op|','
name|'info'
op|'['
string|"'account'"
op|']'
op|','
name|'info'
op|'['
string|"'container'"
op|']'
op|','
nl|'\n'
name|'row'
op|'['
string|"'name'"
op|']'
op|','
name|'resp_chunk_size'
op|'='
number|'65536'
op|')'
newline|'\n'
name|'this_timestamp'
op|'='
name|'float'
op|'('
name|'these_headers'
op|'['
string|"'x-timestamp'"
op|']'
op|')'
newline|'\n'
name|'if'
name|'this_timestamp'
op|'>'
name|'timestamp'
op|':'
newline|'\n'
indent|'                            '
name|'timestamp'
op|'='
name|'this_timestamp'
newline|'\n'
name|'headers'
op|'='
name|'these_headers'
newline|'\n'
name|'body'
op|'='
name|'this_body'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'ClientException'
op|','
name|'err'
op|':'
newline|'\n'
comment|'# If any errors are not 404, make sure we report the'
nl|'\n'
comment|"# non-404 one. We don't want to mistakenly assume the"
nl|'\n'
comment|'# object no longer exists just because one says so and'
nl|'\n'
comment|'# the others errored for some other reason.'
nl|'\n'
indent|'                        '
name|'if'
name|'not'
name|'exc'
name|'or'
name|'exc'
op|'.'
name|'http_status'
op|'=='
name|'HTTP_NOT_FOUND'
op|':'
newline|'\n'
indent|'                            '
name|'exc'
op|'='
name|'err'
newline|'\n'
dedent|''
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'Timeout'
op|')'
op|','
name|'err'
op|':'
newline|'\n'
indent|'                        '
name|'exc'
op|'='
name|'err'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'timestamp'
op|'<'
name|'looking_for_timestamp'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'exc'
op|':'
newline|'\n'
indent|'                        '
name|'raise'
name|'exc'
newline|'\n'
dedent|''
name|'raise'
name|'Exception'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Unknown exception trying to GET: %(node)r '"
nl|'\n'
string|"'%(account)r %(container)r %(object)r'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'node'"
op|':'
name|'node'
op|','
string|"'part'"
op|':'
name|'part'
op|','
nl|'\n'
string|"'account'"
op|':'
name|'info'
op|'['
string|"'account'"
op|']'
op|','
nl|'\n'
string|"'container'"
op|':'
name|'info'
op|'['
string|"'container'"
op|']'
op|','
nl|'\n'
string|"'object'"
op|':'
name|'row'
op|'['
string|"'name'"
op|']'
op|'}'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'key'
name|'in'
op|'('
string|"'date'"
op|','
string|"'last-modified'"
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'key'
name|'in'
name|'headers'
op|':'
newline|'\n'
indent|'                        '
name|'del'
name|'headers'
op|'['
name|'key'
op|']'
newline|'\n'
dedent|''
dedent|''
name|'if'
string|"'etag'"
name|'in'
name|'headers'
op|':'
newline|'\n'
indent|'                    '
name|'headers'
op|'['
string|"'etag'"
op|']'
op|'='
name|'headers'
op|'['
string|"'etag'"
op|']'
op|'.'
name|'strip'
op|'('
string|'\'"\''
op|')'
newline|'\n'
dedent|''
name|'headers'
op|'['
string|"'x-timestamp'"
op|']'
op|'='
name|'row'
op|'['
string|"'created_at'"
op|']'
newline|'\n'
name|'headers'
op|'['
string|"'x-container-sync-key'"
op|']'
op|'='
name|'sync_key'
newline|'\n'
name|'put_object'
op|'('
name|'sync_to'
op|','
name|'name'
op|'='
name|'row'
op|'['
string|"'name'"
op|']'
op|','
name|'headers'
op|'='
name|'headers'
op|','
nl|'\n'
name|'contents'
op|'='
name|'_Iter2FileLikeObject'
op|'('
name|'body'
op|')'
op|','
nl|'\n'
name|'proxy'
op|'='
name|'self'
op|'.'
name|'proxy'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'container_puts'
op|'+='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|"'puts'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'timing_since'
op|'('
string|"'puts.timing'"
op|','
name|'start_time'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'ClientException'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'err'
op|'.'
name|'http_status'
op|'=='
name|'HTTP_UNAUTHORIZED'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Unauth %(sync_from)r => %(sync_to)r'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'sync_from'"
op|':'
string|"'%s/%s'"
op|'%'
nl|'\n'
op|'('
name|'quote'
op|'('
name|'info'
op|'['
string|"'account'"
op|']'
op|')'
op|','
name|'quote'
op|'('
name|'info'
op|'['
string|"'container'"
op|']'
op|')'
op|')'
op|','
nl|'\n'
string|"'sync_to'"
op|':'
name|'sync_to'
op|'}'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'err'
op|'.'
name|'http_status'
op|'=='
name|'HTTP_NOT_FOUND'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Not found %(sync_from)r => %(sync_to)r'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'sync_from'"
op|':'
string|"'%s/%s'"
op|'%'
nl|'\n'
op|'('
name|'quote'
op|'('
name|'info'
op|'['
string|"'account'"
op|']'
op|')'
op|','
name|'quote'
op|'('
name|'info'
op|'['
string|"'container'"
op|']'
op|')'
op|')'
op|','
nl|'\n'
string|"'sync_to'"
op|':'
name|'sync_to'
op|'}'
op|')'
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
name|'exception'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'ERROR Syncing %(db_file)s %(row)s'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'db_file'"
op|':'
name|'broker'
op|'.'
name|'db_file'
op|','
string|"'row'"
op|':'
name|'row'
op|'}'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'container_failures'
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
name|'return'
name|'False'
newline|'\n'
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'Timeout'
op|')'
op|','
name|'err'
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
string|"'ERROR Syncing %(db_file)s %(row)s'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'db_file'"
op|':'
name|'broker'
op|'.'
name|'db_file'
op|','
string|"'row'"
op|':'
name|'row'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'container_failures'
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
name|'return'
name|'False'
newline|'\n'
dedent|''
name|'return'
name|'True'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
