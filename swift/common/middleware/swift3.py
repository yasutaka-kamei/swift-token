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
string|'"""\nThe swift3 middleware will emulate the S3 REST api on top of swift.\n\nThe boto python library is necessary to use this middleware (install\nthe python-boto package if you use Ubuntu).\n\nThe following opperations are currently supported:\n\n    * GET Service\n    * DELETE Bucket\n    * GET Bucket (List Objects)\n    * PUT Bucket\n    * DELETE Object\n    * GET Object\n    * HEAD Object\n    * PUT Object\n    * PUT Object (Copy)\n\nTo add this middleware to your configuration, add the swift3 middleware\nin front of the auth middleware, and before any other middleware that\nlook at swift requests (like rate limiting).\n\nTo set up your client, the access key will be the concatenation of the\naccount and user strings that should look like test:tester, and the\nsecret access key is the account password.  The host should also point\nto the swift storage hostname.  It also will have to use the old style\ncalling format, and not the hostname based container format.\n\nAn example client using the python boto library might look like the\nfollowing for an SAIO setup::\n\n    connection = boto.s3.Connection(\n        aws_access_key_id=\'test:tester\',\n        aws_secret_access_key=\'testing\',\n        port=8080,\n        host=\'127.0.0.1\',\n        is_secure=False,\n        calling_format=boto.s3.connection.OrdinaryCallingFormat())\n"""'
newline|'\n'
nl|'\n'
name|'from'
name|'urllib'
name|'import'
name|'unquote'
op|','
name|'quote'
newline|'\n'
name|'import'
name|'rfc822'
newline|'\n'
name|'import'
name|'hmac'
newline|'\n'
name|'import'
name|'base64'
newline|'\n'
name|'import'
name|'errno'
newline|'\n'
name|'import'
name|'boto'
op|'.'
name|'utils'
newline|'\n'
name|'from'
name|'xml'
op|'.'
name|'sax'
op|'.'
name|'saxutils'
name|'import'
name|'escape'
name|'as'
name|'xml_escape'
newline|'\n'
name|'import'
name|'cgi'
newline|'\n'
nl|'\n'
name|'from'
name|'webob'
name|'import'
name|'Request'
op|','
name|'Response'
newline|'\n'
name|'from'
name|'webob'
op|'.'
name|'exc'
name|'import'
name|'HTTPNotFound'
newline|'\n'
name|'from'
name|'simplejson'
name|'import'
name|'loads'
newline|'\n'
nl|'\n'
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
DECL|variable|MAX_BUCKET_LISTING
name|'MAX_BUCKET_LISTING'
op|'='
number|'1000'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_err_response
name|'def'
name|'get_err_response'
op|'('
name|'code'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Given an HTTP response code, create a properly formatted xml error response\n\n    :param code: error code\n    :returns: webob.response object\n    """'
newline|'\n'
name|'error_table'
op|'='
op|'{'
nl|'\n'
string|"'AccessDenied'"
op|':'
nl|'\n'
op|'('
number|'403'
op|','
string|"'Access denied'"
op|')'
op|','
nl|'\n'
string|"'BucketAlreadyExists'"
op|':'
nl|'\n'
op|'('
number|'409'
op|','
string|"'The requested bucket name is not available'"
op|')'
op|','
nl|'\n'
string|"'BucketNotEmpty'"
op|':'
nl|'\n'
op|'('
number|'409'
op|','
string|"'The bucket you tried to delete is not empty'"
op|')'
op|','
nl|'\n'
string|"'InvalidArgument'"
op|':'
nl|'\n'
op|'('
number|'400'
op|','
string|"'Invalid Argument'"
op|')'
op|','
nl|'\n'
string|"'InvalidBucketName'"
op|':'
nl|'\n'
op|'('
number|'400'
op|','
string|"'The specified bucket is not valid'"
op|')'
op|','
nl|'\n'
string|"'InvalidURI'"
op|':'
nl|'\n'
op|'('
number|'400'
op|','
string|"'Could not parse the specified URI'"
op|')'
op|','
nl|'\n'
string|"'NoSuchBucket'"
op|':'
nl|'\n'
op|'('
number|'404'
op|','
string|"'The specified bucket does not exist'"
op|')'
op|','
nl|'\n'
string|"'SignatureDoesNotMatch'"
op|':'
nl|'\n'
op|'('
number|'403'
op|','
string|"'The calculated request signature does not match '"
string|"'your provided one'"
op|')'
op|','
nl|'\n'
string|"'NoSuchKey'"
op|':'
nl|'\n'
op|'('
number|'404'
op|','
string|"'The resource you requested does not exist'"
op|')'
op|'}'
newline|'\n'
nl|'\n'
name|'resp'
op|'='
name|'Response'
op|'('
name|'content_type'
op|'='
string|"'text/xml'"
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'status'
op|'='
name|'error_table'
op|'['
name|'code'
op|']'
op|'['
number|'0'
op|']'
newline|'\n'
name|'resp'
op|'.'
name|'body'
op|'='
name|'error_table'
op|'['
name|'code'
op|']'
op|'['
number|'1'
op|']'
newline|'\n'
name|'resp'
op|'.'
name|'body'
op|'='
string|'\'<?xml version="1.0" encoding="UTF-8"?>\\r\\n<Error>\\r\\n  \''
string|"'<Code>%s</Code>\\r\\n  <Message>%s</Message>\\r\\n</Error>\\r\\n'"
op|'%'
op|'('
name|'code'
op|','
name|'error_table'
op|'['
name|'code'
op|']'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|Controller
dedent|''
name|'class'
name|'Controller'
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
name|'response_args'
op|'='
op|'['
op|']'
newline|'\n'
nl|'\n'
DECL|member|do_start_response
dedent|''
name|'def'
name|'do_start_response'
op|'('
name|'self'
op|','
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'response_args'
op|'.'
name|'extend'
op|'('
name|'args'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ServiceController
dedent|''
dedent|''
name|'class'
name|'ServiceController'
op|'('
name|'Controller'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Handles account level requests.\n    """'
newline|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'app'
op|','
name|'account_name'
op|','
name|'token'
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
name|'env'
op|'['
string|"'HTTP_X_AUTH_TOKEN'"
op|']'
op|'='
name|'token'
newline|'\n'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'='
string|"'/v1/%s'"
op|'%'
name|'account_name'
newline|'\n'
nl|'\n'
DECL|member|GET
dedent|''
name|'def'
name|'GET'
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
string|'"""\n        Handle GET Service request\n        """'
newline|'\n'
name|'env'
op|'['
string|"'QUERY_STRING'"
op|']'
op|'='
string|"'format=json'"
newline|'\n'
name|'body_iter'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'self'
op|'.'
name|'do_start_response'
op|')'
newline|'\n'
name|'status'
op|'='
name|'int'
op|'('
name|'self'
op|'.'
name|'response_args'
op|'['
number|'0'
op|']'
op|'.'
name|'split'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'headers'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'response_args'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'if'
name|'status'
op|'!='
number|'200'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'status'
op|'=='
number|'401'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'AccessDenied'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidURI'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'containers'
op|'='
name|'loads'
op|'('
string|"''"
op|'.'
name|'join'
op|'('
name|'list'
op|'('
name|'body_iter'
op|')'
op|')'
op|')'
newline|'\n'
comment|"# we don't keep the creation time of a backet (s3cmd doesn't"
nl|'\n'
comment|'# work without that) so we use something bogus.'
nl|'\n'
name|'body'
op|'='
string|'\'<?xml version="1.0" encoding="UTF-8"?>\''
string|"'<ListAllMyBucketsResult '"
string|'\'xmlns="http://doc.s3.amazonaws.com/2006-03-01">\''
string|"'<Buckets>%s</Buckets>'"
string|"'</ListAllMyBucketsResult>'"
op|'%'
op|'('
string|'""'
op|'.'
name|'join'
op|'('
op|'['
string|"'<Bucket><Name>%s</Name><CreationDate>'"
string|"'2009-02-03T16:45:09.000Z</CreationDate></Bucket>'"
op|'%'
nl|'\n'
name|'xml_escape'
op|'('
name|'i'
op|'['
string|"'name'"
op|']'
op|')'
name|'for'
name|'i'
name|'in'
name|'containers'
op|']'
op|')'
op|')'
newline|'\n'
name|'resp'
op|'='
name|'Response'
op|'('
name|'status'
op|'='
number|'200'
op|','
name|'content_type'
op|'='
string|"'text/xml'"
op|','
name|'body'
op|'='
name|'body'
op|')'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|BucketController
dedent|''
dedent|''
name|'class'
name|'BucketController'
op|'('
name|'Controller'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Handles bucket request.\n    """'
newline|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'app'
op|','
name|'account_name'
op|','
name|'token'
op|','
name|'container_name'
op|','
nl|'\n'
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
name|'container_name'
op|'='
name|'unquote'
op|'('
name|'container_name'
op|')'
newline|'\n'
name|'env'
op|'['
string|"'HTTP_X_AUTH_TOKEN'"
op|']'
op|'='
name|'token'
newline|'\n'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'='
string|"'/v1/%s/%s'"
op|'%'
op|'('
name|'account_name'
op|','
name|'container_name'
op|')'
newline|'\n'
nl|'\n'
DECL|member|GET
dedent|''
name|'def'
name|'GET'
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
string|'"""\n        Handle GET Bucket (List Objects) request\n        """'
newline|'\n'
name|'if'
string|"'QUERY_STRING'"
name|'in'
name|'env'
op|':'
newline|'\n'
indent|'            '
name|'args'
op|'='
name|'dict'
op|'('
name|'cgi'
op|'.'
name|'parse_qsl'
op|'('
name|'env'
op|'['
string|"'QUERY_STRING'"
op|']'
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'args'
op|'='
op|'{'
op|'}'
newline|'\n'
dedent|''
name|'max_keys'
op|'='
name|'min'
op|'('
name|'int'
op|'('
name|'args'
op|'.'
name|'get'
op|'('
string|"'max-keys'"
op|','
name|'MAX_BUCKET_LISTING'
op|')'
op|')'
op|','
nl|'\n'
name|'MAX_BUCKET_LISTING'
op|')'
newline|'\n'
name|'env'
op|'['
string|"'QUERY_STRING'"
op|']'
op|'='
string|"'format=json&limit=%s'"
op|'%'
op|'('
name|'max_keys'
op|'+'
number|'1'
op|')'
newline|'\n'
name|'if'
string|"'marker'"
name|'in'
name|'args'
op|':'
newline|'\n'
indent|'            '
name|'env'
op|'['
string|"'QUERY_STRING'"
op|']'
op|'+='
string|"'&marker=%s'"
op|'%'
name|'quote'
op|'('
name|'args'
op|'['
string|"'marker'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'if'
string|"'prefix'"
name|'in'
name|'args'
op|':'
newline|'\n'
indent|'            '
name|'env'
op|'['
string|"'QUERY_STRING'"
op|']'
op|'+='
string|"'&prefix=%s'"
op|'%'
name|'quote'
op|'('
name|'args'
op|'['
string|"'prefix'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'if'
string|"'delimiter'"
name|'in'
name|'args'
op|':'
newline|'\n'
indent|'            '
name|'env'
op|'['
string|"'QUERY_STRING'"
op|']'
op|'+='
string|"'&delimiter=%s'"
op|'%'
name|'quote'
op|'('
name|'args'
op|'['
string|"'delimiter'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'body_iter'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'self'
op|'.'
name|'do_start_response'
op|')'
newline|'\n'
name|'status'
op|'='
name|'int'
op|'('
name|'self'
op|'.'
name|'response_args'
op|'['
number|'0'
op|']'
op|'.'
name|'split'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'headers'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'response_args'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'if'
name|'status'
op|'!='
number|'200'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'status'
op|'=='
number|'401'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'AccessDenied'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'status'
op|'=='
number|'404'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidBucketName'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidURI'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'objects'
op|'='
name|'loads'
op|'('
string|"''"
op|'.'
name|'join'
op|'('
name|'list'
op|'('
name|'body_iter'
op|')'
op|')'
op|')'
newline|'\n'
name|'body'
op|'='
op|'('
string|'\'<?xml version="1.0" encoding="UTF-8"?>\''
nl|'\n'
string|"'<ListBucketResult '"
nl|'\n'
string|'\'xmlns="http://s3.amazonaws.com/doc/2006-03-01">\''
nl|'\n'
string|"'<Prefix>%s</Prefix>'"
nl|'\n'
string|"'<Marker>%s</Marker>'"
nl|'\n'
string|"'<Delimiter>%s</Delimiter>'"
nl|'\n'
string|"'<IsTruncated>%s</IsTruncated>'"
nl|'\n'
string|"'<MaxKeys>%s</MaxKeys>'"
nl|'\n'
string|"'<Name>%s</Name>'"
nl|'\n'
string|"'%s'"
nl|'\n'
string|"'%s'"
nl|'\n'
string|"'</ListBucketResult>'"
op|'%'
nl|'\n'
op|'('
nl|'\n'
name|'xml_escape'
op|'('
name|'args'
op|'.'
name|'get'
op|'('
string|"'prefix'"
op|','
string|"''"
op|')'
op|')'
op|','
nl|'\n'
name|'xml_escape'
op|'('
name|'args'
op|'.'
name|'get'
op|'('
string|"'marker'"
op|','
string|"''"
op|')'
op|')'
op|','
nl|'\n'
name|'xml_escape'
op|'('
name|'args'
op|'.'
name|'get'
op|'('
string|"'delimiter'"
op|','
string|"''"
op|')'
op|')'
op|','
nl|'\n'
string|"'true'"
name|'if'
name|'len'
op|'('
name|'objects'
op|')'
op|'=='
op|'('
name|'max_keys'
op|'+'
number|'1'
op|')'
name|'else'
string|"'false'"
op|','
nl|'\n'
name|'max_keys'
op|','
nl|'\n'
name|'xml_escape'
op|'('
name|'self'
op|'.'
name|'container_name'
op|')'
op|','
nl|'\n'
string|'""'
op|'.'
name|'join'
op|'('
op|'['
string|"'<Contents><Key>%s</Key><LastModified>%s</LastModif'"
string|"'ied><ETag>%s</ETag><Size>%s</Size><StorageClass>STA'"
string|"'NDARD</StorageClass></Contents>'"
op|'%'
nl|'\n'
op|'('
name|'xml_escape'
op|'('
name|'i'
op|'['
string|"'name'"
op|']'
op|')'
op|','
name|'i'
op|'['
string|"'last_modified'"
op|']'
op|','
name|'i'
op|'['
string|"'hash'"
op|']'
op|','
nl|'\n'
name|'i'
op|'['
string|"'bytes'"
op|']'
op|')'
nl|'\n'
name|'for'
name|'i'
name|'in'
name|'objects'
op|'['
op|':'
name|'max_keys'
op|']'
name|'if'
string|"'subdir'"
name|'not'
name|'in'
name|'i'
op|']'
op|')'
op|','
nl|'\n'
string|'""'
op|'.'
name|'join'
op|'('
op|'['
string|"'<CommonPrefixes><Prefix>%s</Prefix></CommonPrefixes>'"
nl|'\n'
op|'%'
name|'xml_escape'
op|'('
name|'i'
op|'['
string|"'subdir'"
op|']'
op|')'
nl|'\n'
name|'for'
name|'i'
name|'in'
name|'objects'
op|'['
op|':'
name|'max_keys'
op|']'
name|'if'
string|"'subdir'"
name|'in'
name|'i'
op|']'
op|')'
op|')'
op|')'
newline|'\n'
name|'return'
name|'Response'
op|'('
name|'body'
op|'='
name|'body'
op|','
name|'content_type'
op|'='
string|"'text/xml'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|PUT
dedent|''
name|'def'
name|'PUT'
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
string|'"""\n        Handle PUT Bucket request\n        """'
newline|'\n'
name|'body_iter'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'self'
op|'.'
name|'do_start_response'
op|')'
newline|'\n'
name|'status'
op|'='
name|'int'
op|'('
name|'self'
op|'.'
name|'response_args'
op|'['
number|'0'
op|']'
op|'.'
name|'split'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'headers'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'response_args'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'if'
name|'status'
op|'!='
number|'201'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'status'
op|'=='
number|'401'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'AccessDenied'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'status'
op|'=='
number|'202'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'BucketAlreadyExists'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidURI'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'resp'
op|'='
name|'Response'
op|'('
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'headers'
op|'.'
name|'add'
op|'('
string|"'Location'"
op|','
name|'self'
op|'.'
name|'container_name'
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'status'
op|'='
number|'200'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
DECL|member|DELETE
dedent|''
name|'def'
name|'DELETE'
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
string|'"""\n        Handle DELETE Bucket request\n        """'
newline|'\n'
name|'body_iter'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'self'
op|'.'
name|'do_start_response'
op|')'
newline|'\n'
name|'status'
op|'='
name|'int'
op|'('
name|'self'
op|'.'
name|'response_args'
op|'['
number|'0'
op|']'
op|'.'
name|'split'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'headers'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'response_args'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'if'
name|'status'
op|'!='
number|'204'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'status'
op|'=='
number|'401'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'AccessDenied'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'status'
op|'=='
number|'404'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidBucketName'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'status'
op|'=='
number|'409'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'BucketNotEmpty'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidURI'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'resp'
op|'='
name|'Response'
op|'('
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'status'
op|'='
number|'204'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|ObjectController
dedent|''
dedent|''
name|'class'
name|'ObjectController'
op|'('
name|'Controller'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Handles requests on objects\n    """'
newline|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'app'
op|','
name|'account_name'
op|','
name|'token'
op|','
name|'container_name'
op|','
nl|'\n'
name|'object_name'
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
name|'container_name'
op|'='
name|'unquote'
op|'('
name|'container_name'
op|')'
newline|'\n'
name|'env'
op|'['
string|"'HTTP_X_AUTH_TOKEN'"
op|']'
op|'='
name|'token'
newline|'\n'
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'='
string|"'/v1/%s/%s/%s'"
op|'%'
op|'('
name|'account_name'
op|','
name|'container_name'
op|','
nl|'\n'
name|'object_name'
op|')'
newline|'\n'
nl|'\n'
DECL|member|GETorHEAD
dedent|''
name|'def'
name|'GETorHEAD'
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
name|'app_iter'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'self'
op|'.'
name|'do_start_response'
op|')'
newline|'\n'
name|'status'
op|'='
name|'int'
op|'('
name|'self'
op|'.'
name|'response_args'
op|'['
number|'0'
op|']'
op|'.'
name|'split'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'headers'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'response_args'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'if'
number|'200'
op|'<='
name|'status'
op|'<'
number|'300'
op|':'
newline|'\n'
indent|'            '
name|'new_hdrs'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'key'
op|','
name|'val'
name|'in'
name|'headers'
op|'.'
name|'iteritems'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'_key'
op|'='
name|'key'
op|'.'
name|'lower'
op|'('
op|')'
newline|'\n'
name|'if'
name|'_key'
op|'.'
name|'startswith'
op|'('
string|"'x-object-meta-'"
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'new_hdrs'
op|'['
string|"'x-amz-meta-'"
op|'+'
name|'key'
op|'['
number|'14'
op|':'
op|']'
op|']'
op|'='
name|'val'
newline|'\n'
dedent|''
name|'elif'
name|'_key'
name|'in'
op|'('
string|"'content-length'"
op|','
string|"'content-type'"
op|','
nl|'\n'
string|"'content-encoding'"
op|','
string|"'etag'"
op|','
string|"'last-modified'"
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'new_hdrs'
op|'['
name|'key'
op|']'
op|'='
name|'val'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'Response'
op|'('
name|'status'
op|'='
name|'status'
op|','
name|'headers'
op|'='
name|'new_hdrs'
op|','
name|'app_iter'
op|'='
name|'app_iter'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'status'
op|'=='
number|'401'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'AccessDenied'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'status'
op|'=='
number|'404'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'NoSuchKey'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidURI'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|HEAD
dedent|''
dedent|''
name|'def'
name|'HEAD'
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
string|'"""\n        Handle HEAD Object request\n        """'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'GETorHEAD'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
DECL|member|GET
dedent|''
name|'def'
name|'GET'
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
string|'"""\n        Handle GET Object request\n        """'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'GETorHEAD'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
DECL|member|PUT
dedent|''
name|'def'
name|'PUT'
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
string|'"""\n        Handle PUT Object and PUT Object (Copy) request\n        """'
newline|'\n'
name|'for'
name|'key'
op|','
name|'value'
name|'in'
name|'env'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'key'
op|'.'
name|'startswith'
op|'('
string|"'HTTP_X_AMZ_META_'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'del'
name|'env'
op|'['
name|'key'
op|']'
newline|'\n'
name|'env'
op|'['
string|"'HTTP_X_OBJECT_META_'"
op|'+'
name|'key'
op|'['
number|'16'
op|':'
op|']'
op|']'
op|'='
name|'value'
newline|'\n'
dedent|''
name|'elif'
name|'key'
op|'=='
string|"'HTTP_CONTENT_MD5'"
op|':'
newline|'\n'
indent|'                '
name|'env'
op|'['
string|"'HTTP_ETAG'"
op|']'
op|'='
name|'value'
op|'.'
name|'decode'
op|'('
string|"'base64'"
op|')'
op|'.'
name|'encode'
op|'('
string|"'hex'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'key'
op|'=='
string|"'HTTP_X_AMZ_COPY_SOURCE'"
op|':'
newline|'\n'
indent|'                '
name|'env'
op|'['
string|"'HTTP_X_COPY_FROM'"
op|']'
op|'='
name|'value'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'body_iter'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'self'
op|'.'
name|'do_start_response'
op|')'
newline|'\n'
name|'status'
op|'='
name|'int'
op|'('
name|'self'
op|'.'
name|'response_args'
op|'['
number|'0'
op|']'
op|'.'
name|'split'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'headers'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'response_args'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'if'
name|'status'
op|'!='
number|'201'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'status'
op|'=='
number|'401'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'AccessDenied'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'status'
op|'=='
number|'404'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidBucketName'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidURI'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'if'
string|"'HTTP_X_COPY_FROM'"
name|'in'
name|'env'
op|':'
newline|'\n'
indent|'            '
name|'body'
op|'='
string|"'<CopyObjectResult>'"
string|'\'<ETag>"%s"</ETag>\''
string|"'</CopyObjectResult>'"
op|'%'
name|'headers'
op|'['
string|"'etag'"
op|']'
newline|'\n'
name|'return'
name|'Response'
op|'('
name|'status'
op|'='
number|'200'
op|','
name|'body'
op|'='
name|'body'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'Response'
op|'('
name|'status'
op|'='
number|'200'
op|','
name|'etag'
op|'='
name|'headers'
op|'['
string|"'etag'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|DELETE
dedent|''
name|'def'
name|'DELETE'
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
string|'"""\n        Handle DELETE Object request\n        """'
newline|'\n'
name|'body_iter'
op|'='
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'self'
op|'.'
name|'do_start_response'
op|')'
newline|'\n'
name|'status'
op|'='
name|'int'
op|'('
name|'self'
op|'.'
name|'response_args'
op|'['
number|'0'
op|']'
op|'.'
name|'split'
op|'('
op|')'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
name|'headers'
op|'='
name|'dict'
op|'('
name|'self'
op|'.'
name|'response_args'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'if'
name|'status'
op|'!='
number|'204'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'status'
op|'=='
number|'401'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'AccessDenied'"
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'status'
op|'=='
number|'404'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'NoSuchKey'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidURI'"
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'resp'
op|'='
name|'Response'
op|'('
op|')'
newline|'\n'
name|'resp'
op|'.'
name|'status'
op|'='
number|'204'
newline|'\n'
name|'return'
name|'resp'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|Swift3Middleware
dedent|''
dedent|''
name|'class'
name|'Swift3Middleware'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Swift3 S3 compatibility midleware"""'
newline|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'app'
op|','
name|'conf'
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
DECL|member|get_controller
dedent|''
name|'def'
name|'get_controller'
op|'('
name|'self'
op|','
name|'path'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'container'
op|','
name|'obj'
op|'='
name|'split_path'
op|'('
name|'path'
op|','
number|'0'
op|','
number|'2'
op|')'
newline|'\n'
name|'d'
op|'='
name|'dict'
op|'('
name|'container_name'
op|'='
name|'container'
op|','
name|'object_name'
op|'='
name|'obj'
op|')'
newline|'\n'
nl|'\n'
name|'if'
name|'container'
name|'and'
name|'obj'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'ObjectController'
op|','
name|'d'
newline|'\n'
dedent|''
name|'elif'
name|'container'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'BucketController'
op|','
name|'d'
newline|'\n'
dedent|''
name|'return'
name|'ServiceController'
op|','
name|'d'
newline|'\n'
nl|'\n'
DECL|member|get_account_info
dedent|''
name|'def'
name|'get_account_info'
op|'('
name|'self'
op|','
name|'env'
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
name|'account'
op|','
name|'user'
op|','
name|'_junk'
op|'='
name|'req'
op|'.'
name|'headers'
op|'['
string|"'Authorization'"
op|']'
op|'.'
name|'split'
op|'('
string|"' '"
op|')'
op|'['
op|'-'
number|'1'
op|']'
op|'.'
name|'split'
op|'('
string|"':'"
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'None'
op|','
name|'None'
newline|'\n'
nl|'\n'
dedent|''
name|'headers'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'key'
name|'in'
name|'req'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'type'
op|'('
name|'req'
op|'.'
name|'headers'
op|'['
name|'key'
op|']'
op|')'
op|'=='
name|'str'
op|':'
newline|'\n'
indent|'                '
name|'headers'
op|'['
name|'key'
op|']'
op|'='
name|'req'
op|'.'
name|'headers'
op|'['
name|'key'
op|']'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'h'
op|'='
name|'boto'
op|'.'
name|'utils'
op|'.'
name|'canonical_string'
op|'('
name|'req'
op|'.'
name|'method'
op|','
name|'req'
op|'.'
name|'path_qs'
op|','
name|'headers'
op|')'
newline|'\n'
name|'token'
op|'='
name|'base64'
op|'.'
name|'urlsafe_b64encode'
op|'('
name|'h'
op|')'
newline|'\n'
name|'return'
string|"'%s:%s'"
op|'%'
op|'('
name|'account'
op|','
name|'user'
op|')'
op|','
name|'token'
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
name|'req'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
newline|'\n'
name|'if'
name|'not'
string|"'Authorization'"
name|'in'
name|'req'
op|'.'
name|'headers'
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
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'controller'
op|','
name|'path_parts'
op|'='
name|'self'
op|'.'
name|'get_controller'
op|'('
name|'req'
op|'.'
name|'path'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidURI'"
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'account_name'
op|','
name|'token'
op|'='
name|'self'
op|'.'
name|'get_account_info'
op|'('
name|'env'
op|','
name|'req'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'account_name'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidArgument'"
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'controller'
op|'='
name|'controller'
op|'('
name|'env'
op|','
name|'self'
op|'.'
name|'app'
op|','
name|'account_name'
op|','
name|'token'
op|','
nl|'\n'
op|'**'
name|'path_parts'
op|')'
newline|'\n'
name|'if'
name|'hasattr'
op|'('
name|'controller'
op|','
name|'req'
op|'.'
name|'method'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'res'
op|'='
name|'getattr'
op|'('
name|'controller'
op|','
name|'req'
op|'.'
name|'method'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'get_err_response'
op|'('
string|"'InvalidURI'"
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'res'
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
string|'"""Standard filter factory to use the middleware with paste.deploy"""'
newline|'\n'
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
DECL|function|swift3_filter
name|'def'
name|'swift3_filter'
op|'('
name|'app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'Swift3Middleware'
op|'('
name|'app'
op|','
name|'conf'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'swift3_filter'
newline|'\n'
dedent|''
endmarker|''
end_unit
