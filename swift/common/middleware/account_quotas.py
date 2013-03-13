begin_unit
comment|'# Copyright (c) 2013 OpenStack Foundation.'
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
string|'""" Account quota middleware for Openstack Swift Proxy """'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'HTTPForbidden'
op|','
name|'HTTPRequestEntityTooLarge'
op|','
name|'HTTPBadRequest'
op|','
name|'wsgify'
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
name|'get_account_info'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|AccountQuotaMiddleware
name|'class'
name|'AccountQuotaMiddleware'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    account_quotas is a middleware which blocks write requests (PUT, POST) if a\n    given quota (in bytes) is exceeded while DELETE requests are still allowed.\n\n    account_quotas uses the x-account-meta-quota-bytes metadata to store the\n    quota. Write requests to this metadata setting are only allowed for\n    resellers. There is no quota limit if x-account-meta-quota-bytes is not\n    set.\n\n    The following shows an example proxy-server.conf:\n\n    [pipeline:main]\n    pipeline = catch_errors cache tempauth account-quotas proxy-server\n\n    [filter:account-quotas]\n    use = egg:swift#account_quotas\n\n    """'
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
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
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
nl|'\n'
dedent|''
op|'@'
name|'wsgify'
newline|'\n'
DECL|member|__call__
name|'def'
name|'__call__'
op|'('
name|'self'
op|','
name|'request'
op|')'
op|':'
newline|'\n'
nl|'\n'
indent|'        '
name|'if'
name|'request'
op|'.'
name|'method'
name|'not'
name|'in'
op|'('
string|'"POST"'
op|','
string|'"PUT"'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'app'
newline|'\n'
nl|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'request'
op|'.'
name|'split_path'
op|'('
number|'2'
op|','
number|'4'
op|','
name|'rest_with_last'
op|'='
name|'True'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'app'
newline|'\n'
nl|'\n'
dedent|''
name|'new_quota'
op|'='
name|'request'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'X-Account-Meta-Quota-Bytes'"
op|')'
newline|'\n'
nl|'\n'
name|'if'
name|'request'
op|'.'
name|'environ'
op|'.'
name|'get'
op|'('
string|"'reseller_request'"
op|')'
name|'is'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'new_quota'
name|'and'
name|'not'
name|'new_quota'
op|'.'
name|'isdigit'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'HTTPBadRequest'
op|'('
op|')'
newline|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'app'
newline|'\n'
nl|'\n'
comment|'# deny quota set for non-reseller'
nl|'\n'
dedent|''
name|'if'
name|'new_quota'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPForbidden'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'account_info'
op|'='
name|'get_account_info'
op|'('
name|'request'
op|'.'
name|'environ'
op|','
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'new_size'
op|'='
name|'int'
op|'('
name|'account_info'
op|'['
string|"'bytes'"
op|']'
op|')'
op|'+'
op|'('
name|'request'
op|'.'
name|'content_length'
name|'or'
number|'0'
op|')'
newline|'\n'
name|'quota'
op|'='
name|'int'
op|'('
name|'account_info'
op|'['
string|"'meta'"
op|']'
op|'.'
name|'get'
op|'('
string|"'quota-bytes'"
op|','
op|'-'
number|'1'
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'if'
number|'0'
op|'<='
name|'quota'
op|'<'
name|'new_size'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPRequestEntityTooLarge'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'app'
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
string|'"""Returns a WSGI filter app for use with paste.deploy."""'
newline|'\n'
DECL|function|account_quota_filter
name|'def'
name|'account_quota_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'AccountQuotaMiddleware'
op|'('
name|'app'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'account_quota_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit