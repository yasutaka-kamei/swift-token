begin_unit
comment|'# Copyright (c) 2013 OpenStack, LLC.'
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
name|'unittest'
newline|'\n'
name|'from'
name|'mock'
name|'import'
name|'patch'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'middleware'
name|'import'
name|'slo'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'json'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'constraints'
name|'import'
name|'MAX_META_VALUE_LENGTH'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'Request'
op|','
name|'Response'
op|','
name|'HTTPException'
op|','
name|'HTTPRequestEntityTooLarge'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FakeApp
name|'class'
name|'FakeApp'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'calls'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'req_method_paths'
op|'='
op|'['
op|']'
newline|'\n'
nl|'\n'
DECL|member|__call__
dedent|''
name|'def'
name|'__call__'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'calls'
op|'+='
number|'1'
newline|'\n'
name|'if'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'=='
string|"'/'"
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'Response'
op|'('
name|'status'
op|'='
number|'200'
op|','
name|'body'
op|'='
string|"'passed'"
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'.'
name|'startswith'
op|'('
string|"'/test_good/'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'j'
op|','
name|'v'
op|','
name|'a'
op|','
name|'cont'
op|','
name|'obj'
op|'='
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'.'
name|'split'
op|'('
string|"'/'"
op|')'
newline|'\n'
name|'if'
name|'obj'
op|'=='
string|"'a_2'"
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'Response'
op|'('
name|'status'
op|'='
number|'400'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'cont_len'
op|'='
number|'100'
newline|'\n'
name|'if'
name|'obj'
op|'=='
string|"'small_object'"
op|':'
newline|'\n'
indent|'                '
name|'cont_len'
op|'='
number|'10'
newline|'\n'
dedent|''
name|'return'
name|'Response'
op|'('
nl|'\n'
name|'status'
op|'='
number|'200'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'etag'"
op|':'
string|"'etagoftheobjectsegment'"
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
name|'cont_len'
op|'}'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'.'
name|'startswith'
op|'('
string|"'/test_good_check/'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'j'
op|','
name|'v'
op|','
name|'a'
op|','
name|'cont'
op|','
name|'obj'
op|'='
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'.'
name|'split'
op|'('
string|"'/'"
op|')'
newline|'\n'
name|'etag'
op|','
name|'size'
op|'='
name|'obj'
op|'.'
name|'split'
op|'('
string|"'_'"
op|')'
newline|'\n'
name|'last_mod'
op|'='
string|"'Fri, 01 Feb 2012 20:38:36 GMT'"
newline|'\n'
name|'if'
name|'obj'
op|'=='
string|"'a_1'"
op|':'
newline|'\n'
indent|'                '
name|'last_mod'
op|'='
string|"''"
newline|'\n'
dedent|''
name|'return'
name|'Response'
op|'('
nl|'\n'
name|'status'
op|'='
number|'200'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'etag'"
op|':'
name|'etag'
op|','
string|"'Last-Modified'"
op|':'
name|'last_mod'
op|','
nl|'\n'
string|"'Content-Length'"
op|':'
name|'size'
op|'}'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'.'
name|'startswith'
op|'('
string|"'/test_get/'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'good_data'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
nl|'\n'
op|'['
op|'{'
string|"'name'"
op|':'
string|"'/c/a_1'"
op|','
string|"'hash'"
op|':'
string|"'a'"
op|','
string|"'bytes'"
op|':'
string|"'1'"
op|'}'
op|','
nl|'\n'
op|'{'
string|"'name'"
op|':'
string|"'/d/b_2'"
op|','
string|"'hash'"
op|':'
string|"'b'"
op|','
string|"'bytes'"
op|':'
string|"'2'"
op|'}'
op|']'
op|')'
newline|'\n'
name|'return'
name|'Response'
op|'('
name|'status'
op|'='
number|'200'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Static-Large-Object'"
op|':'
string|"'True'"
op|','
nl|'\n'
string|"'Content-Type'"
op|':'
string|"'html;swift_bytes=55'"
op|'}'
op|','
nl|'\n'
name|'body'
op|'='
name|'good_data'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'.'
name|'startswith'
op|'('
string|"'/test_get_broke_json/'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'good_data'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
nl|'\n'
op|'['
op|'{'
string|"'name'"
op|':'
string|"'/c/a_1'"
op|','
string|"'hash'"
op|':'
string|"'a'"
op|','
string|"'bytes'"
op|':'
string|"'1'"
op|'}'
op|','
nl|'\n'
op|'{'
string|"'name'"
op|':'
string|"'/d/b_2'"
op|','
string|"'hash'"
op|':'
string|"'b'"
op|','
string|"'bytes'"
op|':'
string|"'2'"
op|'}'
op|']'
op|')'
newline|'\n'
name|'return'
name|'Response'
op|'('
name|'status'
op|'='
number|'200'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Static-Large-Object'"
op|':'
string|"'True'"
op|'}'
op|','
nl|'\n'
name|'body'
op|'='
name|'good_data'
op|'['
op|':'
op|'-'
number|'5'
op|']'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'.'
name|'startswith'
op|'('
string|"'/test_get_bad_json/'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'bad_data'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
nl|'\n'
op|'['
op|'{'
string|"'name'"
op|':'
string|"'/c/a_1'"
op|','
string|"'something'"
op|':'
string|"'a'"
op|','
string|"'bytes'"
op|':'
string|"'1'"
op|'}'
op|','
nl|'\n'
op|'{'
string|"'name'"
op|':'
string|"'/d/b_2'"
op|','
string|"'bytes'"
op|':'
string|"'2'"
op|'}'
op|']'
op|')'
newline|'\n'
name|'return'
name|'Response'
op|'('
name|'status'
op|'='
number|'200'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Static-Large-Object'"
op|':'
string|"'True'"
op|'}'
op|','
nl|'\n'
name|'body'
op|'='
name|'bad_data'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'.'
name|'startswith'
op|'('
string|"'/test_get_not_slo/'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'Response'
op|'('
name|'status'
op|'='
number|'200'
op|','
name|'body'
op|'='
string|"'lalala'"
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'.'
name|'startswith'
op|'('
string|"'/test_delete_404/'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'req_method_paths'
op|'.'
name|'append'
op|'('
op|'('
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
op|','
nl|'\n'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|')'
op|')'
newline|'\n'
name|'return'
name|'Response'
op|'('
name|'status'
op|'='
number|'404'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'.'
name|'startswith'
op|'('
string|"'/test_delete/'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'good_data'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
nl|'\n'
op|'['
op|'{'
string|"'name'"
op|':'
string|"'/c/a_1'"
op|','
string|"'hash'"
op|':'
string|"'a'"
op|','
string|"'bytes'"
op|':'
string|"'1'"
op|'}'
op|','
nl|'\n'
op|'{'
string|"'name'"
op|':'
string|"'/d/b_2'"
op|','
string|"'hash'"
op|':'
string|"'b'"
op|','
string|"'bytes'"
op|':'
string|"'2'"
op|'}'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'req_method_paths'
op|'.'
name|'append'
op|'('
op|'('
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
op|','
nl|'\n'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|')'
op|')'
newline|'\n'
name|'return'
name|'Response'
op|'('
name|'status'
op|'='
number|'200'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Static-Large-Object'"
op|':'
string|"'True'"
op|'}'
op|','
nl|'\n'
name|'body'
op|'='
name|'good_data'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'.'
name|'startswith'
op|'('
string|"'/test_delete_bad_json/'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'req_method_paths'
op|'.'
name|'append'
op|'('
op|'('
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
op|','
nl|'\n'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|')'
op|')'
newline|'\n'
name|'return'
name|'Response'
op|'('
name|'status'
op|'='
number|'200'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Static-Large-Object'"
op|':'
string|"'True'"
op|'}'
op|','
nl|'\n'
name|'body'
op|'='
string|"'bad json'"
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'.'
name|'startswith'
op|'('
string|"'/test_delete_bad_man/'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'req_method_paths'
op|'.'
name|'append'
op|'('
op|'('
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
op|','
nl|'\n'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|')'
op|')'
newline|'\n'
name|'return'
name|'Response'
op|'('
name|'status'
op|'='
number|'200'
op|','
name|'body'
op|'='
string|"''"
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'.'
name|'startswith'
op|'('
string|"'/test_delete_bad/'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'good_data'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
nl|'\n'
op|'['
op|'{'
string|"'name'"
op|':'
string|"'/c/a_1'"
op|','
string|"'hash'"
op|':'
string|"'a'"
op|','
string|"'bytes'"
op|':'
string|"'1'"
op|'}'
op|','
nl|'\n'
op|'{'
string|"'name'"
op|':'
string|"'/d/b_2'"
op|','
string|"'hash'"
op|':'
string|"'b'"
op|','
string|"'bytes'"
op|':'
string|"'2'"
op|'}'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'req_method_paths'
op|'.'
name|'append'
op|'('
op|'('
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
op|','
nl|'\n'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|')'
op|')'
newline|'\n'
name|'if'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'.'
name|'endswith'
op|'('
string|"'/c/a_1'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'Response'
op|'('
name|'status'
op|'='
number|'401'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'Response'
op|'('
name|'status'
op|'='
number|'200'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Static-Large-Object'"
op|':'
string|"'True'"
op|'}'
op|','
nl|'\n'
name|'body'
op|'='
name|'good_data'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
dedent|''
name|'test_xml_data'
op|'='
string|'\'\'\'<?xml version="1.0" encoding="UTF-8"?>\n<static_large_object>\n<object_segment>\n<path>/cont/object</path>\n<etag>etagoftheobjectsegment</etag>\n<size_bytes>100</size_bytes>\n</object_segment>\n</static_large_object>\n\'\'\''
newline|'\n'
DECL|variable|test_json_data
name|'test_json_data'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
op|'['
op|'{'
string|"'path'"
op|':'
string|"'/cont/object'"
op|','
nl|'\n'
string|"'etag'"
op|':'
string|"'etagoftheobjectsegment'"
op|','
nl|'\n'
string|"'size_bytes'"
op|':'
number|'100'
op|'}'
op|']'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|fake_start_response
name|'def'
name|'fake_start_response'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestStaticLargeObject
dedent|''
name|'class'
name|'TestStaticLargeObject'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|setUp
indent|'    '
name|'def'
name|'setUp'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'app'
op|'='
name|'FakeApp'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'slo'
op|'='
name|'slo'
op|'.'
name|'filter_factory'
op|'('
op|'{'
op|'}'
op|')'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'slo'
op|'.'
name|'min_segment_size'
op|'='
number|'1'
newline|'\n'
nl|'\n'
DECL|member|tearDown
dedent|''
name|'def'
name|'tearDown'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|test_handle_multipart_no_obj
dedent|''
name|'def'
name|'test_handle_multipart_no_obj'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|')'
newline|'\n'
name|'resp_iter'
op|'='
name|'self'
op|'.'
name|'slo'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'fake_start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'calls'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
string|"''"
op|'.'
name|'join'
op|'('
name|'resp_iter'
op|')'
op|','
string|"'passed'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_parse_input
dedent|''
name|'def'
name|'test_parse_input'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'HTTPException'
op|','
name|'slo'
op|'.'
name|'parse_input'
op|','
string|"'some non json'"
op|')'
newline|'\n'
name|'data'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
nl|'\n'
op|'['
op|'{'
string|"'path'"
op|':'
string|"'/cont/object'"
op|','
string|"'etag'"
op|':'
string|"'etagoftheobjecitsegment'"
op|','
nl|'\n'
string|"'size_bytes'"
op|':'
number|'100'
op|'}'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
string|"'/cont/object'"
op|','
nl|'\n'
name|'slo'
op|'.'
name|'parse_input'
op|'('
name|'data'
op|')'
op|'['
number|'0'
op|']'
op|'['
string|"'path'"
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'bad_data'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
op|'['
op|'{'
string|"'path'"
op|':'
string|"'/cont/object'"
op|','
string|"'size_bytes'"
op|':'
number|'100'
op|'}'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'HTTPException'
op|','
name|'slo'
op|'.'
name|'parse_input'
op|','
name|'bad_data'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_put_manifest_too_quick_fail
dedent|''
name|'def'
name|'test_put_manifest_too_quick_fail'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v/a/c/o'"
op|')'
newline|'\n'
name|'req'
op|'.'
name|'content_length'
op|'='
name|'self'
op|'.'
name|'slo'
op|'.'
name|'max_manifest_size'
op|'+'
number|'1'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'slo'
op|'.'
name|'handle_multipart_put'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'HTTPException'
op|','
name|'e'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'e'
op|'.'
name|'status_int'
op|','
number|'413'
op|')'
newline|'\n'
nl|'\n'
name|'with'
name|'patch'
op|'.'
name|'object'
op|'('
name|'self'
op|'.'
name|'slo'
op|','
string|"'max_manifest_segments'"
op|','
number|'0'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v/a/c/o'"
op|','
name|'body'
op|'='
name|'test_json_data'
op|')'
newline|'\n'
name|'e'
op|'='
name|'None'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'slo'
op|'.'
name|'handle_multipart_put'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'HTTPException'
op|','
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'e'
op|'.'
name|'status_int'
op|','
number|'413'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'with'
name|'patch'
op|'.'
name|'object'
op|'('
name|'self'
op|'.'
name|'slo'
op|','
string|"'min_segment_size'"
op|','
number|'1000'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v/a/c/o'"
op|','
name|'body'
op|'='
name|'test_json_data'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'slo'
op|'.'
name|'handle_multipart_put'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'HTTPException'
op|','
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'e'
op|'.'
name|'status_int'
op|','
number|'400'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v/a/c/o'"
op|','
name|'headers'
op|'='
op|'{'
string|"'X-Copy-From'"
op|':'
string|"'lala'"
op|'}'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'slo'
op|'.'
name|'handle_multipart_put'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'HTTPException'
op|','
name|'e'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'e'
op|'.'
name|'status_int'
op|','
number|'405'
op|')'
newline|'\n'
nl|'\n'
comment|'# ignores requests to /'
nl|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/?multipart-manifest=put'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
op|','
name|'body'
op|'='
name|'test_json_data'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'slo'
op|'.'
name|'handle_multipart_put'
op|'('
name|'req'
op|')'
op|','
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_handle_multipart_put_success
dedent|''
name|'def'
name|'test_handle_multipart_put_success'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/test_good/AUTH_test/c/man?multipart-manifest=put'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
op|','
name|'headers'
op|'='
op|'{'
string|"'Accept'"
op|':'
string|"'test'"
op|'}'
op|','
nl|'\n'
name|'body'
op|'='
name|'test_json_data'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'X-Static-Large-Object'"
name|'not'
name|'in'
name|'req'
op|'.'
name|'headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'slo'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'fake_start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'X-Static-Large-Object'"
name|'in'
name|'req'
op|'.'
name|'headers'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_handle_multipart_put_success_allow_small_last_segment
dedent|''
name|'def'
name|'test_handle_multipart_put_success_allow_small_last_segment'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'with'
name|'patch'
op|'.'
name|'object'
op|'('
name|'self'
op|'.'
name|'slo'
op|','
string|"'min_segment_size'"
op|','
number|'50'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'test_json_data'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
op|'['
op|'{'
string|"'path'"
op|':'
string|"'/cont/object'"
op|','
nl|'\n'
string|"'etag'"
op|':'
string|"'etagoftheobjectsegment'"
op|','
nl|'\n'
string|"'size_bytes'"
op|':'
number|'100'
op|'}'
op|','
nl|'\n'
op|'{'
string|"'path'"
op|':'
string|"'/cont/small_object'"
op|','
nl|'\n'
string|"'etag'"
op|':'
string|"'etagoftheobjectsegment'"
op|','
nl|'\n'
string|"'size_bytes'"
op|':'
number|'10'
op|'}'
op|']'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/test_good/AUTH_test/c/man?multipart-manifest=put'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
op|','
name|'headers'
op|'='
op|'{'
string|"'Accept'"
op|':'
string|"'test'"
op|'}'
op|','
nl|'\n'
name|'body'
op|'='
name|'test_json_data'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'X-Static-Large-Object'"
name|'not'
name|'in'
name|'req'
op|'.'
name|'headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'slo'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'fake_start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'X-Static-Large-Object'"
name|'in'
name|'req'
op|'.'
name|'headers'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_handle_multipart_put_success_unicode
dedent|''
dedent|''
name|'def'
name|'test_handle_multipart_put_success_unicode'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'test_json_data'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
op|'['
op|'{'
string|"'path'"
op|':'
string|"u'/cont/object\\u2661'"
op|','
nl|'\n'
string|"'etag'"
op|':'
string|"'etagoftheobjectsegment'"
op|','
nl|'\n'
string|"'size_bytes'"
op|':'
number|'100'
op|'}'
op|']'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/test_good/AUTH_test/c/man?multipart-manifest=put'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
op|','
name|'headers'
op|'='
op|'{'
string|"'Accept'"
op|':'
string|"'test'"
op|'}'
op|','
nl|'\n'
name|'body'
op|'='
name|'test_json_data'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'X-Static-Large-Object'"
name|'not'
name|'in'
name|'req'
op|'.'
name|'headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'slo'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'fake_start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|"'X-Static-Large-Object'"
name|'in'
name|'req'
op|'.'
name|'headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'req'
op|'.'
name|'environ'
op|'['
string|"'PATH_INFO'"
op|']'
op|','
string|"'/cont/object\\xe2\\x99\\xa4'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_handle_multipart_put_no_xml
dedent|''
name|'def'
name|'test_handle_multipart_put_no_xml'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/test_good/AUTH_test/c/man?multipart-manifest=put'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
op|','
name|'headers'
op|'='
op|'{'
string|"'Accept'"
op|':'
string|"'test'"
op|'}'
op|','
nl|'\n'
name|'body'
op|'='
name|'test_xml_data'
op|')'
newline|'\n'
name|'no_xml'
op|'='
name|'self'
op|'.'
name|'slo'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'fake_start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'no_xml'
op|','
op|'['
string|"'Manifest must be valid json.'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_handle_multipart_put_bad_data
dedent|''
name|'def'
name|'test_handle_multipart_put_bad_data'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'bad_data'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
op|'['
op|'{'
string|"'path'"
op|':'
string|"'/cont/object'"
op|','
nl|'\n'
string|"'etag'"
op|':'
string|"'etagoftheobj'"
op|','
nl|'\n'
string|"'size_bytes'"
op|':'
string|"'lala'"
op|'}'
op|']'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/test_good/AUTH_test/c/man?multipart-manifest=put'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
op|','
name|'body'
op|'='
name|'bad_data'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'HTTPException'
op|','
name|'self'
op|'.'
name|'slo'
op|'.'
name|'handle_multipart_put'
op|','
name|'req'
op|')'
newline|'\n'
nl|'\n'
name|'for'
name|'bad_data'
name|'in'
op|'['
nl|'\n'
name|'json'
op|'.'
name|'dumps'
op|'('
op|'['
op|'{'
string|"'path'"
op|':'
string|"'/cont'"
op|','
string|"'etag'"
op|':'
string|"'etagoftheobj'"
op|','
nl|'\n'
string|"'size_bytes'"
op|':'
number|'100'
op|'}'
op|']'
op|')'
op|','
nl|'\n'
name|'json'
op|'.'
name|'dumps'
op|'('
string|"'asdf'"
op|')'
op|','
name|'json'
op|'.'
name|'dumps'
op|'('
name|'None'
op|')'
op|','
name|'json'
op|'.'
name|'dumps'
op|'('
number|'5'
op|')'
op|','
nl|'\n'
string|"'not json'"
op|','
string|"'1234'"
op|','
name|'None'
op|','
string|"''"
op|','
name|'json'
op|'.'
name|'dumps'
op|'('
op|'{'
string|"'path'"
op|':'
name|'None'
op|'}'
op|')'
op|','
nl|'\n'
name|'json'
op|'.'
name|'dumps'
op|'('
op|'['
op|'{'
string|"'path'"
op|':'
string|"'/c/o'"
op|','
string|"'etag'"
op|':'
name|'None'
op|','
nl|'\n'
string|"'size_bytes'"
op|':'
number|'12'
op|'}'
op|']'
op|')'
op|','
nl|'\n'
name|'json'
op|'.'
name|'dumps'
op|'('
op|'['
op|'{'
string|"'path'"
op|':'
string|"'/c/o'"
op|','
string|"'etag'"
op|':'
string|"'asdf'"
op|','
nl|'\n'
string|"'size_bytes'"
op|':'
string|"'sd'"
op|'}'
op|']'
op|')'
op|','
nl|'\n'
name|'json'
op|'.'
name|'dumps'
op|'('
op|'['
op|'{'
string|"'path'"
op|':'
number|'12'
op|','
string|"'etag'"
op|':'
string|"'etagoftheobj'"
op|','
nl|'\n'
string|"'size_bytes'"
op|':'
number|'100'
op|'}'
op|']'
op|')'
op|','
nl|'\n'
name|'json'
op|'.'
name|'dumps'
op|'('
op|'['
op|'{'
string|"'path'"
op|':'
string|"u'/cont/object\\u2661'"
op|','
nl|'\n'
string|"'etag'"
op|':'
string|"'etagoftheobj'"
op|','
string|"'size_bytes'"
op|':'
number|'100'
op|'}'
op|']'
op|')'
op|','
nl|'\n'
name|'json'
op|'.'
name|'dumps'
op|'('
op|'['
op|'{'
string|"'path'"
op|':'
number|'12'
op|','
string|"'size_bytes'"
op|':'
number|'100'
op|'}'
op|']'
op|')'
op|','
nl|'\n'
name|'json'
op|'.'
name|'dumps'
op|'('
op|'['
op|'{'
string|"'path'"
op|':'
number|'12'
op|','
string|"'size_bytes'"
op|':'
number|'100'
op|'}'
op|']'
op|')'
op|','
nl|'\n'
name|'json'
op|'.'
name|'dumps'
op|'('
op|'['
op|'{'
string|"'path'"
op|':'
name|'None'
op|','
string|"'etag'"
op|':'
string|"'etagoftheobj'"
op|','
nl|'\n'
string|"'size_bytes'"
op|':'
number|'100'
op|'}'
op|']'
op|')'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/test_good/AUTH_test/c/man?multipart-manifest=put'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
op|','
name|'body'
op|'='
name|'bad_data'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertRaises'
op|'('
name|'HTTPException'
op|','
name|'self'
op|'.'
name|'slo'
op|'.'
name|'handle_multipart_put'
op|','
nl|'\n'
name|'req'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_handle_multipart_put_check_data
dedent|''
dedent|''
name|'def'
name|'test_handle_multipart_put_check_data'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'good_data'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
nl|'\n'
op|'['
op|'{'
string|"'path'"
op|':'
string|"'/c/a_1'"
op|','
string|"'etag'"
op|':'
string|"'a'"
op|','
string|"'size_bytes'"
op|':'
string|"'1'"
op|'}'
op|','
nl|'\n'
op|'{'
string|"'path'"
op|':'
string|"'/d/b_2'"
op|','
string|"'etag'"
op|':'
string|"'b'"
op|','
string|"'size_bytes'"
op|':'
string|"'2'"
op|'}'
op|']'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/test_good_check/A/c/man?multipart-manifest=put'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
op|','
name|'body'
op|'='
name|'good_data'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'slo'
op|'.'
name|'handle_multipart_put'
op|'('
name|'req'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'calls'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'req'
op|'.'
name|'environ'
op|'['
string|"'CONTENT_TYPE'"
op|']'
op|'.'
name|'endswith'
op|'('
string|"';swift_bytes=3'"
op|')'
op|')'
newline|'\n'
name|'manifest_data'
op|'='
name|'json'
op|'.'
name|'loads'
op|'('
name|'req'
op|'.'
name|'environ'
op|'['
string|"'wsgi.input'"
op|']'
op|'.'
name|'read'
op|'('
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'len'
op|'('
name|'manifest_data'
op|')'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'manifest_data'
op|'['
number|'0'
op|']'
op|'['
string|"'hash'"
op|']'
op|','
string|"'a'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'manifest_data'
op|'['
number|'0'
op|']'
op|'['
string|"'bytes'"
op|']'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'not'
name|'manifest_data'
op|'['
number|'0'
op|']'
op|'['
string|"'last_modified'"
op|']'
op|'.'
name|'startswith'
op|'('
string|"'2012'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'manifest_data'
op|'['
number|'1'
op|']'
op|'['
string|"'last_modified'"
op|']'
op|'.'
name|'startswith'
op|'('
string|"'2012'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_handle_multipart_put_check_data_bad
dedent|''
name|'def'
name|'test_handle_multipart_put_check_data_bad'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'bad_data'
op|'='
name|'json'
op|'.'
name|'dumps'
op|'('
nl|'\n'
op|'['
op|'{'
string|"'path'"
op|':'
string|"'/c/a_1'"
op|','
string|"'etag'"
op|':'
string|"'a'"
op|','
string|"'size_bytes'"
op|':'
string|"'1'"
op|'}'
op|','
nl|'\n'
op|'{'
string|"'path'"
op|':'
string|"'/c/a_2'"
op|','
string|"'etag'"
op|':'
string|"'a'"
op|','
string|"'size_bytes'"
op|':'
string|"'1'"
op|'}'
op|','
nl|'\n'
op|'{'
string|"'path'"
op|':'
string|"'/d/b_2'"
op|','
string|"'etag'"
op|':'
string|"'b'"
op|','
string|"'size_bytes'"
op|':'
string|"'2'"
op|'}'
op|']'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/test_good/A/c/man?multipart-manifest=put'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Accept'"
op|':'
string|"'application/json'"
op|'}'
op|','
nl|'\n'
name|'body'
op|'='
name|'bad_data'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'slo'
op|'.'
name|'handle_multipart_put'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'HTTPException'
op|','
name|'e'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'calls'
op|','
number|'3'
op|')'
newline|'\n'
name|'data'
op|'='
name|'json'
op|'.'
name|'loads'
op|'('
name|'e'
op|'.'
name|'body'
op|')'
newline|'\n'
name|'errors'
op|'='
name|'data'
op|'['
string|"'Errors'"
op|']'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'errors'
op|'['
number|'0'
op|']'
op|'['
number|'0'
op|']'
op|','
string|"'/test_good/A/c/a_1'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'errors'
op|'['
number|'0'
op|']'
op|'['
number|'1'
op|']'
op|','
string|"'Size Mismatch'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'errors'
op|'['
number|'2'
op|']'
op|'['
number|'1'
op|']'
op|','
string|"'400 Bad Request'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'errors'
op|'['
op|'-'
number|'1'
op|']'
op|'['
number|'0'
op|']'
op|','
string|"'/test_good/A/d/b_2'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'errors'
op|'['
op|'-'
number|'1'
op|']'
op|'['
number|'1'
op|']'
op|','
string|"'Etag Mismatch'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assert_'
op|'('
name|'False'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_handle_multipart_delete_man
dedent|''
dedent|''
name|'def'
name|'test_handle_multipart_delete_man'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/test_good/A/c/man'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'DELETE'"
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'slo'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'fake_start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'calls'
op|','
number|'1'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_handle_multipart_delete_whole_404
dedent|''
name|'def'
name|'test_handle_multipart_delete_whole_404'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/test_delete_404/A/c/man?multipart-manifest=delete'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'DELETE'"
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'slo'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'fake_start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'calls'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'req_method_paths'
op|','
nl|'\n'
op|'['
op|'('
string|"'GET'"
op|','
string|"'/test_delete_404/A/c/man'"
op|')'
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_handle_multipart_delete_whole
dedent|''
name|'def'
name|'test_handle_multipart_delete_whole'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/test_delete/A/c/man?multipart-manifest=delete'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'DELETE'"
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'slo'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'fake_start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'calls'
op|','
number|'4'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'req_method_paths'
op|','
nl|'\n'
op|'['
op|'('
string|"'GET'"
op|','
string|"'/test_delete/A/c/man'"
op|')'
op|','
nl|'\n'
op|'('
string|"'DELETE'"
op|','
string|"'/test_delete/A/c/a_1'"
op|')'
op|','
nl|'\n'
op|'('
string|"'DELETE'"
op|','
string|"'/test_delete/A/d/b_2'"
op|')'
op|','
nl|'\n'
op|'('
string|"'DELETE'"
op|','
string|"'/test_delete/A/c/man'"
op|')'
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_handle_multipart_delete_bad_manifest
dedent|''
name|'def'
name|'test_handle_multipart_delete_bad_manifest'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/test_delete_bad_man/A/c/man?multipart-manifest=delete'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'DELETE'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'slo'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'fake_start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'calls'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'req_method_paths'
op|','
nl|'\n'
op|'['
op|'('
string|"'GET'"
op|','
string|"'/test_delete_bad_man/A/c/man'"
op|')'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|','
op|'['
string|"'Not an SLO manifest'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_handle_multipart_delete_bad_json
dedent|''
name|'def'
name|'test_handle_multipart_delete_bad_json'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/test_delete_bad_json/A/c/man?multipart-manifest=delete'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'DELETE'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'slo'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'fake_start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'calls'
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'req_method_paths'
op|','
nl|'\n'
op|'['
op|'('
string|"'GET'"
op|','
string|"'/test_delete_bad_json/A/c/man'"
op|')'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|','
op|'['
string|"'Invalid manifest file'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_handle_multipart_delete_whole_bad
dedent|''
name|'def'
name|'test_handle_multipart_delete_whole_bad'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
nl|'\n'
string|"'/test_delete_bad/A/c/man?multipart-manifest=delete'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'DELETE'"
op|'}'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'slo'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'fake_start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'calls'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'req_method_paths'
op|','
nl|'\n'
op|'['
op|'('
string|"'GET'"
op|','
string|"'/test_delete_bad/A/c/man'"
op|')'
op|','
nl|'\n'
op|'('
string|"'DELETE'"
op|','
string|"'/test_delete_bad/A/c/a_1'"
op|')'
op|']'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'if'
name|'__name__'
op|'=='
string|"'__main__'"
op|':'
newline|'\n'
indent|'    '
name|'unittest'
op|'.'
name|'main'
op|'('
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit