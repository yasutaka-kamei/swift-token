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
nl|'\n'
string|'"""\nDomain Remap Middleware\n\nMiddleware that translates container and account parts of a domain to\npath parameters that the proxy server understands.\n\ncontainer.account.storageurl/object gets translated to\ncontainer.account.storageurl/path_root/account/container/object\n\naccount.storageurl/path_root/container/object gets translated to\naccount.storageurl/path_root/account/container/object\n\nBrowsers can convert a host header to lowercase, so check that reseller\nprefix on the account is the correct case. This is done by comparing the\nitems in the reseller_prefixes config option to the found prefix. If they\nmatch except for case, the item from reseller_prefixes will be used\ninstead of the found reseller prefix. When none match, the default reseller\nprefix is used. When no default reseller prefix is configured, any request with\nan account prefix not in that list will be ignored by this middleware.\nreseller_prefixes defaults to \'AUTH\'.\n\nNote that this middleware requires that container names and account names\n(except as described above) must be DNS-compatible. This means that the\naccount name created in the system and the containers created by users\ncannot exceed 63 characters or have UTF-8 characters. These are\nrestrictions over and above what swift requires and are not explicitly\nchecked. Simply put, the this middleware will do a best-effort attempt to\nderive account and container names from elements in the domain name and\nput those derived values into the URL path (leaving the Host header\nunchanged).\n\nAlso note that using container sync with remapped domain names is not\nadvised. With container sync, you should use the true storage end points as\nsync destinations.\n"""'
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
name|'HTTPBadRequest'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'list_from_csv'
op|','
name|'register_swift_info'
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
string|'"""\n    Domain Remap Middleware\n\n    See above for a full description.\n\n    :param app: The next WSGI filter or app in the paste.deploy\n                chain.\n    :param conf: The configuration dict for the middleware.\n    """'
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
name|'if'
name|'self'
op|'.'
name|'storage_domain'
name|'and'
name|'self'
op|'.'
name|'storage_domain'
op|'['
number|'0'
op|']'
op|'!='
string|"'.'"
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'storage_domain'
op|'='
string|"'.'"
op|'+'
name|'self'
op|'.'
name|'storage_domain'
newline|'\n'
dedent|''
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
name|'prefixes'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'reseller_prefixes'"
op|','
string|"'AUTH'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'reseller_prefixes'
op|'='
name|'list_from_csv'
op|'('
name|'prefixes'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'reseller_prefixes_lower'
op|'='
op|'['
name|'x'
op|'.'
name|'lower'
op|'('
op|')'
nl|'\n'
name|'for'
name|'x'
name|'in'
name|'self'
op|'.'
name|'reseller_prefixes'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'default_reseller_prefix'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'default_reseller_prefix'"
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
name|'if'
name|'not'
name|'self'
op|'.'
name|'storage_domain'
op|':'
newline|'\n'
indent|'            '
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
dedent|''
name|'if'
string|"'HTTP_HOST'"
name|'in'
name|'env'
op|':'
newline|'\n'
indent|'            '
name|'given_domain'
op|'='
name|'env'
op|'['
string|"'HTTP_HOST'"
op|']'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'given_domain'
op|'='
name|'env'
op|'['
string|"'SERVER_NAME'"
op|']'
newline|'\n'
dedent|''
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
name|'len'
op|'('
name|'self'
op|'.'
name|'reseller_prefixes'
op|')'
op|'>'
number|'0'
op|':'
newline|'\n'
indent|'                '
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
indent|'                    '
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
name|'account_reseller_prefix'
op|'='
name|'account'
op|'.'
name|'split'
op|'('
string|"'_'"
op|','
number|'1'
op|')'
op|'['
number|'0'
op|']'
op|'.'
name|'lower'
op|'('
op|')'
newline|'\n'
nl|'\n'
name|'if'
name|'account_reseller_prefix'
name|'in'
name|'self'
op|'.'
name|'reseller_prefixes_lower'
op|':'
newline|'\n'
indent|'                    '
name|'prefix_index'
op|'='
name|'self'
op|'.'
name|'reseller_prefixes_lower'
op|'.'
name|'index'
op|'('
nl|'\n'
name|'account_reseller_prefix'
op|')'
newline|'\n'
name|'real_prefix'
op|'='
name|'self'
op|'.'
name|'reseller_prefixes'
op|'['
name|'prefix_index'
op|']'
newline|'\n'
name|'if'
name|'not'
name|'account'
op|'.'
name|'startswith'
op|'('
name|'real_prefix'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'account_suffix'
op|'='
name|'account'
op|'['
name|'len'
op|'('
name|'real_prefix'
op|')'
op|':'
op|']'
newline|'\n'
name|'account'
op|'='
name|'real_prefix'
op|'+'
name|'account_suffix'
newline|'\n'
dedent|''
dedent|''
name|'elif'
name|'self'
op|'.'
name|'default_reseller_prefix'
op|':'
newline|'\n'
comment|'# account prefix is not in config list. Add default one.'
nl|'\n'
indent|'                    '
name|'account'
op|'='
string|'"%s_%s"'
op|'%'
op|'('
name|'self'
op|'.'
name|'default_reseller_prefix'
op|','
name|'account'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
comment|'# account prefix is not in config list. bail.'
nl|'\n'
indent|'                    '
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
dedent|''
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
name|'register_swift_info'
op|'('
nl|'\n'
string|"'domain_remap'"
op|','
nl|'\n'
name|'default_reseller_prefix'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'default_reseller_prefix'"
op|')'
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
