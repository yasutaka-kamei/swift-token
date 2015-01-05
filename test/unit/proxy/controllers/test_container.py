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
name|'mock'
newline|'\n'
name|'import'
name|'unittest'
newline|'\n'
nl|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'Timeout'
newline|'\n'
nl|'\n'
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
name|'proxy'
name|'import'
name|'server'
name|'as'
name|'proxy_server'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'base'
name|'import'
name|'headers_to_container_info'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
name|'import'
name|'fake_http_connect'
op|','
name|'FakeRing'
op|','
name|'FakeMemcache'
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
name|'request_helpers'
name|'import'
name|'get_sys_meta_prefix'
newline|'\n'
nl|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
name|'import'
name|'patch_policies'
op|','
name|'mocked_http_conn'
op|','
name|'debug_logger'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
op|'.'
name|'common'
op|'.'
name|'ring'
op|'.'
name|'test_ring'
name|'import'
name|'TestRingBase'
newline|'\n'
name|'from'
name|'test'
op|'.'
name|'unit'
op|'.'
name|'proxy'
op|'.'
name|'test_server'
name|'import'
name|'node_error_count'
newline|'\n'
nl|'\n'
nl|'\n'
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
name|'object_ring'
op|'='
name|'FakeRing'
op|'('
op|')'
op|')'
op|']'
op|')'
newline|'\n'
DECL|class|TestContainerController
name|'class'
name|'TestContainerController'
op|'('
name|'TestRingBase'
op|')'
op|':'
newline|'\n'
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
name|'TestRingBase'
op|'.'
name|'setUp'
op|'('
name|'self'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'='
name|'debug_logger'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'container_ring'
op|'='
name|'FakeRing'
op|'('
name|'max_more_nodes'
op|'='
number|'9'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'='
name|'proxy_server'
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
name|'self'
op|'.'
name|'logger'
op|','
nl|'\n'
name|'account_ring'
op|'='
name|'FakeRing'
op|'('
op|')'
op|','
nl|'\n'
name|'container_ring'
op|'='
name|'self'
op|'.'
name|'container_ring'
op|')'
newline|'\n'
nl|'\n'
name|'self'
op|'.'
name|'account_info'
op|'='
op|'{'
nl|'\n'
string|"'status'"
op|':'
number|'200'
op|','
nl|'\n'
string|"'container_count'"
op|':'
string|"'10'"
op|','
nl|'\n'
string|"'total_object_count'"
op|':'
string|"'100'"
op|','
nl|'\n'
string|"'bytes'"
op|':'
string|"'1000'"
op|','
nl|'\n'
string|"'meta'"
op|':'
op|'{'
op|'}'
op|','
nl|'\n'
string|"'sysmeta'"
op|':'
op|'{'
op|'}'
op|','
nl|'\n'
op|'}'
newline|'\n'
nl|'\n'
name|'class'
name|'FakeAccountInfoContainerController'
op|'('
nl|'\n'
DECL|class|FakeAccountInfoContainerController
name|'proxy_server'
op|'.'
name|'ContainerController'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|account_info
indent|'            '
name|'def'
name|'account_info'
op|'('
name|'controller'
op|','
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'patch_path'
op|'='
string|"'swift.proxy.controllers.base.get_info'"
newline|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
name|'patch_path'
op|')'
name|'as'
name|'mock_get_info'
op|':'
newline|'\n'
indent|'                    '
name|'mock_get_info'
op|'.'
name|'return_value'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'account_info'
op|')'
newline|'\n'
name|'return'
name|'super'
op|'('
name|'FakeAccountInfoContainerController'
op|','
nl|'\n'
name|'controller'
op|')'
op|'.'
name|'account_info'
op|'('
nl|'\n'
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'_orig_get_controller'
op|'='
name|'self'
op|'.'
name|'app'
op|'.'
name|'get_controller'
newline|'\n'
nl|'\n'
DECL|function|wrapped_get_controller
name|'def'
name|'wrapped_get_controller'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'swift.proxy.server.ContainerController'"
op|','
nl|'\n'
name|'new'
op|'='
name|'FakeAccountInfoContainerController'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'_orig_get_controller'
op|'('
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'app'
op|'.'
name|'get_controller'
op|'='
name|'wrapped_get_controller'
newline|'\n'
nl|'\n'
DECL|member|test_container_info_in_response_env
dedent|''
name|'def'
name|'test_container_info_in_response_env'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'controller'
op|'='
name|'proxy_server'
op|'.'
name|'ContainerController'
op|'('
name|'self'
op|'.'
name|'app'
op|','
string|"'a'"
op|','
string|"'c'"
op|')'
newline|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.http_connect'"
op|','
nl|'\n'
name|'fake_http_connect'
op|'('
number|'200'
op|','
number|'200'
op|','
name|'body'
op|'='
string|"''"
op|')'
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
string|"'/v1/a/c'"
op|','
op|'{'
string|"'PATH_INFO'"
op|':'
string|"'/v1/a/c'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'controller'
op|'.'
name|'HEAD'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEqual'
op|'('
number|'2'
op|','
name|'resp'
op|'.'
name|'status_int'
op|'//'
number|'100'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
string|'"swift.container/a/c"'
name|'in'
name|'resp'
op|'.'
name|'environ'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'headers_to_container_info'
op|'('
name|'resp'
op|'.'
name|'headers'
op|')'
op|','
nl|'\n'
name|'resp'
op|'.'
name|'environ'
op|'['
string|"'swift.container/a/c'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_swift_owner
dedent|''
name|'def'
name|'test_swift_owner'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'owner_headers'
op|'='
op|'{'
nl|'\n'
string|"'x-container-read'"
op|':'
string|"'value'"
op|','
string|"'x-container-write'"
op|':'
string|"'value'"
op|','
nl|'\n'
string|"'x-container-sync-key'"
op|':'
string|"'value'"
op|','
string|"'x-container-sync-to'"
op|':'
string|"'value'"
op|'}'
newline|'\n'
name|'controller'
op|'='
name|'proxy_server'
op|'.'
name|'ContainerController'
op|'('
name|'self'
op|'.'
name|'app'
op|','
string|"'a'"
op|','
string|"'c'"
op|')'
newline|'\n'
nl|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a/c'"
op|')'
newline|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.http_connect'"
op|','
nl|'\n'
name|'fake_http_connect'
op|'('
number|'200'
op|','
number|'200'
op|','
name|'headers'
op|'='
name|'owner_headers'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'controller'
op|'.'
name|'HEAD'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
number|'2'
op|','
name|'resp'
op|'.'
name|'status_int'
op|'//'
number|'100'
op|')'
newline|'\n'
name|'for'
name|'key'
name|'in'
name|'owner_headers'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'key'
name|'not'
name|'in'
name|'resp'
op|'.'
name|'headers'
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
string|"'/v1/a/c'"
op|','
name|'environ'
op|'='
op|'{'
string|"'swift_owner'"
op|':'
name|'True'
op|'}'
op|')'
newline|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.http_connect'"
op|','
nl|'\n'
name|'fake_http_connect'
op|'('
number|'200'
op|','
number|'200'
op|','
name|'headers'
op|'='
name|'owner_headers'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'controller'
op|'.'
name|'HEAD'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEquals'
op|'('
number|'2'
op|','
name|'resp'
op|'.'
name|'status_int'
op|'//'
number|'100'
op|')'
newline|'\n'
name|'for'
name|'key'
name|'in'
name|'owner_headers'
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
op|')'
newline|'\n'
nl|'\n'
DECL|member|_make_callback_func
dedent|''
dedent|''
name|'def'
name|'_make_callback_func'
op|'('
name|'self'
op|','
name|'context'
op|')'
op|':'
newline|'\n'
DECL|function|callback
indent|'        '
name|'def'
name|'callback'
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
op|','
name|'ssl'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'context'
op|'['
string|"'method'"
op|']'
op|'='
name|'method'
newline|'\n'
name|'context'
op|'['
string|"'path'"
op|']'
op|'='
name|'path'
newline|'\n'
name|'context'
op|'['
string|"'headers'"
op|']'
op|'='
name|'headers'
name|'or'
op|'{'
op|'}'
newline|'\n'
dedent|''
name|'return'
name|'callback'
newline|'\n'
nl|'\n'
DECL|member|test_sys_meta_headers_PUT
dedent|''
name|'def'
name|'test_sys_meta_headers_PUT'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# check that headers in sys meta namespace make it through'
nl|'\n'
comment|'# the container controller'
nl|'\n'
indent|'        '
name|'sys_meta_key'
op|'='
string|"'%stest'"
op|'%'
name|'get_sys_meta_prefix'
op|'('
string|"'container'"
op|')'
newline|'\n'
name|'sys_meta_key'
op|'='
name|'sys_meta_key'
op|'.'
name|'title'
op|'('
op|')'
newline|'\n'
name|'user_meta_key'
op|'='
string|"'X-Container-Meta-Test'"
newline|'\n'
name|'controller'
op|'='
name|'proxy_server'
op|'.'
name|'ContainerController'
op|'('
name|'self'
op|'.'
name|'app'
op|','
string|"'a'"
op|','
string|"'c'"
op|')'
newline|'\n'
nl|'\n'
name|'context'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'callback'
op|'='
name|'self'
op|'.'
name|'_make_callback_func'
op|'('
name|'context'
op|')'
newline|'\n'
name|'hdrs_in'
op|'='
op|'{'
name|'sys_meta_key'
op|':'
string|"'foo'"
op|','
nl|'\n'
name|'user_meta_key'
op|':'
string|"'bar'"
op|','
nl|'\n'
string|"'x-timestamp'"
op|':'
string|"'1.0'"
op|'}'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a/c'"
op|','
name|'headers'
op|'='
name|'hdrs_in'
op|')'
newline|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.http_connect'"
op|','
nl|'\n'
name|'fake_http_connect'
op|'('
number|'200'
op|','
number|'200'
op|','
name|'give_connect'
op|'='
name|'callback'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'controller'
op|'.'
name|'PUT'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'context'
op|'['
string|"'method'"
op|']'
op|','
string|"'PUT'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'sys_meta_key'
name|'in'
name|'context'
op|'['
string|"'headers'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'context'
op|'['
string|"'headers'"
op|']'
op|'['
name|'sys_meta_key'
op|']'
op|','
string|"'foo'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'user_meta_key'
name|'in'
name|'context'
op|'['
string|"'headers'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'context'
op|'['
string|"'headers'"
op|']'
op|'['
name|'user_meta_key'
op|']'
op|','
string|"'bar'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertNotEqual'
op|'('
name|'context'
op|'['
string|"'headers'"
op|']'
op|'['
string|"'x-timestamp'"
op|']'
op|','
string|"'1.0'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_sys_meta_headers_POST
dedent|''
name|'def'
name|'test_sys_meta_headers_POST'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# check that headers in sys meta namespace make it through'
nl|'\n'
comment|'# the container controller'
nl|'\n'
indent|'        '
name|'sys_meta_key'
op|'='
string|"'%stest'"
op|'%'
name|'get_sys_meta_prefix'
op|'('
string|"'container'"
op|')'
newline|'\n'
name|'sys_meta_key'
op|'='
name|'sys_meta_key'
op|'.'
name|'title'
op|'('
op|')'
newline|'\n'
name|'user_meta_key'
op|'='
string|"'X-Container-Meta-Test'"
newline|'\n'
name|'controller'
op|'='
name|'proxy_server'
op|'.'
name|'ContainerController'
op|'('
name|'self'
op|'.'
name|'app'
op|','
string|"'a'"
op|','
string|"'c'"
op|')'
newline|'\n'
name|'context'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'callback'
op|'='
name|'self'
op|'.'
name|'_make_callback_func'
op|'('
name|'context'
op|')'
newline|'\n'
name|'hdrs_in'
op|'='
op|'{'
name|'sys_meta_key'
op|':'
string|"'foo'"
op|','
nl|'\n'
name|'user_meta_key'
op|':'
string|"'bar'"
op|','
nl|'\n'
string|"'x-timestamp'"
op|':'
string|"'1.0'"
op|'}'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a/c'"
op|','
name|'headers'
op|'='
name|'hdrs_in'
op|')'
newline|'\n'
name|'with'
name|'mock'
op|'.'
name|'patch'
op|'('
string|"'swift.proxy.controllers.base.http_connect'"
op|','
nl|'\n'
name|'fake_http_connect'
op|'('
number|'200'
op|','
number|'200'
op|','
name|'give_connect'
op|'='
name|'callback'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'controller'
op|'.'
name|'POST'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'context'
op|'['
string|"'method'"
op|']'
op|','
string|"'POST'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'sys_meta_key'
name|'in'
name|'context'
op|'['
string|"'headers'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'context'
op|'['
string|"'headers'"
op|']'
op|'['
name|'sys_meta_key'
op|']'
op|','
string|"'foo'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'user_meta_key'
name|'in'
name|'context'
op|'['
string|"'headers'"
op|']'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'context'
op|'['
string|"'headers'"
op|']'
op|'['
name|'user_meta_key'
op|']'
op|','
string|"'bar'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertNotEqual'
op|'('
name|'context'
op|'['
string|"'headers'"
op|']'
op|'['
string|"'x-timestamp'"
op|']'
op|','
string|"'1.0'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_node_errors
dedent|''
name|'def'
name|'test_node_errors'
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
name|'sort_nodes'
op|'='
name|'lambda'
name|'n'
op|':'
name|'n'
newline|'\n'
nl|'\n'
name|'for'
name|'method'
name|'in'
op|'('
string|"'PUT'"
op|','
string|"'DELETE'"
op|','
string|"'POST'"
op|')'
op|':'
newline|'\n'
DECL|function|test_status_map
indent|'            '
name|'def'
name|'test_status_map'
op|'('
name|'statuses'
op|','
name|'expected'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'app'
op|'.'
name|'_error_limiting'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a/c'"
op|','
name|'method'
op|'='
name|'method'
op|')'
newline|'\n'
name|'with'
name|'mocked_http_conn'
op|'('
op|'*'
name|'statuses'
op|')'
name|'as'
name|'fake_conn'
op|':'
newline|'\n'
indent|'                    '
name|'print'
string|"'a'"
op|'*'
number|'50'
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
dedent|''
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'resp'
op|'.'
name|'status_int'
op|','
name|'expected'
op|')'
newline|'\n'
name|'for'
name|'req'
name|'in'
name|'fake_conn'
op|'.'
name|'requests'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'req'
op|'['
string|"'method'"
op|']'
op|','
name|'method'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assert_'
op|'('
name|'req'
op|'['
string|"'path'"
op|']'
op|'.'
name|'endswith'
op|'('
string|"'/a/c'"
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'base_status'
op|'='
op|'['
number|'201'
op|']'
op|'*'
number|'3'
newline|'\n'
comment|'# test happy path'
nl|'\n'
name|'test_status_map'
op|'('
name|'list'
op|'('
name|'base_status'
op|')'
op|','
number|'201'
op|')'
newline|'\n'
name|'for'
name|'i'
name|'in'
name|'range'
op|'('
number|'3'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'node_error_count'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'app'
op|','
name|'self'
op|'.'
name|'container_ring'
op|'.'
name|'devs'
op|'['
name|'i'
op|']'
op|')'
op|','
number|'0'
op|')'
newline|'\n'
comment|'# single node errors and test isolation'
nl|'\n'
dedent|''
name|'for'
name|'i'
name|'in'
name|'range'
op|'('
number|'3'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'status_list'
op|'='
name|'list'
op|'('
name|'base_status'
op|')'
newline|'\n'
name|'status_list'
op|'['
name|'i'
op|']'
op|'='
number|'503'
newline|'\n'
name|'status_list'
op|'.'
name|'append'
op|'('
number|'201'
op|')'
newline|'\n'
name|'test_status_map'
op|'('
name|'status_list'
op|','
number|'201'
op|')'
newline|'\n'
name|'for'
name|'j'
name|'in'
name|'range'
op|'('
number|'3'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'expected'
op|'='
number|'1'
name|'if'
name|'j'
op|'=='
name|'i'
name|'else'
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'node_error_count'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'app'
op|','
name|'self'
op|'.'
name|'container_ring'
op|'.'
name|'devs'
op|'['
name|'j'
op|']'
op|')'
op|','
name|'expected'
op|')'
newline|'\n'
comment|'# timeout'
nl|'\n'
dedent|''
dedent|''
name|'test_status_map'
op|'('
op|'('
number|'201'
op|','
name|'Timeout'
op|'('
op|')'
op|','
number|'201'
op|','
number|'201'
op|')'
op|','
number|'201'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'node_error_count'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'app'
op|','
name|'self'
op|'.'
name|'container_ring'
op|'.'
name|'devs'
op|'['
number|'1'
op|']'
op|')'
op|','
number|'1'
op|')'
newline|'\n'
nl|'\n'
comment|'# exception'
nl|'\n'
name|'test_status_map'
op|'('
op|'('
name|'Exception'
op|'('
string|"'kaboom!'"
op|')'
op|','
number|'201'
op|','
number|'201'
op|','
number|'201'
op|')'
op|','
number|'201'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'node_error_count'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'app'
op|','
name|'self'
op|'.'
name|'container_ring'
op|'.'
name|'devs'
op|'['
number|'0'
op|']'
op|')'
op|','
number|'1'
op|')'
newline|'\n'
nl|'\n'
comment|'# insufficient storage'
nl|'\n'
name|'test_status_map'
op|'('
op|'('
number|'201'
op|','
number|'201'
op|','
number|'507'
op|','
number|'201'
op|')'
op|','
number|'201'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEqual'
op|'('
name|'node_error_count'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'app'
op|','
name|'self'
op|'.'
name|'container_ring'
op|'.'
name|'devs'
op|'['
number|'2'
op|']'
op|')'
op|','
nl|'\n'
name|'self'
op|'.'
name|'app'
op|'.'
name|'error_suppression_limit'
op|'+'
number|'1'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
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
