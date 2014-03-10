begin_unit
comment|'# Copyright (c) 2010-2013 OpenStack Foundation'
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
string|'"""\nMiscellaneous utility functions for use in generating responses.\n\nWhy not swift.common.utils, you ask? Because this way we can import things\nfrom swob in here without creating circular imports.\n"""'
newline|'\n'
nl|'\n'
name|'import'
name|'hashlib'
newline|'\n'
name|'import'
name|'sys'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'contextlib'
name|'import'
name|'contextmanager'
newline|'\n'
name|'from'
name|'urllib'
name|'import'
name|'unquote'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'constraints'
name|'import'
name|'FORMAT2CONTENT_TYPE'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'exceptions'
name|'import'
name|'ListingIterError'
op|','
name|'SegmentError'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'http'
name|'import'
name|'is_success'
op|','
name|'HTTP_SERVICE_UNAVAILABLE'
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
name|'HTTPNotAcceptable'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'split_path'
op|','
name|'validate_device_partition'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'wsgi'
name|'import'
name|'make_subrequest'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_param
name|'def'
name|'get_param'
op|'('
name|'req'
op|','
name|'name'
op|','
name|'default'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Get parameters from an HTTP request ensuring proper handling UTF-8\n    encoding.\n\n    :param req: request object\n    :param name: parameter name\n    :param default: result to return if the parameter is not found\n    :returns: HTTP request parameter value\n              (as UTF-8 encoded str, not unicode object)\n    :raises: HTTPBadRequest if param not valid UTF-8 byte sequence\n    """'
newline|'\n'
name|'value'
op|'='
name|'req'
op|'.'
name|'params'
op|'.'
name|'get'
op|'('
name|'name'
op|','
name|'default'
op|')'
newline|'\n'
name|'if'
name|'value'
name|'and'
name|'not'
name|'isinstance'
op|'('
name|'value'
op|','
name|'unicode'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'value'
op|'.'
name|'decode'
op|'('
string|"'utf8'"
op|')'
comment|'# Ensure UTF8ness'
newline|'\n'
dedent|''
name|'except'
name|'UnicodeDecodeError'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'HTTPBadRequest'
op|'('
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|','
nl|'\n'
name|'body'
op|'='
string|'\'"%s" parameter not valid UTF-8\''
op|'%'
name|'name'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'value'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_listing_content_type
dedent|''
name|'def'
name|'get_listing_content_type'
op|'('
name|'req'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Determine the content type to use for an account or container listing\n    response.\n\n    :param req: request object\n    :returns: content type as a string (e.g. text/plain, application/json)\n    :raises: HTTPNotAcceptable if the requested content type is not acceptable\n    :raises: HTTPBadRequest if the \'format\' query param is provided and\n             not valid UTF-8\n    """'
newline|'\n'
name|'query_format'
op|'='
name|'get_param'
op|'('
name|'req'
op|','
string|"'format'"
op|')'
newline|'\n'
name|'if'
name|'query_format'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'.'
name|'accept'
op|'='
name|'FORMAT2CONTENT_TYPE'
op|'.'
name|'get'
op|'('
nl|'\n'
name|'query_format'
op|'.'
name|'lower'
op|'('
op|')'
op|','
name|'FORMAT2CONTENT_TYPE'
op|'['
string|"'plain'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'out_content_type'
op|'='
name|'req'
op|'.'
name|'accept'
op|'.'
name|'best_match'
op|'('
nl|'\n'
op|'['
string|"'text/plain'"
op|','
string|"'application/json'"
op|','
string|"'application/xml'"
op|','
string|"'text/xml'"
op|']'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'out_content_type'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'HTTPNotAcceptable'
op|'('
name|'request'
op|'='
name|'req'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'out_content_type'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_name_and_placement
dedent|''
name|'def'
name|'get_name_and_placement'
op|'('
name|'request'
op|','
name|'minsegs'
op|'='
number|'1'
op|','
name|'maxsegs'
op|'='
name|'None'
op|','
nl|'\n'
name|'rest_with_last'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Utility function to split and validate the request path and\n    storage_policy_index.  The storage_policy_index is extracted from\n    the headers of the request and converted to an integer, and then the\n    args are passed through to :meth:`split_and_validate_path`.\n\n    :returns: a list, result of :meth:`split_and_validate_path` with\n              storage_policy_index appended on the end\n    :raises: HTTPBadRequest\n    """'
newline|'\n'
name|'policy_idx'
op|'='
name|'request'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'X-Backend-Storage-Policy-Index'"
op|','
string|"'0'"
op|')'
newline|'\n'
name|'policy_idx'
op|'='
name|'int'
op|'('
name|'policy_idx'
op|')'
newline|'\n'
name|'results'
op|'='
name|'split_and_validate_path'
op|'('
name|'request'
op|','
name|'minsegs'
op|'='
name|'minsegs'
op|','
nl|'\n'
name|'maxsegs'
op|'='
name|'maxsegs'
op|','
nl|'\n'
name|'rest_with_last'
op|'='
name|'rest_with_last'
op|')'
newline|'\n'
name|'results'
op|'.'
name|'append'
op|'('
name|'policy_idx'
op|')'
newline|'\n'
name|'return'
name|'results'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|split_and_validate_path
dedent|''
name|'def'
name|'split_and_validate_path'
op|'('
name|'request'
op|','
name|'minsegs'
op|'='
number|'1'
op|','
name|'maxsegs'
op|'='
name|'None'
op|','
nl|'\n'
name|'rest_with_last'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Utility function to split and validate the request path.\n\n    :returns: result of :meth:`~swift.common.utils.split_path` if\n              everything\'s okay\n    :raises: HTTPBadRequest if something\'s not okay\n    """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'segs'
op|'='
name|'split_path'
op|'('
name|'unquote'
op|'('
name|'request'
op|'.'
name|'path'
op|')'
op|','
nl|'\n'
name|'minsegs'
op|','
name|'maxsegs'
op|','
name|'rest_with_last'
op|')'
newline|'\n'
name|'validate_device_partition'
op|'('
name|'segs'
op|'['
number|'0'
op|']'
op|','
name|'segs'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
name|'return'
name|'segs'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'HTTPBadRequest'
op|'('
name|'body'
op|'='
name|'str'
op|'('
name|'err'
op|')'
op|','
name|'request'
op|'='
name|'request'
op|','
nl|'\n'
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|is_user_meta
dedent|''
dedent|''
name|'def'
name|'is_user_meta'
op|'('
name|'server_type'
op|','
name|'key'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Tests if a header key starts with and is longer than the user\n    metadata prefix for given server type.\n\n    :param server_type: type of backend server i.e. [account|container|object]\n    :param key: header key\n    :returns: True if the key satisfies the test, False otherwise\n    """'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'key'
op|')'
op|'<='
number|'8'
op|'+'
name|'len'
op|'('
name|'server_type'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'False'
newline|'\n'
dedent|''
name|'return'
name|'key'
op|'.'
name|'lower'
op|'('
op|')'
op|'.'
name|'startswith'
op|'('
name|'get_user_meta_prefix'
op|'('
name|'server_type'
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|is_sys_meta
dedent|''
name|'def'
name|'is_sys_meta'
op|'('
name|'server_type'
op|','
name|'key'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Tests if a header key starts with and is longer than the system\n    metadata prefix for given server type.\n\n    :param server_type: type of backend server i.e. [account|container|object]\n    :param key: header key\n    :returns: True if the key satisfies the test, False otherwise\n    """'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'key'
op|')'
op|'<='
number|'11'
op|'+'
name|'len'
op|'('
name|'server_type'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'False'
newline|'\n'
dedent|''
name|'return'
name|'key'
op|'.'
name|'lower'
op|'('
op|')'
op|'.'
name|'startswith'
op|'('
name|'get_sys_meta_prefix'
op|'('
name|'server_type'
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|is_sys_or_user_meta
dedent|''
name|'def'
name|'is_sys_or_user_meta'
op|'('
name|'server_type'
op|','
name|'key'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Tests if a header key starts with and is longer than the user or system\n    metadata prefix for given server type.\n\n    :param server_type: type of backend server i.e. [account|container|object]\n    :param key: header key\n    :returns: True if the key satisfies the test, False otherwise\n    """'
newline|'\n'
name|'return'
name|'is_user_meta'
op|'('
name|'server_type'
op|','
name|'key'
op|')'
name|'or'
name|'is_sys_meta'
op|'('
name|'server_type'
op|','
name|'key'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|strip_user_meta_prefix
dedent|''
name|'def'
name|'strip_user_meta_prefix'
op|'('
name|'server_type'
op|','
name|'key'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Removes the user metadata prefix for a given server type from the start\n    of a header key.\n\n    :param server_type: type of backend server i.e. [account|container|object]\n    :param key: header key\n    :returns: stripped header key\n    """'
newline|'\n'
name|'return'
name|'key'
op|'['
name|'len'
op|'('
name|'get_user_meta_prefix'
op|'('
name|'server_type'
op|')'
op|')'
op|':'
op|']'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|strip_sys_meta_prefix
dedent|''
name|'def'
name|'strip_sys_meta_prefix'
op|'('
name|'server_type'
op|','
name|'key'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Removes the system metadata prefix for a given server type from the start\n    of a header key.\n\n    :param server_type: type of backend server i.e. [account|container|object]\n    :param key: header key\n    :returns: stripped header key\n    """'
newline|'\n'
name|'return'
name|'key'
op|'['
name|'len'
op|'('
name|'get_sys_meta_prefix'
op|'('
name|'server_type'
op|')'
op|')'
op|':'
op|']'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_user_meta_prefix
dedent|''
name|'def'
name|'get_user_meta_prefix'
op|'('
name|'server_type'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Returns the prefix for user metadata headers for given server type.\n\n    This prefix defines the namespace for headers that will be persisted\n    by backend servers.\n\n    :param server_type: type of backend server i.e. [account|container|object]\n    :returns: prefix string for server type\'s user metadata headers\n    """'
newline|'\n'
name|'return'
string|"'x-%s-%s-'"
op|'%'
op|'('
name|'server_type'
op|'.'
name|'lower'
op|'('
op|')'
op|','
string|"'meta'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_sys_meta_prefix
dedent|''
name|'def'
name|'get_sys_meta_prefix'
op|'('
name|'server_type'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Returns the prefix for system metadata headers for given server type.\n\n    This prefix defines the namespace for headers that will be persisted\n    by backend servers.\n\n    :param server_type: type of backend server i.e. [account|container|object]\n    :returns: prefix string for server type\'s system metadata headers\n    """'
newline|'\n'
name|'return'
string|"'x-%s-%s-'"
op|'%'
op|'('
name|'server_type'
op|'.'
name|'lower'
op|'('
op|')'
op|','
string|"'sysmeta'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|remove_items
dedent|''
name|'def'
name|'remove_items'
op|'('
name|'headers'
op|','
name|'condition'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Removes items from a dict whose keys satisfy\n    the given condition.\n\n    :param headers: a dict of headers\n    :param condition: a function that will be passed the header key as a\n                      single argument and should return True if the header\n                      is to be removed.\n    :returns: a dict, possibly empty, of headers that have been removed\n    """'
newline|'\n'
name|'removed'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'keys'
op|'='
name|'filter'
op|'('
name|'condition'
op|','
name|'headers'
op|')'
newline|'\n'
name|'removed'
op|'.'
name|'update'
op|'('
op|'('
name|'key'
op|','
name|'headers'
op|'.'
name|'pop'
op|'('
name|'key'
op|')'
op|')'
name|'for'
name|'key'
name|'in'
name|'keys'
op|')'
newline|'\n'
name|'return'
name|'removed'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|copy_header_subset
dedent|''
name|'def'
name|'copy_header_subset'
op|'('
name|'from_r'
op|','
name|'to_r'
op|','
name|'condition'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Will copy desired subset of headers from from_r to to_r.\n\n    :param from_r: a swob Request or Response\n    :param to_r: a swob Request or Response\n    :param condition: a function that will be passed the header key as a\n                      single argument and should return True if the header\n                      is to be copied.\n    """'
newline|'\n'
name|'for'
name|'k'
op|','
name|'v'
name|'in'
name|'from_r'
op|'.'
name|'headers'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'condition'
op|'('
name|'k'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'to_r'
op|'.'
name|'headers'
op|'['
name|'k'
op|']'
op|'='
name|'v'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|close_if_possible
dedent|''
dedent|''
dedent|''
name|'def'
name|'close_if_possible'
op|'('
name|'maybe_closable'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'close_method'
op|'='
name|'getattr'
op|'('
name|'maybe_closable'
op|','
string|"'close'"
op|','
name|'None'
op|')'
newline|'\n'
name|'if'
name|'callable'
op|'('
name|'close_method'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'close_method'
op|'('
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
dedent|''
op|'@'
name|'contextmanager'
newline|'\n'
DECL|function|closing_if_possible
name|'def'
name|'closing_if_possible'
op|'('
name|'maybe_closable'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Like contextlib.closing(), but doesn\'t crash if the object lacks a close()\n    method.\n\n    PEP 333 (WSGI) says: "If the iterable returned by the application has a\n    close() method, the server or gateway must call that method upon\n    completion of the current request[.]" This function makes that easier.\n    """'
newline|'\n'
name|'yield'
name|'maybe_closable'
newline|'\n'
name|'close_if_possible'
op|'('
name|'maybe_closable'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|SegmentedIterable
dedent|''
name|'class'
name|'SegmentedIterable'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Iterable that returns the object contents for a large object.\n\n    :param req: original request object\n    :param app: WSGI application from which segments will come\n    :param listing_iter: iterable yielding the object segments to fetch,\n                         along with the byte subranges to fetch, in the\n                         form of a tuple (object-path, first-byte, last-byte)\n                         or (object-path, None, None) to fetch the whole thing.\n    :param max_get_time: maximum permitted duration of a GET request (seconds)\n    :param logger: logger object\n    :param swift_source: value of swift.source in subrequest environ\n                         (just for logging)\n    :param ua_suffix: string to append to user-agent.\n    :param name: name of manifest (used in logging only)\n    :param response: optional response object for the response being sent\n                     to the client.\n    """'
newline|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'req'
op|','
name|'app'
op|','
name|'listing_iter'
op|','
name|'max_get_time'
op|','
nl|'\n'
name|'logger'
op|','
name|'ua_suffix'
op|','
name|'swift_source'
op|','
nl|'\n'
name|'name'
op|'='
string|"'<not specified>'"
op|','
name|'response'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'req'
op|'='
name|'req'
newline|'\n'
name|'self'
op|'.'
name|'app'
op|'='
name|'app'
newline|'\n'
name|'self'
op|'.'
name|'listing_iter'
op|'='
name|'listing_iter'
newline|'\n'
name|'self'
op|'.'
name|'max_get_time'
op|'='
name|'max_get_time'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'='
name|'logger'
newline|'\n'
name|'self'
op|'.'
name|'ua_suffix'
op|'='
string|'" "'
op|'+'
name|'ua_suffix'
newline|'\n'
name|'self'
op|'.'
name|'swift_source'
op|'='
name|'swift_source'
newline|'\n'
name|'self'
op|'.'
name|'name'
op|'='
name|'name'
newline|'\n'
name|'self'
op|'.'
name|'response'
op|'='
name|'response'
newline|'\n'
nl|'\n'
DECL|member|app_iter_range
dedent|''
name|'def'
name|'app_iter_range'
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
string|'"""\n        swob.Response will only respond with a 206 status in certain cases; one\n        of those is if the body iterator responds to .app_iter_range().\n\n        However, this object (or really, its listing iter) is smart enough to\n        handle the range stuff internally, so we just no-op this out for swob.\n        """'
newline|'\n'
name|'return'
name|'self'
newline|'\n'
nl|'\n'
DECL|member|__iter__
dedent|''
name|'def'
name|'__iter__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'start_time'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'have_yielded_data'
op|'='
name|'False'
newline|'\n'
nl|'\n'
name|'if'
name|'self'
op|'.'
name|'response'
name|'and'
name|'self'
op|'.'
name|'response'
op|'.'
name|'content_length'
op|':'
newline|'\n'
indent|'            '
name|'bytes_left'
op|'='
name|'int'
op|'('
name|'self'
op|'.'
name|'response'
op|'.'
name|'content_length'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'bytes_left'
op|'='
name|'None'
newline|'\n'
nl|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'seg_path'
op|','
name|'seg_etag'
op|','
name|'seg_size'
op|','
name|'first_byte'
op|','
name|'last_byte'
name|'in'
name|'self'
op|'.'
name|'listing_iter'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'start_time'
op|'>'
name|'self'
op|'.'
name|'max_get_time'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
name|'SegmentError'
op|'('
nl|'\n'
string|"'ERROR: While processing manifest %s, '"
nl|'\n'
string|"'max LO GET time of %ds exceeded'"
op|'%'
nl|'\n'
op|'('
name|'self'
op|'.'
name|'name'
op|','
name|'self'
op|'.'
name|'max_get_time'
op|')'
op|')'
newline|'\n'
comment|'# Make sure that the segment is a plain old object, not some'
nl|'\n'
comment|'# flavor of large object, so that we can check its MD5.'
nl|'\n'
dedent|''
name|'path'
op|'='
name|'seg_path'
op|'+'
string|"'?multipart-manifest=get'"
newline|'\n'
name|'seg_req'
op|'='
name|'make_subrequest'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'req'
op|'.'
name|'environ'
op|','
name|'path'
op|'='
name|'path'
op|','
name|'method'
op|'='
string|"'GET'"
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'x-auth-token'"
op|':'
name|'self'
op|'.'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
nl|'\n'
string|"'x-auth-token'"
op|')'
op|'}'
op|','
nl|'\n'
name|'agent'
op|'='
op|'('
string|"'%(orig)s '"
op|'+'
name|'self'
op|'.'
name|'ua_suffix'
op|')'
op|','
nl|'\n'
name|'swift_source'
op|'='
name|'self'
op|'.'
name|'swift_source'
op|')'
newline|'\n'
name|'if'
name|'first_byte'
name|'is'
name|'not'
name|'None'
name|'or'
name|'last_byte'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'                    '
name|'seg_req'
op|'.'
name|'headers'
op|'['
string|"'Range'"
op|']'
op|'='
string|'"bytes=%s-%s"'
op|'%'
op|'('
nl|'\n'
comment|'# The 0 is to avoid having a range like "bytes=-10",'
nl|'\n'
comment|'# which actually means the *last* 10 bytes.'
nl|'\n'
string|"'0'"
name|'if'
name|'first_byte'
name|'is'
name|'None'
name|'else'
name|'first_byte'
op|','
nl|'\n'
string|"''"
name|'if'
name|'last_byte'
name|'is'
name|'None'
name|'else'
name|'last_byte'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'seg_resp'
op|'='
name|'seg_req'
op|'.'
name|'get_response'
op|'('
name|'self'
op|'.'
name|'app'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'is_success'
op|'('
name|'seg_resp'
op|'.'
name|'status_int'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'close_if_possible'
op|'('
name|'seg_resp'
op|'.'
name|'app_iter'
op|')'
newline|'\n'
name|'raise'
name|'SegmentError'
op|'('
nl|'\n'
string|"'ERROR: While processing manifest %s, '"
nl|'\n'
string|"'got %d while retrieving %s'"
op|'%'
nl|'\n'
op|'('
name|'self'
op|'.'
name|'name'
op|','
name|'seg_resp'
op|'.'
name|'status_int'
op|','
name|'seg_path'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'elif'
op|'('
op|'('
name|'seg_etag'
name|'and'
op|'('
name|'seg_resp'
op|'.'
name|'etag'
op|'!='
name|'seg_etag'
op|')'
op|')'
name|'or'
nl|'\n'
op|'('
name|'seg_size'
name|'and'
op|'('
name|'seg_resp'
op|'.'
name|'content_length'
op|'!='
name|'seg_size'
op|')'
name|'and'
nl|'\n'
name|'not'
name|'seg_req'
op|'.'
name|'range'
op|')'
op|')'
op|':'
newline|'\n'
comment|'# The content-length check is for security reasons. Seems'
nl|'\n'
comment|'# possible that an attacker could upload a >1mb object and'
nl|'\n'
comment|'# then replace it with a much smaller object with same'
nl|'\n'
comment|'# etag. Then create a big nested SLO that calls that'
nl|'\n'
comment|'# object many times which would hammer our obj servers. If'
nl|'\n'
comment|"# this is a range request, don't check content-length"
nl|'\n'
comment|"# because it won't match."
nl|'\n'
indent|'                    '
name|'close_if_possible'
op|'('
name|'seg_resp'
op|'.'
name|'app_iter'
op|')'
newline|'\n'
name|'raise'
name|'SegmentError'
op|'('
nl|'\n'
string|"'Object segment no longer valid: '"
nl|'\n'
string|"'%(path)s etag: %(r_etag)s != %(s_etag)s or '"
nl|'\n'
string|"'%(r_size)s != %(s_size)s.'"
op|'%'
nl|'\n'
op|'{'
string|"'path'"
op|':'
name|'seg_req'
op|'.'
name|'path'
op|','
string|"'r_etag'"
op|':'
name|'seg_resp'
op|'.'
name|'etag'
op|','
nl|'\n'
string|"'r_size'"
op|':'
name|'seg_resp'
op|'.'
name|'content_length'
op|','
nl|'\n'
string|"'s_etag'"
op|':'
name|'seg_etag'
op|','
nl|'\n'
string|"'s_size'"
op|':'
name|'seg_size'
op|'}'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'seg_hash'
op|'='
name|'hashlib'
op|'.'
name|'md5'
op|'('
op|')'
newline|'\n'
name|'for'
name|'chunk'
name|'in'
name|'seg_resp'
op|'.'
name|'app_iter'
op|':'
newline|'\n'
indent|'                    '
name|'seg_hash'
op|'.'
name|'update'
op|'('
name|'chunk'
op|')'
newline|'\n'
name|'have_yielded_data'
op|'='
name|'True'
newline|'\n'
name|'if'
name|'bytes_left'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                        '
name|'yield'
name|'chunk'
newline|'\n'
dedent|''
name|'elif'
name|'bytes_left'
op|'>='
name|'len'
op|'('
name|'chunk'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'yield'
name|'chunk'
newline|'\n'
name|'bytes_left'
op|'-='
name|'len'
op|'('
name|'chunk'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'yield'
name|'chunk'
op|'['
op|':'
name|'bytes_left'
op|']'
newline|'\n'
name|'bytes_left'
op|'-='
name|'len'
op|'('
name|'chunk'
op|')'
newline|'\n'
name|'close_if_possible'
op|'('
name|'seg_resp'
op|'.'
name|'app_iter'
op|')'
newline|'\n'
name|'raise'
name|'SegmentError'
op|'('
nl|'\n'
string|"'Too many bytes for %(name)s; truncating in '"
nl|'\n'
string|"'%(seg)s with %(left)d bytes left'"
op|'%'
nl|'\n'
op|'{'
string|"'name'"
op|':'
name|'self'
op|'.'
name|'name'
op|','
string|"'seg'"
op|':'
name|'seg_req'
op|'.'
name|'path'
op|','
nl|'\n'
string|"'left'"
op|':'
name|'bytes_left'
op|'}'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'close_if_possible'
op|'('
name|'seg_resp'
op|'.'
name|'app_iter'
op|')'
newline|'\n'
nl|'\n'
name|'if'
name|'seg_resp'
op|'.'
name|'etag'
name|'and'
name|'seg_hash'
op|'.'
name|'hexdigest'
op|'('
op|')'
op|'!='
name|'seg_resp'
op|'.'
name|'etag'
name|'and'
name|'first_byte'
name|'is'
name|'None'
name|'and'
name|'last_byte'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
name|'SegmentError'
op|'('
nl|'\n'
string|'"Bad MD5 checksum in %(name)s for %(seg)s: headers had"'
nl|'\n'
string|'" %(etag)s, but object MD5 was actually %(actual)s"'
op|'%'
nl|'\n'
op|'{'
string|"'seg'"
op|':'
name|'seg_req'
op|'.'
name|'path'
op|','
string|"'etag'"
op|':'
name|'seg_resp'
op|'.'
name|'etag'
op|','
nl|'\n'
string|"'name'"
op|':'
name|'self'
op|'.'
name|'name'
op|','
string|"'actual'"
op|':'
name|'seg_hash'
op|'.'
name|'hexdigest'
op|'('
op|')'
op|'}'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'if'
name|'bytes_left'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'SegmentError'
op|'('
nl|'\n'
string|"'Not enough bytes for %s; closing connection'"
op|'%'
nl|'\n'
name|'self'
op|'.'
name|'name'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'except'
name|'ListingIterError'
name|'as'
name|'err'
op|':'
newline|'\n'
comment|"# I have to save this error because yielding the ' ' below clears"
nl|'\n'
comment|'# the exception from the current stack frame.'
nl|'\n'
indent|'            '
name|'excinfo'
op|'='
name|'sys'
op|'.'
name|'exc_info'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
string|"'ERROR: While processing manifest %s, %s'"
op|','
nl|'\n'
name|'self'
op|'.'
name|'name'
op|','
name|'err'
op|')'
newline|'\n'
comment|'# Normally, exceptions before any data has been yielded will'
nl|'\n'
comment|'# cause Eventlet to send a 5xx response. In this particular'
nl|'\n'
comment|"# case of ListingIterError we don't want that and we'd rather"
nl|'\n'
comment|'# just send the normal 2xx response and then hang up early'
nl|'\n'
comment|'# since 5xx codes are often used to judge Service Level'
nl|'\n'
comment|'# Agreements and this ListingIterError indicates the user has'
nl|'\n'
comment|'# created an invalid condition.'
nl|'\n'
name|'if'
name|'not'
name|'have_yielded_data'
op|':'
newline|'\n'
indent|'                '
name|'yield'
string|"' '"
newline|'\n'
dedent|''
name|'raise'
name|'excinfo'
newline|'\n'
dedent|''
name|'except'
name|'SegmentError'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
name|'err'
op|')'
newline|'\n'
comment|"# This doesn't actually change the response status (we're too"
nl|'\n'
comment|'# late for that), but this does make it to the logs.'
nl|'\n'
name|'if'
name|'self'
op|'.'
name|'response'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'response'
op|'.'
name|'status'
op|'='
name|'HTTP_SERVICE_UNAVAILABLE'
newline|'\n'
dedent|''
name|'raise'
newline|'\n'
dedent|''
dedent|''
dedent|''
endmarker|''
end_unit
