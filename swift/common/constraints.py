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
name|'import'
name|'functools'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
nl|'\n'
name|'import'
name|'six'
newline|'\n'
name|'from'
name|'six'
op|'.'
name|'moves'
op|'.'
name|'configparser'
name|'import'
name|'ConfigParser'
op|','
name|'NoSectionError'
op|','
name|'NoOptionError'
newline|'\n'
name|'from'
name|'six'
op|'.'
name|'moves'
name|'import'
name|'urllib'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'utils'
op|','
name|'exceptions'
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
name|'HTTPLengthRequired'
op|','
name|'HTTPRequestEntityTooLarge'
op|','
name|'HTTPPreconditionFailed'
op|','
name|'HTTPNotImplemented'
op|','
name|'HTTPException'
newline|'\n'
nl|'\n'
DECL|variable|MAX_FILE_SIZE
name|'MAX_FILE_SIZE'
op|'='
number|'5368709122'
newline|'\n'
DECL|variable|MAX_META_NAME_LENGTH
name|'MAX_META_NAME_LENGTH'
op|'='
number|'128'
newline|'\n'
DECL|variable|MAX_META_VALUE_LENGTH
name|'MAX_META_VALUE_LENGTH'
op|'='
number|'256'
newline|'\n'
DECL|variable|MAX_META_COUNT
name|'MAX_META_COUNT'
op|'='
number|'90'
newline|'\n'
DECL|variable|MAX_META_OVERALL_SIZE
name|'MAX_META_OVERALL_SIZE'
op|'='
number|'4096'
newline|'\n'
DECL|variable|MAX_HEADER_SIZE
name|'MAX_HEADER_SIZE'
op|'='
number|'8192'
newline|'\n'
DECL|variable|MAX_OBJECT_NAME_LENGTH
name|'MAX_OBJECT_NAME_LENGTH'
op|'='
number|'1024'
newline|'\n'
DECL|variable|CONTAINER_LISTING_LIMIT
name|'CONTAINER_LISTING_LIMIT'
op|'='
number|'10000'
newline|'\n'
DECL|variable|ACCOUNT_LISTING_LIMIT
name|'ACCOUNT_LISTING_LIMIT'
op|'='
number|'10000'
newline|'\n'
DECL|variable|MAX_ACCOUNT_NAME_LENGTH
name|'MAX_ACCOUNT_NAME_LENGTH'
op|'='
number|'256'
newline|'\n'
DECL|variable|MAX_CONTAINER_NAME_LENGTH
name|'MAX_CONTAINER_NAME_LENGTH'
op|'='
number|'256'
newline|'\n'
DECL|variable|VALID_API_VERSIONS
name|'VALID_API_VERSIONS'
op|'='
op|'['
string|'"v1"'
op|','
string|'"v1.0"'
op|']'
newline|'\n'
DECL|variable|EXTRA_HEADER_COUNT
name|'EXTRA_HEADER_COUNT'
op|'='
number|'0'
newline|'\n'
nl|'\n'
comment|'# If adding an entry to DEFAULT_CONSTRAINTS, note that'
nl|'\n'
comment|'# these constraints are automatically published by the'
nl|'\n'
comment|'# proxy server in responses to /info requests, with values'
nl|'\n'
comment|'# updated by reload_constraints()'
nl|'\n'
DECL|variable|DEFAULT_CONSTRAINTS
name|'DEFAULT_CONSTRAINTS'
op|'='
op|'{'
nl|'\n'
string|"'max_file_size'"
op|':'
name|'MAX_FILE_SIZE'
op|','
nl|'\n'
string|"'max_meta_name_length'"
op|':'
name|'MAX_META_NAME_LENGTH'
op|','
nl|'\n'
string|"'max_meta_value_length'"
op|':'
name|'MAX_META_VALUE_LENGTH'
op|','
nl|'\n'
string|"'max_meta_count'"
op|':'
name|'MAX_META_COUNT'
op|','
nl|'\n'
string|"'max_meta_overall_size'"
op|':'
name|'MAX_META_OVERALL_SIZE'
op|','
nl|'\n'
string|"'max_header_size'"
op|':'
name|'MAX_HEADER_SIZE'
op|','
nl|'\n'
string|"'max_object_name_length'"
op|':'
name|'MAX_OBJECT_NAME_LENGTH'
op|','
nl|'\n'
string|"'container_listing_limit'"
op|':'
name|'CONTAINER_LISTING_LIMIT'
op|','
nl|'\n'
string|"'account_listing_limit'"
op|':'
name|'ACCOUNT_LISTING_LIMIT'
op|','
nl|'\n'
string|"'max_account_name_length'"
op|':'
name|'MAX_ACCOUNT_NAME_LENGTH'
op|','
nl|'\n'
string|"'max_container_name_length'"
op|':'
name|'MAX_CONTAINER_NAME_LENGTH'
op|','
nl|'\n'
string|"'valid_api_versions'"
op|':'
name|'VALID_API_VERSIONS'
op|','
nl|'\n'
string|"'extra_header_count'"
op|':'
name|'EXTRA_HEADER_COUNT'
op|','
nl|'\n'
op|'}'
newline|'\n'
nl|'\n'
DECL|variable|SWIFT_CONSTRAINTS_LOADED
name|'SWIFT_CONSTRAINTS_LOADED'
op|'='
name|'False'
newline|'\n'
DECL|variable|OVERRIDE_CONSTRAINTS
name|'OVERRIDE_CONSTRAINTS'
op|'='
op|'{'
op|'}'
comment|'# any constraints overridden by SWIFT_CONF_FILE'
newline|'\n'
DECL|variable|EFFECTIVE_CONSTRAINTS
name|'EFFECTIVE_CONSTRAINTS'
op|'='
op|'{'
op|'}'
comment|'# populated by reload_constraints'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|reload_constraints
name|'def'
name|'reload_constraints'
op|'('
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Parse SWIFT_CONF_FILE and reset module level global contraint attrs,\n    populating OVERRIDE_CONSTRAINTS AND EFFECTIVE_CONSTRAINTS along the way.\n    """'
newline|'\n'
name|'global'
name|'SWIFT_CONSTRAINTS_LOADED'
op|','
name|'OVERRIDE_CONSTRAINTS'
newline|'\n'
name|'SWIFT_CONSTRAINTS_LOADED'
op|'='
name|'False'
newline|'\n'
name|'OVERRIDE_CONSTRAINTS'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'constraints_conf'
op|'='
name|'ConfigParser'
op|'('
op|')'
newline|'\n'
name|'if'
name|'constraints_conf'
op|'.'
name|'read'
op|'('
name|'utils'
op|'.'
name|'SWIFT_CONF_FILE'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'SWIFT_CONSTRAINTS_LOADED'
op|'='
name|'True'
newline|'\n'
name|'for'
name|'name'
name|'in'
name|'DEFAULT_CONSTRAINTS'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'value'
op|'='
name|'constraints_conf'
op|'.'
name|'get'
op|'('
string|"'swift-constraints'"
op|','
name|'name'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'NoOptionError'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
dedent|''
name|'except'
name|'NoSectionError'
op|':'
newline|'\n'
comment|'# We are never going to find the section for another option'
nl|'\n'
indent|'                '
name|'break'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'value'
op|'='
name|'int'
op|'('
name|'value'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'                    '
name|'value'
op|'='
name|'utils'
op|'.'
name|'list_from_csv'
op|'('
name|'value'
op|')'
newline|'\n'
dedent|''
name|'OVERRIDE_CONSTRAINTS'
op|'['
name|'name'
op|']'
op|'='
name|'value'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'for'
name|'name'
op|','
name|'default'
name|'in'
name|'DEFAULT_CONSTRAINTS'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'        '
name|'value'
op|'='
name|'OVERRIDE_CONSTRAINTS'
op|'.'
name|'get'
op|'('
name|'name'
op|','
name|'default'
op|')'
newline|'\n'
name|'EFFECTIVE_CONSTRAINTS'
op|'['
name|'name'
op|']'
op|'='
name|'value'
newline|'\n'
comment|'# "globals" in this context is module level globals, always.'
nl|'\n'
name|'globals'
op|'('
op|')'
op|'['
name|'name'
op|'.'
name|'upper'
op|'('
op|')'
op|']'
op|'='
name|'value'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
dedent|''
name|'reload_constraints'
op|'('
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
comment|'# Maximum slo segments in buffer'
nl|'\n'
DECL|variable|MAX_BUFFERED_SLO_SEGMENTS
name|'MAX_BUFFERED_SLO_SEGMENTS'
op|'='
number|'10000'
newline|'\n'
nl|'\n'
nl|'\n'
comment|'#: Query string format= values to their corresponding content-type values'
nl|'\n'
DECL|variable|FORMAT2CONTENT_TYPE
name|'FORMAT2CONTENT_TYPE'
op|'='
op|'{'
string|"'plain'"
op|':'
string|"'text/plain'"
op|','
string|"'json'"
op|':'
string|"'application/json'"
op|','
nl|'\n'
string|"'xml'"
op|':'
string|"'application/xml'"
op|'}'
newline|'\n'
nl|'\n'
nl|'\n'
comment|'# By default the maximum number of allowed headers depends on the number of max'
nl|'\n'
comment|'# allowed metadata settings plus a default value of 32 for regular http'
nl|'\n'
comment|'# headers.  If for some reason this is not enough (custom middleware for'
nl|'\n'
comment|'# example) it can be increased with the extra_header_count constraint.'
nl|'\n'
DECL|variable|MAX_HEADER_COUNT
name|'MAX_HEADER_COUNT'
op|'='
name|'MAX_META_COUNT'
op|'+'
number|'32'
op|'+'
name|'max'
op|'('
name|'EXTRA_HEADER_COUNT'
op|','
number|'0'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|check_metadata
name|'def'
name|'check_metadata'
op|'('
name|'req'
op|','
name|'target_type'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Check metadata sent in the request headers.  This should only check\n    that the metadata in the request given is valid.  Checks against\n    account/container overall metadata should be forwarded on to its\n    respective server to be checked.\n\n    :param req: request object\n    :param target_type: str: one of: object, container, or account: indicates\n                        which type the target storage for the metadata is\n    :returns: HTTPBadRequest with bad metadata otherwise None\n    """'
newline|'\n'
name|'target_type'
op|'='
name|'target_type'
op|'.'
name|'lower'
op|'('
op|')'
newline|'\n'
name|'prefix'
op|'='
string|"'x-%s-meta-'"
op|'%'
name|'target_type'
newline|'\n'
name|'meta_count'
op|'='
number|'0'
newline|'\n'
name|'meta_size'
op|'='
number|'0'
newline|'\n'
name|'for'
name|'key'
op|','
name|'value'
name|'in'
name|'req'
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
op|'('
name|'isinstance'
op|'('
name|'value'
op|','
name|'six'
op|'.'
name|'string_types'
op|')'
nl|'\n'
name|'and'
name|'len'
op|'('
name|'value'
op|')'
op|'>'
name|'MAX_HEADER_SIZE'
op|')'
op|':'
newline|'\n'
nl|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'body'
op|'='
string|"'Header value too long: %s'"
op|'%'
nl|'\n'
name|'key'
op|'['
op|':'
name|'MAX_META_NAME_LENGTH'
op|']'
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'key'
op|'.'
name|'lower'
op|'('
op|')'
op|'.'
name|'startswith'
op|'('
name|'prefix'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'continue'
newline|'\n'
dedent|''
name|'key'
op|'='
name|'key'
op|'['
name|'len'
op|'('
name|'prefix'
op|')'
op|':'
op|']'
newline|'\n'
name|'if'
name|'not'
name|'key'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'body'
op|'='
string|"'Metadata name cannot be empty'"
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
name|'bad_key'
op|'='
name|'not'
name|'check_utf8'
op|'('
name|'key'
op|')'
newline|'\n'
name|'bad_value'
op|'='
name|'value'
name|'and'
name|'not'
name|'check_utf8'
op|'('
name|'value'
op|')'
newline|'\n'
name|'if'
name|'target_type'
name|'in'
op|'('
string|"'account'"
op|','
string|"'container'"
op|')'
name|'and'
op|'('
name|'bad_key'
name|'or'
name|'bad_value'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'body'
op|'='
string|"'Metadata must be valid UTF-8'"
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
name|'meta_count'
op|'+='
number|'1'
newline|'\n'
name|'meta_size'
op|'+='
name|'len'
op|'('
name|'key'
op|')'
op|'+'
name|'len'
op|'('
name|'value'
op|')'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'key'
op|')'
op|'>'
name|'MAX_META_NAME_LENGTH'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
nl|'\n'
name|'body'
op|'='
string|"'Metadata name too long: %s%s'"
op|'%'
op|'('
name|'prefix'
op|','
name|'key'
op|')'
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'len'
op|'('
name|'value'
op|')'
op|'>'
name|'MAX_META_VALUE_LENGTH'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
nl|'\n'
name|'body'
op|'='
string|"'Metadata value longer than %d: %s%s'"
op|'%'
op|'('
nl|'\n'
name|'MAX_META_VALUE_LENGTH'
op|','
name|'prefix'
op|','
name|'key'
op|')'
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'meta_count'
op|'>'
name|'MAX_META_COUNT'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
nl|'\n'
name|'body'
op|'='
string|"'Too many metadata items; max %d'"
op|'%'
name|'MAX_META_COUNT'
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'meta_size'
op|'>'
name|'MAX_META_OVERALL_SIZE'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
nl|'\n'
name|'body'
op|'='
string|"'Total metadata too large; max %d'"
nl|'\n'
op|'%'
name|'MAX_META_OVERALL_SIZE'
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'None'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|check_object_creation
dedent|''
name|'def'
name|'check_object_creation'
op|'('
name|'req'
op|','
name|'object_name'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Check to ensure that everything is alright about an object to be created.\n\n    :param req: HTTP request object\n    :param object_name: name of object to be created\n    :returns HTTPRequestEntityTooLarge: the object is too large\n    :returns HTTPLengthRequired: missing content-length header and not\n                                 a chunked request\n    :returns HTTPBadRequest: missing or bad content-type header, or\n                             bad metadata\n    :returns HTTPNotImplemented: unsupported transfer-encoding header value\n    """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'ml'
op|'='
name|'req'
op|'.'
name|'message_length'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'HTTPBadRequest'
op|'('
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
name|'str'
op|'('
name|'e'
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'AttributeError'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'HTTPNotImplemented'
op|'('
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
name|'str'
op|'('
name|'e'
op|')'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'ml'
name|'is'
name|'not'
name|'None'
name|'and'
name|'ml'
op|'>'
name|'MAX_FILE_SIZE'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'HTTPRequestEntityTooLarge'
op|'('
name|'body'
op|'='
string|"'Your request is too large.'"
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
nl|'\n'
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
name|'if'
name|'req'
op|'.'
name|'content_length'
name|'is'
name|'None'
name|'and'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'transfer-encoding'"
op|')'
op|'!='
string|"'chunked'"
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'HTTPLengthRequired'
op|'('
name|'body'
op|'='
string|"'Missing Content-Length header.'"
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
nl|'\n'
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'len'
op|'('
name|'object_name'
op|')'
op|'>'
name|'MAX_OBJECT_NAME_LENGTH'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'body'
op|'='
string|"'Object name length of %d longer than %d'"
op|'%'
nl|'\n'
op|'('
name|'len'
op|'('
name|'object_name'
op|')'
op|','
name|'MAX_OBJECT_NAME_LENGTH'
op|')'
op|','
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
string|"'Content-Type'"
name|'not'
name|'in'
name|'req'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'HTTPBadRequest'
op|'('
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
string|"'No content type'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'req'
op|'='
name|'check_delete_headers'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'HTTPException'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'req'
op|','
name|'body'
op|'='
name|'e'
op|'.'
name|'body'
op|','
nl|'\n'
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'not'
name|'check_utf8'
op|'('
name|'req'
op|'.'
name|'headers'
op|'['
string|"'Content-Type'"
op|']'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'req'
op|','
name|'body'
op|'='
string|"'Invalid Content-Type'"
op|','
nl|'\n'
name|'content_type'
op|'='
string|"'text/plain'"
op|')'
newline|'\n'
dedent|''
name|'return'
name|'check_metadata'
op|'('
name|'req'
op|','
string|"'object'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|check_dir
dedent|''
name|'def'
name|'check_dir'
op|'('
name|'root'
op|','
name|'drive'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Verify that the path to the device is a directory and is a lesser\n    constraint that is enforced when a full mount_check isn\'t possible\n    with, for instance, a VM using loopback or partitions.\n\n    :param root:  base path where the dir is\n    :param drive: drive name to be checked\n    :returns: True if it is a valid directoy, False otherwise\n    """'
newline|'\n'
name|'return'
name|'os'
op|'.'
name|'path'
op|'.'
name|'isdir'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'root'
op|','
name|'drive'
op|')'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|check_mount
dedent|''
name|'def'
name|'check_mount'
op|'('
name|'root'
op|','
name|'drive'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Verify that the path to the device is a mount point and mounted.  This\n    allows us to fast fail on drives that have been unmounted because of\n    issues, and also prevents us for accidentally filling up the root\n    partition.\n\n    :param root:  base path where the devices are mounted\n    :param drive: drive name to be checked\n    :returns: True if it is a valid mounted device, False otherwise\n    """'
newline|'\n'
name|'if'
name|'not'
op|'('
name|'urllib'
op|'.'
name|'parse'
op|'.'
name|'quote_plus'
op|'('
name|'drive'
op|')'
op|'=='
name|'drive'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'False'
newline|'\n'
dedent|''
name|'path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'root'
op|','
name|'drive'
op|')'
newline|'\n'
name|'return'
name|'utils'
op|'.'
name|'ismount'
op|'('
name|'path'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|check_float
dedent|''
name|'def'
name|'check_float'
op|'('
name|'string'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Helper function for checking if a string can be converted to a float.\n\n    :param string: string to be verified as a float\n    :returns: True if the string can be converted to a float, False otherwise\n    """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'float'
op|'('
name|'string'
op|')'
newline|'\n'
name|'return'
name|'True'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'False'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|valid_timestamp
dedent|''
dedent|''
name|'def'
name|'valid_timestamp'
op|'('
name|'request'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Helper function to extract a timestamp from requests that require one.\n\n    :param request: the swob request object\n\n    :returns: a valid Timestamp instance\n    :raises: HTTPBadRequest on missing or invalid X-Timestamp\n    """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'request'
op|'.'
name|'timestamp'
newline|'\n'
dedent|''
name|'except'
name|'exceptions'
op|'.'
name|'InvalidTimestamp'
name|'as'
name|'e'
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
name|'e'
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
DECL|function|check_delete_headers
dedent|''
dedent|''
name|'def'
name|'check_delete_headers'
op|'('
name|'request'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Validate if \'x-delete\' headers are have correct values\n    values should be positive integers and correspond to\n    a time in the future.\n\n    :param request: the swob request object\n\n    :returns: HTTPBadRequest in case of invalid values\n              or None if values are ok\n    """'
newline|'\n'
name|'if'
string|"'x-delete-after'"
name|'in'
name|'request'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'x_delete_after'
op|'='
name|'int'
op|'('
name|'request'
op|'.'
name|'headers'
op|'['
string|"'x-delete-after'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'request'
op|','
nl|'\n'
name|'content_type'
op|'='
string|"'text/plain'"
op|','
nl|'\n'
name|'body'
op|'='
string|"'Non-integer X-Delete-After'"
op|')'
newline|'\n'
dedent|''
name|'actual_del_time'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'+'
name|'x_delete_after'
newline|'\n'
name|'if'
name|'actual_del_time'
op|'<'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'request'
op|','
nl|'\n'
name|'content_type'
op|'='
string|"'text/plain'"
op|','
nl|'\n'
name|'body'
op|'='
string|"'X-Delete-After in past'"
op|')'
newline|'\n'
dedent|''
name|'request'
op|'.'
name|'headers'
op|'['
string|"'x-delete-at'"
op|']'
op|'='
name|'utils'
op|'.'
name|'normalize_delete_at_timestamp'
op|'('
nl|'\n'
name|'actual_del_time'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
string|"'x-delete-at'"
name|'in'
name|'request'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'x_delete_at'
op|'='
name|'int'
op|'('
name|'utils'
op|'.'
name|'normalize_delete_at_timestamp'
op|'('
nl|'\n'
name|'int'
op|'('
name|'request'
op|'.'
name|'headers'
op|'['
string|"'x-delete-at'"
op|']'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'request'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|','
nl|'\n'
name|'body'
op|'='
string|"'Non-integer X-Delete-At'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'x_delete_at'
op|'<'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'request'
op|','
name|'content_type'
op|'='
string|"'text/plain'"
op|','
nl|'\n'
name|'body'
op|'='
string|"'X-Delete-At in past'"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'request'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|check_utf8
dedent|''
name|'def'
name|'check_utf8'
op|'('
name|'string'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Validate if a string is valid UTF-8 str or unicode and that it\n    does not contain any null character.\n\n    :param string: string to be validated\n    :returns: True if the string is valid utf-8 str or unicode and\n              contains no null characters, False otherwise\n    """'
newline|'\n'
name|'if'
name|'not'
name|'string'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'False'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'isinstance'
op|'('
name|'string'
op|','
name|'six'
op|'.'
name|'text_type'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'string'
op|'.'
name|'encode'
op|'('
string|"'utf-8'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'decoded'
op|'='
name|'string'
op|'.'
name|'decode'
op|'('
string|"'UTF-8'"
op|')'
newline|'\n'
name|'if'
name|'decoded'
op|'.'
name|'encode'
op|'('
string|"'UTF-8'"
op|')'
op|'!='
name|'string'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'False'
newline|'\n'
comment|'# A UTF-8 string with surrogates in it is invalid.'
nl|'\n'
dedent|''
name|'if'
name|'any'
op|'('
number|'0xD800'
op|'<='
name|'ord'
op|'('
name|'codepoint'
op|')'
op|'<='
number|'0xDFFF'
nl|'\n'
name|'for'
name|'codepoint'
name|'in'
name|'decoded'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'False'
newline|'\n'
dedent|''
dedent|''
name|'return'
string|"'\\x00'"
name|'not'
name|'in'
name|'string'
newline|'\n'
comment|'# If string is unicode, decode() will raise UnicodeEncodeError'
nl|'\n'
comment|'# So, we should catch both UnicodeDecodeError & UnicodeEncodeError'
nl|'\n'
dedent|''
name|'except'
name|'UnicodeError'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'False'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|check_name_format
dedent|''
dedent|''
name|'def'
name|'check_name_format'
op|'('
name|'req'
op|','
name|'name'
op|','
name|'target_type'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Validate that the header contains valid account or container name.\n\n    :param req: HTTP request object\n    :param name: header value to validate\n    :param target_type: which header is being validated (Account or Container)\n    :returns: A properly encoded account name or container name\n    :raise: HTTPPreconditionFailed if account header\n            is not well formatted.\n    """'
newline|'\n'
name|'if'
name|'not'
name|'name'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'HTTPPreconditionFailed'
op|'('
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
nl|'\n'
name|'body'
op|'='
string|"'%s name cannot be empty'"
op|'%'
name|'target_type'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'isinstance'
op|'('
name|'name'
op|','
name|'six'
op|'.'
name|'text_type'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'name'
op|'='
name|'name'
op|'.'
name|'encode'
op|'('
string|"'utf-8'"
op|')'
newline|'\n'
dedent|''
name|'if'
string|"'/'"
name|'in'
name|'name'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'HTTPPreconditionFailed'
op|'('
nl|'\n'
name|'request'
op|'='
name|'req'
op|','
nl|'\n'
name|'body'
op|'='
string|"'%s name cannot contain slashes'"
op|'%'
name|'target_type'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'name'
newline|'\n'
nl|'\n'
DECL|variable|check_account_format
dedent|''
name|'check_account_format'
op|'='
name|'functools'
op|'.'
name|'partial'
op|'('
name|'check_name_format'
op|','
nl|'\n'
DECL|variable|target_type
name|'target_type'
op|'='
string|"'Account'"
op|')'
newline|'\n'
DECL|variable|check_container_format
name|'check_container_format'
op|'='
name|'functools'
op|'.'
name|'partial'
op|'('
name|'check_name_format'
op|','
nl|'\n'
DECL|variable|target_type
name|'target_type'
op|'='
string|"'Container'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|valid_api_version
name|'def'
name|'valid_api_version'
op|'('
name|'version'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'""" Checks if the requested version is valid.\n\n    Currently Swift only supports "v1" and "v1.0". """'
newline|'\n'
name|'global'
name|'VALID_API_VERSIONS'
newline|'\n'
name|'if'
name|'not'
name|'isinstance'
op|'('
name|'VALID_API_VERSIONS'
op|','
name|'list'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'VALID_API_VERSIONS'
op|'='
op|'['
name|'str'
op|'('
name|'VALID_API_VERSIONS'
op|')'
op|']'
newline|'\n'
dedent|''
name|'return'
name|'version'
name|'in'
name|'VALID_API_VERSIONS'
newline|'\n'
dedent|''
endmarker|''
end_unit
