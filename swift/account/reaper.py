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
name|'random'
newline|'\n'
name|'from'
name|'logging'
name|'import'
name|'DEBUG'
newline|'\n'
name|'from'
name|'math'
name|'import'
name|'sqrt'
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'time'
newline|'\n'
nl|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'GreenPool'
op|','
name|'sleep'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'account'
op|'.'
name|'server'
name|'import'
name|'DATADIR'
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
name|'direct_client'
name|'import'
name|'ClientException'
op|','
name|'direct_delete_container'
op|','
name|'direct_delete_object'
op|','
name|'direct_get_container'
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
nl|'\n'
nl|'\n'
DECL|class|AccountReaper
name|'class'
name|'AccountReaper'
op|'('
name|'Daemon'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Removes data from status=DELETED accounts. These are accounts that have\n    been asked to be removed by the reseller via services\n    remove_storage_account XMLRPC call.\n\n    The account is not deleted immediately by the services call, but instead\n    the account is simply marked for deletion by setting the status column in\n    the account_stat table of the account database. This account reaper scans\n    for such accounts and removes the data in the background. The background\n    deletion process will occur on the primary account server for the account.\n\n    :param server_conf: The [account-server] dictionary of the account server\n                        configuration file\n    :param reaper_conf: The [account-reaper] dictionary of the account server\n                        configuration file\n\n    See the etc/account-server.conf-sample for information on the possible\n    configuration parameters.\n    """'
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
number|'3600'
op|')'
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
name|'account_ring'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'container_ring'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'object_ring'
op|'='
name|'None'
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
name|'myips'
op|'='
name|'whataremyips'
op|'('
op|')'
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
number|'25'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'container_concurrency'
op|'='
name|'self'
op|'.'
name|'object_concurrency'
op|'='
name|'sqrt'
op|'('
name|'self'
op|'.'
name|'concurrency'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'container_pool'
op|'='
name|'GreenPool'
op|'('
name|'size'
op|'='
name|'self'
op|'.'
name|'container_concurrency'
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_account_ring
dedent|''
name|'def'
name|'get_account_ring'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'""" The account :class:`swift.common.ring.Ring` for the cluster. """'
newline|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'account_ring'
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
name|'_'
op|'('
string|"'Loading account ring from %s'"
op|')'
op|','
name|'self'
op|'.'
name|'account_ring_path'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account_ring'
op|'='
name|'Ring'
op|'('
name|'self'
op|'.'
name|'account_ring_path'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'account_ring'
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
string|'""" The container :class:`swift.common.ring.Ring` for the cluster. """'
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
name|'_'
op|'('
string|"'Loading container ring from %s'"
op|')'
op|','
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
DECL|member|get_object_ring
dedent|''
name|'def'
name|'get_object_ring'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'""" The object :class:`swift.common.ring.Ring` for the cluster. """'
newline|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'object_ring'
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
name|'_'
op|'('
string|"'Loading object ring from %s'"
op|')'
op|','
name|'self'
op|'.'
name|'object_ring_path'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'object_ring'
op|'='
name|'Ring'
op|'('
name|'self'
op|'.'
name|'object_ring_path'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'object_ring'
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
string|'"""\n        Main entry point when running the reaper in its normal daemon mode.\n        This repeatedly calls :func:`reap_once` no quicker than the\n        configuration interval.\n        """'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|"'Daemon started.'"
op|')'
op|')'
newline|'\n'
name|'sleep'
op|'('
name|'random'
op|'.'
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
name|'self'
op|'.'
name|'run_once'
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
string|'"""\n        Main entry point when running the reaper in \'once\' mode, where it will\n        do a single pass over all accounts on the server. This is called\n        repeatedly by :func:`run_forever`. This will call :func:`reap_device`\n        once for each device on the server.\n        """'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|"'Begin devices pass: %s'"
op|')'
op|','
name|'self'
op|'.'
name|'devices'
op|')'
newline|'\n'
name|'begin'
op|'='
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
name|'reap_device'
op|'('
name|'device'
op|')'
newline|'\n'
dedent|''
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
name|'_'
op|'('
string|"'Devices pass completed: %.02fs'"
op|')'
op|','
name|'elapsed'
op|')'
newline|'\n'
nl|'\n'
DECL|member|reap_device
dedent|''
name|'def'
name|'reap_device'
op|'('
name|'self'
op|','
name|'device'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Called once per pass for each device on the server. This will scan the\n        accounts directory for the device, looking for partitions this device\n        is the primary for, then looking for account databases that are marked\n        status=DELETED and still have containers and calling\n        :func:`reap_account`. Account databases marked status=DELETED that no\n        longer have containers will eventually be permanently removed by the\n        reclaim process within the account replicator (see\n        :mod:`swift.db_replicator`).\n\n        :param device: The device to look for accounts to be deleted.\n        """'
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
name|'for'
name|'partition'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'datadir'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'partition_path'
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
name|'partition'
op|'.'
name|'isdigit'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'continue'
newline|'\n'
dedent|''
name|'nodes'
op|'='
name|'self'
op|'.'
name|'get_account_ring'
op|'('
op|')'
op|'.'
name|'get_part_nodes'
op|'('
name|'int'
op|'('
name|'partition'
op|')'
op|')'
newline|'\n'
name|'if'
name|'nodes'
op|'['
number|'0'
op|']'
op|'['
string|"'ip'"
op|']'
name|'not'
name|'in'
name|'self'
op|'.'
name|'myips'
name|'or'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'isdir'
op|'('
name|'partition_path'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'continue'
newline|'\n'
dedent|''
name|'for'
name|'suffix'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'partition_path'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'suffix_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'partition_path'
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
name|'suffix_path'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'continue'
newline|'\n'
dedent|''
name|'for'
name|'hsh'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'suffix_path'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'hsh_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'suffix_path'
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
name|'hsh_path'
op|')'
op|':'
newline|'\n'
indent|'                        '
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
name|'hsh_path'
op|')'
op|','
name|'reverse'
op|'='
name|'True'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'if'
name|'fname'
op|'.'
name|'endswith'
op|'('
string|"'.ts'"
op|')'
op|':'
newline|'\n'
indent|'                            '
name|'break'
newline|'\n'
dedent|''
name|'elif'
name|'fname'
op|'.'
name|'endswith'
op|'('
string|"'.db'"
op|')'
op|':'
newline|'\n'
indent|'                            '
name|'broker'
op|'='
name|'AccountBroker'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'hsh_path'
op|','
name|'fname'
op|')'
op|')'
newline|'\n'
name|'if'
name|'broker'
op|'.'
name|'is_status_deleted'
op|'('
op|')'
name|'and'
name|'not'
name|'broker'
op|'.'
name|'empty'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                                '
name|'self'
op|'.'
name|'reap_account'
op|'('
name|'broker'
op|','
name|'partition'
op|','
name|'nodes'
op|')'
newline|'\n'
nl|'\n'
DECL|member|reap_account
dedent|''
dedent|''
dedent|''
dedent|''
dedent|''
dedent|''
dedent|''
name|'def'
name|'reap_account'
op|'('
name|'self'
op|','
name|'broker'
op|','
name|'partition'
op|','
name|'nodes'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Called once per pass for each account this server is the primary for\n        and attempts to delete the data for the given account. The reaper will\n        only delete one account at any given time. It will call\n        :func:`reap_container` up to sqrt(self.concurrency) times concurrently\n        while reaping the account.\n\n        If there is any exception while deleting a single container, the\n        process will continue for any other containers and the failed\n        containers will be tried again the next time this function is called\n        with the same parameters.\n\n        If there is any exception while listing the containers for deletion,\n        the process will stop (but will obviously be tried again the next time\n        this function is called with the same parameters). This isn\'t likely\n        since the listing comes from the local database.\n\n        After the process completes (successfully or not) statistics about what\n        was accomplished will be logged.\n\n        This function returns nothing and should raise no exception but only\n        update various self.stats_* values for what occurs.\n\n        :param broker: The AccountBroker for the account to delete.\n        :param partition: The partition in the account ring the account is on.\n        :param nodes: The primary node dicts for the account to delete.\n\n        .. seealso::\n\n            :class:`swift.common.db.AccountBroker` for the broker class.\n\n        .. seealso::\n\n            :func:`swift.common.ring.Ring.get_nodes` for a description\n            of the node dicts.\n        """'
newline|'\n'
name|'begin'
op|'='
name|'time'
op|'('
op|')'
newline|'\n'
name|'account'
op|'='
name|'broker'
op|'.'
name|'get_info'
op|'('
op|')'
op|'['
string|"'account'"
op|']'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|"'Beginning pass on account %s'"
op|')'
op|','
name|'account'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'stats_return_codes'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'stats_containers_deleted'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'stats_objects_deleted'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'stats_containers_remaining'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'stats_objects_remaining'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'stats_containers_possibly_remaining'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'stats_objects_possibly_remaining'
op|'='
number|'0'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'marker'
op|'='
string|"''"
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'                '
name|'containers'
op|'='
name|'list'
op|'('
name|'broker'
op|'.'
name|'list_containers_iter'
op|'('
number|'1000'
op|','
name|'marker'
op|','
name|'None'
op|','
name|'None'
op|','
nl|'\n'
name|'None'
op|')'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'containers'
op|':'
newline|'\n'
indent|'                    '
name|'break'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'for'
op|'('
name|'container'
op|','
name|'_'
op|','
name|'_'
op|','
name|'_'
op|')'
name|'in'
name|'containers'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'container_pool'
op|'.'
name|'spawn'
op|'('
name|'self'
op|'.'
name|'reap_container'
op|','
name|'account'
op|','
nl|'\n'
name|'partition'
op|','
name|'nodes'
op|','
name|'container'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'container_pool'
op|'.'
name|'waitall'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Exception with containers for account %s'"
op|')'
op|','
name|'account'
op|')'
newline|'\n'
dedent|''
name|'marker'
op|'='
name|'containers'
op|'['
op|'-'
number|'1'
op|']'
op|'['
number|'0'
op|']'
newline|'\n'
dedent|''
name|'log'
op|'='
string|"'Completed pass on account %s'"
op|'%'
name|'account'
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
string|"'Exception with account %s'"
op|')'
op|','
name|'account'
op|')'
newline|'\n'
name|'log'
op|'='
string|"'Incomplete pass on account %s'"
op|'%'
name|'account'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'stats_containers_deleted'
op|':'
newline|'\n'
indent|'            '
name|'log'
op|'+='
string|"', %s containers deleted'"
op|'%'
name|'self'
op|'.'
name|'stats_containers_deleted'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'stats_objects_deleted'
op|':'
newline|'\n'
indent|'            '
name|'log'
op|'+='
string|"', %s objects deleted'"
op|'%'
name|'self'
op|'.'
name|'stats_objects_deleted'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'stats_containers_remaining'
op|':'
newline|'\n'
indent|'            '
name|'log'
op|'+='
string|"', %s containers remaining'"
op|'%'
name|'self'
op|'.'
name|'stats_containers_remaining'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'stats_objects_remaining'
op|':'
newline|'\n'
indent|'            '
name|'log'
op|'+='
string|"', %s objects remaining'"
op|'%'
name|'self'
op|'.'
name|'stats_objects_remaining'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'stats_containers_possibly_remaining'
op|':'
newline|'\n'
indent|'            '
name|'log'
op|'+='
string|"', %s containers possibly remaining'"
op|'%'
name|'self'
op|'.'
name|'stats_containers_possibly_remaining'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'stats_objects_possibly_remaining'
op|':'
newline|'\n'
indent|'            '
name|'log'
op|'+='
string|"', %s objects possibly remaining'"
op|'%'
name|'self'
op|'.'
name|'stats_objects_possibly_remaining'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'stats_return_codes'
op|':'
newline|'\n'
indent|'            '
name|'log'
op|'+='
string|"', return codes: '"
newline|'\n'
name|'for'
name|'code'
name|'in'
name|'sorted'
op|'('
name|'self'
op|'.'
name|'stats_return_codes'
op|'.'
name|'keys'
op|'('
op|')'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'log'
op|'+='
string|"'%s %sxxs, '"
op|'%'
op|'('
name|'self'
op|'.'
name|'stats_return_codes'
op|'['
name|'code'
op|']'
op|','
name|'code'
op|')'
newline|'\n'
dedent|''
name|'log'
op|'='
name|'log'
op|'['
op|':'
op|'-'
number|'2'
op|']'
newline|'\n'
dedent|''
name|'log'
op|'+='
string|"', elapsed: %.02fs'"
op|'%'
op|'('
name|'time'
op|'('
op|')'
op|'-'
name|'begin'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'log'
op|')'
newline|'\n'
nl|'\n'
DECL|member|reap_container
dedent|''
name|'def'
name|'reap_container'
op|'('
name|'self'
op|','
name|'account'
op|','
name|'account_partition'
op|','
name|'account_nodes'
op|','
nl|'\n'
name|'container'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Deletes the data and the container itself for the given container. This\n        will call :func:`reap_object` up to sqrt(self.concurrency) times\n        concurrently for the objects in the container.\n\n        If there is any exception while deleting a single object, the process\n        will continue for any other objects in the container and the failed\n        objects will be tried again the next time this function is called with\n        the same parameters.\n\n        If there is any exception while listing the objects for deletion, the\n        process will stop (but will obviously be tried again the next time this\n        function is called with the same parameters). This is a possibility\n        since the listing comes from querying just the primary remote container\n        server.\n\n        Once all objects have been attempted to be deleted, the container\n        itself will be attempted to be deleted by sending a delete request to\n        all container nodes. The format of the delete request is such that each\n        container server will update a corresponding account server, removing\n        the container from the account\'s listing.\n\n        This function returns nothing and should raise no exception but only\n        update various self.stats_* values for what occurs.\n\n        :param account: The name of the account for the container.\n        :param account_partition: The partition for the account on the account\n                                  ring.\n        :param account_nodes: The primary node dicts for the account.\n        :param container: The name of the container to delete.\n\n        * See also: :func:`swift.common.ring.Ring.get_nodes` for a description\n          of the account node dicts.\n        """'
newline|'\n'
name|'account_nodes'
op|'='
name|'list'
op|'('
name|'account_nodes'
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
name|'account'
op|','
name|'container'
op|')'
newline|'\n'
name|'node'
op|'='
name|'nodes'
op|'['
op|'-'
number|'1'
op|']'
newline|'\n'
name|'pool'
op|'='
name|'GreenPool'
op|'('
name|'size'
op|'='
name|'self'
op|'.'
name|'object_concurrency'
op|')'
newline|'\n'
name|'marker'
op|'='
string|"''"
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'objects'
op|'='
name|'None'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'objects'
op|'='
name|'direct_get_container'
op|'('
name|'node'
op|','
name|'part'
op|','
name|'account'
op|','
name|'container'
op|','
nl|'\n'
name|'marker'
op|'='
name|'marker'
op|','
name|'conn_timeout'
op|'='
name|'self'
op|'.'
name|'conn_timeout'
op|','
nl|'\n'
name|'response_timeout'
op|'='
name|'self'
op|'.'
name|'node_timeout'
op|')'
op|'['
number|'1'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'stats_return_codes'
op|'['
number|'2'
op|']'
op|'='
name|'self'
op|'.'
name|'stats_return_codes'
op|'.'
name|'get'
op|'('
number|'2'
op|','
number|'0'
op|')'
op|'+'
number|'1'
newline|'\n'
dedent|''
name|'except'
name|'ClientException'
op|','
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'getEffectiveLevel'
op|'('
op|')'
op|'<='
name|'DEBUG'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Exception with %(ip)s:%(port)s/%(device)s'"
op|')'
op|','
name|'node'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'stats_return_codes'
op|'['
name|'err'
op|'.'
name|'http_status'
op|'/'
number|'100'
op|']'
op|'='
name|'self'
op|'.'
name|'stats_return_codes'
op|'.'
name|'get'
op|'('
name|'err'
op|'.'
name|'http_status'
op|'/'
number|'100'
op|','
number|'0'
op|')'
op|'+'
number|'1'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'objects'
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'obj'
name|'in'
name|'objects'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'isinstance'
op|'('
name|'obj'
op|'['
string|"'name'"
op|']'
op|','
name|'unicode'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'obj'
op|'['
string|"'name'"
op|']'
op|'='
name|'obj'
op|'['
string|"'name'"
op|']'
op|'.'
name|'encode'
op|'('
string|"'utf8'"
op|')'
newline|'\n'
dedent|''
name|'pool'
op|'.'
name|'spawn'
op|'('
name|'self'
op|'.'
name|'reap_object'
op|','
name|'account'
op|','
name|'container'
op|','
name|'part'
op|','
nl|'\n'
name|'nodes'
op|','
name|'obj'
op|'['
string|"'name'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'pool'
op|'.'
name|'waitall'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
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
string|"'Exception with objects for container '"
nl|'\n'
string|"'%(container)s for account %(account)s'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'container'"
op|':'
name|'container'
op|','
string|"'account'"
op|':'
name|'account'
op|'}'
op|')'
newline|'\n'
dedent|''
name|'marker'
op|'='
name|'objects'
op|'['
op|'-'
number|'1'
op|']'
op|'['
string|"'name'"
op|']'
newline|'\n'
dedent|''
name|'successes'
op|'='
number|'0'
newline|'\n'
name|'failures'
op|'='
number|'0'
newline|'\n'
name|'for'
name|'node'
name|'in'
name|'nodes'
op|':'
newline|'\n'
indent|'            '
name|'anode'
op|'='
name|'account_nodes'
op|'.'
name|'pop'
op|'('
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'direct_delete_container'
op|'('
name|'node'
op|','
name|'part'
op|','
name|'account'
op|','
name|'container'
op|','
nl|'\n'
name|'conn_timeout'
op|'='
name|'self'
op|'.'
name|'conn_timeout'
op|','
nl|'\n'
name|'response_timeout'
op|'='
name|'self'
op|'.'
name|'node_timeout'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Account-Host'"
op|':'
string|"'%(ip)s:%(port)s'"
op|'%'
name|'anode'
op|','
nl|'\n'
string|"'X-Account-Partition'"
op|':'
name|'str'
op|'('
name|'account_partition'
op|')'
op|','
nl|'\n'
string|"'X-Account-Device'"
op|':'
name|'anode'
op|'['
string|"'device'"
op|']'
op|','
nl|'\n'
string|"'X-Account-Override-Deleted'"
op|':'
string|"'yes'"
op|'}'
op|')'
newline|'\n'
name|'successes'
op|'+='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'stats_return_codes'
op|'['
number|'2'
op|']'
op|'='
name|'self'
op|'.'
name|'stats_return_codes'
op|'.'
name|'get'
op|'('
number|'2'
op|','
number|'0'
op|')'
op|'+'
number|'1'
newline|'\n'
dedent|''
name|'except'
name|'ClientException'
op|','
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'getEffectiveLevel'
op|'('
op|')'
op|'<='
name|'DEBUG'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Exception with %(ip)s:%(port)s/%(device)s'"
op|')'
op|','
name|'node'
op|')'
newline|'\n'
dedent|''
name|'failures'
op|'+='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'stats_return_codes'
op|'['
name|'err'
op|'.'
name|'http_status'
op|'/'
number|'100'
op|']'
op|'='
name|'self'
op|'.'
name|'stats_return_codes'
op|'.'
name|'get'
op|'('
name|'err'
op|'.'
name|'http_status'
op|'/'
number|'100'
op|','
number|'0'
op|')'
op|'+'
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'successes'
op|'>'
name|'failures'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'stats_containers_deleted'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'elif'
name|'not'
name|'successes'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'stats_containers_remaining'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'stats_containers_possibly_remaining'
op|'+='
number|'1'
newline|'\n'
nl|'\n'
DECL|member|reap_object
dedent|''
dedent|''
name|'def'
name|'reap_object'
op|'('
name|'self'
op|','
name|'account'
op|','
name|'container'
op|','
name|'container_partition'
op|','
nl|'\n'
name|'container_nodes'
op|','
name|'obj'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Deletes the given object by issuing a delete request to each node for\n        the object. The format of the delete request is such that each object\n        server will update a corresponding container server, removing the\n        object from the container\'s listing.\n\n        This function returns nothing and should raise no exception but only\n        update various self.stats_* values for what occurs.\n\n        :param account: The name of the account for the object.\n        :param container: The name of the container for the object.\n        :param container_partition: The partition for the container on the\n                                    container ring.\n        :param container_nodes: The primary node dicts for the container.\n        :param obj: The name of the object to delete.\n\n        * See also: :func:`swift.common.ring.Ring.get_nodes` for a description\n          of the container node dicts.\n        """'
newline|'\n'
name|'container_nodes'
op|'='
name|'list'
op|'('
name|'container_nodes'
op|')'
newline|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'get_object_ring'
op|'('
op|')'
op|'.'
name|'get_nodes'
op|'('
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
name|'successes'
op|'='
number|'0'
newline|'\n'
name|'failures'
op|'='
number|'0'
newline|'\n'
name|'for'
name|'node'
name|'in'
name|'nodes'
op|':'
newline|'\n'
indent|'            '
name|'cnode'
op|'='
name|'container_nodes'
op|'.'
name|'pop'
op|'('
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'direct_delete_object'
op|'('
name|'node'
op|','
name|'part'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|','
nl|'\n'
name|'conn_timeout'
op|'='
name|'self'
op|'.'
name|'conn_timeout'
op|','
nl|'\n'
name|'response_timeout'
op|'='
name|'self'
op|'.'
name|'node_timeout'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Container-Host'"
op|':'
string|"'%(ip)s:%(port)s'"
op|'%'
name|'cnode'
op|','
nl|'\n'
string|"'X-Container-Partition'"
op|':'
name|'str'
op|'('
name|'container_partition'
op|')'
op|','
nl|'\n'
string|"'X-Container-Device'"
op|':'
name|'cnode'
op|'['
string|"'device'"
op|']'
op|'}'
op|')'
newline|'\n'
name|'successes'
op|'+='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'stats_return_codes'
op|'['
number|'2'
op|']'
op|'='
name|'self'
op|'.'
name|'stats_return_codes'
op|'.'
name|'get'
op|'('
number|'2'
op|','
number|'0'
op|')'
op|'+'
number|'1'
newline|'\n'
dedent|''
name|'except'
name|'ClientException'
op|','
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'getEffectiveLevel'
op|'('
op|')'
op|'<='
name|'DEBUG'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Exception with %(ip)s:%(port)s/%(device)s'"
op|')'
op|','
name|'node'
op|')'
newline|'\n'
dedent|''
name|'failures'
op|'+='
number|'1'
newline|'\n'
name|'self'
op|'.'
name|'stats_return_codes'
op|'['
name|'err'
op|'.'
name|'http_status'
op|'/'
number|'100'
op|']'
op|'='
name|'self'
op|'.'
name|'stats_return_codes'
op|'.'
name|'get'
op|'('
name|'err'
op|'.'
name|'http_status'
op|'/'
number|'100'
op|','
number|'0'
op|')'
op|'+'
number|'1'
newline|'\n'
dedent|''
name|'if'
name|'successes'
op|'>'
name|'failures'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'stats_objects_deleted'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'elif'
name|'not'
name|'successes'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'stats_objects_remaining'
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
name|'stats_objects_possibly_remaining'
op|'+='
number|'1'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
endmarker|''
end_unit
