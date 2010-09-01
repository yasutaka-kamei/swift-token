begin_unit
name|'import'
name|'unittest'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'stats'
name|'import'
name|'log_processor'
newline|'\n'
nl|'\n'
DECL|class|DumbLogger
name|'class'
name|'DumbLogger'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|__getattr__
indent|'    '
name|'def'
name|'__getattr__'
op|'('
name|'self'
op|','
name|'n'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'self'
op|'.'
name|'foo'
newline|'\n'
nl|'\n'
DECL|member|foo
dedent|''
name|'def'
name|'foo'
op|'('
name|'self'
op|','
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
DECL|class|DumbInternalProxy
dedent|''
dedent|''
name|'class'
name|'DumbInternalProxy'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|get_container_list
indent|'    '
name|'def'
name|'get_container_list'
op|'('
name|'self'
op|','
name|'account'
op|','
name|'container'
op|','
name|'marker'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'n'
op|'='
string|"'2010/03/14/13/obj1'"
newline|'\n'
name|'if'
name|'marker'
name|'is'
name|'None'
name|'or'
name|'n'
op|'>'
name|'marker'
op|':'
newline|'\n'
indent|'            '
name|'return'
op|'['
op|'{'
string|"'name'"
op|':'
name|'n'
op|'}'
op|']'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'return'
op|'['
op|']'
newline|'\n'
nl|'\n'
DECL|member|get_object
dedent|''
dedent|''
name|'def'
name|'get_object'
op|'('
name|'self'
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
name|'if'
name|'object_name'
op|'.'
name|'endswith'
op|'('
string|"'.gz'"
op|')'
op|':'
newline|'\n'
comment|'# same data as below, compressed with gzip -9'
nl|'\n'
indent|'            '
name|'yield'
string|"'\\x1f\\x8b\\x08'"
newline|'\n'
name|'yield'
string|'\'\\x08"\\xd79L\''
newline|'\n'
name|'yield'
string|"'\\x02\\x03te'"
newline|'\n'
name|'yield'
string|"'st\\x00\\xcbO'"
newline|'\n'
name|'yield'
string|"'\\xca\\xe2JI,I'"
newline|'\n'
name|'yield'
string|"'\\xe4\\x02\\x00O\\xff'"
newline|'\n'
name|'yield'
string|"'\\xa3Y\\t\\x00\\x00\\x00'"
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'yield'
string|"'obj\\n'"
newline|'\n'
name|'yield'
string|"'data'"
newline|'\n'
nl|'\n'
DECL|class|TestLogProcessor
dedent|''
dedent|''
dedent|''
name|'class'
name|'TestLogProcessor'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
indent|'    '
name|'access_test_line'
op|'='
string|"'Jul  9 04:14:30 saio proxy 1.2.3.4 4.5.6.7 '"
string|"'09/Jul/2010/04/14/30 GET '"
string|"'/v1/acct/foo/bar?format=json&foo HTTP/1.0 200 - '"
string|"'curl tk4e350daf-9338-4cc6-aabb-090e49babfbd '"
string|"'6 95 - txfa431231-7f07-42fd-8fc7-7da9d8cc1f90 - 0.0262'"
newline|'\n'
DECL|variable|stats_test_line
name|'stats_test_line'
op|'='
string|"'account,1,2,3,1283378584.881391'"
newline|'\n'
DECL|variable|proxy_config
name|'proxy_config'
op|'='
op|'{'
string|"'log-processor'"
op|':'
op|'{'
nl|'\n'
nl|'\n'
op|'}'
nl|'\n'
op|'}'
newline|'\n'
nl|'\n'
DECL|member|test_access_log_line_parser
name|'def'
name|'test_access_log_line_parser'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'access_proxy_config'
op|'='
name|'self'
op|'.'
name|'proxy_config'
newline|'\n'
name|'access_proxy_config'
op|'.'
name|'update'
op|'('
op|'{'
nl|'\n'
string|"'log-processor-access'"
op|':'
op|'{'
nl|'\n'
string|"'source_filename_format'"
op|':'
string|"'%Y%m%d%H*'"
op|','
nl|'\n'
string|"'class_path'"
op|':'
nl|'\n'
string|"'swift.stats.access_processor.AccessLogProcessor'"
nl|'\n'
op|'}'
op|'}'
op|')'
newline|'\n'
name|'p'
op|'='
name|'log_processor'
op|'.'
name|'LogProcessor'
op|'('
name|'access_proxy_config'
op|','
name|'DumbLogger'
op|'('
op|')'
op|')'
newline|'\n'
name|'result'
op|'='
name|'p'
op|'.'
name|'plugins'
op|'['
string|"'access'"
op|']'
op|'['
string|"'instance'"
op|']'
op|'.'
name|'log_line_parser'
op|'('
name|'self'
op|'.'
name|'access_test_line'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'result'
op|','
op|'{'
string|"'code'"
op|':'
number|'200'
op|','
nl|'\n'
string|"'processing_time'"
op|':'
string|"'0.0262'"
op|','
nl|'\n'
string|"'auth_token'"
op|':'
string|"'tk4e350daf-9338-4cc6-aabb-090e49babfbd'"
op|','
nl|'\n'
string|"'month'"
op|':'
string|"'07'"
op|','
nl|'\n'
string|"'second'"
op|':'
string|"'30'"
op|','
nl|'\n'
string|"'year'"
op|':'
string|"'2010'"
op|','
nl|'\n'
string|"'query'"
op|':'
string|"'format=json&foo'"
op|','
nl|'\n'
string|"'tz'"
op|':'
string|"'+0000'"
op|','
nl|'\n'
string|"'http_version'"
op|':'
string|"'HTTP/1.0'"
op|','
nl|'\n'
string|"'object_name'"
op|':'
string|"'bar'"
op|','
nl|'\n'
string|"'etag'"
op|':'
string|"'-'"
op|','
nl|'\n'
string|"'foo'"
op|':'
number|'1'
op|','
nl|'\n'
string|"'method'"
op|':'
string|"'GET'"
op|','
nl|'\n'
string|"'trans_id'"
op|':'
string|"'txfa431231-7f07-42fd-8fc7-7da9d8cc1f90'"
op|','
nl|'\n'
string|"'client_ip'"
op|':'
string|"'1.2.3.4'"
op|','
nl|'\n'
string|"'format'"
op|':'
number|'1'
op|','
nl|'\n'
string|"'bytes_out'"
op|':'
number|'95'
op|','
nl|'\n'
string|"'container_name'"
op|':'
string|"'foo'"
op|','
nl|'\n'
string|"'day'"
op|':'
string|"'09'"
op|','
nl|'\n'
string|"'minute'"
op|':'
string|"'14'"
op|','
nl|'\n'
string|"'account'"
op|':'
string|"'acct'"
op|','
nl|'\n'
string|"'hour'"
op|':'
string|"'04'"
op|','
nl|'\n'
string|"'referrer'"
op|':'
string|"'-'"
op|','
nl|'\n'
string|"'request'"
op|':'
string|"'/v1/acct/foo/bar'"
op|','
nl|'\n'
string|"'user_agent'"
op|':'
string|"'curl'"
op|','
nl|'\n'
string|"'bytes_in'"
op|':'
number|'6'
op|','
nl|'\n'
string|"'lb_ip'"
op|':'
string|"'4.5.6.7'"
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_process_one_access_file
dedent|''
name|'def'
name|'test_process_one_access_file'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'access_proxy_config'
op|'='
name|'self'
op|'.'
name|'proxy_config'
newline|'\n'
name|'access_proxy_config'
op|'.'
name|'update'
op|'('
op|'{'
nl|'\n'
string|"'log-processor-access'"
op|':'
op|'{'
nl|'\n'
string|"'source_filename_format'"
op|':'
string|"'%Y%m%d%H*'"
op|','
nl|'\n'
string|"'class_path'"
op|':'
nl|'\n'
string|"'swift.stats.access_processor.AccessLogProcessor'"
nl|'\n'
op|'}'
op|'}'
op|')'
newline|'\n'
name|'p'
op|'='
name|'log_processor'
op|'.'
name|'LogProcessor'
op|'('
name|'access_proxy_config'
op|','
name|'DumbLogger'
op|'('
op|')'
op|')'
newline|'\n'
DECL|function|get_object_data
name|'def'
name|'get_object_data'
op|'('
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
op|'['
name|'self'
op|'.'
name|'access_test_line'
op|']'
newline|'\n'
dedent|''
name|'p'
op|'.'
name|'get_object_data'
op|'='
name|'get_object_data'
newline|'\n'
name|'result'
op|'='
name|'p'
op|'.'
name|'process_one_file'
op|'('
string|"'access'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'expected'
op|'='
op|'{'
op|'('
string|"'acct'"
op|','
string|"'2010'"
op|','
string|"'07'"
op|','
string|"'09'"
op|','
string|"'04'"
op|')'
op|':'
nl|'\n'
op|'{'
op|'('
string|"'public'"
op|','
string|"'object'"
op|','
string|"'GET'"
op|','
string|"'2xx'"
op|')'
op|':'
number|'1'
op|','
nl|'\n'
op|'('
string|"'public'"
op|','
string|"'bytes_out'"
op|')'
op|':'
number|'95'
op|','
nl|'\n'
string|"'marker_query'"
op|':'
number|'0'
op|','
nl|'\n'
string|"'format_query'"
op|':'
number|'1'
op|','
nl|'\n'
string|"'delimiter_query'"
op|':'
number|'0'
op|','
nl|'\n'
string|"'path_query'"
op|':'
number|'0'
op|','
nl|'\n'
op|'('
string|"'public'"
op|','
string|"'bytes_in'"
op|')'
op|':'
number|'6'
op|','
nl|'\n'
string|"'prefix_query'"
op|':'
number|'0'
op|'}'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'result'
op|','
name|'expected'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_container_listing
dedent|''
name|'def'
name|'test_get_container_listing'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'p'
op|'='
name|'log_processor'
op|'.'
name|'LogProcessor'
op|'('
name|'self'
op|'.'
name|'proxy_config'
op|','
name|'DumbLogger'
op|'('
op|')'
op|')'
newline|'\n'
name|'p'
op|'.'
name|'internal_proxy'
op|'='
name|'DumbInternalProxy'
op|'('
op|')'
newline|'\n'
name|'result'
op|'='
name|'p'
op|'.'
name|'get_container_listing'
op|'('
string|"'a'"
op|','
string|"'foo'"
op|')'
newline|'\n'
name|'expected'
op|'='
op|'['
string|"'2010/03/14/13/obj1'"
op|']'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'result'
op|','
name|'expected'
op|')'
newline|'\n'
name|'result'
op|'='
name|'p'
op|'.'
name|'get_container_listing'
op|'('
string|"'a'"
op|','
string|"'foo'"
op|','
name|'listing_filter'
op|'='
name|'expected'
op|')'
newline|'\n'
name|'expected'
op|'='
op|'['
op|']'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'result'
op|','
name|'expected'
op|')'
newline|'\n'
name|'result'
op|'='
name|'p'
op|'.'
name|'get_container_listing'
op|'('
string|"'a'"
op|','
string|"'foo'"
op|','
name|'start_date'
op|'='
string|"'2010031412'"
op|','
nl|'\n'
name|'end_date'
op|'='
string|"'2010031414'"
op|')'
newline|'\n'
name|'expected'
op|'='
op|'['
string|"'2010/03/14/13/obj1'"
op|']'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'result'
op|','
name|'expected'
op|')'
newline|'\n'
name|'result'
op|'='
name|'p'
op|'.'
name|'get_container_listing'
op|'('
string|"'a'"
op|','
string|"'foo'"
op|','
name|'start_date'
op|'='
string|"'2010031414'"
op|')'
newline|'\n'
name|'expected'
op|'='
op|'['
op|']'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'result'
op|','
name|'expected'
op|')'
newline|'\n'
name|'result'
op|'='
name|'p'
op|'.'
name|'get_container_listing'
op|'('
string|"'a'"
op|','
string|"'foo'"
op|','
name|'start_date'
op|'='
string|"'2010031410'"
op|','
nl|'\n'
name|'end_date'
op|'='
string|"'2010031412'"
op|')'
newline|'\n'
name|'expected'
op|'='
op|'['
op|']'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'result'
op|','
name|'expected'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_object_data
dedent|''
name|'def'
name|'test_get_object_data'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'p'
op|'='
name|'log_processor'
op|'.'
name|'LogProcessor'
op|'('
name|'self'
op|'.'
name|'proxy_config'
op|','
name|'DumbLogger'
op|'('
op|')'
op|')'
newline|'\n'
name|'p'
op|'.'
name|'internal_proxy'
op|'='
name|'DumbInternalProxy'
op|'('
op|')'
newline|'\n'
name|'result'
op|'='
name|'list'
op|'('
name|'p'
op|'.'
name|'get_object_data'
op|'('
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|','
name|'False'
op|')'
op|')'
newline|'\n'
name|'expected'
op|'='
op|'['
string|"'obj'"
op|','
string|"'data'"
op|']'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'result'
op|','
name|'expected'
op|')'
newline|'\n'
name|'result'
op|'='
name|'list'
op|'('
name|'p'
op|'.'
name|'get_object_data'
op|'('
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o.gz'"
op|','
name|'True'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'result'
op|','
name|'expected'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_get_stat_totals
dedent|''
name|'def'
name|'test_get_stat_totals'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'stats_proxy_config'
op|'='
name|'self'
op|'.'
name|'proxy_config'
newline|'\n'
name|'stats_proxy_config'
op|'.'
name|'update'
op|'('
op|'{'
nl|'\n'
string|"'log-processor-stats'"
op|':'
op|'{'
nl|'\n'
string|"'class_path'"
op|':'
nl|'\n'
string|"'swift.stats.stats_processor.StatsLogProcessor'"
nl|'\n'
op|'}'
op|'}'
op|')'
newline|'\n'
name|'p'
op|'='
name|'log_processor'
op|'.'
name|'LogProcessor'
op|'('
name|'stats_proxy_config'
op|','
name|'DumbLogger'
op|'('
op|')'
op|')'
newline|'\n'
name|'p'
op|'.'
name|'internal_proxy'
op|'='
name|'DumbInternalProxy'
op|'('
op|')'
newline|'\n'
DECL|function|get_object_data
name|'def'
name|'get_object_data'
op|'('
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
op|'['
name|'self'
op|'.'
name|'stats_test_line'
op|']'
newline|'\n'
dedent|''
name|'p'
op|'.'
name|'get_object_data'
op|'='
name|'get_object_data'
newline|'\n'
name|'result'
op|'='
name|'p'
op|'.'
name|'process_one_file'
op|'('
string|"'stats'"
op|','
string|"'a'"
op|','
string|"'c'"
op|','
string|"'o'"
op|')'
newline|'\n'
name|'expected'
op|'='
op|'{'
string|"'account'"
op|':'
nl|'\n'
op|'{'
string|"'count'"
op|':'
number|'1'
op|','
nl|'\n'
string|"'object_count'"
op|':'
number|'2'
op|','
nl|'\n'
string|"'container_count'"
op|':'
number|'1'
op|','
nl|'\n'
string|"'bytes_used'"
op|':'
number|'3'
op|','
nl|'\n'
string|"'created_at'"
op|':'
string|"'1283378584.881391'"
op|'}'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'result'
op|','
name|'expected'
op|')'
dedent|''
dedent|''
endmarker|''
end_unit
