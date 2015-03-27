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
name|'import'
name|'unittest'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'from'
name|'tempfile'
name|'import'
name|'mkdtemp'
newline|'\n'
name|'from'
name|'urllib'
name|'import'
name|'quote'
newline|'\n'
name|'import'
name|'shutil'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'storage_policy'
name|'import'
name|'StoragePolicy'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'Request'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'mkdirs'
op|','
name|'split_path'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'wsgi'
name|'import'
name|'monkey_patch_mimetools'
op|','
name|'WSGIContext'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'obj'
name|'import'
name|'server'
name|'as'
name|'object_server'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'proxy'
name|'import'
name|'server'
name|'as'
name|'proxy'
newline|'\n'
name|'import'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
name|'import'
name|'FakeMemcache'
op|','
name|'debug_logger'
op|','
name|'FakeRing'
op|','
name|'fake_http_connect'
op|','
name|'patch_policies'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FakeServerConnection
name|'class'
name|'FakeServerConnection'
op|'('
name|'WSGIContext'
op|')'
op|':'
newline|'\n'
indent|'    '
string|"'''Fakes an HTTPConnection to a server instance.'''"
newline|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'super'
op|'('
name|'FakeServerConnection'
op|','
name|'self'
op|')'
op|'.'
name|'__init__'
op|'('
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'data'
op|'='
string|"''"
newline|'\n'
nl|'\n'
DECL|member|getheaders
dedent|''
name|'def'
name|'getheaders'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'self'
op|'.'
name|'_response_headers'
newline|'\n'
nl|'\n'
DECL|member|read
dedent|''
name|'def'
name|'read'
op|'('
name|'self'
op|','
name|'amt'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'result'
op|'='
name|'self'
op|'.'
name|'resp_iter'
op|'.'
name|'next'
op|'('
op|')'
newline|'\n'
name|'return'
name|'result'
newline|'\n'
dedent|''
name|'except'
name|'StopIteration'
op|':'
newline|'\n'
indent|'            '
name|'return'
string|"''"
newline|'\n'
nl|'\n'
DECL|member|getheader
dedent|''
dedent|''
name|'def'
name|'getheader'
op|'('
name|'self'
op|','
name|'name'
op|','
name|'default'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'result'
op|'='
name|'self'
op|'.'
name|'_response_header_value'
op|'('
name|'name'
op|')'
newline|'\n'
name|'return'
name|'result'
name|'if'
name|'result'
name|'else'
name|'default'
newline|'\n'
nl|'\n'
DECL|member|getresponse
dedent|''
name|'def'
name|'getresponse'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
name|'self'
op|'.'
name|'method'
op|'}'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'self'
op|'.'
name|'path'
op|','
name|'environ'
op|','
name|'headers'
op|'='
name|'self'
op|'.'
name|'req_headers'
op|','
nl|'\n'
name|'body'
op|'='
name|'self'
op|'.'
name|'data'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'data'
op|'='
string|"''"
newline|'\n'
name|'self'
op|'.'
name|'resp'
op|'='
name|'self'
op|'.'
name|'_app_call'
op|'('
name|'req'
op|'.'
name|'environ'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'resp_iter'
op|'='
name|'iter'
op|'('
name|'self'
op|'.'
name|'resp'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'_response_headers'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_response_headers'
op|'='
op|'['
op|']'
newline|'\n'
dedent|''
name|'status_parts'
op|'='
name|'self'
op|'.'
name|'_response_status'
op|'.'
name|'split'
op|'('
string|"' '"
op|','
number|'1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'status'
op|'='
name|'int'
op|'('
name|'status_parts'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'reason'
op|'='
name|'status_parts'
op|'['
number|'1'
op|']'
name|'if'
name|'len'
op|'('
name|'status_parts'
op|')'
op|'=='
number|'2'
name|'else'
string|"''"
newline|'\n'
name|'return'
name|'self'
newline|'\n'
nl|'\n'
DECL|member|getexpect
dedent|''
name|'def'
name|'getexpect'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
DECL|class|ContinueResponse
indent|'        '
name|'class'
name|'ContinueResponse'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|variable|status
indent|'            '
name|'status'
op|'='
number|'100'
newline|'\n'
dedent|''
name|'return'
name|'ContinueResponse'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|send
dedent|''
name|'def'
name|'send'
op|'('
name|'self'
op|','
name|'data'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'data'
op|'+='
name|'data'
newline|'\n'
nl|'\n'
DECL|member|close
dedent|''
name|'def'
name|'close'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|__call__
dedent|''
name|'def'
name|'__call__'
op|'('
name|'self'
op|','
name|'ipaddr'
op|','
name|'port'
op|','
name|'device'
op|','
name|'partition'
op|','
name|'method'
op|','
name|'path'
op|','
nl|'\n'
name|'headers'
op|'='
name|'None'
op|','
name|'query_string'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'path'
op|'='
name|'quote'
op|'('
string|"'/'"
op|'+'
name|'device'
op|'+'
string|"'/'"
op|'+'
name|'str'
op|'('
name|'partition'
op|')'
op|'+'
name|'path'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'method'
op|'='
name|'method'
newline|'\n'
name|'self'
op|'.'
name|'req_headers'
op|'='
name|'headers'
newline|'\n'
name|'return'
name|'self'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_http_connect
dedent|''
dedent|''
name|'def'
name|'get_http_connect'
op|'('
name|'account_func'
op|','
name|'container_func'
op|','
name|'object_func'
op|')'
op|':'
newline|'\n'
indent|'    '
string|"'''Returns a http_connect function that delegates to\n    entity-specific http_connect methods based on request path.\n    '''"
newline|'\n'
DECL|function|http_connect
name|'def'
name|'http_connect'
op|'('
name|'ipaddr'
op|','
name|'port'
op|','
name|'device'
op|','
name|'partition'
op|','
name|'method'
op|','
name|'path'
op|','
nl|'\n'
name|'headers'
op|'='
name|'None'
op|','
name|'query_string'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'a'
op|','
name|'c'
op|','
name|'o'
op|'='
name|'split_path'
op|'('
name|'path'
op|','
number|'1'
op|','
number|'3'
op|','
name|'True'
op|')'
newline|'\n'
name|'if'
name|'o'
op|':'
newline|'\n'
indent|'            '
name|'func'
op|'='
name|'object_func'
newline|'\n'
dedent|''
name|'elif'
name|'c'
op|':'
newline|'\n'
indent|'            '
name|'func'
op|'='
name|'container_func'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'func'
op|'='
name|'account_func'
newline|'\n'
dedent|''
name|'resp'
op|'='
name|'func'
op|'('
name|'ipaddr'
op|','
name|'port'
op|','
name|'device'
op|','
name|'partition'
op|','
name|'method'
op|','
name|'path'
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|','
name|'query_string'
op|'='
name|'query_string'
op|')'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'http_connect'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
op|'@'
name|'patch_policies'
op|'('
op|'['
name|'StoragePolicy'
op|'('
number|'0'
op|','
string|"'zero'"
op|','
name|'True'
op|','
nl|'\n'
name|'object_ring'
op|'='
name|'FakeRing'
op|'('
name|'replicas'
op|'='
number|'1'
op|')'
op|')'
op|']'
op|')'
newline|'\n'
DECL|class|TestObjectSysmeta
name|'class'
name|'TestObjectSysmeta'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
indent|'    '
string|"'''Tests object sysmeta is correctly handled by combination\n    of proxy server and object server.\n    '''"
newline|'\n'
DECL|member|_assertStatus
name|'def'
name|'_assertStatus'
op|'('
name|'self'
op|','
name|'resp'
op|','
name|'expected'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status_int'
op|','
name|'expected'
op|','
nl|'\n'
string|"'Expected %d, got %s'"
nl|'\n'
op|'%'
op|'('
name|'expected'
op|','
name|'resp'
op|'.'
name|'status'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_assertInHeaders
dedent|''
name|'def'
name|'_assertInHeaders'
op|'('
name|'self'
op|','
name|'resp'
op|','
name|'expected'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'key'
op|','
name|'val'
name|'in'
name|'expected'
op|'.'
name|'iteritems'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'key'
name|'in'
name|'resp'
op|'.'
name|'headers'
op|','
nl|'\n'
string|"'Header %s missing from %s'"
op|'%'
op|'('
name|'key'
op|','
name|'resp'
op|'.'
name|'headers'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'val'
op|','
name|'resp'
op|'.'
name|'headers'
op|'['
name|'key'
op|']'
op|','
nl|'\n'
string|"'Expected header %s:%s, got %s:%s'"
nl|'\n'
op|'%'
op|'('
name|'key'
op|','
name|'val'
op|','
name|'key'
op|','
name|'resp'
op|'.'
name|'headers'
op|'['
name|'key'
op|']'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_assertNotInHeaders
dedent|''
dedent|''
name|'def'
name|'_assertNotInHeaders'
op|'('
name|'self'
op|','
name|'resp'
op|','
name|'unexpected'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'key'
op|','
name|'val'
name|'in'
name|'unexpected'
op|'.'
name|'iteritems'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'key'
name|'in'
name|'resp'
op|'.'
name|'headers'
op|','
nl|'\n'
string|"'Header %s not expected in %s'"
nl|'\n'
op|'%'
op|'('
name|'key'
op|','
name|'resp'
op|'.'
name|'headers'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|setUp
dedent|''
dedent|''
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
name|'proxy'
op|'.'
name|'Application'
op|'('
name|'None'
op|','
name|'FakeMemcache'
op|'('
op|')'
op|','
nl|'\n'
name|'logger'
op|'='
name|'debug_logger'
op|'('
string|"'proxy-ut'"
op|')'
op|','
nl|'\n'
name|'account_ring'
op|'='
name|'FakeRing'
op|'('
name|'replicas'
op|'='
number|'1'
op|')'
op|','
nl|'\n'
name|'container_ring'
op|'='
name|'FakeRing'
op|'('
name|'replicas'
op|'='
number|'1'
op|')'
op|')'
newline|'\n'
name|'monkey_patch_mimetools'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'tmpdir'
op|'='
name|'mkdtemp'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'testdir'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'tmpdir'
op|','
nl|'\n'
string|"'tmp_test_object_server_ObjectController'"
op|')'
newline|'\n'
name|'mkdirs'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'testdir'
op|','
string|"'sda'"
op|','
string|"'tmp'"
op|')'
op|')'
newline|'\n'
name|'conf'
op|'='
op|'{'
string|"'devices'"
op|':'
name|'self'
op|'.'
name|'testdir'
op|','
string|"'mount_check'"
op|':'
string|"'false'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'obj_ctlr'
op|'='
name|'object_server'
op|'.'
name|'ObjectController'
op|'('
nl|'\n'
name|'conf'
op|','
name|'logger'
op|'='
name|'debug_logger'
op|'('
string|"'obj-ut'"
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'http_connect'
op|'='
name|'get_http_connect'
op|'('
name|'fake_http_connect'
op|'('
number|'200'
op|')'
op|','
nl|'\n'
name|'fake_http_connect'
op|'('
number|'200'
op|')'
op|','
nl|'\n'
name|'FakeServerConnection'
op|'('
name|'self'
op|'.'
name|'obj_ctlr'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'orig_base_http_connect'
op|'='
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'base'
op|'.'
name|'http_connect'
newline|'\n'
name|'self'
op|'.'
name|'orig_obj_http_connect'
op|'='
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'obj'
op|'.'
name|'http_connect'
newline|'\n'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'base'
op|'.'
name|'http_connect'
op|'='
name|'http_connect'
newline|'\n'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'obj'
op|'.'
name|'http_connect'
op|'='
name|'http_connect'
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
name|'shutil'
op|'.'
name|'rmtree'
op|'('
name|'self'
op|'.'
name|'tmpdir'
op|')'
newline|'\n'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'base'
op|'.'
name|'http_connect'
op|'='
name|'self'
op|'.'
name|'orig_base_http_connect'
newline|'\n'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'obj'
op|'.'
name|'http_connect'
op|'='
name|'self'
op|'.'
name|'orig_obj_http_connect'
newline|'\n'
nl|'\n'
DECL|variable|original_sysmeta_headers_1
dedent|''
name|'original_sysmeta_headers_1'
op|'='
op|'{'
string|"'x-object-sysmeta-test0'"
op|':'
string|"'val0'"
op|','
nl|'\n'
string|"'x-object-sysmeta-test1'"
op|':'
string|"'val1'"
op|'}'
newline|'\n'
DECL|variable|original_sysmeta_headers_2
name|'original_sysmeta_headers_2'
op|'='
op|'{'
string|"'x-object-sysmeta-test2'"
op|':'
string|"'val2'"
op|'}'
newline|'\n'
DECL|variable|changed_sysmeta_headers
name|'changed_sysmeta_headers'
op|'='
op|'{'
string|"'x-object-sysmeta-test0'"
op|':'
string|"''"
op|','
nl|'\n'
string|"'x-object-sysmeta-test1'"
op|':'
string|"'val1 changed'"
op|'}'
newline|'\n'
DECL|variable|new_sysmeta_headers
name|'new_sysmeta_headers'
op|'='
op|'{'
string|"'x-object-sysmeta-test3'"
op|':'
string|"'val3'"
op|'}'
newline|'\n'
DECL|variable|original_meta_headers_1
name|'original_meta_headers_1'
op|'='
op|'{'
string|"'x-object-meta-test0'"
op|':'
string|"'meta0'"
op|','
nl|'\n'
string|"'x-object-meta-test1'"
op|':'
string|"'meta1'"
op|'}'
newline|'\n'
DECL|variable|original_meta_headers_2
name|'original_meta_headers_2'
op|'='
op|'{'
string|"'x-object-meta-test2'"
op|':'
string|"'meta2'"
op|'}'
newline|'\n'
DECL|variable|changed_meta_headers
name|'changed_meta_headers'
op|'='
op|'{'
string|"'x-object-meta-test0'"
op|':'
string|"''"
op|','
nl|'\n'
string|"'x-object-meta-test1'"
op|':'
string|"'meta1 changed'"
op|'}'
newline|'\n'
DECL|variable|new_meta_headers
name|'new_meta_headers'
op|'='
op|'{'
string|"'x-object-meta-test3'"
op|':'
string|"'meta3'"
op|'}'
newline|'\n'
DECL|variable|bad_headers
name|'bad_headers'
op|'='
op|'{'
string|"'x-account-sysmeta-test1'"
op|':'
string|"'bad1'"
op|'}'
newline|'\n'
nl|'\n'
DECL|member|test_PUT_sysmeta_then_GET
name|'def'
name|'test_PUT_sysmeta_then_GET'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'path'
op|'='
string|"'/v1/a/c/o'"
newline|'\n'
nl|'\n'
name|'env'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
newline|'\n'
name|'hdrs'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'original_sysmeta_headers_1'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'original_meta_headers_1'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'bad_headers'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
op|','
name|'environ'
op|'='
name|'env'
op|','
name|'headers'
op|'='
name|'hdrs'
op|','
name|'body'
op|'='
string|"'x'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertStatus'
op|'('
name|'resp'
op|','
number|'201'
op|')'
newline|'\n'
nl|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
op|','
name|'environ'
op|'='
op|'{'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertStatus'
op|'('
name|'resp'
op|','
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'original_sysmeta_headers_1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'original_meta_headers_1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertNotInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'bad_headers'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_PUT_sysmeta_then_HEAD
dedent|''
name|'def'
name|'test_PUT_sysmeta_then_HEAD'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'path'
op|'='
string|"'/v1/a/c/o'"
newline|'\n'
nl|'\n'
name|'env'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
newline|'\n'
name|'hdrs'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'original_sysmeta_headers_1'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'original_meta_headers_1'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'bad_headers'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
op|','
name|'environ'
op|'='
name|'env'
op|','
name|'headers'
op|'='
name|'hdrs'
op|','
name|'body'
op|'='
string|"'x'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertStatus'
op|'('
name|'resp'
op|','
number|'201'
op|')'
newline|'\n'
nl|'\n'
name|'env'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'HEAD'"
op|'}'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
op|','
name|'environ'
op|'='
name|'env'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertStatus'
op|'('
name|'resp'
op|','
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'original_sysmeta_headers_1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'original_meta_headers_1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertNotInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'bad_headers'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_sysmeta_replaced_by_PUT
dedent|''
name|'def'
name|'test_sysmeta_replaced_by_PUT'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'path'
op|'='
string|"'/v1/a/c/o'"
newline|'\n'
nl|'\n'
name|'env'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
newline|'\n'
name|'hdrs'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'original_sysmeta_headers_1'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'original_sysmeta_headers_2'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'original_meta_headers_1'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'original_meta_headers_2'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
op|','
name|'environ'
op|'='
name|'env'
op|','
name|'headers'
op|'='
name|'hdrs'
op|','
name|'body'
op|'='
string|"'x'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertStatus'
op|'('
name|'resp'
op|','
number|'201'
op|')'
newline|'\n'
nl|'\n'
name|'env'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
newline|'\n'
name|'hdrs'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'changed_sysmeta_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'new_sysmeta_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'changed_meta_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'new_meta_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'bad_headers'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
op|','
name|'environ'
op|'='
name|'env'
op|','
name|'headers'
op|'='
name|'hdrs'
op|','
name|'body'
op|'='
string|"'x'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertStatus'
op|'('
name|'resp'
op|','
number|'201'
op|')'
newline|'\n'
nl|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
op|','
name|'environ'
op|'='
op|'{'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertStatus'
op|'('
name|'resp'
op|','
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'changed_sysmeta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'new_sysmeta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertNotInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'original_sysmeta_headers_2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'changed_meta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'new_meta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertNotInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'original_meta_headers_2'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_test_sysmeta_not_updated_by_POST
dedent|''
name|'def'
name|'_test_sysmeta_not_updated_by_POST'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# check sysmeta is not changed by a POST but user meta is replaced'
nl|'\n'
indent|'        '
name|'path'
op|'='
string|"'/v1/a/c/o'"
newline|'\n'
nl|'\n'
name|'env'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
newline|'\n'
name|'hdrs'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'original_sysmeta_headers_1'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'original_meta_headers_1'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
op|','
name|'environ'
op|'='
name|'env'
op|','
name|'headers'
op|'='
name|'hdrs'
op|','
name|'body'
op|'='
string|"'x'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertStatus'
op|'('
name|'resp'
op|','
number|'201'
op|')'
newline|'\n'
nl|'\n'
name|'env'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'POST'"
op|'}'
newline|'\n'
name|'hdrs'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'changed_sysmeta_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'new_sysmeta_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'changed_meta_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'new_meta_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'bad_headers'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
op|','
name|'environ'
op|'='
name|'env'
op|','
name|'headers'
op|'='
name|'hdrs'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertStatus'
op|'('
name|'resp'
op|','
number|'202'
op|')'
newline|'\n'
nl|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
op|','
name|'environ'
op|'='
op|'{'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertStatus'
op|'('
name|'resp'
op|','
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'original_sysmeta_headers_1'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertNotInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'new_sysmeta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'changed_meta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'new_meta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertNotInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'bad_headers'
op|')'
newline|'\n'
nl|'\n'
name|'env'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
newline|'\n'
name|'hdrs'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'changed_sysmeta_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'new_sysmeta_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'bad_headers'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
op|','
name|'environ'
op|'='
name|'env'
op|','
name|'headers'
op|'='
name|'hdrs'
op|','
name|'body'
op|'='
string|"'x'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertStatus'
op|'('
name|'resp'
op|','
number|'201'
op|')'
newline|'\n'
nl|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
op|','
name|'environ'
op|'='
op|'{'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertStatus'
op|'('
name|'resp'
op|','
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'changed_sysmeta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'new_sysmeta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertNotInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'original_sysmeta_headers_2'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_sysmeta_not_updated_by_POST
dedent|''
name|'def'
name|'test_sysmeta_not_updated_by_POST'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'app'
op|'.'
name|'object_post_as_copy'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'_test_sysmeta_not_updated_by_POST'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_sysmeta_not_updated_by_POST_as_copy
dedent|''
name|'def'
name|'test_sysmeta_not_updated_by_POST_as_copy'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'app'
op|'.'
name|'object_post_as_copy'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'_test_sysmeta_not_updated_by_POST'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_sysmeta_updated_by_COPY
dedent|''
name|'def'
name|'test_sysmeta_updated_by_COPY'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# check sysmeta is updated by a COPY in same way as user meta'
nl|'\n'
indent|'        '
name|'path'
op|'='
string|"'/v1/a/c/o'"
newline|'\n'
name|'dest'
op|'='
string|"'/c/o2'"
newline|'\n'
name|'env'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
newline|'\n'
name|'hdrs'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'original_sysmeta_headers_1'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'original_sysmeta_headers_2'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'original_meta_headers_1'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'original_meta_headers_2'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
op|','
name|'environ'
op|'='
name|'env'
op|','
name|'headers'
op|'='
name|'hdrs'
op|','
name|'body'
op|'='
string|"'x'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertStatus'
op|'('
name|'resp'
op|','
number|'201'
op|')'
newline|'\n'
nl|'\n'
name|'env'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'COPY'"
op|'}'
newline|'\n'
name|'hdrs'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'changed_sysmeta_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'new_sysmeta_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'changed_meta_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'new_meta_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'bad_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
op|'{'
string|"'Destination'"
op|':'
name|'dest'
op|'}'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
op|','
name|'environ'
op|'='
name|'env'
op|','
name|'headers'
op|'='
name|'hdrs'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertStatus'
op|'('
name|'resp'
op|','
number|'201'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'changed_sysmeta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'new_sysmeta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'original_sysmeta_headers_2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'changed_meta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'new_meta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'original_meta_headers_2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertNotInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'bad_headers'
op|')'
newline|'\n'
nl|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a/c/o2'"
op|','
name|'environ'
op|'='
op|'{'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertStatus'
op|'('
name|'resp'
op|','
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'changed_sysmeta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'new_sysmeta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'original_sysmeta_headers_2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'changed_meta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'new_meta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'original_meta_headers_2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertNotInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'bad_headers'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_sysmeta_updated_by_COPY_from
dedent|''
name|'def'
name|'test_sysmeta_updated_by_COPY_from'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# check sysmeta is updated by a COPY in same way as user meta'
nl|'\n'
indent|'        '
name|'path'
op|'='
string|"'/v1/a/c/o'"
newline|'\n'
name|'env'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
newline|'\n'
name|'hdrs'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'original_sysmeta_headers_1'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'original_sysmeta_headers_2'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'original_meta_headers_1'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'original_meta_headers_2'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
op|','
name|'environ'
op|'='
name|'env'
op|','
name|'headers'
op|'='
name|'hdrs'
op|','
name|'body'
op|'='
string|"'x'"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertStatus'
op|'('
name|'resp'
op|','
number|'201'
op|')'
newline|'\n'
nl|'\n'
name|'env'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
newline|'\n'
name|'hdrs'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'changed_sysmeta_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'new_sysmeta_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'changed_meta_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'new_meta_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
name|'self'
op|'.'
name|'bad_headers'
op|')'
newline|'\n'
name|'hdrs'
op|'.'
name|'update'
op|'('
op|'{'
string|"'X-Copy-From'"
op|':'
string|"'/c/o'"
op|'}'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a/c/o2'"
op|','
name|'environ'
op|'='
name|'env'
op|','
name|'headers'
op|'='
name|'hdrs'
op|','
name|'body'
op|'='
string|"''"
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertStatus'
op|'('
name|'resp'
op|','
number|'201'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'changed_sysmeta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'new_sysmeta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'original_sysmeta_headers_2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'changed_meta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'new_meta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'original_meta_headers_2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertNotInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'bad_headers'
op|')'
newline|'\n'
nl|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a/c/o2'"
op|','
name|'environ'
op|'='
op|'{'
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertStatus'
op|'('
name|'resp'
op|','
number|'200'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'changed_sysmeta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'new_sysmeta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'original_sysmeta_headers_2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'changed_meta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'new_meta_headers'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'original_meta_headers_2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_assertNotInHeaders'
op|'('
name|'resp'
op|','
name|'self'
op|'.'
name|'bad_headers'
op|')'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
