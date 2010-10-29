begin_unit
comment|'# Copyright (c) 2010 OpenStack, LLC.'
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
name|'webob'
name|'import'
name|'Request'
newline|'\n'
name|'from'
name|'webob'
op|'.'
name|'exc'
name|'import'
name|'HTTPBadRequest'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DomainRemapMiddleware
name|'class'
name|'DomainRemapMiddleware'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Middleware that translates container and account parts of a domain to\n    path parameters that the proxy server understands.\n    \n    container.account.storageurl/object gets translated to\n    container.account.storageurl/path_root/account/container/object\n    \n    account.storageurl/path_root/container/object gets translated to\n    account.storageurl/path_root/account/container/object\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'app'
op|','
name|'conf'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'app'
op|'='
name|'app'
newline|'\n'
name|'self'
op|'.'
name|'storage_domain'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'storage_domain'"
op|','
string|"'example.com'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'path_root'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'path_root'"
op|','
string|"'v1'"
op|')'
op|'.'
name|'strip'
op|'('
string|"'/'"
op|')'
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
name|'given_domain'
op|'='
name|'env'
op|'['
string|"'HTTP_HOST'"
op|']'
newline|'\n'
name|'port'
op|'='
string|"''"
newline|'\n'
name|'if'
string|"':'"
name|'in'
name|'given_domain'
op|':'
newline|'\n'
indent|'            '
name|'given_domain'
op|','
name|'port'
op|'='
name|'given_domain'
op|'.'
name|'rsplit'
op|'('
string|"':'"
op|','
number|'1'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'given_domain'
op|'!='
name|'self'
op|'.'
name|'storage_domain'
name|'and'
name|'given_domain'
op|'.'
name|'endswith'
op|'('
name|'self'
op|'.'
name|'storage_domain'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'parts_to_parse'
op|'='
name|'given_domain'
op|'['
op|':'
op|'-'
name|'len'
op|'('
name|'self'
op|'.'
name|'storage_domain'
op|')'
op|']'
newline|'\n'
name|'parts_to_parse'
op|'='
name|'parts_to_parse'
op|'.'
name|'strip'
op|'('
string|"'.'"
op|')'
op|'.'
name|'split'
op|'('
string|"'.'"
op|')'
newline|'\n'
name|'len_parts_to_parse'
op|'='
name|'len'
op|'('
name|'parts_to_parse'
op|')'
newline|'\n'
name|'if'
name|'len_parts_to_parse'
op|'=='
number|'2'
op|':'
newline|'\n'
indent|'                '
name|'container'
op|','
name|'account'
op|'='
name|'parts_to_parse'
newline|'\n'
dedent|''
name|'elif'
name|'len_parts_to_parse'
op|'=='
number|'1'
op|':'
newline|'\n'
indent|'                '
name|'container'
op|','
name|'account'
op|'='
name|'None'
op|','
name|'parts_to_parse'
op|'['
number|'0'
op|']'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'resp'
op|'='
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
op|','
nl|'\n'
name|'body'
op|'='
string|"'Bad domain in host header'"
op|','
nl|'\n'
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
name|'return'
name|'resp'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'if'
string|"'_'"
name|'not'
name|'in'
name|'account'
name|'and'
string|"'-'"
name|'in'
name|'account'
op|':'
newline|'\n'
indent|'                '
name|'account'
op|'='
name|'account'
op|'.'
name|'replace'
op|'('
string|"'-'"
op|','
string|"'_'"
op|','
number|'1'
op|')'
newline|'\n'
dedent|''
name|'path'
op|'='
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'.'
name|'strip'
op|'('
string|"'/'"
op|')'
newline|'\n'
name|'new_path_parts'
op|'='
op|'['
string|"''"
op|','
name|'self'
op|'.'
name|'path_root'
op|','
name|'account'
op|']'
newline|'\n'
name|'if'
name|'container'
op|':'
newline|'\n'
indent|'                '
name|'new_path_parts'
op|'.'
name|'append'
op|'('
name|'container'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'path'
op|'.'
name|'startswith'
op|'('
name|'self'
op|'.'
name|'path_root'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'path'
op|'='
name|'path'
op|'['
name|'len'
op|'('
name|'self'
op|'.'
name|'path_root'
op|')'
op|':'
op|']'
op|'.'
name|'lstrip'
op|'('
string|"'/'"
op|')'
newline|'\n'
dedent|''
name|'if'
name|'path'
op|':'
newline|'\n'
indent|'                '
name|'new_path_parts'
op|'.'
name|'append'
op|'('
name|'path'
op|')'
newline|'\n'
dedent|''
name|'new_path'
op|'='
string|"'/'"
op|'.'
name|'join'
op|'('
name|'new_path_parts'
op|')'
newline|'\n'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'='
name|'new_path'
newline|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|filter_factory
dedent|''
dedent|''
name|'def'
name|'filter_factory'
op|'('
name|'global_conf'
op|','
op|'**'
name|'local_conf'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'conf'
op|'='
name|'global_conf'
op|'.'
name|'copy'
op|'('
op|')'
newline|'\n'
name|'conf'
op|'.'
name|'update'
op|'('
name|'local_conf'
op|')'
newline|'\n'
nl|'\n'
DECL|function|domain_filter
name|'def'
name|'domain_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'DomainRemapMiddleware'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'domain_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
