begin_unit
comment|'# Copyright (c) 2013 OpenStack Foundation'
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
name|'urllib'
newline|'\n'
name|'from'
name|'itertools'
name|'import'
name|'ifilter'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'bufferedhttp'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'exceptions'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'http'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|Sender
name|'class'
name|'Sender'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Sends SSYNC requests to the object server.\n\n    These requests are eventually handled by\n    :py:mod:`.ssync_receiver` and full documentation about the\n    process is there.\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'daemon'
op|','
name|'node'
op|','
name|'job'
op|','
name|'suffixes'
op|','
name|'remote_check_objs'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'daemon'
op|'='
name|'daemon'
newline|'\n'
name|'self'
op|'.'
name|'df_mgr'
op|'='
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'_diskfile_mgr'
newline|'\n'
name|'self'
op|'.'
name|'node'
op|'='
name|'node'
newline|'\n'
name|'self'
op|'.'
name|'job'
op|'='
name|'job'
newline|'\n'
name|'self'
op|'.'
name|'suffixes'
op|'='
name|'suffixes'
newline|'\n'
name|'self'
op|'.'
name|'connection'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'response'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'response_buffer'
op|'='
string|"''"
newline|'\n'
name|'self'
op|'.'
name|'response_chunk_left'
op|'='
number|'0'
newline|'\n'
comment|'# available_map has an entry for each object in given suffixes that'
nl|'\n'
comment|"# is available to be sync'd; each entry is a hash => timestamp"
nl|'\n'
name|'self'
op|'.'
name|'available_map'
op|'='
op|'{'
op|'}'
newline|'\n'
comment|'# When remote_check_objs is given in job, ssync_sender trys only to'
nl|'\n'
comment|'# make sure those objects exist or not in remote.'
nl|'\n'
name|'self'
op|'.'
name|'remote_check_objs'
op|'='
name|'remote_check_objs'
newline|'\n'
comment|'# send_list has an entry for each object that the receiver wants to'
nl|'\n'
comment|"# be sync'ed; each entry is an object hash"
nl|'\n'
name|'self'
op|'.'
name|'send_list'
op|'='
op|'['
op|']'
newline|'\n'
name|'self'
op|'.'
name|'failures'
op|'='
number|'0'
newline|'\n'
nl|'\n'
DECL|member|__call__
dedent|''
name|'def'
name|'__call__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Perform ssync with remote node.\n\n        :returns: a 2-tuple, in the form (success, can_delete_objs) where\n                  success is a boolean and can_delete_objs is the map of\n                  objects that are in sync with the receiver. Each entry in\n                  can_delete_objs maps a hash => timestamp\n        """'
newline|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'suffixes'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'True'
op|','
op|'{'
op|'}'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
comment|'# Double try blocks in case our main error handler fails.'
nl|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
comment|'# The general theme for these functions is that they should'
nl|'\n'
comment|'# raise exceptions.MessageTimeout for client timeouts and'
nl|'\n'
comment|'# exceptions.ReplicationException for common issues that will'
nl|'\n'
comment|'# abort the replication attempt and log a simple error. All'
nl|'\n'
comment|'# other exceptions will be logged with a full stack trace.'
nl|'\n'
indent|'                '
name|'self'
op|'.'
name|'connect'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'missing_check'
op|'('
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'remote_check_objs'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'updates'
op|'('
op|')'
newline|'\n'
name|'can_delete_obj'
op|'='
name|'self'
op|'.'
name|'available_map'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
comment|"# when we are initialized with remote_check_objs we don't"
nl|'\n'
comment|'# *send* any requested updates; instead we only collect'
nl|'\n'
comment|"# what's already in sync and safe for deletion"
nl|'\n'
indent|'                    '
name|'in_sync_hashes'
op|'='
op|'('
name|'set'
op|'('
name|'self'
op|'.'
name|'available_map'
op|'.'
name|'keys'
op|'('
op|')'
op|')'
op|'-'
nl|'\n'
name|'set'
op|'('
name|'self'
op|'.'
name|'send_list'
op|')'
op|')'
newline|'\n'
name|'can_delete_obj'
op|'='
name|'dict'
op|'('
op|'('
name|'hash_'
op|','
name|'self'
op|'.'
name|'available_map'
op|'['
name|'hash_'
op|']'
op|')'
nl|'\n'
name|'for'
name|'hash_'
name|'in'
name|'in_sync_hashes'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'disconnect'
op|'('
op|')'
newline|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'failures'
op|':'
newline|'\n'
indent|'                    '
name|'return'
name|'True'
op|','
name|'can_delete_obj'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'return'
name|'False'
op|','
op|'{'
op|'}'
newline|'\n'
dedent|''
dedent|''
name|'except'
op|'('
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|','
nl|'\n'
name|'exceptions'
op|'.'
name|'ReplicationException'
op|')'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
nl|'\n'
string|"'%s:%s/%s/%s %s'"
op|','
name|'self'
op|'.'
name|'node'
op|'.'
name|'get'
op|'('
string|"'replication_ip'"
op|')'
op|','
nl|'\n'
name|'self'
op|'.'
name|'node'
op|'.'
name|'get'
op|'('
string|"'replication_port'"
op|')'
op|','
name|'self'
op|'.'
name|'node'
op|'.'
name|'get'
op|'('
string|"'device'"
op|')'
op|','
nl|'\n'
name|'self'
op|'.'
name|'job'
op|'.'
name|'get'
op|'('
string|"'partition'"
op|')'
op|','
name|'err'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
comment|"# We don't want any exceptions to escape our code and possibly"
nl|'\n'
comment|'# mess up the original replicator code that called us since it'
nl|'\n'
comment|'# was originally written to shell out to rsync which would do'
nl|'\n'
comment|'# no such thing.'
nl|'\n'
indent|'                '
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
nl|'\n'
string|"'%s:%s/%s/%s EXCEPTION in replication.Sender'"
op|','
nl|'\n'
name|'self'
op|'.'
name|'node'
op|'.'
name|'get'
op|'('
string|"'replication_ip'"
op|')'
op|','
nl|'\n'
name|'self'
op|'.'
name|'node'
op|'.'
name|'get'
op|'('
string|"'replication_port'"
op|')'
op|','
nl|'\n'
name|'self'
op|'.'
name|'node'
op|'.'
name|'get'
op|'('
string|"'device'"
op|')'
op|','
name|'self'
op|'.'
name|'job'
op|'.'
name|'get'
op|'('
string|"'partition'"
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
comment|"# We don't want any exceptions to escape our code and possibly"
nl|'\n'
comment|'# mess up the original replicator code that called us since it'
nl|'\n'
comment|'# was originally written to shell out to rsync which would do'
nl|'\n'
comment|'# no such thing.'
nl|'\n'
comment|'# This particular exception handler does the minimal amount as it'
nl|'\n'
comment|'# would only get called if the above except Exception handler'
nl|'\n'
comment|'# failed (bad node or job data).'
nl|'\n'
indent|'            '
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
string|"'EXCEPTION in replication.Sender'"
op|')'
newline|'\n'
dedent|''
name|'return'
name|'False'
op|','
op|'{'
op|'}'
newline|'\n'
nl|'\n'
DECL|member|connect
dedent|''
name|'def'
name|'connect'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Establishes a connection and starts an SSYNC request\n        with the object server.\n        """'
newline|'\n'
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'conn_timeout'
op|','
string|"'connect send'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'connection'
op|'='
name|'bufferedhttp'
op|'.'
name|'BufferedHTTPConnection'
op|'('
nl|'\n'
string|"'%s:%s'"
op|'%'
op|'('
name|'self'
op|'.'
name|'node'
op|'['
string|"'replication_ip'"
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'node'
op|'['
string|"'replication_port'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'connection'
op|'.'
name|'putrequest'
op|'('
string|"'SSYNC'"
op|','
string|"'/%s/%s'"
op|'%'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'node'
op|'['
string|"'device'"
op|']'
op|','
name|'self'
op|'.'
name|'job'
op|'['
string|"'partition'"
op|']'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'connection'
op|'.'
name|'putheader'
op|'('
string|"'Transfer-Encoding'"
op|','
string|"'chunked'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'connection'
op|'.'
name|'putheader'
op|'('
string|"'X-Backend-Storage-Policy-Index'"
op|','
nl|'\n'
name|'int'
op|'('
name|'self'
op|'.'
name|'job'
op|'['
string|"'policy'"
op|']'
op|')'
op|')'
newline|'\n'
comment|"# a sync job must use the node's index for the frag_index of the"
nl|'\n'
comment|'# rebuilt fragments instead of the frag_index from the job which'
nl|'\n'
comment|'# will be rebuilding them'
nl|'\n'
name|'self'
op|'.'
name|'connection'
op|'.'
name|'putheader'
op|'('
nl|'\n'
string|"'X-Backend-Ssync-Frag-Index'"
op|','
name|'self'
op|'.'
name|'node'
op|'.'
name|'get'
op|'('
nl|'\n'
string|"'index'"
op|','
name|'self'
op|'.'
name|'job'
op|'.'
name|'get'
op|'('
string|"'frag_index'"
op|')'
op|')'
op|')'
newline|'\n'
comment|'# a revert job to a handoff will not have a node index'
nl|'\n'
name|'self'
op|'.'
name|'connection'
op|'.'
name|'putheader'
op|'('
string|"'X-Backend-Ssync-Node-Index'"
op|','
nl|'\n'
name|'self'
op|'.'
name|'node'
op|'.'
name|'get'
op|'('
string|"'index'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'connection'
op|'.'
name|'endheaders'
op|'('
op|')'
newline|'\n'
dedent|''
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'node_timeout'
op|','
string|"'connect receive'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'response'
op|'='
name|'self'
op|'.'
name|'connection'
op|'.'
name|'getresponse'
op|'('
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'response'
op|'.'
name|'status'
op|'!='
name|'http'
op|'.'
name|'HTTP_OK'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'exceptions'
op|'.'
name|'ReplicationException'
op|'('
nl|'\n'
string|"'Expected status %s; got %s'"
op|'%'
nl|'\n'
op|'('
name|'http'
op|'.'
name|'HTTP_OK'
op|','
name|'self'
op|'.'
name|'response'
op|'.'
name|'status'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|readline
dedent|''
dedent|''
dedent|''
name|'def'
name|'readline'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Reads a line from the SSYNC response body.\n\n        httplib has no readline and will block on read(x) until x is\n        read, so we have to do the work ourselves. A bit of this is\n        taken from Python\'s httplib itself.\n        """'
newline|'\n'
name|'data'
op|'='
name|'self'
op|'.'
name|'response_buffer'
newline|'\n'
name|'self'
op|'.'
name|'response_buffer'
op|'='
string|"''"
newline|'\n'
name|'while'
string|"'\\n'"
name|'not'
name|'in'
name|'data'
name|'and'
name|'len'
op|'('
name|'data'
op|')'
op|'<'
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'network_chunk_size'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'self'
op|'.'
name|'response_chunk_left'
op|'=='
op|'-'
number|'1'
op|':'
comment|'# EOF-already indicator'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'response_chunk_left'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'                '
name|'line'
op|'='
name|'self'
op|'.'
name|'response'
op|'.'
name|'fp'
op|'.'
name|'readline'
op|'('
op|')'
newline|'\n'
name|'i'
op|'='
name|'line'
op|'.'
name|'find'
op|'('
string|"';'"
op|')'
newline|'\n'
name|'if'
name|'i'
op|'>='
number|'0'
op|':'
newline|'\n'
indent|'                    '
name|'line'
op|'='
name|'line'
op|'['
op|':'
name|'i'
op|']'
comment|'# strip chunk-extensions'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'response_chunk_left'
op|'='
name|'int'
op|'('
name|'line'
op|'.'
name|'strip'
op|'('
op|')'
op|','
number|'16'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
comment|'# close the connection as protocol synchronisation is'
nl|'\n'
comment|'# probably lost'
nl|'\n'
indent|'                    '
name|'self'
op|'.'
name|'response'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
name|'raise'
name|'exceptions'
op|'.'
name|'ReplicationException'
op|'('
string|"'Early disconnect'"
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'response_chunk_left'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'response_chunk_left'
op|'='
op|'-'
number|'1'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'chunk'
op|'='
name|'self'
op|'.'
name|'response'
op|'.'
name|'fp'
op|'.'
name|'read'
op|'('
name|'min'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'response_chunk_left'
op|','
nl|'\n'
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'network_chunk_size'
op|'-'
name|'len'
op|'('
name|'data'
op|')'
op|')'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'chunk'
op|':'
newline|'\n'
comment|'# close the connection as protocol synchronisation is'
nl|'\n'
comment|'# probably lost'
nl|'\n'
indent|'                '
name|'self'
op|'.'
name|'response'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
name|'raise'
name|'exceptions'
op|'.'
name|'ReplicationException'
op|'('
string|"'Early disconnect'"
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'response_chunk_left'
op|'-='
name|'len'
op|'('
name|'chunk'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'response_chunk_left'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'response'
op|'.'
name|'fp'
op|'.'
name|'read'
op|'('
number|'2'
op|')'
comment|'# discard the trailing \\r\\n'
newline|'\n'
dedent|''
name|'data'
op|'+='
name|'chunk'
newline|'\n'
dedent|''
name|'if'
string|"'\\n'"
name|'in'
name|'data'
op|':'
newline|'\n'
indent|'            '
name|'data'
op|','
name|'self'
op|'.'
name|'response_buffer'
op|'='
name|'data'
op|'.'
name|'split'
op|'('
string|"'\\n'"
op|','
number|'1'
op|')'
newline|'\n'
name|'data'
op|'+='
string|"'\\n'"
newline|'\n'
dedent|''
name|'return'
name|'data'
newline|'\n'
nl|'\n'
DECL|member|missing_check
dedent|''
name|'def'
name|'missing_check'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Handles the sender-side of the MISSING_CHECK step of a\n        SSYNC request.\n\n        Full documentation of this can be found at\n        :py:meth:`.Receiver.missing_check`.\n        """'
newline|'\n'
comment|'# First, send our list.'
nl|'\n'
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'node_timeout'
op|','
string|"'missing_check start'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'msg'
op|'='
string|"':MISSING_CHECK: START\\r\\n'"
newline|'\n'
name|'self'
op|'.'
name|'connection'
op|'.'
name|'send'
op|'('
string|"'%x\\r\\n%s\\r\\n'"
op|'%'
op|'('
name|'len'
op|'('
name|'msg'
op|')'
op|','
name|'msg'
op|')'
op|')'
newline|'\n'
dedent|''
name|'hash_gen'
op|'='
name|'self'
op|'.'
name|'df_mgr'
op|'.'
name|'yield_hashes'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'job'
op|'['
string|"'device'"
op|']'
op|','
name|'self'
op|'.'
name|'job'
op|'['
string|"'partition'"
op|']'
op|','
nl|'\n'
name|'self'
op|'.'
name|'job'
op|'['
string|"'policy'"
op|']'
op|','
name|'self'
op|'.'
name|'suffixes'
op|','
nl|'\n'
name|'frag_index'
op|'='
name|'self'
op|'.'
name|'job'
op|'.'
name|'get'
op|'('
string|"'frag_index'"
op|')'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'remote_check_objs'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'hash_gen'
op|'='
name|'ifilter'
op|'('
name|'lambda'
op|'('
name|'path'
op|','
name|'object_hash'
op|','
name|'timestamp'
op|')'
op|':'
nl|'\n'
name|'object_hash'
name|'in'
name|'self'
op|'.'
name|'remote_check_objs'
op|','
name|'hash_gen'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'path'
op|','
name|'object_hash'
op|','
name|'timestamp'
name|'in'
name|'hash_gen'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'available_map'
op|'['
name|'object_hash'
op|']'
op|'='
name|'timestamp'
newline|'\n'
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'node_timeout'
op|','
nl|'\n'
string|"'missing_check send line'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'msg'
op|'='
string|"'%s %s\\r\\n'"
op|'%'
op|'('
nl|'\n'
name|'urllib'
op|'.'
name|'quote'
op|'('
name|'object_hash'
op|')'
op|','
nl|'\n'
name|'urllib'
op|'.'
name|'quote'
op|'('
name|'timestamp'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'connection'
op|'.'
name|'send'
op|'('
string|"'%x\\r\\n%s\\r\\n'"
op|'%'
op|'('
name|'len'
op|'('
name|'msg'
op|')'
op|','
name|'msg'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'node_timeout'
op|','
string|"'missing_check end'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'msg'
op|'='
string|"':MISSING_CHECK: END\\r\\n'"
newline|'\n'
name|'self'
op|'.'
name|'connection'
op|'.'
name|'send'
op|'('
string|"'%x\\r\\n%s\\r\\n'"
op|'%'
op|'('
name|'len'
op|'('
name|'msg'
op|')'
op|','
name|'msg'
op|')'
op|')'
newline|'\n'
comment|'# Now, retrieve the list of what they want.'
nl|'\n'
dedent|''
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'http_timeout'
op|','
string|"'missing_check start wait'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'line'
op|'='
name|'self'
op|'.'
name|'readline'
op|'('
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'line'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'exceptions'
op|'.'
name|'ReplicationException'
op|'('
string|"'Early disconnect'"
op|')'
newline|'\n'
dedent|''
name|'line'
op|'='
name|'line'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
name|'if'
name|'line'
op|'=='
string|"':MISSING_CHECK: START'"
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
name|'elif'
name|'line'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'exceptions'
op|'.'
name|'ReplicationException'
op|'('
nl|'\n'
string|"'Unexpected response: %r'"
op|'%'
name|'line'
op|'['
op|':'
number|'1024'
op|']'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'http_timeout'
op|','
string|"'missing_check line wait'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'line'
op|'='
name|'self'
op|'.'
name|'readline'
op|'('
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'line'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'exceptions'
op|'.'
name|'ReplicationException'
op|'('
string|"'Early disconnect'"
op|')'
newline|'\n'
dedent|''
name|'line'
op|'='
name|'line'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
name|'if'
name|'line'
op|'=='
string|"':MISSING_CHECK: END'"
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
name|'parts'
op|'='
name|'line'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'if'
name|'parts'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'send_list'
op|'.'
name|'append'
op|'('
name|'parts'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|updates
dedent|''
dedent|''
dedent|''
name|'def'
name|'updates'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Handles the sender-side of the UPDATES step of an SSYNC\n        request.\n\n        Full documentation of this can be found at\n        :py:meth:`.Receiver.updates`.\n        """'
newline|'\n'
comment|'# First, send all our subrequests based on the send_list.'
nl|'\n'
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'node_timeout'
op|','
string|"'updates start'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'msg'
op|'='
string|"':UPDATES: START\\r\\n'"
newline|'\n'
name|'self'
op|'.'
name|'connection'
op|'.'
name|'send'
op|'('
string|"'%x\\r\\n%s\\r\\n'"
op|'%'
op|'('
name|'len'
op|'('
name|'msg'
op|')'
op|','
name|'msg'
op|')'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'object_hash'
name|'in'
name|'self'
op|'.'
name|'send_list'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'df'
op|'='
name|'self'
op|'.'
name|'df_mgr'
op|'.'
name|'get_diskfile_from_hash'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'job'
op|'['
string|"'device'"
op|']'
op|','
name|'self'
op|'.'
name|'job'
op|'['
string|"'partition'"
op|']'
op|','
name|'object_hash'
op|','
nl|'\n'
name|'self'
op|'.'
name|'job'
op|'['
string|"'policy'"
op|']'
op|','
name|'frag_index'
op|'='
name|'self'
op|'.'
name|'job'
op|'.'
name|'get'
op|'('
string|"'frag_index'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'exceptions'
op|'.'
name|'DiskFileNotExist'
op|':'
newline|'\n'
indent|'                '
name|'continue'
newline|'\n'
dedent|''
name|'url_path'
op|'='
name|'urllib'
op|'.'
name|'quote'
op|'('
nl|'\n'
string|"'/%s/%s/%s'"
op|'%'
op|'('
name|'df'
op|'.'
name|'account'
op|','
name|'df'
op|'.'
name|'container'
op|','
name|'df'
op|'.'
name|'obj'
op|')'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'df'
op|'.'
name|'open'
op|'('
op|')'
newline|'\n'
comment|'# EC reconstructor may have passed a callback to build'
nl|'\n'
comment|'# an alternative diskfile...'
nl|'\n'
name|'df'
op|'='
name|'self'
op|'.'
name|'job'
op|'.'
name|'get'
op|'('
string|"'sync_diskfile_builder'"
op|','
name|'lambda'
op|'*'
name|'args'
op|':'
name|'df'
op|')'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'job'
op|','
name|'self'
op|'.'
name|'node'
op|','
name|'df'
op|'.'
name|'get_metadata'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'exceptions'
op|'.'
name|'DiskFileDeleted'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'send_delete'
op|'('
name|'url_path'
op|','
name|'err'
op|'.'
name|'timestamp'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'exceptions'
op|'.'
name|'DiskFileError'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'send_put'
op|'('
name|'url_path'
op|','
name|'df'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'node_timeout'
op|','
string|"'updates end'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'msg'
op|'='
string|"':UPDATES: END\\r\\n'"
newline|'\n'
name|'self'
op|'.'
name|'connection'
op|'.'
name|'send'
op|'('
string|"'%x\\r\\n%s\\r\\n'"
op|'%'
op|'('
name|'len'
op|'('
name|'msg'
op|')'
op|','
name|'msg'
op|')'
op|')'
newline|'\n'
comment|'# Now, read their response for any issues.'
nl|'\n'
dedent|''
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'http_timeout'
op|','
string|"'updates start wait'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'line'
op|'='
name|'self'
op|'.'
name|'readline'
op|'('
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'line'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'exceptions'
op|'.'
name|'ReplicationException'
op|'('
string|"'Early disconnect'"
op|')'
newline|'\n'
dedent|''
name|'line'
op|'='
name|'line'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
name|'if'
name|'line'
op|'=='
string|"':UPDATES: START'"
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
name|'elif'
name|'line'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'exceptions'
op|'.'
name|'ReplicationException'
op|'('
nl|'\n'
string|"'Unexpected response: %r'"
op|'%'
name|'line'
op|'['
op|':'
number|'1024'
op|']'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'http_timeout'
op|','
string|"'updates line wait'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'line'
op|'='
name|'self'
op|'.'
name|'readline'
op|'('
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'line'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'exceptions'
op|'.'
name|'ReplicationException'
op|'('
string|"'Early disconnect'"
op|')'
newline|'\n'
dedent|''
name|'line'
op|'='
name|'line'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
name|'if'
name|'line'
op|'=='
string|"':UPDATES: END'"
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
name|'elif'
name|'line'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'exceptions'
op|'.'
name|'ReplicationException'
op|'('
nl|'\n'
string|"'Unexpected response: %r'"
op|'%'
name|'line'
op|'['
op|':'
number|'1024'
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|send_delete
dedent|''
dedent|''
dedent|''
name|'def'
name|'send_delete'
op|'('
name|'self'
op|','
name|'url_path'
op|','
name|'timestamp'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Sends a DELETE subrequest with the given information.\n        """'
newline|'\n'
name|'msg'
op|'='
op|'['
string|"'DELETE '"
op|'+'
name|'url_path'
op|','
string|"'X-Timestamp: '"
op|'+'
name|'timestamp'
op|'.'
name|'internal'
op|']'
newline|'\n'
name|'msg'
op|'='
string|"'\\r\\n'"
op|'.'
name|'join'
op|'('
name|'msg'
op|')'
op|'+'
string|"'\\r\\n\\r\\n'"
newline|'\n'
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'node_timeout'
op|','
string|"'send_delete'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'connection'
op|'.'
name|'send'
op|'('
string|"'%x\\r\\n%s\\r\\n'"
op|'%'
op|'('
name|'len'
op|'('
name|'msg'
op|')'
op|','
name|'msg'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|send_put
dedent|''
dedent|''
name|'def'
name|'send_put'
op|'('
name|'self'
op|','
name|'url_path'
op|','
name|'df'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Sends a PUT subrequest for the url_path using the source df\n        (DiskFile) and content_length.\n        """'
newline|'\n'
name|'msg'
op|'='
op|'['
string|"'PUT '"
op|'+'
name|'url_path'
op|','
string|"'Content-Length: '"
op|'+'
name|'str'
op|'('
name|'df'
op|'.'
name|'content_length'
op|')'
op|']'
newline|'\n'
comment|'# Sorted to make it easier to test.'
nl|'\n'
name|'for'
name|'key'
op|','
name|'value'
name|'in'
name|'sorted'
op|'('
name|'df'
op|'.'
name|'get_metadata'
op|'('
op|')'
op|'.'
name|'items'
op|'('
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'key'
name|'not'
name|'in'
op|'('
string|"'name'"
op|','
string|"'Content-Length'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'msg'
op|'.'
name|'append'
op|'('
string|"'%s: %s'"
op|'%'
op|'('
name|'key'
op|','
name|'value'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'msg'
op|'='
string|"'\\r\\n'"
op|'.'
name|'join'
op|'('
name|'msg'
op|')'
op|'+'
string|"'\\r\\n\\r\\n'"
newline|'\n'
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'node_timeout'
op|','
string|"'send_put'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'connection'
op|'.'
name|'send'
op|'('
string|"'%x\\r\\n%s\\r\\n'"
op|'%'
op|'('
name|'len'
op|'('
name|'msg'
op|')'
op|','
name|'msg'
op|')'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'chunk'
name|'in'
name|'df'
op|'.'
name|'reader'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'node_timeout'
op|','
string|"'send_put chunk'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'connection'
op|'.'
name|'send'
op|'('
string|"'%x\\r\\n%s\\r\\n'"
op|'%'
op|'('
name|'len'
op|'('
name|'chunk'
op|')'
op|','
name|'chunk'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|disconnect
dedent|''
dedent|''
dedent|''
name|'def'
name|'disconnect'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Closes down the connection to the object server once done\n        with the SSYNC request.\n        """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'exceptions'
op|'.'
name|'MessageTimeout'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'daemon'
op|'.'
name|'node_timeout'
op|','
string|"'disconnect'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'connection'
op|'.'
name|'send'
op|'('
string|"'0\\r\\n\\r\\n'"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'exceptions'
op|'.'
name|'Timeout'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'pass'
comment|"# We're okay with the above failing."
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'connection'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
