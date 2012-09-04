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
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'middleware'
name|'import'
name|'domain_remap'
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
nl|'\n'
DECL|member|__call__
indent|'    '
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
name|'return'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
newline|'\n'
nl|'\n'
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
nl|'\n'
DECL|class|TestDomainRemap
dedent|''
name|'class'
name|'TestDomainRemap'
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
name|'domain_remap'
op|'.'
name|'DomainRemapMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
op|'{'
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_domain_remap_passthrough
dedent|''
name|'def'
name|'test_domain_remap_passthrough'
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
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'example.com'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|','
string|"'/'"
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'example.com:8080'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|','
string|"'/'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_domain_remap_account
dedent|''
name|'def'
name|'test_domain_remap_account'
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
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'AUTH_a.example.com'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|','
string|"'/v1/AUTH_a'"
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'AUTH-uuid.example.com'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|','
string|"'/v1/AUTH_uuid'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_domain_remap_account_container
dedent|''
name|'def'
name|'test_domain_remap_account_container'
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
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'c.AUTH_a.example.com'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|','
string|"'/v1/AUTH_a/c'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_domain_remap_extra_subdomains
dedent|''
name|'def'
name|'test_domain_remap_extra_subdomains'
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
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'x.y.c.AUTH_a.example.com'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|','
op|'['
string|"'Bad domain in host header'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_domain_remap_account_with_path_root
dedent|''
name|'def'
name|'test_domain_remap_account_with_path_root'
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
string|"'/v1'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'AUTH_a.example.com'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|','
string|"'/v1/AUTH_a'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_domain_remap_account_container_with_path_root
dedent|''
name|'def'
name|'test_domain_remap_account_container_with_path_root'
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
string|"'/v1'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'c.AUTH_a.example.com'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|','
string|"'/v1/AUTH_a/c'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_domain_remap_account_container_with_path
dedent|''
name|'def'
name|'test_domain_remap_account_container_with_path'
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
string|"'/obj'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'c.AUTH_a.example.com'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|','
string|"'/v1/AUTH_a/c/obj'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_domain_remap_account_container_with_path_root_and_path
dedent|''
name|'def'
name|'test_domain_remap_account_container_with_path_root_and_path'
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
string|"'/v1/obj'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'c.AUTH_a.example.com'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|','
string|"'/v1/AUTH_a/c/obj'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_domain_remap_account_matching_ending_not_domain
dedent|''
name|'def'
name|'test_domain_remap_account_matching_ending_not_domain'
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
string|"'/dontchange'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'c.aexample.com'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|','
string|"'/dontchange'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_domain_remap_configured_with_empty_storage_domain
dedent|''
name|'def'
name|'test_domain_remap_configured_with_empty_storage_domain'
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
name|'domain_remap'
op|'.'
name|'DomainRemapMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
nl|'\n'
op|'{'
string|"'storage_domain'"
op|':'
string|"''"
op|'}'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/test'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'c.AUTH_a.example.com'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|','
string|"'/test'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_domain_remap_configured_with_prefixes
dedent|''
name|'def'
name|'test_domain_remap_configured_with_prefixes'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'conf'
op|'='
op|'{'
string|"'reseller_prefixes'"
op|':'
string|"'PREFIX'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'='
name|'domain_remap'
op|'.'
name|'DomainRemapMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
name|'conf'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/test'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'c.prefix_uuid.example.com'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|','
string|"'/v1/PREFIX_uuid/c/test'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_domain_remap_configured_with_bad_prefixes
dedent|''
name|'def'
name|'test_domain_remap_configured_with_bad_prefixes'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'conf'
op|'='
op|'{'
string|"'reseller_prefixes'"
op|':'
string|"'UNKNOWN'"
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'='
name|'domain_remap'
op|'.'
name|'DomainRemapMiddleware'
op|'('
name|'FakeApp'
op|'('
op|')'
op|','
name|'conf'
op|')'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/test'"
op|','
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Host'"
op|':'
string|"'c.prefix_uuid.example.com'"
op|'}'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'req'
op|'.'
name|'environ'
op|','
name|'start_response'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'assertEquals'
op|'('
name|'resp'
op|','
string|"'/test'"
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
