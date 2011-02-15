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
name|'from'
name|'ConfigParser'
name|'import'
name|'ConfigParser'
newline|'\n'
name|'import'
name|'zlib'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'datetime'
newline|'\n'
name|'import'
name|'cStringIO'
newline|'\n'
name|'import'
name|'collections'
newline|'\n'
name|'from'
name|'paste'
op|'.'
name|'deploy'
name|'import'
name|'appconfig'
newline|'\n'
name|'import'
name|'multiprocessing'
newline|'\n'
name|'import'
name|'Queue'
newline|'\n'
name|'import'
name|'cPickle'
newline|'\n'
name|'import'
name|'hashlib'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'internal_proxy'
name|'import'
name|'InternalProxy'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'exceptions'
name|'import'
name|'ChunkReadTimeout'
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
name|'readconf'
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
DECL|class|BadFileDownload
name|'class'
name|'BadFileDownload'
op|'('
name|'Exception'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|LogProcessor
dedent|''
name|'class'
name|'LogProcessor'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Load plugins, process logs"""'
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
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'isinstance'
op|'('
name|'logger'
op|','
name|'tuple'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'='
name|'get_logger'
op|'('
op|'*'
name|'logger'
op|','
name|'log_route'
op|'='
string|"'log-processor'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'='
name|'logger'
newline|'\n'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'conf'
op|'='
name|'conf'
newline|'\n'
name|'self'
op|'.'
name|'_internal_proxy'
op|'='
name|'None'
newline|'\n'
nl|'\n'
comment|'# load the processing plugins'
nl|'\n'
name|'self'
op|'.'
name|'plugins'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'plugin_prefix'
op|'='
string|"'log-processor-'"
newline|'\n'
name|'for'
name|'section'
name|'in'
op|'('
name|'x'
name|'for'
name|'x'
name|'in'
name|'conf'
name|'if'
name|'x'
op|'.'
name|'startswith'
op|'('
name|'plugin_prefix'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'plugin_name'
op|'='
name|'section'
op|'['
name|'len'
op|'('
name|'plugin_prefix'
op|')'
op|':'
op|']'
newline|'\n'
name|'plugin_conf'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
name|'section'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'plugins'
op|'['
name|'plugin_name'
op|']'
op|'='
name|'plugin_conf'
newline|'\n'
name|'class_path'
op|'='
name|'self'
op|'.'
name|'plugins'
op|'['
name|'plugin_name'
op|']'
op|'['
string|"'class_path'"
op|']'
newline|'\n'
name|'import_target'
op|','
name|'class_name'
op|'='
name|'class_path'
op|'.'
name|'rsplit'
op|'('
string|"'.'"
op|','
number|'1'
op|')'
newline|'\n'
name|'module'
op|'='
name|'__import__'
op|'('
name|'import_target'
op|','
name|'fromlist'
op|'='
op|'['
name|'import_target'
op|']'
op|')'
newline|'\n'
name|'klass'
op|'='
name|'getattr'
op|'('
name|'module'
op|','
name|'class_name'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'plugins'
op|'['
name|'plugin_name'
op|']'
op|'['
string|"'instance'"
op|']'
op|'='
name|'klass'
op|'('
name|'plugin_conf'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|'\'Loaded plugin "%s"\''
op|')'
op|'%'
name|'plugin_name'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
op|'@'
name|'property'
newline|'\n'
DECL|member|internal_proxy
name|'def'
name|'internal_proxy'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'self'
op|'.'
name|'_internal_proxy'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'stats_conf'
op|'='
name|'self'
op|'.'
name|'conf'
op|'.'
name|'get'
op|'('
string|"'log-processor'"
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'proxy_server_conf_loc'
op|'='
name|'stats_conf'
op|'.'
name|'get'
op|'('
string|"'proxy_server_conf'"
op|','
nl|'\n'
string|"'/etc/swift/proxy-server.conf'"
op|')'
newline|'\n'
name|'proxy_server_conf'
op|'='
name|'appconfig'
op|'('
nl|'\n'
string|"'config:%s'"
op|'%'
name|'proxy_server_conf_loc'
op|','
nl|'\n'
name|'name'
op|'='
string|"'proxy-server'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_internal_proxy'
op|'='
name|'InternalProxy'
op|'('
name|'proxy_server_conf'
op|','
nl|'\n'
name|'self'
op|'.'
name|'logger'
op|','
nl|'\n'
name|'retries'
op|'='
number|'3'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'_internal_proxy'
newline|'\n'
nl|'\n'
DECL|member|process_one_file
dedent|''
name|'def'
name|'process_one_file'
op|'('
name|'self'
op|','
name|'plugin_name'
op|','
name|'account'
op|','
name|'container'
op|','
name|'object_name'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|'\'Processing %(obj)s with plugin "%(plugin)s"\''
op|')'
op|'%'
nl|'\n'
op|'{'
string|"'obj'"
op|':'
string|"'/'"
op|'.'
name|'join'
op|'('
op|'('
name|'account'
op|','
name|'container'
op|','
name|'object_name'
op|')'
op|')'
op|','
nl|'\n'
string|"'plugin'"
op|':'
name|'plugin_name'
op|'}'
op|')'
newline|'\n'
comment|'# get an iter of the object data'
nl|'\n'
name|'compressed'
op|'='
name|'object_name'
op|'.'
name|'endswith'
op|'('
string|"'.gz'"
op|')'
newline|'\n'
name|'stream'
op|'='
name|'self'
op|'.'
name|'get_object_data'
op|'('
name|'account'
op|','
name|'container'
op|','
name|'object_name'
op|','
nl|'\n'
name|'compressed'
op|'='
name|'compressed'
op|')'
newline|'\n'
comment|'# look up the correct plugin and send the stream to it'
nl|'\n'
name|'return'
name|'self'
op|'.'
name|'plugins'
op|'['
name|'plugin_name'
op|']'
op|'['
string|"'instance'"
op|']'
op|'.'
name|'process'
op|'('
name|'stream'
op|','
nl|'\n'
name|'account'
op|','
nl|'\n'
name|'container'
op|','
nl|'\n'
name|'object_name'
op|')'
newline|'\n'
nl|'\n'
DECL|member|get_data_list
dedent|''
name|'def'
name|'get_data_list'
op|'('
name|'self'
op|','
name|'start_date'
op|'='
name|'None'
op|','
name|'end_date'
op|'='
name|'None'
op|','
nl|'\n'
name|'listing_filter'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'total_list'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'plugin_name'
op|','
name|'data'
name|'in'
name|'self'
op|'.'
name|'plugins'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'account'
op|'='
name|'data'
op|'['
string|"'swift_account'"
op|']'
newline|'\n'
name|'container'
op|'='
name|'data'
op|'['
string|"'container_name'"
op|']'
newline|'\n'
name|'listing'
op|'='
name|'self'
op|'.'
name|'get_container_listing'
op|'('
name|'account'
op|','
nl|'\n'
name|'container'
op|','
nl|'\n'
name|'start_date'
op|','
nl|'\n'
name|'end_date'
op|')'
newline|'\n'
name|'for'
name|'object_name'
name|'in'
name|'listing'
op|':'
newline|'\n'
comment|'# The items in this list end up being passed as positional'
nl|'\n'
comment|'# parameters to process_one_file.'
nl|'\n'
indent|'                '
name|'x'
op|'='
op|'('
name|'plugin_name'
op|','
name|'account'
op|','
name|'container'
op|','
name|'object_name'
op|')'
newline|'\n'
name|'if'
name|'x'
name|'not'
name|'in'
name|'listing_filter'
op|':'
newline|'\n'
indent|'                    '
name|'total_list'
op|'.'
name|'append'
op|'('
name|'x'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'return'
name|'total_list'
newline|'\n'
nl|'\n'
DECL|member|get_container_listing
dedent|''
name|'def'
name|'get_container_listing'
op|'('
name|'self'
op|','
name|'swift_account'
op|','
name|'container_name'
op|','
nl|'\n'
name|'start_date'
op|'='
name|'None'
op|','
name|'end_date'
op|'='
name|'None'
op|','
nl|'\n'
name|'listing_filter'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''\n        Get a container listing, filtered by start_date, end_date, and\n        listing_filter. Dates, if given, must be in YYYYMMDDHH format\n        '''"
newline|'\n'
name|'search_key'
op|'='
name|'None'
newline|'\n'
name|'if'
name|'start_date'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'parsed_date'
op|'='
name|'time'
op|'.'
name|'strptime'
op|'('
name|'start_date'
op|','
string|"'%Y%m%d%H'"
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
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
name|'year'
op|'='
string|"'%04d'"
op|'%'
name|'parsed_date'
op|'.'
name|'tm_year'
newline|'\n'
name|'month'
op|'='
string|"'%02d'"
op|'%'
name|'parsed_date'
op|'.'
name|'tm_mon'
newline|'\n'
name|'day'
op|'='
string|"'%02d'"
op|'%'
name|'parsed_date'
op|'.'
name|'tm_mday'
newline|'\n'
name|'hour'
op|'='
string|"'%02d'"
op|'%'
name|'parsed_date'
op|'.'
name|'tm_hour'
newline|'\n'
name|'search_key'
op|'='
string|"'/'"
op|'.'
name|'join'
op|'('
op|'['
name|'year'
op|','
name|'month'
op|','
name|'day'
op|','
name|'hour'
op|']'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'end_key'
op|'='
name|'None'
newline|'\n'
name|'if'
name|'end_date'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'parsed_date'
op|'='
name|'time'
op|'.'
name|'strptime'
op|'('
name|'end_date'
op|','
string|"'%Y%m%d%H'"
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
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
name|'year'
op|'='
string|"'%04d'"
op|'%'
name|'parsed_date'
op|'.'
name|'tm_year'
newline|'\n'
name|'month'
op|'='
string|"'%02d'"
op|'%'
name|'parsed_date'
op|'.'
name|'tm_mon'
newline|'\n'
name|'day'
op|'='
string|"'%02d'"
op|'%'
name|'parsed_date'
op|'.'
name|'tm_mday'
newline|'\n'
comment|'# Since the end_marker filters by <, we need to add something'
nl|'\n'
comment|'# to make sure we get all the data under the last hour. Adding'
nl|'\n'
comment|'# one to the hour should be all-inclusive.'
nl|'\n'
name|'hour'
op|'='
string|"'%02d'"
op|'%'
op|'('
name|'parsed_date'
op|'.'
name|'tm_hour'
op|'+'
number|'1'
op|')'
newline|'\n'
name|'end_key'
op|'='
string|"'/'"
op|'.'
name|'join'
op|'('
op|'['
name|'year'
op|','
name|'month'
op|','
name|'day'
op|','
name|'hour'
op|']'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'container_listing'
op|'='
name|'self'
op|'.'
name|'internal_proxy'
op|'.'
name|'get_container_list'
op|'('
nl|'\n'
name|'swift_account'
op|','
nl|'\n'
name|'container_name'
op|','
nl|'\n'
name|'marker'
op|'='
name|'search_key'
op|','
nl|'\n'
name|'end_marker'
op|'='
name|'end_key'
op|')'
newline|'\n'
name|'results'
op|'='
op|'['
op|']'
newline|'\n'
name|'if'
name|'container_listing'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'listing_filter'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'listing_filter'
op|'='
name|'set'
op|'('
op|')'
newline|'\n'
dedent|''
name|'for'
name|'item'
name|'in'
name|'container_listing'
op|':'
newline|'\n'
indent|'                '
name|'name'
op|'='
name|'item'
op|'['
string|"'name'"
op|']'
newline|'\n'
name|'if'
name|'name'
name|'not'
name|'in'
name|'listing_filter'
op|':'
newline|'\n'
indent|'                    '
name|'results'
op|'.'
name|'append'
op|'('
name|'name'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'return'
name|'results'
newline|'\n'
nl|'\n'
DECL|member|get_object_data
dedent|''
name|'def'
name|'get_object_data'
op|'('
name|'self'
op|','
name|'swift_account'
op|','
name|'container_name'
op|','
name|'object_name'
op|','
nl|'\n'
name|'compressed'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'        '
string|"'''reads an object and yields its lines'''"
newline|'\n'
name|'code'
op|','
name|'o'
op|'='
name|'self'
op|'.'
name|'internal_proxy'
op|'.'
name|'get_object'
op|'('
name|'swift_account'
op|','
nl|'\n'
name|'container_name'
op|','
nl|'\n'
name|'object_name'
op|')'
newline|'\n'
name|'if'
name|'code'
op|'<'
number|'200'
name|'or'
name|'code'
op|'>='
number|'300'
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
dedent|''
name|'last_part'
op|'='
string|"''"
newline|'\n'
name|'last_compressed_part'
op|'='
string|"''"
newline|'\n'
comment|'# magic in the following zlib.decompressobj argument is courtesy of'
nl|'\n'
comment|'# Python decompressing gzip chunk-by-chunk'
nl|'\n'
comment|'# http://stackoverflow.com/questions/2423866'
nl|'\n'
name|'d'
op|'='
name|'zlib'
op|'.'
name|'decompressobj'
op|'('
number|'16'
op|'+'
name|'zlib'
op|'.'
name|'MAX_WBITS'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'chunk'
name|'in'
name|'o'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'compressed'
op|':'
newline|'\n'
indent|'                    '
name|'try'
op|':'
newline|'\n'
indent|'                        '
name|'chunk'
op|'='
name|'d'
op|'.'
name|'decompress'
op|'('
name|'chunk'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'zlib'
op|'.'
name|'error'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|"'Bad compressed data for %s'"
op|')'
nl|'\n'
op|'%'
string|"'/'"
op|'.'
name|'join'
op|'('
op|'('
name|'swift_account'
op|','
name|'container_name'
op|','
nl|'\n'
name|'object_name'
op|')'
op|')'
op|')'
newline|'\n'
name|'raise'
name|'BadFileDownload'
op|'('
op|')'
comment|'# bad compressed data'
newline|'\n'
dedent|''
dedent|''
name|'parts'
op|'='
name|'chunk'
op|'.'
name|'split'
op|'('
string|"'\\n'"
op|')'
newline|'\n'
name|'parts'
op|'['
number|'0'
op|']'
op|'='
name|'last_part'
op|'+'
name|'parts'
op|'['
number|'0'
op|']'
newline|'\n'
name|'for'
name|'part'
name|'in'
name|'parts'
op|'['
op|':'
op|'-'
number|'1'
op|']'
op|':'
newline|'\n'
indent|'                    '
name|'yield'
name|'part'
newline|'\n'
dedent|''
name|'last_part'
op|'='
name|'parts'
op|'['
op|'-'
number|'1'
op|']'
newline|'\n'
dedent|''
name|'if'
name|'last_part'
op|':'
newline|'\n'
indent|'                '
name|'yield'
name|'last_part'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'ChunkReadTimeout'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'BadFileDownload'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|generate_keylist_mapping
dedent|''
dedent|''
name|'def'
name|'generate_keylist_mapping'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'keylist'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'plugin'
name|'in'
name|'self'
op|'.'
name|'plugins'
op|':'
newline|'\n'
indent|'            '
name|'plugin_keylist'
op|'='
name|'self'
op|'.'
name|'plugins'
op|'['
name|'plugin'
op|']'
op|'['
string|"'instance'"
op|']'
op|'.'
name|'keylist_mapping'
op|'('
op|')'
newline|'\n'
name|'if'
name|'not'
name|'plugin_keylist'
op|':'
newline|'\n'
indent|'                '
name|'continue'
newline|'\n'
dedent|''
name|'for'
name|'k'
op|','
name|'v'
name|'in'
name|'plugin_keylist'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'o'
op|'='
name|'keylist'
op|'.'
name|'get'
op|'('
name|'k'
op|')'
newline|'\n'
name|'if'
name|'o'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'isinstance'
op|'('
name|'o'
op|','
name|'set'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'if'
name|'isinstance'
op|'('
name|'v'
op|','
name|'set'
op|')'
op|':'
newline|'\n'
indent|'                            '
name|'o'
op|'.'
name|'update'
op|'('
name|'v'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                            '
name|'o'
op|'.'
name|'update'
op|'('
op|'['
name|'v'
op|']'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'o'
op|'='
name|'set'
op|'('
name|'o'
op|')'
newline|'\n'
name|'if'
name|'isinstance'
op|'('
name|'v'
op|','
name|'set'
op|')'
op|':'
newline|'\n'
indent|'                            '
name|'o'
op|'.'
name|'update'
op|'('
name|'v'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                            '
name|'o'
op|'.'
name|'update'
op|'('
op|'['
name|'v'
op|']'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'o'
op|'='
name|'v'
newline|'\n'
dedent|''
name|'keylist'
op|'['
name|'k'
op|']'
op|'='
name|'o'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'keylist'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|LogProcessorDaemon
dedent|''
dedent|''
name|'class'
name|'LogProcessorDaemon'
op|'('
name|'Daemon'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Gather raw log data and farm proccessing to generate a csv that is\n    uploaded to swift.\n    """'
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
name|'c'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'log-processor'"
op|')'
newline|'\n'
name|'super'
op|'('
name|'LogProcessorDaemon'
op|','
name|'self'
op|')'
op|'.'
name|'__init__'
op|'('
name|'c'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'total_conf'
op|'='
name|'conf'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'c'
op|','
name|'log_route'
op|'='
string|"'log-processor'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'log_processor'
op|'='
name|'LogProcessor'
op|'('
name|'conf'
op|','
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'lookback_hours'
op|'='
name|'int'
op|'('
name|'c'
op|'.'
name|'get'
op|'('
string|"'lookback_hours'"
op|','
string|"'120'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'lookback_window'
op|'='
name|'int'
op|'('
name|'c'
op|'.'
name|'get'
op|'('
string|"'lookback_window'"
op|','
nl|'\n'
name|'str'
op|'('
name|'self'
op|'.'
name|'lookback_hours'
op|')'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'log_processor_account'
op|'='
name|'c'
op|'['
string|"'swift_account'"
op|']'
newline|'\n'
name|'self'
op|'.'
name|'log_processor_container'
op|'='
name|'c'
op|'.'
name|'get'
op|'('
string|"'container_name'"
op|','
nl|'\n'
string|"'log_processing_data'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'worker_count'
op|'='
name|'int'
op|'('
name|'c'
op|'.'
name|'get'
op|'('
string|"'worker_count'"
op|','
string|"'1'"
op|')'
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
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|'"Beginning log processing"'
op|')'
op|')'
newline|'\n'
name|'start'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'lookback_hours'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'lookback_start'
op|'='
name|'None'
newline|'\n'
name|'lookback_end'
op|'='
name|'None'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'delta_hours'
op|'='
name|'datetime'
op|'.'
name|'timedelta'
op|'('
name|'hours'
op|'='
name|'self'
op|'.'
name|'lookback_hours'
op|')'
newline|'\n'
name|'lookback_start'
op|'='
name|'datetime'
op|'.'
name|'datetime'
op|'.'
name|'now'
op|'('
op|')'
op|'-'
name|'delta_hours'
newline|'\n'
name|'lookback_start'
op|'='
name|'lookback_start'
op|'.'
name|'strftime'
op|'('
string|"'%Y%m%d%H'"
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'lookback_window'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'                '
name|'lookback_end'
op|'='
name|'None'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'delta_window'
op|'='
name|'datetime'
op|'.'
name|'timedelta'
op|'('
name|'hours'
op|'='
name|'self'
op|'.'
name|'lookback_window'
op|')'
newline|'\n'
name|'lookback_end'
op|'='
name|'datetime'
op|'.'
name|'datetime'
op|'.'
name|'now'
op|'('
op|')'
op|'-'
name|'delta_hours'
op|'+'
name|'delta_window'
newline|'\n'
name|'lookback_end'
op|'='
name|'lookback_end'
op|'.'
name|'strftime'
op|'('
string|"'%Y%m%d%H'"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
string|"'lookback_start: %s'"
op|'%'
name|'lookback_start'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
string|"'lookback_end: %s'"
op|'%'
name|'lookback_end'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
comment|'# Note: this file (or data set) will grow without bound.'
nl|'\n'
comment|'# In practice, if it becomes a problem (say, after many months of'
nl|'\n'
comment|'# running), one could manually prune the file to remove older'
nl|'\n'
comment|'# entries. Automatically pruning on each run could be dangerous.'
nl|'\n'
comment|'# There is not a good way to determine when an old entry should be'
nl|'\n'
comment|'# pruned (lookback_hours could be set to anything and could change)'
nl|'\n'
indent|'            '
name|'processed_files_stream'
op|'='
name|'self'
op|'.'
name|'log_processor'
op|'.'
name|'get_object_data'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'log_processor_account'
op|','
nl|'\n'
name|'self'
op|'.'
name|'log_processor_container'
op|','
nl|'\n'
string|"'processed_files.pickle.gz'"
op|','
nl|'\n'
name|'compressed'
op|'='
name|'True'
op|')'
newline|'\n'
name|'buf'
op|'='
string|"'\\n'"
op|'.'
name|'join'
op|'('
name|'x'
name|'for'
name|'x'
name|'in'
name|'processed_files_stream'
op|')'
newline|'\n'
name|'if'
name|'buf'
op|':'
newline|'\n'
indent|'                '
name|'already_processed_files'
op|'='
name|'cPickle'
op|'.'
name|'loads'
op|'('
name|'buf'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'already_processed_files'
op|'='
name|'set'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'already_processed_files'
op|'='
name|'set'
op|'('
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|"'found %d processed files'"
op|')'
op|'%'
name|'len'
op|'('
name|'already_processed_files'
op|')'
op|')'
newline|'\n'
name|'logs_to_process'
op|'='
name|'self'
op|'.'
name|'log_processor'
op|'.'
name|'get_data_list'
op|'('
name|'lookback_start'
op|','
nl|'\n'
name|'lookback_end'
op|','
nl|'\n'
name|'already_processed_files'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|"'loaded %d files to process'"
op|')'
op|'%'
nl|'\n'
name|'len'
op|'('
name|'logs_to_process'
op|')'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'logs_to_process'
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
string|'"Log processing done (%0.2f minutes)"'
op|')'
op|'%'
nl|'\n'
op|'('
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'start'
op|')'
op|'/'
number|'60'
op|')'
op|')'
newline|'\n'
name|'return'
newline|'\n'
nl|'\n'
comment|'# map'
nl|'\n'
dedent|''
name|'processor_args'
op|'='
op|'('
name|'self'
op|'.'
name|'total_conf'
op|','
name|'self'
op|'.'
name|'logger'
op|')'
newline|'\n'
name|'results'
op|'='
name|'multiprocess_collate'
op|'('
name|'processor_args'
op|','
name|'logs_to_process'
op|','
nl|'\n'
name|'self'
op|'.'
name|'worker_count'
op|')'
newline|'\n'
nl|'\n'
comment|'#reduce'
nl|'\n'
name|'aggr_data'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'processed_files'
op|'='
name|'already_processed_files'
newline|'\n'
name|'for'
name|'item'
op|','
name|'data'
name|'in'
name|'results'
op|':'
newline|'\n'
comment|'# since item contains the plugin and the log name, new plugins will'
nl|'\n'
comment|'# "reprocess" the file and the results will be in the final csv.'
nl|'\n'
indent|'            '
name|'processed_files'
op|'.'
name|'add'
op|'('
name|'item'
op|')'
newline|'\n'
name|'for'
name|'k'
op|','
name|'d'
name|'in'
name|'data'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'existing_data'
op|'='
name|'aggr_data'
op|'.'
name|'get'
op|'('
name|'k'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'for'
name|'i'
op|','
name|'j'
name|'in'
name|'d'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'current'
op|'='
name|'existing_data'
op|'.'
name|'get'
op|'('
name|'i'
op|','
number|'0'
op|')'
newline|'\n'
comment|'# merging strategy for key collisions is addition'
nl|'\n'
comment|'# processing plugins need to realize this'
nl|'\n'
name|'existing_data'
op|'['
name|'i'
op|']'
op|'='
name|'current'
op|'+'
name|'j'
newline|'\n'
dedent|''
name|'aggr_data'
op|'['
name|'k'
op|']'
op|'='
name|'existing_data'
newline|'\n'
nl|'\n'
comment|'# group'
nl|'\n'
comment|'# reduce a large number of keys in aggr_data[k] to a small number of'
nl|'\n'
comment|'# output keys'
nl|'\n'
dedent|''
dedent|''
name|'keylist_mapping'
op|'='
name|'self'
op|'.'
name|'log_processor'
op|'.'
name|'generate_keylist_mapping'
op|'('
op|')'
newline|'\n'
name|'final_info'
op|'='
name|'collections'
op|'.'
name|'defaultdict'
op|'('
name|'dict'
op|')'
newline|'\n'
name|'for'
name|'account'
op|','
name|'data'
name|'in'
name|'aggr_data'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'key'
op|','
name|'mapping'
name|'in'
name|'keylist_mapping'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'isinstance'
op|'('
name|'mapping'
op|','
op|'('
name|'list'
op|','
name|'set'
op|')'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'value'
op|'='
number|'0'
newline|'\n'
name|'for'
name|'k'
name|'in'
name|'mapping'
op|':'
newline|'\n'
indent|'                        '
name|'try'
op|':'
newline|'\n'
indent|'                            '
name|'value'
op|'+='
name|'data'
op|'['
name|'k'
op|']'
newline|'\n'
dedent|''
name|'except'
name|'KeyError'
op|':'
newline|'\n'
indent|'                            '
name|'pass'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'try'
op|':'
newline|'\n'
indent|'                        '
name|'value'
op|'='
name|'data'
op|'['
name|'mapping'
op|']'
newline|'\n'
dedent|''
name|'except'
name|'KeyError'
op|':'
newline|'\n'
indent|'                        '
name|'value'
op|'='
number|'0'
newline|'\n'
dedent|''
dedent|''
name|'final_info'
op|'['
name|'account'
op|']'
op|'['
name|'key'
op|']'
op|'='
name|'value'
newline|'\n'
nl|'\n'
comment|'# output'
nl|'\n'
dedent|''
dedent|''
name|'sorted_keylist_mapping'
op|'='
name|'sorted'
op|'('
name|'keylist_mapping'
op|')'
newline|'\n'
name|'columns'
op|'='
string|"'data_ts,account,'"
op|'+'
string|"','"
op|'.'
name|'join'
op|'('
name|'sorted_keylist_mapping'
op|')'
newline|'\n'
name|'out_buf'
op|'='
op|'['
name|'columns'
op|']'
newline|'\n'
name|'for'
op|'('
name|'account'
op|','
name|'year'
op|','
name|'month'
op|','
name|'day'
op|','
name|'hour'
op|')'
op|','
name|'d'
name|'in'
name|'final_info'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'data_ts'
op|'='
string|"'%s/%s/%s %s:00:00'"
op|'%'
op|'('
name|'year'
op|','
name|'month'
op|','
name|'day'
op|','
name|'hour'
op|')'
newline|'\n'
name|'row'
op|'='
op|'['
name|'data_ts'
op|']'
newline|'\n'
name|'row'
op|'.'
name|'append'
op|'('
string|"'%s'"
op|'%'
name|'account'
op|')'
newline|'\n'
name|'for'
name|'k'
name|'in'
name|'sorted_keylist_mapping'
op|':'
newline|'\n'
indent|'                '
name|'row'
op|'.'
name|'append'
op|'('
string|"'%s'"
op|'%'
name|'d'
op|'['
name|'k'
op|']'
op|')'
newline|'\n'
dedent|''
name|'out_buf'
op|'.'
name|'append'
op|'('
string|"','"
op|'.'
name|'join'
op|'('
name|'row'
op|')'
op|')'
newline|'\n'
dedent|''
name|'out_buf'
op|'='
string|"'\\n'"
op|'.'
name|'join'
op|'('
name|'out_buf'
op|')'
newline|'\n'
name|'h'
op|'='
name|'hashlib'
op|'.'
name|'md5'
op|'('
name|'out_buf'
op|')'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'upload_name'
op|'='
name|'time'
op|'.'
name|'strftime'
op|'('
string|"'%Y/%m/%d/%H/'"
op|')'
op|'+'
string|"'%s.csv.gz'"
op|'%'
name|'h'
newline|'\n'
name|'f'
op|'='
name|'cStringIO'
op|'.'
name|'StringIO'
op|'('
name|'out_buf'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'log_processor'
op|'.'
name|'internal_proxy'
op|'.'
name|'upload_file'
op|'('
name|'f'
op|','
nl|'\n'
name|'self'
op|'.'
name|'log_processor_account'
op|','
nl|'\n'
name|'self'
op|'.'
name|'log_processor_container'
op|','
nl|'\n'
name|'upload_name'
op|')'
newline|'\n'
nl|'\n'
comment|'# cleanup'
nl|'\n'
name|'s'
op|'='
name|'cPickle'
op|'.'
name|'dumps'
op|'('
name|'processed_files'
op|','
name|'cPickle'
op|'.'
name|'HIGHEST_PROTOCOL'
op|')'
newline|'\n'
name|'f'
op|'='
name|'cStringIO'
op|'.'
name|'StringIO'
op|'('
name|'s'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'log_processor'
op|'.'
name|'internal_proxy'
op|'.'
name|'upload_file'
op|'('
name|'f'
op|','
nl|'\n'
name|'self'
op|'.'
name|'log_processor_account'
op|','
nl|'\n'
name|'self'
op|'.'
name|'log_processor_container'
op|','
nl|'\n'
string|"'processed_files.pickle.gz'"
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|'"Log processing done (%0.2f minutes)"'
op|')'
op|'%'
nl|'\n'
op|'('
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'start'
op|')'
op|'/'
number|'60'
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|multiprocess_collate
dedent|''
dedent|''
name|'def'
name|'multiprocess_collate'
op|'('
name|'processor_args'
op|','
name|'logs_to_process'
op|','
name|'worker_count'
op|')'
op|':'
newline|'\n'
indent|'    '
string|"'''yield hourly data from logs_to_process'''"
newline|'\n'
name|'results'
op|'='
op|'['
op|']'
newline|'\n'
name|'in_queue'
op|'='
name|'multiprocessing'
op|'.'
name|'Queue'
op|'('
op|')'
newline|'\n'
name|'out_queue'
op|'='
name|'multiprocessing'
op|'.'
name|'Queue'
op|'('
op|')'
newline|'\n'
name|'for'
name|'_junk'
name|'in'
name|'range'
op|'('
name|'worker_count'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'p'
op|'='
name|'multiprocessing'
op|'.'
name|'Process'
op|'('
name|'target'
op|'='
name|'collate_worker'
op|','
nl|'\n'
name|'args'
op|'='
op|'('
name|'processor_args'
op|','
nl|'\n'
name|'in_queue'
op|','
nl|'\n'
name|'out_queue'
op|')'
op|')'
newline|'\n'
name|'p'
op|'.'
name|'start'
op|'('
op|')'
newline|'\n'
name|'results'
op|'.'
name|'append'
op|'('
name|'p'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'x'
name|'in'
name|'logs_to_process'
op|':'
newline|'\n'
indent|'        '
name|'in_queue'
op|'.'
name|'put'
op|'('
name|'x'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'_junk'
name|'in'
name|'range'
op|'('
name|'worker_count'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'in_queue'
op|'.'
name|'put'
op|'('
name|'None'
op|')'
newline|'\n'
dedent|''
name|'count'
op|'='
number|'0'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'item'
op|','
name|'data'
op|'='
name|'out_queue'
op|'.'
name|'get_nowait'
op|'('
op|')'
newline|'\n'
name|'count'
op|'+='
number|'1'
newline|'\n'
name|'if'
name|'data'
op|':'
newline|'\n'
indent|'                '
name|'yield'
name|'item'
op|','
name|'data'
newline|'\n'
dedent|''
name|'if'
name|'count'
op|'>='
name|'len'
op|'('
name|'logs_to_process'
op|')'
op|':'
newline|'\n'
comment|'# this implies that one result will come from every request'
nl|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'Queue'
op|'.'
name|'Empty'
op|':'
newline|'\n'
indent|'            '
name|'time'
op|'.'
name|'sleep'
op|'('
number|'.1'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'for'
name|'r'
name|'in'
name|'results'
op|':'
newline|'\n'
indent|'        '
name|'r'
op|'.'
name|'join'
op|'('
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|collate_worker
dedent|''
dedent|''
name|'def'
name|'collate_worker'
op|'('
name|'processor_args'
op|','
name|'in_queue'
op|','
name|'out_queue'
op|')'
op|':'
newline|'\n'
indent|'    '
string|"'''worker process for multiprocess_collate'''"
newline|'\n'
name|'p'
op|'='
name|'LogProcessor'
op|'('
op|'*'
name|'processor_args'
op|')'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'item'
op|'='
name|'in_queue'
op|'.'
name|'get_nowait'
op|'('
op|')'
newline|'\n'
name|'if'
name|'item'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'Queue'
op|'.'
name|'Empty'
op|':'
newline|'\n'
indent|'            '
name|'time'
op|'.'
name|'sleep'
op|'('
number|'.1'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'ret'
op|'='
name|'p'
op|'.'
name|'process_one_file'
op|'('
op|'*'
name|'item'
op|')'
newline|'\n'
name|'out_queue'
op|'.'
name|'put'
op|'('
op|'('
name|'item'
op|','
name|'ret'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
endmarker|''
end_unit
