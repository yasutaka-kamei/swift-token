begin_unit
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
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'middleware'
name|'import'
name|'account_quotas'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'controllers'
op|'.'
name|'base'
name|'import'
name|'_get_cache_key'
op|','
name|'headers_to_account_info'
op|','
name|'get_object_env_key'
op|','
name|'headers_to_object_info'
newline|'\n'
nl|'\n'
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
DECL|member|set
dedent|''
name|'def'
name|'set'
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
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FakeBadApp
dedent|''
dedent|''
name|'class'
name|'FakeBadApp'
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
name|'headers'
op|'='
op|'['
op|']'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'headers'
op|'='
name|'headers'
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
string|"'404 NotFound'"
op|','
name|'self'
op|'.'
name|'headers'
op|')'
newline|'\n'
name|'return'
op|'['
op|']'
newline|'\n'
nl|'\n'
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
op|','
name|'headers'
op|'='
op|'['
op|']'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'headers'
op|'='
name|'headers'
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
name|'if'
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
op|'=='
string|'"HEAD"'
name|'and'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'=='
string|"'/v1/a/c2/o2'"
op|':'
newline|'\n'
indent|'            '
name|'env_key'
op|'='
name|'get_object_env_key'
op|'('
string|"'a'"
op|','
string|"'c2'"
op|','
string|"'o2'"
op|')'
newline|'\n'
name|'env'
op|'['
name|'env_key'
op|']'
op|'='
name|'headers_to_object_info'
op|'('
name|'self'
op|'.'
name|'headers'
op|','
number|'200'
op|')'
newline|'\n'
name|'start_response'
op|'('
string|"'200 OK'"
op|','
name|'self'
op|'.'
name|'headers'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
op|'=='
string|'"HEAD"'
name|'and'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'=='
string|"'/v1/a/c2/o3'"
op|':'
newline|'\n'
indent|'            '
name|'start_response'
op|'('
string|"'404 Not Found'"
op|','
op|'['
op|']'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
comment|'# Cache the account_info (same as a real application)'
nl|'\n'
indent|'            '
name|'cache_key'
op|','
name|'env_key'
op|'='
name|'_get_cache_key'
op|'('
string|"'a'"
op|','
name|'None'
op|')'
newline|'\n'
name|'env'
op|'['
name|'env_key'
op|']'
op|'='
name|'headers_to_account_info'
op|'('
name|'self'
op|'.'
name|'headers'
op|','
number|'200'
op|')'
newline|'\n'
name|'start_response'
op|'('
string|"'200 OK'"
op|','
name|'self'
op|'.'
name|'headers'
op|')'
newline|'\n'
dedent|''
name|'return'
op|'['
op|']'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestAccountQuota
dedent|''
dedent|''
name|'class'
name|'TestAccountQuota'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|test_unauthorized
indent|'    '
name|'def'
name|'test_unauthorized'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'1000'"
op|')'
op|','
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
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
nl|'\n'
string|"'swift.cache'"
op|':'
name|'cache'
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
comment|'#Response code of 200 because authentication itself is not done here'
nl|'\n'
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
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'1000'"
op|')'
op|','
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
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
nl|'\n'
string|"'swift.cache'"
op|':'
name|'cache'
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
DECL|member|test_obj_request_ignores_attempt_to_set_quotas
dedent|''
name|'def'
name|'test_obj_request_ignores_attempt_to_set_quotas'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|"# If you try to set X-Account-Meta-* on an object, it's ignored, so"
nl|'\n'
comment|"# the quota middleware shouldn't complain about it even if we're not a"
nl|'\n'
comment|'# reseller admin.'
nl|'\n'
indent|'        '
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'1000'"
op|')'
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
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
name|'headers'
op|'='
op|'{'
string|"'X-Account-Meta-Quota-Bytes'"
op|':'
string|"'99999'"
op|'}'
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|','
nl|'\n'
string|"'swift.cache'"
op|':'
name|'cache'
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
DECL|member|test_container_request_ignores_attempt_to_set_quotas
dedent|''
name|'def'
name|'test_container_request_ignores_attempt_to_set_quotas'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# As with an object, if you try to set X-Account-Meta-* on a'
nl|'\n'
comment|"# container, it's ignored."
nl|'\n'
indent|'        '
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'1000'"
op|')'
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
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
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Account-Meta-Quota-Bytes'"
op|':'
string|"'99999'"
op|'}'
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|','
nl|'\n'
string|"'swift.cache'"
op|':'
name|'cache'
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
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'1000'"
op|')'
op|','
nl|'\n'
op|'('
string|"'x-account-meta-quota-bytes'"
op|','
string|"'0'"
op|')'
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
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
nl|'\n'
string|"'swift.cache'"
op|':'
name|'cache'
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
DECL|member|test_over_quota_obj_post_still_works
dedent|''
name|'def'
name|'test_over_quota_obj_post_still_works'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'1001'"
op|')'
op|','
nl|'\n'
op|'('
string|"'x-account-meta-quota-bytes'"
op|','
string|"'1000'"
op|')'
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
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
string|"'POST'"
op|','
nl|'\n'
string|"'HTTP_X_OBJECT_META_BERT'"
op|':'
string|"'ernie'"
op|','
nl|'\n'
string|"'swift.cache'"
op|':'
name|'cache'
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
DECL|member|test_exceed_bytes_quota_copy_from
dedent|''
name|'def'
name|'test_exceed_bytes_quota_copy_from'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'500'"
op|')'
op|','
nl|'\n'
op|'('
string|"'x-account-meta-quota-bytes'"
op|','
string|"'1000'"
op|')'
op|','
nl|'\n'
op|'('
string|"'content-length'"
op|','
string|"'1000'"
op|')'
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
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
nl|'\n'
string|"'swift.cache'"
op|':'
name|'cache'
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'x-copy-from'"
op|':'
string|"'/c2/o2'"
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
DECL|member|test_not_exceed_bytes_quota_copy_from
dedent|''
name|'def'
name|'test_not_exceed_bytes_quota_copy_from'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'0'"
op|')'
op|','
nl|'\n'
op|'('
string|"'x-account-meta-quota-bytes'"
op|','
string|"'1000'"
op|')'
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
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
nl|'\n'
string|"'swift.cache'"
op|':'
name|'cache'
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'x-copy-from'"
op|':'
string|"'/c2/o2'"
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
DECL|member|test_quota_copy_from_no_src
dedent|''
name|'def'
name|'test_quota_copy_from_no_src'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'0'"
op|')'
op|','
nl|'\n'
op|'('
string|"'x-account-meta-quota-bytes'"
op|','
string|"'1000'"
op|')'
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
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
nl|'\n'
string|"'swift.cache'"
op|':'
name|'cache'
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'x-copy-from'"
op|':'
string|"'/c2/o3'"
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
DECL|member|test_exceed_bytes_quota_reseller
dedent|''
name|'def'
name|'test_exceed_bytes_quota_reseller'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'1000'"
op|')'
op|','
nl|'\n'
op|'('
string|"'x-account-meta-quota-bytes'"
op|','
string|"'0'"
op|')'
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|','
nl|'\n'
string|"'swift.cache'"
op|':'
name|'cache'
op|','
nl|'\n'
string|"'reseller_request'"
op|':'
name|'True'
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
DECL|member|test_exceed_bytes_quota_reseller_copy_from
dedent|''
name|'def'
name|'test_exceed_bytes_quota_reseller_copy_from'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'1000'"
op|')'
op|','
nl|'\n'
op|'('
string|"'x-account-meta-quota-bytes'"
op|','
string|"'0'"
op|')'
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
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
nl|'\n'
string|"'swift.cache'"
op|':'
name|'cache'
op|','
nl|'\n'
string|"'reseller_request'"
op|':'
name|'True'
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'x-copy-from'"
op|':'
string|"'c2/o2'"
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
DECL|member|test_bad_application_quota
dedent|''
name|'def'
name|'test_bad_application_quota'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'['
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeBadApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
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
nl|'\n'
string|"'swift.cache'"
op|':'
name|'cache'
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
DECL|member|test_no_info_quota
dedent|''
name|'def'
name|'test_no_info_quota'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'['
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
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
nl|'\n'
string|"'swift.cache'"
op|':'
name|'cache'
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
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'1000'"
op|')'
op|','
nl|'\n'
op|'('
string|"'x-account-meta-quota-bytes'"
op|','
number|'2000'
op|')'
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
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
nl|'\n'
string|"'swift.cache'"
op|':'
name|'cache'
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
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'0'"
op|')'
op|','
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a'"
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
string|"'swift.cache'"
op|':'
name|'cache'
op|','
nl|'\n'
string|"'HTTP_X_ACCOUNT_META_QUOTA_BYTES'"
op|':'
string|"'abc'"
op|','
nl|'\n'
string|"'reseller_request'"
op|':'
name|'True'
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
number|'400'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_valid_quotas_admin
dedent|''
name|'def'
name|'test_valid_quotas_admin'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'0'"
op|')'
op|','
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a'"
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
string|"'swift.cache'"
op|':'
name|'cache'
op|','
nl|'\n'
string|"'HTTP_X_ACCOUNT_META_QUOTA_BYTES'"
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
number|'403'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_valid_quotas_reseller
dedent|''
name|'def'
name|'test_valid_quotas_reseller'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'0'"
op|')'
op|','
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a'"
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
string|"'swift.cache'"
op|':'
name|'cache'
op|','
nl|'\n'
string|"'HTTP_X_ACCOUNT_META_QUOTA_BYTES'"
op|':'
string|"'100'"
op|','
nl|'\n'
string|"'reseller_request'"
op|':'
name|'True'
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
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'0'"
op|')'
op|','
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a'"
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
string|"'swift.cache'"
op|':'
name|'cache'
op|','
nl|'\n'
string|"'HTTP_X_ACCOUNT_META_QUOTA_BYTES'"
op|':'
string|"''"
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
number|'403'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_delete_quotas_with_remove_header
dedent|''
name|'def'
name|'test_delete_quotas_with_remove_header'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'0'"
op|')'
op|','
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a'"
op|','
name|'environ'
op|'='
op|'{'
nl|'\n'
string|"'REQUEST_METHOD'"
op|':'
string|"'POST'"
op|','
nl|'\n'
string|"'swift.cache'"
op|':'
name|'cache'
op|','
nl|'\n'
string|"'HTTP_X_REMOVE_ACCOUNT_META_QUOTA_BYTES'"
op|':'
string|"'True'"
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
number|'403'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_delete_quotas_reseller
dedent|''
name|'def'
name|'test_delete_quotas_reseller'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'0'"
op|')'
op|','
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a'"
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
string|"'HTTP_X_ACCOUNT_META_QUOTA_BYTES'"
op|':'
string|"''"
op|','
nl|'\n'
string|"'reseller_request'"
op|':'
name|'True'
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
DECL|member|test_delete_quotas_with_remove_header_reseller
dedent|''
name|'def'
name|'test_delete_quotas_with_remove_header_reseller'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'0'"
op|')'
op|','
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/a'"
op|','
name|'environ'
op|'='
op|'{'
nl|'\n'
string|"'REQUEST_METHOD'"
op|':'
string|"'POST'"
op|','
nl|'\n'
string|"'swift.cache'"
op|':'
name|'cache'
op|','
nl|'\n'
string|"'HTTP_X_REMOVE_ACCOUNT_META_QUOTA_BYTES'"
op|':'
string|"'True'"
op|','
nl|'\n'
string|"'reseller_request'"
op|':'
name|'True'
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
DECL|member|test_invalid_request_exception
dedent|''
name|'def'
name|'test_invalid_request_exception'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'['
op|'('
string|"'x-account-bytes-used'"
op|','
string|"'1000'"
op|')'
op|','
op|']'
newline|'\n'
name|'app'
op|'='
name|'account_quotas'
op|'.'
name|'AccountQuotaMiddleware'
op|'('
name|'FakeApp'
op|'('
name|'headers'
op|')'
op|')'
newline|'\n'
name|'cache'
op|'='
name|'FakeCache'
op|'('
name|'None'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1'"
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|','
nl|'\n'
string|"'swift.cache'"
op|':'
name|'cache'
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
comment|'# Response code of 200 because authentication itself is not done here'
nl|'\n'
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
