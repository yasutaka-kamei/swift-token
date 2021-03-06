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
string|'"""\nThe ``container_quotas`` middleware implements simple quotas that can be\nimposed on swift containers by a user with the ability to set container\nmetadata, most likely the account administrator.  This can be useful for\nlimiting the scope of containers that are delegated to non-admin users, exposed\nto ``formpost`` uploads, or just as a self-imposed sanity check.\n\nAny object PUT operations that exceed these quotas return a 413 response\n(request entity too large) with a descriptive body.\n\nQuotas are subject to several limitations: eventual consistency, the timeliness\nof the cached container_info (60 second ttl by default), and it\'s unable to\nreject chunked transfer uploads that exceed the quota (though once the quota\nis exceeded, new chunked transfers will be refused).\n\nQuotas are set by adding meta values to the container, and are validated when\nset:\n\n+---------------------------------------------+-------------------------------+\n|Metadata                                     | Use                           |\n+=============================================+===============================+\n| X-Container-Meta-Quota-Bytes                | Maximum size of the           |\n|                                             | container, in bytes.          |\n+---------------------------------------------+-------------------------------+\n| X-Container-Meta-Quota-Count                | Maximum object count of the   |\n|                                             | container.                    |\n+---------------------------------------------+-------------------------------+\n\nThe ``container_quotas`` middleware should be added to the pipeline in your\n``/etc/swift/proxy-server.conf`` file just after any auth middleware.\nFor example::\n\n    [pipeline:main]\n    pipeline = catch_errors cache tempauth container_quotas proxy-server\n\n    [filter:container_quotas]\n    use = egg:swift#container_quotas\n"""'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'http'
name|'import'
name|'is_success'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'HTTPRequestEntityTooLarge'
op|','
name|'HTTPBadRequest'
op|','
name|'wsgify'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'register_swift_info'
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
name|'get_container_info'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ContainerQuotaMiddleware
name|'class'
name|'ContainerQuotaMiddleware'
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
DECL|member|bad_response
dedent|''
name|'def'
name|'bad_response'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'container_info'
op|')'
op|':'
newline|'\n'
comment|"# 401 if the user couldn't have PUT this object in the first place."
nl|'\n'
comment|"# This prevents leaking the container's existence to unauthed users."
nl|'\n'
indent|'        '
name|'if'
string|"'swift.authorize'"
name|'in'
name|'req'
op|'.'
name|'environ'
op|':'
newline|'\n'
indent|'            '
name|'req'
op|'.'
name|'acl'
op|'='
name|'container_info'
op|'['
string|"'write_acl'"
op|']'
newline|'\n'
name|'aresp'
op|'='
name|'req'
op|'.'
name|'environ'
op|'['
string|"'swift.authorize'"
op|']'
op|'('
name|'req'
op|')'
newline|'\n'
name|'if'
name|'aresp'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'aresp'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'HTTPRequestEntityTooLarge'
op|'('
name|'body'
op|'='
string|"'Upload exceeds quota.'"
op|')'
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
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
op|'('
name|'version'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
op|'='
name|'req'
op|'.'
name|'split_path'
op|'('
number|'3'
op|','
number|'4'
op|','
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
comment|'# verify new quota headers are properly formatted'
nl|'\n'
dedent|''
name|'if'
name|'not'
name|'obj'
name|'and'
name|'req'
op|'.'
name|'method'
name|'in'
op|'('
string|"'PUT'"
op|','
string|"'POST'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'val'
op|'='
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'X-Container-Meta-Quota-Bytes'"
op|')'
newline|'\n'
name|'if'
name|'val'
name|'and'
name|'not'
name|'val'
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
name|'body'
op|'='
string|"'Invalid bytes quota.'"
op|')'
newline|'\n'
dedent|''
name|'val'
op|'='
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'X-Container-Meta-Quota-Count'"
op|')'
newline|'\n'
name|'if'
name|'val'
name|'and'
name|'not'
name|'val'
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
name|'body'
op|'='
string|"'Invalid count quota.'"
op|')'
newline|'\n'
nl|'\n'
comment|'# check user uploads against quotas'
nl|'\n'
dedent|''
dedent|''
name|'elif'
name|'obj'
name|'and'
name|'req'
op|'.'
name|'method'
name|'in'
op|'('
string|"'PUT'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'container_info'
op|'='
name|'get_container_info'
op|'('
nl|'\n'
name|'req'
op|'.'
name|'environ'
op|','
name|'self'
op|'.'
name|'app'
op|','
name|'swift_source'
op|'='
string|"'CQ'"
op|')'
newline|'\n'
name|'if'
name|'not'
name|'container_info'
name|'or'
name|'not'
name|'is_success'
op|'('
name|'container_info'
op|'['
string|"'status'"
op|']'
op|')'
op|':'
newline|'\n'
comment|'# this will hopefully 404 later'
nl|'\n'
indent|'                '
name|'return'
name|'self'
op|'.'
name|'app'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
string|"'quota-bytes'"
name|'in'
name|'container_info'
op|'.'
name|'get'
op|'('
string|"'meta'"
op|','
op|'{'
op|'}'
op|')'
name|'and'
string|"'bytes'"
name|'in'
name|'container_info'
name|'and'
name|'container_info'
op|'['
string|"'meta'"
op|']'
op|'['
string|"'quota-bytes'"
op|']'
op|'.'
name|'isdigit'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'content_length'
op|'='
op|'('
name|'req'
op|'.'
name|'content_length'
name|'or'
number|'0'
op|')'
newline|'\n'
name|'new_size'
op|'='
name|'int'
op|'('
name|'container_info'
op|'['
string|"'bytes'"
op|']'
op|')'
op|'+'
name|'content_length'
newline|'\n'
name|'if'
name|'int'
op|'('
name|'container_info'
op|'['
string|"'meta'"
op|']'
op|'['
string|"'quota-bytes'"
op|']'
op|')'
op|'<'
name|'new_size'
op|':'
newline|'\n'
indent|'                    '
name|'return'
name|'self'
op|'.'
name|'bad_response'
op|'('
name|'req'
op|','
name|'container_info'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'if'
string|"'quota-count'"
name|'in'
name|'container_info'
op|'.'
name|'get'
op|'('
string|"'meta'"
op|','
op|'{'
op|'}'
op|')'
name|'and'
string|"'object_count'"
name|'in'
name|'container_info'
name|'and'
name|'container_info'
op|'['
string|"'meta'"
op|']'
op|'['
string|"'quota-count'"
op|']'
op|'.'
name|'isdigit'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'new_count'
op|'='
name|'int'
op|'('
name|'container_info'
op|'['
string|"'object_count'"
op|']'
op|')'
op|'+'
number|'1'
newline|'\n'
name|'if'
name|'int'
op|'('
name|'container_info'
op|'['
string|"'meta'"
op|']'
op|'['
string|"'quota-count'"
op|']'
op|')'
op|'<'
name|'new_count'
op|':'
newline|'\n'
indent|'                    '
name|'return'
name|'self'
op|'.'
name|'bad_response'
op|'('
name|'req'
op|','
name|'container_info'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
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
name|'register_swift_info'
op|'('
string|"'container_quotas'"
op|')'
newline|'\n'
nl|'\n'
DECL|function|container_quota_filter
name|'def'
name|'container_quota_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'ContainerQuotaMiddleware'
op|'('
name|'app'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'container_quota_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
