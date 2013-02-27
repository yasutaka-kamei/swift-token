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
name|'unittest'
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
op|','
name|'Response'
op|','
name|'HTTPUnauthorized'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'middleware'
name|'import'
name|'container_quotas'
newline|'\n'
nl|'\n'
DECL|class|FakeCache
name|'class'
name|'FakeCache'
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
op|','
name|'val'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
string|"'status'"
name|'not'
name|'in'
name|'val'
op|':'
newline|'\n'
indent|'            '
name|'val'
op|'['
string|"'status'"
op|']'
op|'='
number|'200'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'val'
op|'='
name|'val'
newline|'\n'
nl|'\n'
DECL|member|get
dedent|''
name|'def'
name|'get'
op|'('
name|'self'
op|','
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'self'
op|'.'
name|'val'
newline|'\n'
nl|'\n'
DECL|class|FakeApp
dedent|''
dedent|''
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
name|'env'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'start_response'
op|'('
string|"'200 OK'"
op|','
op|'['
op|']'
op|')'
newline|'\n'
name|'return'
op|'['
op|']'
newline|'\n'
nl|'\n'
DECL|class|FakeMissingApp
dedent|''
dedent|''
name|'class'
name|'FakeMissingApp'
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
name|'env'
op|','
name|'start_response'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'start_response'
op|'('
string|"'404 Not Found'"
op|','
op|'['
op|']'
op|')'
newline|'\n'
name|'return'
op|'['
op|']'
newline|'\n'
nl|'\n'
DECL|function|start_response
dedent|''
dedent|''
name|'def'
name|'start_response'
op|'('
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'pass'
newline|'\n'
nl|'\n'
DECL|class|TestContainerQuotas
dedent|''
name|'class'
name|'TestContainerQuotas'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_not_handled
indent|'    '
name|'def'
name|'test_not_handled'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'container_quotas'
op|'.'
name|'ContainerQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
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
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'res'
op|'.'
name|'status_int'
op|','
number|'200'
op|')'
newline|'\n'
nl|'\n'
name|'app'
op|'='
name|'container_quotas'
op|'.'
name|'ContainerQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a/c/o'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'res'
op|'.'
name|'status_int'
op|','
number|'200'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_no_quotas
dedent|''
name|'def'
name|'test_no_quotas'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'container_quotas'
op|'.'
name|'ContainerQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a/c/o'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|','
string|"'swift.cache'"
op|':'
name|'FakeCache'
op|'('
op|'{'
op|'}'
op|')'
op|','
nl|'\n'
string|"'CONTENT_LENGTH'"
op|':'
string|"'100'"
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'res'
op|'.'
name|'status_int'
op|','
number|'200'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_exceed_bytes_quota
dedent|''
name|'def'
name|'test_exceed_bytes_quota'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'container_quotas'
op|'.'
name|'ContainerQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
op|'{'
string|"'bytes'"
op|':'
number|'0'
op|','
string|"'meta'"
op|':'
op|'{'
string|"'quota-bytes'"
op|':'
string|"'2'"
op|'}'
op|'}'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a/c/o'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|','
string|"'swift.cache'"
op|':'
name|'cache'
op|','
nl|'\n'
string|"'CONTENT_LENGTH'"
op|':'
string|"'100'"
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'res'
op|'.'
name|'status_int'
op|','
number|'413'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_not_exceed_bytes_quota
dedent|''
name|'def'
name|'test_not_exceed_bytes_quota'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'container_quotas'
op|'.'
name|'ContainerQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
op|'{'
string|"'bytes'"
op|':'
number|'0'
op|','
string|"'meta'"
op|':'
op|'{'
string|"'quota-bytes'"
op|':'
string|"'100'"
op|'}'
op|'}'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a/c/o'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|','
string|"'swift.cache'"
op|':'
name|'cache'
op|','
nl|'\n'
string|"'CONTENT_LENGTH'"
op|':'
string|"'100'"
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'res'
op|'.'
name|'status_int'
op|','
number|'200'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_exceed_counts_quota
dedent|''
name|'def'
name|'test_exceed_counts_quota'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'container_quotas'
op|'.'
name|'ContainerQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
op|'{'
string|"'object_count'"
op|':'
number|'1'
op|','
string|"'meta'"
op|':'
op|'{'
string|"'quota-count'"
op|':'
string|"'1'"
op|'}'
op|'}'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a/c/o'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|','
string|"'swift.cache'"
op|':'
name|'cache'
op|','
nl|'\n'
string|"'CONTENT_LENGTH'"
op|':'
string|"'100'"
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'res'
op|'.'
name|'status_int'
op|','
number|'413'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_not_exceed_counts_quota
dedent|''
name|'def'
name|'test_not_exceed_counts_quota'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'container_quotas'
op|'.'
name|'ContainerQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
op|'{'
string|"'object_count'"
op|':'
number|'1'
op|','
string|"'meta'"
op|':'
op|'{'
string|"'quota-count'"
op|':'
string|"'2'"
op|'}'
op|'}'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a/c/o'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|','
string|"'swift.cache'"
op|':'
name|'cache'
op|','
nl|'\n'
string|"'CONTENT_LENGTH'"
op|':'
string|"'100'"
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'res'
op|'.'
name|'status_int'
op|','
number|'200'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_invalid_quotas
dedent|''
name|'def'
name|'test_invalid_quotas'
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
string|"'/v1/a/c'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'POST'"
op|','
nl|'\n'
string|"'HTTP_X_CONTAINER_META_QUOTA_BYTES'"
op|':'
string|"'abc'"
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
nl|'\n'
name|'container_quotas'
op|'.'
name|'ContainerQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'res'
op|'.'
name|'status_int'
op|','
number|'400'
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
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'POST'"
op|','
nl|'\n'
string|"'HTTP_X_CONTAINER_META_QUOTA_COUNT'"
op|':'
string|"'abc'"
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
nl|'\n'
name|'container_quotas'
op|'.'
name|'ContainerQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'res'
op|'.'
name|'status_int'
op|','
number|'400'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_valid_quotas
dedent|''
name|'def'
name|'test_valid_quotas'
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
string|"'/v1/a/c'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'POST'"
op|','
nl|'\n'
string|"'HTTP_X_CONTAINER_META_QUOTA_BYTES'"
op|':'
string|"'123'"
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
nl|'\n'
name|'container_quotas'
op|'.'
name|'ContainerQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'res'
op|'.'
name|'status_int'
op|','
number|'200'
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
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'POST'"
op|','
nl|'\n'
string|"'HTTP_X_CONTAINER_META_QUOTA_COUNT'"
op|':'
string|"'123'"
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
nl|'\n'
name|'container_quotas'
op|'.'
name|'ContainerQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'res'
op|'.'
name|'status_int'
op|','
number|'200'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_delete_quotas
dedent|''
name|'def'
name|'test_delete_quotas'
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
string|"'/v1/a/c'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'POST'"
op|','
nl|'\n'
string|"'HTTP_X_CONTAINER_META_QUOTA_BYTES'"
op|':'
name|'None'
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
nl|'\n'
name|'container_quotas'
op|'.'
name|'ContainerQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'res'
op|'.'
name|'status_int'
op|','
number|'200'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_missing_container
dedent|''
name|'def'
name|'test_missing_container'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'container_quotas'
op|'.'
name|'ContainerQuotaMiddleware'
op|'('
name|'FakeMissingApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
op|'{'
string|"'bytes'"
op|':'
number|'0'
op|','
string|"'meta'"
op|':'
op|'{'
string|"'quota-bytes'"
op|':'
string|"'100'"
op|'}'
op|'}'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a/c/o'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|','
string|"'swift.cache'"
op|':'
name|'cache'
op|','
nl|'\n'
string|"'CONTENT_LENGTH'"
op|':'
string|"'100'"
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'res'
op|'.'
name|'status_int'
op|','
number|'404'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_auth_fail
dedent|''
name|'def'
name|'test_auth_fail'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'app'
op|'='
name|'container_quotas'
op|'.'
name|'ContainerQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
op|'{'
string|"'object_count'"
op|':'
number|'1'
op|','
string|"'meta'"
op|':'
op|'{'
string|"'quota-count'"
op|':'
string|"'1'"
op|'}'
op|','
nl|'\n'
string|"'write_acl'"
op|':'
name|'None'
op|'}'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a/c/o'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|','
string|"'swift.cache'"
op|':'
name|'cache'
op|','
nl|'\n'
string|"'CONTENT_LENGTH'"
op|':'
string|"'100'"
op|','
nl|'\n'
string|"'swift.authorize'"
op|':'
name|'lambda'
op|'*'
name|'args'
op|':'
name|'HTTPUnauthorized'
op|'('
op|')'
op|'}'
op|')'
newline|'\n'
name|'res'
op|'='
name|'req'
op|'.'
name|'get_response'
op|'('
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'res'
op|'.'
name|'status_int'
op|','
number|'401'
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
