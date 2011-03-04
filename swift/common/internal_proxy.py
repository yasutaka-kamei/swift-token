begin_unit
comment|'# Copyright (c) 2010-2011 OpenStack, LLC.'
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
name|'webob'
newline|'\n'
name|'from'
name|'urllib'
name|'import'
name|'quote'
op|','
name|'unquote'
newline|'\n'
name|'from'
name|'json'
name|'import'
name|'loads'
name|'as'
name|'json_loads'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'compressing_file_reader'
name|'import'
name|'CompressingFileReader'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'proxy'
op|'.'
name|'server'
name|'import'
name|'BaseApplication'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|MemcacheStub
name|'class'
name|'MemcacheStub'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|get
indent|'    '
name|'def'
name|'get'
op|'('
name|'self'
op|','
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'None'
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
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'None'
newline|'\n'
nl|'\n'
DECL|member|incr
dedent|''
name|'def'
name|'incr'
op|'('
name|'self'
op|','
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
number|'0'
newline|'\n'
nl|'\n'
DECL|member|delete
dedent|''
name|'def'
name|'delete'
op|'('
name|'self'
op|','
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'None'
newline|'\n'
nl|'\n'
DECL|member|set_multi
dedent|''
name|'def'
name|'set_multi'
op|'('
name|'self'
op|','
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'None'
newline|'\n'
nl|'\n'
DECL|member|get_multi
dedent|''
name|'def'
name|'get_multi'
op|'('
name|'self'
op|','
op|'*'
name|'a'
op|','
op|'**'
name|'kw'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
op|'['
op|']'
newline|'\n'
nl|'\n'
DECL|function|webob_request_copy
dedent|''
dedent|''
name|'def'
name|'webob_request_copy'
op|'('
name|'orig_req'
op|')'
op|':'
newline|'\n'
comment|'# this should be as simple as return orig_req.copy(), but webob is buggy'
nl|'\n'
indent|'    '
name|'req_copy'
op|'='
name|'webob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
name|'orig_req'
op|'.'
name|'path'
op|','
name|'environ'
op|'='
name|'orig_req'
op|'.'
name|'environ'
op|')'
newline|'\n'
name|'req_copy'
op|'.'
name|'body_file'
op|'='
name|'orig_req'
op|'.'
name|'body_file'
comment|"# TODO: can't do this"
newline|'\n'
name|'return'
name|'req_copy'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|InternalProxy
dedent|''
name|'class'
name|'InternalProxy'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Set up a private instance of a proxy server that allows normal requests\n    to be made without having to actually send the request to the proxy.\n    This also doesn\'t log the requests to the normal proxy logs.\n\n    :param proxy_server_conf: proxy server configuration dictionary\n    :param logger: logger to log requests to\n    :param retries: number of times to retry each request\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'proxy_server_conf'
op|'='
name|'None'
op|','
name|'logger'
op|'='
name|'None'
op|','
name|'retries'
op|'='
number|'0'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'upload_app'
op|'='
name|'BaseApplication'
op|'('
name|'proxy_server_conf'
op|','
nl|'\n'
name|'memcache'
op|'='
name|'MemcacheStub'
op|'('
op|')'
op|','
nl|'\n'
name|'logger'
op|'='
name|'logger'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'retries'
op|'='
name|'retries'
newline|'\n'
nl|'\n'
DECL|member|_handle_request
dedent|''
name|'def'
name|'_handle_request'
op|'('
name|'self'
op|','
name|'req'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'req_copy'
op|'='
name|'webob_request_copy'
op|'('
name|'req'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'upload_app'
op|'.'
name|'handle_request'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'upload_app'
op|'.'
name|'update_request'
op|'('
name|'req_copy'
op|')'
op|')'
newline|'\n'
name|'tries'
op|'='
number|'1'
newline|'\n'
name|'while'
op|'('
name|'resp'
op|'.'
name|'status_int'
op|'<'
number|'200'
name|'or'
name|'resp'
op|'.'
name|'status_int'
op|'>'
number|'299'
op|')'
name|'and'
name|'tries'
op|'<'
name|'self'
op|'.'
name|'retries'
op|':'
newline|'\n'
indent|'            '
name|'req_copy'
op|'='
name|'webob_request_copy'
op|'('
name|'req'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'upload_app'
op|'.'
name|'handle_request'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'upload_app'
op|'.'
name|'update_request'
op|'('
name|'req_copy'
op|')'
op|')'
newline|'\n'
name|'tries'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
DECL|member|upload_file
dedent|''
name|'def'
name|'upload_file'
op|'('
name|'self'
op|','
name|'source_file'
op|','
name|'account'
op|','
name|'container'
op|','
name|'object_name'
op|','
nl|'\n'
name|'compress'
op|'='
name|'True'
op|','
name|'content_type'
op|'='
string|"'application/x-gzip'"
op|','
nl|'\n'
name|'etag'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Upload a file to cloud files.\n\n        :param source_file: path to or file like object to upload\n        :param account: account to upload to\n        :param container: container to upload to\n        :param object_name: name of object being uploaded\n        :param compress: if True, compresses object as it is uploaded\n        :param content_type: content-type of object\n        :param etag: etag for object to check successful upload\n        :returns: True if successful, False otherwise\n        """'
newline|'\n'
name|'target_name'
op|'='
string|"'/v1/%s/%s/%s'"
op|'%'
op|'('
name|'account'
op|','
name|'container'
op|','
name|'object_name'
op|')'
newline|'\n'
nl|'\n'
comment|'# create the container'
nl|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'create_container'
op|'('
name|'account'
op|','
name|'container'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'False'
newline|'\n'
nl|'\n'
comment|'# upload the file to the account'
nl|'\n'
dedent|''
name|'req'
op|'='
name|'webob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
name|'target_name'
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'Transfer-Encoding'"
op|':'
string|"'chunked'"
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|function|make_request_body_file
name|'def'
name|'make_request_body_file'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'hasattr'
op|'('
name|'source_file'
op|','
string|"'read'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'_source_file'
op|'='
name|'open'
op|'('
name|'source_file'
op|'.'
name|'name'
op|','
string|"'rb'"
op|')'
comment|'#TODO: fix with stringIO'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'_source_file'
op|'='
name|'open'
op|'('
name|'source_file'
op|','
string|"'rb'"
op|')'
newline|'\n'
dedent|''
name|'_source_file'
op|'.'
name|'seek'
op|'('
number|'0'
op|')'
newline|'\n'
name|'if'
name|'compress'
op|':'
newline|'\n'
indent|'                '
name|'compressed_file'
op|'='
name|'CompressingFileReader'
op|'('
name|'_source_file'
op|')'
newline|'\n'
name|'return'
name|'compressed_file'
newline|'\n'
dedent|''
name|'return'
name|'_source_file'
newline|'\n'
nl|'\n'
dedent|''
name|'req'
op|'.'
name|'body_file'
op|'='
name|'make_request_body_file'
op|'('
op|')'
newline|'\n'
name|'req'
op|'.'
name|'account'
op|'='
name|'account'
newline|'\n'
name|'req'
op|'.'
name|'content_type'
op|'='
name|'content_type'
newline|'\n'
name|'req'
op|'.'
name|'content_length'
op|'='
name|'None'
comment|'# to make sure we send chunked data'
newline|'\n'
name|'if'
name|'etag'
op|':'
newline|'\n'
indent|'            '
name|'req'
op|'.'
name|'etag'
op|'='
name|'etag'
newline|'\n'
dedent|''
name|'req_copy'
op|'='
name|'webob_request_copy'
op|'('
name|'req'
op|')'
newline|'\n'
name|'req_copy'
op|'.'
name|'body_file'
op|'='
name|'make_request_body_file'
op|'('
op|')'
comment|'# reset the read pointer'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'upload_app'
op|'.'
name|'handle_request'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'upload_app'
op|'.'
name|'update_request'
op|'('
name|'req_copy'
op|')'
op|')'
newline|'\n'
name|'tries'
op|'='
number|'1'
newline|'\n'
name|'while'
op|'('
name|'resp'
op|'.'
name|'status_int'
op|'<'
number|'200'
name|'or'
name|'resp'
op|'.'
name|'status_int'
op|'>'
number|'299'
op|')'
name|'and'
name|'tries'
op|'<'
name|'self'
op|'.'
name|'retries'
op|':'
newline|'\n'
indent|'            '
name|'req_copy'
op|'='
name|'webob_request_copy'
op|'('
name|'req'
op|')'
newline|'\n'
name|'req_copy'
op|'.'
name|'body_file'
op|'='
name|'make_request_body_file'
op|'('
op|')'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'upload_app'
op|'.'
name|'handle_request'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'upload_app'
op|'.'
name|'update_request'
op|'('
name|'req_copy'
op|')'
op|')'
newline|'\n'
name|'tries'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'if'
name|'not'
op|'('
number|'200'
op|'<='
name|'resp'
op|'.'
name|'status_int'
op|'<'
number|'300'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'False'
newline|'\n'
dedent|''
name|'return'
name|'True'
newline|'\n'
nl|'\n'
DECL|member|get_object
dedent|''
name|'def'
name|'get_object'
op|'('
name|'self'
op|','
name|'account'
op|','
name|'container'
op|','
name|'object_name'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Get object.\n\n        :param account: account name object is in\n        :param container: container name object is in\n        :param object_name: name of object to get\n        :returns: iterator for object data\n        """'
newline|'\n'
name|'req'
op|'='
name|'webob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/%s/%s/%s'"
op|'%'
nl|'\n'
op|'('
name|'account'
op|','
name|'container'
op|','
name|'object_name'
op|')'
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'GET'"
op|'}'
op|')'
newline|'\n'
name|'req'
op|'.'
name|'account'
op|'='
name|'account'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'_handle_request'
op|'('
name|'req'
op|')'
newline|'\n'
name|'return'
name|'resp'
op|'.'
name|'status_int'
op|','
name|'resp'
op|'.'
name|'app_iter'
newline|'\n'
nl|'\n'
DECL|member|create_container
dedent|''
name|'def'
name|'create_container'
op|'('
name|'self'
op|','
name|'account'
op|','
name|'container'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Create container.\n\n        :param account: account name to put the container in\n        :param container: container name to create\n        :returns: True if successful, otherwise False\n        """'
newline|'\n'
name|'req'
op|'='
name|'webob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
string|"'/v1/%s/%s'"
op|'%'
op|'('
name|'account'
op|','
name|'container'
op|')'
op|','
nl|'\n'
name|'environ'
op|'='
op|'{'
string|"'REQUEST_METHOD'"
op|':'
string|"'PUT'"
op|'}'
op|')'
newline|'\n'
name|'req'
op|'.'
name|'account'
op|'='
name|'account'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'_handle_request'
op|'('
name|'req'
op|')'
newline|'\n'
name|'return'
number|'200'
op|'<='
name|'resp'
op|'.'
name|'status_int'
op|'<'
number|'300'
newline|'\n'
nl|'\n'
DECL|member|get_container_list
dedent|''
name|'def'
name|'get_container_list'
op|'('
name|'self'
op|','
name|'account'
op|','
name|'container'
op|','
name|'marker'
op|'='
name|'None'
op|','
nl|'\n'
name|'end_marker'
op|'='
name|'None'
op|','
name|'limit'
op|'='
name|'None'
op|','
name|'prefix'
op|'='
name|'None'
op|','
nl|'\n'
name|'delimiter'
op|'='
name|'None'
op|','
name|'full_listing'
op|'='
name|'True'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Get a listing of objects for the container.\n\n        :param account: account name for the container\n        :param container: container name to get a listing for\n        :param marker: marker query\n        :param end_marker: end marker query\n        :param limit: limit query\n        :param prefix: prefix query\n        :param delimeter: string to delimit the queries on\n        :param full_listing: if True, return a full listing, else returns a max\n                             of 10000 listings\n        :returns: list of objects\n        """'
newline|'\n'
name|'if'
name|'full_listing'
op|':'
newline|'\n'
indent|'            '
name|'rv'
op|'='
op|'['
op|']'
newline|'\n'
name|'listing'
op|'='
name|'self'
op|'.'
name|'get_container_list'
op|'('
name|'account'
op|','
name|'container'
op|','
name|'marker'
op|','
nl|'\n'
name|'end_marker'
op|','
name|'limit'
op|','
name|'prefix'
op|','
nl|'\n'
name|'delimiter'
op|','
name|'full_listing'
op|'='
name|'False'
op|')'
newline|'\n'
name|'while'
name|'listing'
op|':'
newline|'\n'
indent|'                '
name|'rv'
op|'.'
name|'extend'
op|'('
name|'listing'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'delimiter'
op|':'
newline|'\n'
indent|'                    '
name|'marker'
op|'='
name|'listing'
op|'['
op|'-'
number|'1'
op|']'
op|'['
string|"'name'"
op|']'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'marker'
op|'='
name|'listing'
op|'['
op|'-'
number|'1'
op|']'
op|'.'
name|'get'
op|'('
string|"'name'"
op|','
name|'listing'
op|'['
op|'-'
number|'1'
op|']'
op|'.'
name|'get'
op|'('
string|"'subdir'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'listing'
op|'='
name|'self'
op|'.'
name|'get_container_list'
op|'('
name|'account'
op|','
name|'container'
op|','
name|'marker'
op|','
nl|'\n'
name|'end_marker'
op|','
name|'limit'
op|','
name|'prefix'
op|','
nl|'\n'
name|'delimiter'
op|','
name|'full_listing'
op|'='
name|'False'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'rv'
newline|'\n'
dedent|''
name|'path'
op|'='
string|"'/v1/%s/%s'"
op|'%'
op|'('
name|'account'
op|','
name|'quote'
op|'('
name|'container'
op|')'
op|')'
newline|'\n'
name|'qs'
op|'='
string|"'format=json'"
newline|'\n'
name|'if'
name|'marker'
op|':'
newline|'\n'
indent|'            '
name|'qs'
op|'+='
string|"'&marker=%s'"
op|'%'
name|'quote'
op|'('
name|'marker'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'end_marker'
op|':'
newline|'\n'
indent|'            '
name|'qs'
op|'+='
string|"'&end_marker=%s'"
op|'%'
name|'quote'
op|'('
name|'end_marker'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'limit'
op|':'
newline|'\n'
indent|'            '
name|'qs'
op|'+='
string|"'&limit=%d'"
op|'%'
name|'limit'
newline|'\n'
dedent|''
name|'if'
name|'prefix'
op|':'
newline|'\n'
indent|'            '
name|'qs'
op|'+='
string|"'&prefix=%s'"
op|'%'
name|'quote'
op|'('
name|'prefix'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'delimiter'
op|':'
newline|'\n'
indent|'            '
name|'qs'
op|'+='
string|"'&delimiter=%s'"
op|'%'
name|'quote'
op|'('
name|'delimiter'
op|')'
newline|'\n'
dedent|''
name|'path'
op|'+='
string|"'?%s'"
op|'%'
name|'qs'
newline|'\n'
name|'req'
op|'='
name|'webob'
op|'.'
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
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
name|'req'
op|'.'
name|'account'
op|'='
name|'account'
newline|'\n'
name|'resp'
op|'='
name|'self'
op|'.'
name|'_handle_request'
op|'('
name|'req'
op|')'
newline|'\n'
name|'if'
name|'resp'
op|'.'
name|'status_int'
op|'<'
number|'200'
name|'or'
name|'resp'
op|'.'
name|'status_int'
op|'>='
number|'300'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'Request: %s\\nResponse: %s'"
op|'%'
op|'('
name|'req'
op|','
name|'resp'
op|')'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'resp'
op|'.'
name|'status_int'
op|'=='
number|'204'
op|':'
newline|'\n'
indent|'            '
name|'return'
op|'['
op|']'
newline|'\n'
dedent|''
name|'return'
name|'json_loads'
op|'('
name|'resp'
op|'.'
name|'body'
op|')'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
