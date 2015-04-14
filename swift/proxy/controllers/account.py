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
name|'from'
name|'swift'
name|'import'
name|'gettext_'
name|'as'
name|'_'
newline|'\n'
name|'from'
name|'urllib'
name|'import'
name|'unquote'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'account'
op|'.'
name|'utils'
name|'import'
name|'account_listing_response'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'request_helpers'
name|'import'
name|'get_listing_content_type'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'middleware'
op|'.'
name|'acl'
name|'import'
name|'parse_acl'
op|','
name|'format_acl'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'public'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'constraints'
name|'import'
name|'check_metadata'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'constraints'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'http'
name|'import'
name|'HTTP_NOT_FOUND'
op|','
name|'HTTP_GONE'
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
name|'Controller'
op|','
name|'clear_info_cache'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'HTTPBadRequest'
op|','
name|'HTTPMethodNotAllowed'
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
nl|'\n'
DECL|class|AccountController
name|'class'
name|'AccountController'
op|'('
name|'Controller'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""WSGI controller for account requests"""'
newline|'\n'
DECL|variable|server_type
name|'server_type'
op|'='
string|"'Account'"
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
name|'account_name'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'Controller'
op|'.'
name|'__init__'
op|'('
name|'self'
op|','
name|'app'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'account_name'
op|'='
name|'unquote'
op|'('
name|'account_name'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'app'
op|'.'
name|'allow_account_management'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'allowed_methods'
op|'.'
name|'remove'
op|'('
string|"'PUT'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'allowed_methods'
op|'.'
name|'remove'
op|'('
string|"'DELETE'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|add_acls_from_sys_metadata
dedent|''
dedent|''
name|'def'
name|'add_acls_from_sys_metadata'
op|'('
name|'self'
op|','
name|'resp'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'resp'
op|'.'
name|'environ'
op|'['
string|"'REQUEST_METHOD'"
op|']'
name|'in'
op|'('
string|"'HEAD'"
op|','
string|"'GET'"
op|','
string|"'PUT'"
op|','
string|"'POST'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'prefix'
op|'='
name|'get_sys_meta_prefix'
op|'('
string|"'account'"
op|')'
op|'+'
string|"'core-'"
newline|'\n'
name|'name'
op|'='
string|"'access-control'"
newline|'\n'
op|'('
name|'extname'
op|','
name|'intname'
op|')'
op|'='
op|'('
string|"'x-account-'"
op|'+'
name|'name'
op|','
name|'prefix'
op|'+'
name|'name'
op|')'
newline|'\n'
name|'acl_dict'
op|'='
name|'parse_acl'
op|'('
name|'version'
op|'='
number|'2'
op|','
name|'data'
op|'='
name|'resp'
op|'.'
name|'headers'
op|'.'
name|'pop'
op|'('
name|'intname'
op|')'
op|')'
newline|'\n'
name|'if'
name|'acl_dict'
op|':'
comment|'# treat empty dict as empty header'
newline|'\n'
indent|'                '
name|'resp'
op|'.'
name|'headers'
op|'['
name|'extname'
op|']'
op|'='
name|'format_acl'
op|'('
nl|'\n'
name|'version'
op|'='
number|'2'
op|','
name|'acl_dict'
op|'='
name|'acl_dict'
op|')'
newline|'\n'
nl|'\n'
DECL|member|GETorHEAD
dedent|''
dedent|''
dedent|''
name|'def'
name|'GETorHEAD'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Handler for HTTP GET/HEAD requests."""'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'self'
op|'.'
name|'account_name'
op|')'
op|'>'
name|'constraints'
op|'.'
name|'MAX_ACCOUNT_NAME_LENGTH'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'body'
op|'='
string|"'Account name length of %d longer than %d'"
op|'%'
op|'('
name|'len'
op|'('
name|'self'
op|'.'
name|'account_name'
op|')'
op|','
nl|'\n'
name|'constraints'
op|'.'
name|'MAX_ACCOUNT_NAME_LENGTH'
op|')'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
dedent|''
name|'partition'
op|'='
name|'self'
op|'.'
name|'app'
op|'.'
name|'account_ring'
op|'.'
name|'get_part'
op|'('
name|'self'
op|'.'
name|'account_name'
op|')'
newline|'\n'
name|'node_iter'
op|'='
name|'self'
op|'.'
name|'app'
op|'.'
name|'iter_nodes'
op|'('
name|'self'
op|'.'
name|'app'
op|'.'
name|'account_ring'
op|','
name|'partition'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'GETorHEAD_base'
op|'('
nl|'\n'
name|'req'
op|','
name|'_'
op|'('
string|"'Account'"
op|')'
op|','
name|'node_iter'
op|','
name|'partition'
op|','
nl|'\n'
name|'req'
op|'.'
name|'swift_entity_path'
op|'.'
name|'rstrip'
op|'('
string|"'/'"
op|')'
op|')'
newline|'\n'
name|'if'
name|'resp'
op|'.'
name|'status_int'
op|'=='
name|'HTTP_NOT_FOUND'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'resp'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'X-Account-Status'"
op|','
string|"''"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
op|'=='
string|"'deleted'"
op|':'
newline|'\n'
indent|'                '
name|'resp'
op|'.'
name|'status'
op|'='
name|'HTTP_GONE'
newline|'\n'
dedent|''
name|'elif'
name|'self'
op|'.'
name|'app'
op|'.'
name|'account_autocreate'
op|':'
newline|'\n'
indent|'                '
name|'resp'
op|'='
name|'account_listing_response'
op|'('
name|'self'
op|'.'
name|'account_name'
op|','
name|'req'
op|','
nl|'\n'
name|'get_listing_content_type'
op|'('
name|'req'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'req'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'swift_owner'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'add_acls_from_sys_metadata'
op|'('
name|'resp'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'header'
name|'in'
name|'self'
op|'.'
name|'app'
op|'.'
name|'swift_owner_headers'
op|':'
newline|'\n'
indent|'                '
name|'resp'
op|'.'
name|'headers'
op|'.'
name|'pop'
op|'('
name|'header'
op|','
name|'None'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'public'
newline|'\n'
DECL|member|PUT
name|'def'
name|'PUT'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""HTTP PUT request handler."""'
newline|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'app'
op|'.'
name|'allow_account_management'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPMethodNotAllowed'
op|'('
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Allow'"
op|':'
string|"', '"
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'allowed_methods'
op|')'
op|'}'
op|')'
newline|'\n'
dedent|''
name|'error_response'
op|'='
name|'check_metadata'
op|'('
name|'req'
op|','
string|"'account'"
op|')'
newline|'\n'
name|'if'
name|'error_response'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'error_response'
newline|'\n'
dedent|''
name|'if'
name|'len'
op|'('
name|'self'
op|'.'
name|'account_name'
op|')'
op|'>'
name|'constraints'
op|'.'
name|'MAX_ACCOUNT_NAME_LENGTH'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'body'
op|'='
string|"'Account name length of %d longer than %d'"
op|'%'
op|'('
name|'len'
op|'('
name|'self'
op|'.'
name|'account_name'
op|')'
op|','
nl|'\n'
name|'constraints'
op|'.'
name|'MAX_ACCOUNT_NAME_LENGTH'
op|')'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
dedent|''
name|'account_partition'
op|','
name|'accounts'
op|'='
name|'self'
op|'.'
name|'app'
op|'.'
name|'account_ring'
op|'.'
name|'get_nodes'
op|'('
name|'self'
op|'.'
name|'account_name'
op|')'
newline|'\n'
name|'headers'
op|'='
name|'self'
op|'.'
name|'generate_request_headers'
op|'('
name|'req'
op|','
name|'transfer'
op|'='
name|'True'
op|')'
newline|'\n'
name|'clear_info_cache'
op|'('
name|'self'
op|'.'
name|'app'
op|','
name|'req'
op|'.'
name|'environ'
op|','
name|'self'
op|'.'
name|'account_name'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'make_requests'
op|'('
nl|'\n'
name|'req'
op|','
name|'self'
op|'.'
name|'app'
op|'.'
name|'account_ring'
op|','
name|'account_partition'
op|','
string|"'PUT'"
op|','
nl|'\n'
name|'req'
op|'.'
name|'swift_entity_path'
op|','
op|'['
name|'headers'
op|']'
op|'*'
name|'len'
op|'('
name|'accounts'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'add_acls_from_sys_metadata'
op|'('
name|'resp'
op|')'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'public'
newline|'\n'
DECL|member|POST
name|'def'
name|'POST'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""HTTP POST request handler."""'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'self'
op|'.'
name|'account_name'
op|')'
op|'>'
name|'constraints'
op|'.'
name|'MAX_ACCOUNT_NAME_LENGTH'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'body'
op|'='
string|"'Account name length of %d longer than %d'"
op|'%'
op|'('
name|'len'
op|'('
name|'self'
op|'.'
name|'account_name'
op|')'
op|','
nl|'\n'
name|'constraints'
op|'.'
name|'MAX_ACCOUNT_NAME_LENGTH'
op|')'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
dedent|''
name|'error_response'
op|'='
name|'check_metadata'
op|'('
name|'req'
op|','
string|"'account'"
op|')'
newline|'\n'
name|'if'
name|'error_response'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'error_response'
newline|'\n'
dedent|''
name|'account_partition'
op|','
name|'accounts'
op|'='
name|'self'
op|'.'
name|'app'
op|'.'
name|'account_ring'
op|'.'
name|'get_nodes'
op|'('
name|'self'
op|'.'
name|'account_name'
op|')'
newline|'\n'
name|'headers'
op|'='
name|'self'
op|'.'
name|'generate_request_headers'
op|'('
name|'req'
op|','
name|'transfer'
op|'='
name|'True'
op|')'
newline|'\n'
name|'clear_info_cache'
op|'('
name|'self'
op|'.'
name|'app'
op|','
name|'req'
op|'.'
name|'environ'
op|','
name|'self'
op|'.'
name|'account_name'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'make_requests'
op|'('
nl|'\n'
name|'req'
op|','
name|'self'
op|'.'
name|'app'
op|'.'
name|'account_ring'
op|','
name|'account_partition'
op|','
string|"'POST'"
op|','
nl|'\n'
name|'req'
op|'.'
name|'swift_entity_path'
op|','
op|'['
name|'headers'
op|']'
op|'*'
name|'len'
op|'('
name|'accounts'
op|')'
op|')'
newline|'\n'
name|'if'
name|'resp'
op|'.'
name|'status_int'
op|'=='
name|'HTTP_NOT_FOUND'
name|'and'
name|'self'
op|'.'
name|'app'
op|'.'
name|'account_autocreate'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'autocreate_account'
op|'('
name|'req'
op|','
name|'self'
op|'.'
name|'account_name'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'make_requests'
op|'('
nl|'\n'
name|'req'
op|','
name|'self'
op|'.'
name|'app'
op|'.'
name|'account_ring'
op|','
name|'account_partition'
op|','
string|"'POST'"
op|','
nl|'\n'
name|'req'
op|'.'
name|'swift_entity_path'
op|','
op|'['
name|'headers'
op|']'
op|'*'
name|'len'
op|'('
name|'accounts'
op|')'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'add_acls_from_sys_metadata'
op|'('
name|'resp'
op|')'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'public'
newline|'\n'
DECL|member|DELETE
name|'def'
name|'DELETE'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""HTTP DELETE request handler."""'
newline|'\n'
comment|'# Extra safety in case someone typos a query string for an'
nl|'\n'
comment|'# account-level DELETE request that was really meant to be caught by'
nl|'\n'
comment|'# some middleware.'
nl|'\n'
name|'if'
name|'req'
op|'.'
name|'query_string'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'self'
op|'.'
name|'app'
op|'.'
name|'allow_account_management'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPMethodNotAllowed'
op|'('
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Allow'"
op|':'
string|"', '"
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'allowed_methods'
op|')'
op|'}'
op|')'
newline|'\n'
dedent|''
name|'account_partition'
op|','
name|'accounts'
op|'='
name|'self'
op|'.'
name|'app'
op|'.'
name|'account_ring'
op|'.'
name|'get_nodes'
op|'('
name|'self'
op|'.'
name|'account_name'
op|')'
newline|'\n'
name|'headers'
op|'='
name|'self'
op|'.'
name|'generate_request_headers'
op|'('
name|'req'
op|')'
newline|'\n'
name|'clear_info_cache'
op|'('
name|'self'
op|'.'
name|'app'
op|','
name|'req'
op|'.'
name|'environ'
op|','
name|'self'
op|'.'
name|'account_name'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'make_requests'
op|'('
nl|'\n'
name|'req'
op|','
name|'self'
op|'.'
name|'app'
op|'.'
name|'account_ring'
op|','
name|'account_partition'
op|','
string|"'DELETE'"
op|','
nl|'\n'
name|'req'
op|'.'
name|'swift_entity_path'
op|','
op|'['
name|'headers'
op|']'
op|'*'
name|'len'
op|'('
name|'accounts'
op|')'
op|')'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
