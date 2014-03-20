begin_unit
comment|'# Copyright (c) 2013 OpenStack Foundation'
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
comment|"# This stuff can't live in test/unit/__init__.py due to its swob dependency."
nl|'\n'
nl|'\n'
name|'from'
name|'copy'
name|'import'
name|'deepcopy'
newline|'\n'
name|'from'
name|'hashlib'
name|'import'
name|'md5'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'swob'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'split_path'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|FakeSwift
name|'class'
name|'FakeSwift'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    A good-enough fake Swift proxy server to use in testing middleware.\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'_calls'
op|'='
op|'['
op|']'
newline|'\n'
name|'self'
op|'.'
name|'req_method_paths'
op|'='
op|'['
op|']'
newline|'\n'
name|'self'
op|'.'
name|'swift_sources'
op|'='
op|'['
op|']'
newline|'\n'
name|'self'
op|'.'
name|'uploaded'
op|'='
op|'{'
op|'}'
newline|'\n'
comment|'# mapping of (method, path) --> (response class, headers, body)'
nl|'\n'
name|'self'
op|'.'
name|'_responses'
op|'='
op|'{'
op|'}'
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
name|'method'
op|'='
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
newline|'\n'
name|'path'
op|'='
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
newline|'\n'
name|'_'
op|','
name|'acc'
op|','
name|'cont'
op|','
name|'obj'
op|'='
name|'split_path'
op|'('
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|','
number|'0'
op|','
number|'4'
op|','
nl|'\n'
name|'rest_with_last'
op|'='
name|'True'
op|')'
newline|'\n'
name|'if'
name|'env'
op|'.'
name|'get'
op|'('
string|"'QUERY_STRING'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'path'
op|'+='
string|"'?'"
op|'+'
name|'env'
op|'['
string|"'QUERY_STRING'"
op|']'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
string|"'swift.authorize'"
name|'in'
name|'env'
op|':'
newline|'\n'
indent|'            '
name|'resp'
op|'='
name|'env'
op|'['
string|"'swift.authorize'"
op|']'
op|'('
op|')'
newline|'\n'
name|'if'
name|'resp'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'resp'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'headers'
op|'='
name|'swob'
op|'.'
name|'Request'
op|'('
name|'env'
op|')'
op|'.'
name|'headers'
newline|'\n'
name|'self'
op|'.'
name|'_calls'
op|'.'
name|'append'
op|'('
op|'('
name|'method'
op|','
name|'path'
op|','
name|'headers'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'swift_sources'
op|'.'
name|'append'
op|'('
name|'env'
op|'.'
name|'get'
op|'('
string|"'swift.source'"
op|')'
op|')'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'resp_class'
op|','
name|'raw_headers'
op|','
name|'body'
op|'='
name|'self'
op|'.'
name|'_responses'
op|'['
op|'('
name|'method'
op|','
name|'path'
op|')'
op|']'
newline|'\n'
name|'headers'
op|'='
name|'swob'
op|'.'
name|'HeaderKeyDict'
op|'('
name|'raw_headers'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'KeyError'
op|':'
newline|'\n'
indent|'            '
name|'if'
op|'('
name|'env'
op|'.'
name|'get'
op|'('
string|"'QUERY_STRING'"
op|')'
nl|'\n'
name|'and'
op|'('
name|'method'
op|','
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|')'
name|'in'
name|'self'
op|'.'
name|'_responses'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'resp_class'
op|','
name|'raw_headers'
op|','
name|'body'
op|'='
name|'self'
op|'.'
name|'_responses'
op|'['
nl|'\n'
op|'('
name|'method'
op|','
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|')'
op|']'
newline|'\n'
name|'headers'
op|'='
name|'swob'
op|'.'
name|'HeaderKeyDict'
op|'('
name|'raw_headers'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'method'
op|'=='
string|"'HEAD'"
name|'and'
op|'('
string|"'GET'"
op|','
name|'path'
op|')'
name|'in'
name|'self'
op|'.'
name|'_responses'
op|':'
newline|'\n'
indent|'                '
name|'resp_class'
op|','
name|'raw_headers'
op|','
name|'_'
op|'='
name|'self'
op|'.'
name|'_responses'
op|'['
op|'('
string|"'GET'"
op|','
name|'path'
op|')'
op|']'
newline|'\n'
name|'body'
op|'='
name|'None'
newline|'\n'
name|'headers'
op|'='
name|'swob'
op|'.'
name|'HeaderKeyDict'
op|'('
name|'raw_headers'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'method'
op|'=='
string|"'GET'"
name|'and'
name|'obj'
name|'and'
name|'path'
name|'in'
name|'self'
op|'.'
name|'uploaded'
op|':'
newline|'\n'
indent|'                '
name|'resp_class'
op|'='
name|'swob'
op|'.'
name|'HTTPOk'
newline|'\n'
name|'headers'
op|','
name|'body'
op|'='
name|'self'
op|'.'
name|'uploaded'
op|'['
name|'path'
op|']'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'print'
string|'"Didn\'t find %r in allowed responses"'
op|'%'
op|'('
op|'('
name|'method'
op|','
name|'path'
op|')'
op|','
op|')'
newline|'\n'
name|'raise'
newline|'\n'
nl|'\n'
comment|'# simulate object PUT'
nl|'\n'
dedent|''
dedent|''
name|'if'
name|'method'
op|'=='
string|"'PUT'"
name|'and'
name|'obj'
op|':'
newline|'\n'
indent|'            '
name|'input'
op|'='
name|'env'
op|'['
string|"'wsgi.input'"
op|']'
op|'.'
name|'read'
op|'('
op|')'
newline|'\n'
name|'etag'
op|'='
name|'md5'
op|'('
name|'input'
op|')'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
name|'headers'
op|'.'
name|'setdefault'
op|'('
string|"'Etag'"
op|','
name|'etag'
op|')'
newline|'\n'
name|'headers'
op|'.'
name|'setdefault'
op|'('
string|"'Content-Length'"
op|','
name|'len'
op|'('
name|'input'
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# keep it for subsequent GET requests later'
nl|'\n'
name|'self'
op|'.'
name|'uploaded'
op|'['
name|'path'
op|']'
op|'='
op|'('
name|'deepcopy'
op|'('
name|'headers'
op|')'
op|','
name|'input'
op|')'
newline|'\n'
name|'if'
string|'"CONTENT_TYPE"'
name|'in'
name|'env'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'uploaded'
op|'['
name|'path'
op|']'
op|'['
number|'0'
op|']'
op|'['
string|"'Content-Type'"
op|']'
op|'='
name|'env'
op|'['
string|'"CONTENT_TYPE"'
op|']'
newline|'\n'
nl|'\n'
comment|'# range requests ought to work, hence conditional_response=True'
nl|'\n'
dedent|''
dedent|''
name|'req'
op|'='
name|'swob'
op|'.'
name|'Request'
op|'('
name|'env'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'resp_class'
op|'('
name|'req'
op|'='
name|'req'
op|','
name|'headers'
op|'='
name|'headers'
op|','
name|'body'
op|'='
name|'body'
op|','
nl|'\n'
name|'conditional_response'
op|'='
name|'True'
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
nl|'\n'
dedent|''
op|'@'
name|'property'
newline|'\n'
DECL|member|calls
name|'def'
name|'calls'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
op|'['
op|'('
name|'method'
op|','
name|'path'
op|')'
name|'for'
name|'method'
op|','
name|'path'
op|','
name|'headers'
name|'in'
name|'self'
op|'.'
name|'_calls'
op|']'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'property'
newline|'\n'
DECL|member|calls_with_headers
name|'def'
name|'calls_with_headers'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'self'
op|'.'
name|'_calls'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'property'
newline|'\n'
DECL|member|call_count
name|'def'
name|'call_count'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'len'
op|'('
name|'self'
op|'.'
name|'_calls'
op|')'
newline|'\n'
nl|'\n'
DECL|member|register
dedent|''
name|'def'
name|'register'
op|'('
name|'self'
op|','
name|'method'
op|','
name|'path'
op|','
name|'response_class'
op|','
name|'headers'
op|','
name|'body'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'_responses'
op|'['
op|'('
name|'method'
op|','
name|'path'
op|')'
op|']'
op|'='
op|'('
name|'response_class'
op|','
name|'headers'
op|','
name|'body'
op|')'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit