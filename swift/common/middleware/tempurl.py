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
string|'"""\nTempURL Middleware\n\nAllows the creation of URLs to provide temporary access to objects.\n\nFor example, a website may wish to provide a link to download a large\nobject in Swift, but the Swift account has no public access. The\nwebsite can generate a URL that will provide GET access for a limited\ntime to the resource. When the web browser user clicks on the link,\nthe browser will download the object directly from Swift, obviating\nthe need for the website to act as a proxy for the request.\n\nIf the user were to share the link with all his friends, or\naccidentally post it on a forum, etc. the direct access would be\nlimited to the expiration time set when the website created the link.\n\nTo create such temporary URLs, first an X-Account-Meta-Temp-URL-Key\nheader must be set on the Swift account. Then, an HMAC-SHA1 (RFC 2104)\nsignature is generated using the HTTP method to allow (GET or PUT),\nthe Unix timestamp the access should be allowed until, the full path\nto the object, and the key set on the account.\n\nFor example, here is code generating the signature for a GET for 60\nseconds on /v1/AUTH_account/container/object::\n\n    import hmac\n    from hashlib import sha1\n    from time import time\n    method = \'GET\'\n    expires = int(time() + 60)\n    path = \'/v1/AUTH_account/container/object\'\n    key = \'mykey\'\n    hmac_body = \'%s\\\\n%s\\\\n%s\' % (method, expires, path)\n    sig = hmac.new(key, hmac_body, sha1).hexdigest()\n\nBe certain to use the full path, from the /v1/ onward.\n\nLet\'s say the sig ends up equaling\nda39a3ee5e6b4b0d3255bfef95601890afd80709 and expires ends up\n1323479485. Then, for example, the website could provide a link to::\n\n    https://swift-cluster.example.com/v1/AUTH_account/container/object?\n    temp_url_sig=da39a3ee5e6b4b0d3255bfef95601890afd80709&\n    temp_url_expires=1323479485\n\nAny alteration of the resource path or query arguments would result\nin 401 Unauthorized. Similary, a PUT where GET was the allowed method\nwould 401. HEAD is allowed if GET or PUT is allowed.\n\nUsing this in combination with browser form post translation\nmiddleware could also allow direct-from-browser uploads to specific\nlocations in Swift.\n\nTempURL supports up to two keys, specified by X-Account-Meta-Temp-URL-Key and\nX-Account-Meta-Temp-URL-Key-2. Signatures are checked against both keys, if\npresent. This is to allow for key rotation without invalidating all existing\ntemporary URLs.\n\nWith GET TempURLs, a Content-Disposition header will be set on the\nresponse so that browsers will interpret this as a file attachment to\nbe saved. The filename chosen is based on the object name, but you\ncan override this with a filename query parameter. Modifying the\nabove example::\n\n    https://swift-cluster.example.com/v1/AUTH_account/container/object?\n    temp_url_sig=da39a3ee5e6b4b0d3255bfef95601890afd80709&\n    temp_url_expires=1323479485&filename=My+Test+File.pdf\n\nIf you do not want the object to be downloaded, you can cause\n"Content-Disposition: inline" to be set on the response by adding the "inline"\nparameter to the query string, like so::\n\n    https://swift-cluster.example.com/v1/AUTH_account/container/object?\n    temp_url_sig=da39a3ee5e6b4b0d3255bfef95601890afd80709&\n    temp_url_expires=1323479485&inline\n\n"""'
newline|'\n'
nl|'\n'
DECL|variable|__all__
name|'__all__'
op|'='
op|'['
string|"'TempURL'"
op|','
string|"'filter_factory'"
op|','
nl|'\n'
string|"'DEFAULT_INCOMING_REMOVE_HEADERS'"
op|','
nl|'\n'
string|"'DEFAULT_INCOMING_ALLOW_HEADERS'"
op|','
nl|'\n'
string|"'DEFAULT_OUTGOING_REMOVE_HEADERS'"
op|','
nl|'\n'
string|"'DEFAULT_OUTGOING_ALLOW_HEADERS'"
op|']'
newline|'\n'
nl|'\n'
nl|'\n'
name|'from'
name|'os'
op|'.'
name|'path'
name|'import'
name|'basename'
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'time'
newline|'\n'
name|'from'
name|'urllib'
name|'import'
name|'urlencode'
newline|'\n'
name|'from'
name|'urlparse'
name|'import'
name|'parse_qs'
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
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'HeaderKeyDict'
op|','
name|'HTTPUnauthorized'
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
name|'get_valid_utf8_str'
op|','
name|'register_swift_info'
op|','
name|'get_hmac'
newline|'\n'
nl|'\n'
nl|'\n'
comment|'#: Default headers to remove from incoming requests. Simply a whitespace'
nl|'\n'
comment|"#: delimited list of header names and names can optionally end with '*' to"
nl|'\n'
comment|'#: indicate a prefix match. DEFAULT_INCOMING_ALLOW_HEADERS is a list of'
nl|'\n'
comment|'#: exceptions to these removals.'
nl|'\n'
DECL|variable|DEFAULT_INCOMING_REMOVE_HEADERS
name|'DEFAULT_INCOMING_REMOVE_HEADERS'
op|'='
string|"'x-timestamp'"
newline|'\n'
nl|'\n'
comment|'#: Default headers as exceptions to DEFAULT_INCOMING_REMOVE_HEADERS. Simply a'
nl|'\n'
comment|'#: whitespace delimited list of header names and names can optionally end with'
nl|'\n'
comment|"#: '*' to indicate a prefix match."
nl|'\n'
DECL|variable|DEFAULT_INCOMING_ALLOW_HEADERS
name|'DEFAULT_INCOMING_ALLOW_HEADERS'
op|'='
string|"''"
newline|'\n'
nl|'\n'
comment|'#: Default headers to remove from outgoing responses. Simply a whitespace'
nl|'\n'
comment|"#: delimited list of header names and names can optionally end with '*' to"
nl|'\n'
comment|'#: indicate a prefix match. DEFAULT_OUTGOING_ALLOW_HEADERS is a list of'
nl|'\n'
comment|'#: exceptions to these removals.'
nl|'\n'
DECL|variable|DEFAULT_OUTGOING_REMOVE_HEADERS
name|'DEFAULT_OUTGOING_REMOVE_HEADERS'
op|'='
string|"'x-object-meta-*'"
newline|'\n'
nl|'\n'
comment|'#: Default headers as exceptions to DEFAULT_OUTGOING_REMOVE_HEADERS. Simply a'
nl|'\n'
comment|'#: whitespace delimited list of header names and names can optionally end with'
nl|'\n'
comment|"#: '*' to indicate a prefix match."
nl|'\n'
DECL|variable|DEFAULT_OUTGOING_ALLOW_HEADERS
name|'DEFAULT_OUTGOING_ALLOW_HEADERS'
op|'='
string|"'x-object-meta-public-*'"
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_tempurl_keys_from_metadata
name|'def'
name|'get_tempurl_keys_from_metadata'
op|'('
name|'meta'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Extracts the tempurl keys from metadata.\n\n    :param meta: account metadata\n    :returns: list of keys found (possibly empty if no keys set)\n\n    Example:\n      meta = get_account_info(...)[\'meta\']\n      keys = get_tempurl_keys_from_metadata(meta)\n    """'
newline|'\n'
name|'return'
op|'['
name|'get_valid_utf8_str'
op|'('
name|'value'
op|')'
name|'for'
name|'key'
op|','
name|'value'
name|'in'
name|'meta'
op|'.'
name|'iteritems'
op|'('
op|')'
nl|'\n'
name|'if'
name|'key'
op|'.'
name|'lower'
op|'('
op|')'
name|'in'
op|'('
string|"'temp-url-key'"
op|','
string|"'temp-url-key-2'"
op|')'
op|']'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TempURL
dedent|''
name|'class'
name|'TempURL'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    WSGI Middleware to grant temporary URLs specific access to Swift\n    resources. See the overview for more information.\n\n    This middleware understands the following configuration settings::\n\n        incoming_remove_headers\n            The headers to remove from incoming requests. Simply a\n            whitespace delimited list of header names and names can\n            optionally end with \'*\' to indicate a prefix match.\n            incoming_allow_headers is a list of exceptions to these\n            removals.\n            Default: x-timestamp\n\n        incoming_allow_headers\n            The headers allowed as exceptions to\n            incoming_remove_headers. Simply a whitespace delimited\n            list of header names and names can optionally end with\n            \'*\' to indicate a prefix match.\n            Default: None\n\n        outgoing_remove_headers\n            The headers to remove from outgoing responses. Simply a\n            whitespace delimited list of header names and names can\n            optionally end with \'*\' to indicate a prefix match.\n            outgoing_allow_headers is a list of exceptions to these\n            removals.\n            Default: x-object-meta-*\n\n        outgoing_allow_headers\n            The headers allowed as exceptions to\n            outgoing_remove_headers. Simply a whitespace delimited\n            list of header names and names can optionally end with\n            \'*\' to indicate a prefix match.\n            Default: x-object-meta-public-*\n\n    The proxy logs created for any subrequests made will have swift.source set\n    to "FP".\n\n    :param app: The next WSGI filter or app in the paste.deploy\n                chain.\n    :param conf: The configuration dict for the middleware.\n    """'
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
op|','
name|'methods'
op|'='
op|'('
string|"'GET'"
op|','
string|"'HEAD'"
op|','
string|"'PUT'"
op|')'
op|')'
op|':'
newline|'\n'
comment|'#: The next WSGI application/filter in the paste.deploy pipeline.'
nl|'\n'
indent|'        '
name|'self'
op|'.'
name|'app'
op|'='
name|'app'
newline|'\n'
comment|'#: The filter configuration dict.'
nl|'\n'
name|'self'
op|'.'
name|'conf'
op|'='
name|'conf'
newline|'\n'
nl|'\n'
comment|'#: The methods allowed with Temp URLs.'
nl|'\n'
name|'self'
op|'.'
name|'methods'
op|'='
name|'methods'
newline|'\n'
nl|'\n'
name|'headers'
op|'='
name|'DEFAULT_INCOMING_REMOVE_HEADERS'
newline|'\n'
name|'if'
string|"'incoming_remove_headers'"
name|'in'
name|'conf'
op|':'
newline|'\n'
indent|'            '
name|'headers'
op|'='
name|'conf'
op|'['
string|"'incoming_remove_headers'"
op|']'
newline|'\n'
dedent|''
name|'headers'
op|'='
op|'['
string|"'HTTP_'"
op|'+'
name|'h'
op|'.'
name|'upper'
op|'('
op|')'
op|'.'
name|'replace'
op|'('
string|"'-'"
op|','
string|"'_'"
op|')'
name|'for'
name|'h'
name|'in'
name|'headers'
op|'.'
name|'split'
op|'('
op|')'
op|']'
newline|'\n'
comment|'#: Headers to remove from incoming requests. Uppercase WSGI env style,'
nl|'\n'
comment|'#: like `HTTP_X_PRIVATE`.'
nl|'\n'
name|'self'
op|'.'
name|'incoming_remove_headers'
op|'='
op|'['
name|'h'
name|'for'
name|'h'
name|'in'
name|'headers'
name|'if'
name|'h'
op|'['
op|'-'
number|'1'
op|']'
op|'!='
string|"'*'"
op|']'
newline|'\n'
comment|'#: Header with match prefixes to remove from incoming requests.'
nl|'\n'
comment|'#: Uppercase WSGI env style, like `HTTP_X_SENSITIVE_*`.'
nl|'\n'
name|'self'
op|'.'
name|'incoming_remove_headers_startswith'
op|'='
op|'['
name|'h'
op|'['
op|':'
op|'-'
number|'1'
op|']'
name|'for'
name|'h'
name|'in'
name|'headers'
name|'if'
name|'h'
op|'['
op|'-'
number|'1'
op|']'
op|'=='
string|"'*'"
op|']'
newline|'\n'
nl|'\n'
name|'headers'
op|'='
name|'DEFAULT_INCOMING_ALLOW_HEADERS'
newline|'\n'
name|'if'
string|"'incoming_allow_headers'"
name|'in'
name|'conf'
op|':'
newline|'\n'
indent|'            '
name|'headers'
op|'='
name|'conf'
op|'['
string|"'incoming_allow_headers'"
op|']'
newline|'\n'
dedent|''
name|'headers'
op|'='
op|'['
string|"'HTTP_'"
op|'+'
name|'h'
op|'.'
name|'upper'
op|'('
op|')'
op|'.'
name|'replace'
op|'('
string|"'-'"
op|','
string|"'_'"
op|')'
name|'for'
name|'h'
name|'in'
name|'headers'
op|'.'
name|'split'
op|'('
op|')'
op|']'
newline|'\n'
comment|'#: Headers to allow in incoming requests. Uppercase WSGI env style,'
nl|'\n'
comment|'#: like `HTTP_X_MATCHES_REMOVE_PREFIX_BUT_OKAY`.'
nl|'\n'
name|'self'
op|'.'
name|'incoming_allow_headers'
op|'='
op|'['
name|'h'
name|'for'
name|'h'
name|'in'
name|'headers'
name|'if'
name|'h'
op|'['
op|'-'
number|'1'
op|']'
op|'!='
string|"'*'"
op|']'
newline|'\n'
comment|'#: Header with match prefixes to allow in incoming requests. Uppercase'
nl|'\n'
comment|'#: WSGI env style, like `HTTP_X_MATCHES_REMOVE_PREFIX_BUT_OKAY_*`.'
nl|'\n'
name|'self'
op|'.'
name|'incoming_allow_headers_startswith'
op|'='
op|'['
name|'h'
op|'['
op|':'
op|'-'
number|'1'
op|']'
name|'for'
name|'h'
name|'in'
name|'headers'
name|'if'
name|'h'
op|'['
op|'-'
number|'1'
op|']'
op|'=='
string|"'*'"
op|']'
newline|'\n'
nl|'\n'
name|'headers'
op|'='
name|'DEFAULT_OUTGOING_REMOVE_HEADERS'
newline|'\n'
name|'if'
string|"'outgoing_remove_headers'"
name|'in'
name|'conf'
op|':'
newline|'\n'
indent|'            '
name|'headers'
op|'='
name|'conf'
op|'['
string|"'outgoing_remove_headers'"
op|']'
newline|'\n'
dedent|''
name|'headers'
op|'='
op|'['
name|'h'
op|'.'
name|'title'
op|'('
op|')'
name|'for'
name|'h'
name|'in'
name|'headers'
op|'.'
name|'split'
op|'('
op|')'
op|']'
newline|'\n'
comment|'#: Headers to remove from outgoing responses. Lowercase, like'
nl|'\n'
comment|'#: `x-account-meta-temp-url-key`.'
nl|'\n'
name|'self'
op|'.'
name|'outgoing_remove_headers'
op|'='
op|'['
name|'h'
name|'for'
name|'h'
name|'in'
name|'headers'
name|'if'
name|'h'
op|'['
op|'-'
number|'1'
op|']'
op|'!='
string|"'*'"
op|']'
newline|'\n'
comment|'#: Header with match prefixes to remove from outgoing responses.'
nl|'\n'
comment|'#: Lowercase, like `x-account-meta-private-*`.'
nl|'\n'
name|'self'
op|'.'
name|'outgoing_remove_headers_startswith'
op|'='
op|'['
name|'h'
op|'['
op|':'
op|'-'
number|'1'
op|']'
name|'for'
name|'h'
name|'in'
name|'headers'
name|'if'
name|'h'
op|'['
op|'-'
number|'1'
op|']'
op|'=='
string|"'*'"
op|']'
newline|'\n'
nl|'\n'
name|'headers'
op|'='
name|'DEFAULT_OUTGOING_ALLOW_HEADERS'
newline|'\n'
name|'if'
string|"'outgoing_allow_headers'"
name|'in'
name|'conf'
op|':'
newline|'\n'
indent|'            '
name|'headers'
op|'='
name|'conf'
op|'['
string|"'outgoing_allow_headers'"
op|']'
newline|'\n'
dedent|''
name|'headers'
op|'='
op|'['
name|'h'
op|'.'
name|'title'
op|'('
op|')'
name|'for'
name|'h'
name|'in'
name|'headers'
op|'.'
name|'split'
op|'('
op|')'
op|']'
newline|'\n'
comment|'#: Headers to allow in outgoing responses. Lowercase, like'
nl|'\n'
comment|'#: `x-matches-remove-prefix-but-okay`.'
nl|'\n'
name|'self'
op|'.'
name|'outgoing_allow_headers'
op|'='
op|'['
name|'h'
name|'for'
name|'h'
name|'in'
name|'headers'
name|'if'
name|'h'
op|'['
op|'-'
number|'1'
op|']'
op|'!='
string|"'*'"
op|']'
newline|'\n'
comment|'#: Header with match prefixes to allow in outgoing responses.'
nl|'\n'
comment|'#: Lowercase, like `x-matches-remove-prefix-but-okay-*`.'
nl|'\n'
name|'self'
op|'.'
name|'outgoing_allow_headers_startswith'
op|'='
op|'['
name|'h'
op|'['
op|':'
op|'-'
number|'1'
op|']'
name|'for'
name|'h'
name|'in'
name|'headers'
name|'if'
name|'h'
op|'['
op|'-'
number|'1'
op|']'
op|'=='
string|"'*'"
op|']'
newline|'\n'
comment|'#: HTTP user agent to use for subrequests.'
nl|'\n'
name|'self'
op|'.'
name|'agent'
op|'='
string|"'%(orig)s TempURL'"
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
string|'"""\n        Main hook into the WSGI paste.deploy filter/app pipeline.\n\n        :param env: The WSGI environment dict.\n        :param start_response: The WSGI start_response hook.\n        :returns: Response as per WSGI.\n        """'
newline|'\n'
name|'if'
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
op|'=='
string|"'OPTIONS'"
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
name|'info'
op|'='
name|'self'
op|'.'
name|'_get_temp_url_info'
op|'('
name|'env'
op|')'
newline|'\n'
name|'temp_url_sig'
op|','
name|'temp_url_expires'
op|','
name|'filename'
op|','
name|'inline_disposition'
op|'='
name|'info'
newline|'\n'
name|'if'
name|'temp_url_sig'
name|'is'
name|'None'
name|'and'
name|'temp_url_expires'
name|'is'
name|'None'
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
name|'not'
name|'temp_url_sig'
name|'or'
name|'not'
name|'temp_url_expires'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_invalid'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'account'
op|'='
name|'self'
op|'.'
name|'_get_account'
op|'('
name|'env'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'account'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_invalid'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'keys'
op|'='
name|'self'
op|'.'
name|'_get_keys'
op|'('
name|'env'
op|','
name|'account'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'keys'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_invalid'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
op|'=='
string|"'HEAD'"
op|':'
newline|'\n'
indent|'            '
name|'hmac_vals'
op|'='
op|'('
nl|'\n'
name|'self'
op|'.'
name|'_get_hmacs'
op|'('
name|'env'
op|','
name|'temp_url_expires'
op|','
name|'keys'
op|')'
op|'+'
nl|'\n'
name|'self'
op|'.'
name|'_get_hmacs'
op|'('
name|'env'
op|','
name|'temp_url_expires'
op|','
name|'keys'
op|','
nl|'\n'
name|'request_method'
op|'='
string|"'GET'"
op|')'
op|'+'
nl|'\n'
name|'self'
op|'.'
name|'_get_hmacs'
op|'('
name|'env'
op|','
name|'temp_url_expires'
op|','
name|'keys'
op|','
nl|'\n'
name|'request_method'
op|'='
string|"'PUT'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'hmac_vals'
op|'='
name|'self'
op|'.'
name|'_get_hmacs'
op|'('
name|'env'
op|','
name|'temp_url_expires'
op|','
name|'keys'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'temp_url_sig'
name|'not'
name|'in'
name|'hmac_vals'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'_invalid'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'_clean_incoming_headers'
op|'('
name|'env'
op|')'
newline|'\n'
name|'env'
op|'['
string|"'swift.authorize'"
op|']'
op|'='
name|'lambda'
name|'req'
op|':'
name|'None'
newline|'\n'
name|'env'
op|'['
string|"'swift.authorize_override'"
op|']'
op|'='
name|'True'
newline|'\n'
name|'env'
op|'['
string|"'REMOTE_USER'"
op|']'
op|'='
string|"'.wsgi.tempurl'"
newline|'\n'
name|'qs'
op|'='
op|'{'
string|"'temp_url_sig'"
op|':'
name|'temp_url_sig'
op|','
nl|'\n'
string|"'temp_url_expires'"
op|':'
name|'temp_url_expires'
op|'}'
newline|'\n'
name|'if'
name|'filename'
op|':'
newline|'\n'
indent|'            '
name|'qs'
op|'['
string|"'filename'"
op|']'
op|'='
name|'filename'
newline|'\n'
dedent|''
name|'env'
op|'['
string|"'QUERY_STRING'"
op|']'
op|'='
name|'urlencode'
op|'('
name|'qs'
op|')'
newline|'\n'
nl|'\n'
DECL|function|_start_response
name|'def'
name|'_start_response'
op|'('
name|'status'
op|','
name|'headers'
op|','
name|'exc_info'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'headers'
op|'='
name|'self'
op|'.'
name|'_clean_outgoing_headers'
op|'('
name|'headers'
op|')'
newline|'\n'
name|'if'
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
op|'=='
string|"'GET'"
name|'and'
name|'status'
op|'['
number|'0'
op|']'
op|'=='
string|"'2'"
op|':'
newline|'\n'
comment|'# figure out the right value for content-disposition'
nl|'\n'
comment|'# 1) use the value from the query string'
nl|'\n'
comment|'# 2) use the value from the object metadata'
nl|'\n'
comment|'# 3) use the object name (default)'
nl|'\n'
indent|'                '
name|'out_headers'
op|'='
op|'['
op|']'
newline|'\n'
name|'existing_disposition'
op|'='
name|'None'
newline|'\n'
name|'for'
name|'h'
op|','
name|'v'
name|'in'
name|'headers'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'h'
op|'.'
name|'lower'
op|'('
op|')'
op|'!='
string|"'content-disposition'"
op|':'
newline|'\n'
indent|'                        '
name|'out_headers'
op|'.'
name|'append'
op|'('
op|'('
name|'h'
op|','
name|'v'
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                        '
name|'existing_disposition'
op|'='
name|'v'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'inline_disposition'
op|':'
newline|'\n'
indent|'                    '
name|'disposition_value'
op|'='
string|"'inline'"
newline|'\n'
dedent|''
name|'elif'
name|'filename'
op|':'
newline|'\n'
indent|'                    '
name|'disposition_value'
op|'='
string|'\'attachment; filename="%s"\''
op|'%'
op|'('
nl|'\n'
name|'filename'
op|'.'
name|'replace'
op|'('
string|'\'"\''
op|','
string|'\'\\\\"\''
op|')'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'existing_disposition'
op|':'
newline|'\n'
indent|'                    '
name|'disposition_value'
op|'='
name|'existing_disposition'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'name'
op|'='
name|'basename'
op|'('
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|'.'
name|'rstrip'
op|'('
string|"'/'"
op|')'
op|')'
newline|'\n'
name|'disposition_value'
op|'='
string|'\'attachment; filename="%s"\''
op|'%'
op|'('
nl|'\n'
name|'name'
op|'.'
name|'replace'
op|'('
string|'\'"\''
op|','
string|'\'\\\\"\''
op|')'
op|')'
newline|'\n'
dedent|''
name|'out_headers'
op|'.'
name|'append'
op|'('
op|'('
string|"'Content-Disposition'"
op|','
name|'disposition_value'
op|')'
op|')'
newline|'\n'
name|'headers'
op|'='
name|'out_headers'
newline|'\n'
dedent|''
name|'return'
name|'start_response'
op|'('
name|'status'
op|','
name|'headers'
op|','
name|'exc_info'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'_start_response'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_get_account
dedent|''
name|'def'
name|'_get_account'
op|'('
name|'self'
op|','
name|'env'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Returns just the account for the request, if it\'s an object\n        request and one of the configured methods; otherwise, None is\n        returned.\n\n        :param env: The WSGI environment for the request.\n        :returns: Account str or None.\n        """'
newline|'\n'
name|'if'
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
name|'in'
name|'self'
op|'.'
name|'methods'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'ver'
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
number|'4'
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
indent|'                '
name|'return'
name|'None'
newline|'\n'
dedent|''
name|'if'
name|'ver'
op|'=='
string|"'v1'"
name|'and'
name|'obj'
op|'.'
name|'strip'
op|'('
string|"'/'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'acc'
newline|'\n'
nl|'\n'
DECL|member|_get_temp_url_info
dedent|''
dedent|''
dedent|''
name|'def'
name|'_get_temp_url_info'
op|'('
name|'self'
op|','
name|'env'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Returns the provided temporary URL parameters (sig, expires),\n        if given and syntactically valid. Either sig or expires could\n        be None if not provided. If provided, expires is also\n        converted to an int if possible or 0 if not, and checked for\n        expiration (returns 0 if expired).\n\n        :param env: The WSGI environment for the request.\n        :returns: (sig, expires, filename, inline) as described above.\n        """'
newline|'\n'
name|'temp_url_sig'
op|'='
name|'temp_url_expires'
op|'='
name|'filename'
op|'='
name|'inline'
op|'='
name|'None'
newline|'\n'
name|'qs'
op|'='
name|'parse_qs'
op|'('
name|'env'
op|'.'
name|'get'
op|'('
string|"'QUERY_STRING'"
op|','
string|"''"
op|')'
op|','
name|'keep_blank_values'
op|'='
name|'True'
op|')'
newline|'\n'
name|'if'
string|"'temp_url_sig'"
name|'in'
name|'qs'
op|':'
newline|'\n'
indent|'            '
name|'temp_url_sig'
op|'='
name|'qs'
op|'['
string|"'temp_url_sig'"
op|']'
op|'['
number|'0'
op|']'
newline|'\n'
dedent|''
name|'if'
string|"'temp_url_expires'"
name|'in'
name|'qs'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'temp_url_expires'
op|'='
name|'int'
op|'('
name|'qs'
op|'['
string|"'temp_url_expires'"
op|']'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'                '
name|'temp_url_expires'
op|'='
number|'0'
newline|'\n'
dedent|''
name|'if'
name|'temp_url_expires'
op|'<'
name|'time'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'temp_url_expires'
op|'='
number|'0'
newline|'\n'
dedent|''
dedent|''
name|'if'
string|"'filename'"
name|'in'
name|'qs'
op|':'
newline|'\n'
indent|'            '
name|'filename'
op|'='
name|'qs'
op|'['
string|"'filename'"
op|']'
op|'['
number|'0'
op|']'
newline|'\n'
dedent|''
name|'if'
string|"'inline'"
name|'in'
name|'qs'
op|':'
newline|'\n'
indent|'            '
name|'inline'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'return'
name|'temp_url_sig'
op|','
name|'temp_url_expires'
op|','
name|'filename'
op|','
name|'inline'
newline|'\n'
nl|'\n'
DECL|member|_get_keys
dedent|''
name|'def'
name|'_get_keys'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'account'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Returns the X-Account-Meta-Temp-URL-Key[-2] header values for the\n        account, or an empty list if none is set.\n\n        Returns 0, 1, or 2 elements depending on how many keys are set\n        in the account\'s metadata.\n\n        :param env: The WSGI environment for the request.\n        :param account: Account str.\n        :returns: [X-Account-Meta-Temp-URL-Key str value if set,\n                   X-Account-Meta-Temp-URL-Key-2 str value if set]\n        """'
newline|'\n'
name|'account_info'
op|'='
name|'get_account_info'
op|'('
name|'env'
op|','
name|'self'
op|'.'
name|'app'
op|','
name|'swift_source'
op|'='
string|"'TU'"
op|')'
newline|'\n'
name|'return'
name|'get_tempurl_keys_from_metadata'
op|'('
name|'account_info'
op|'['
string|"'meta'"
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_get_hmacs
dedent|''
name|'def'
name|'_get_hmacs'
op|'('
name|'self'
op|','
name|'env'
op|','
name|'expires'
op|','
name|'keys'
op|','
name|'request_method'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        :param env: The WSGI environment for the request.\n        :param expires: Unix timestamp as an int for when the URL\n                        expires.\n        :param keys: Key strings, from the X-Account-Meta-Temp-URL-Key[-2] of\n                     the account.\n        :param request_method: Optional override of the request in\n                               the WSGI env. For example, if a HEAD\n                               does not match, you may wish to\n                               override with GET to still allow the\n                               HEAD.\n        """'
newline|'\n'
name|'if'
name|'not'
name|'request_method'
op|':'
newline|'\n'
indent|'            '
name|'request_method'
op|'='
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
newline|'\n'
dedent|''
name|'return'
op|'['
name|'get_hmac'
op|'('
nl|'\n'
name|'request_method'
op|','
name|'env'
op|'['
string|"'PATH_INFO'"
op|']'
op|','
name|'expires'
op|','
name|'key'
op|')'
name|'for'
name|'key'
name|'in'
name|'keys'
op|']'
newline|'\n'
nl|'\n'
DECL|member|_invalid
dedent|''
name|'def'
name|'_invalid'
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
string|'"""\n        Performs the necessary steps to indicate a WSGI 401\n        Unauthorized response to the request.\n\n        :param env: The WSGI environment for the request.\n        :param start_response: The WSGI start_response hook.\n        :returns: 401 response as per WSGI.\n        """'
newline|'\n'
name|'if'
name|'env'
op|'['
string|"'REQUEST_METHOD'"
op|']'
op|'=='
string|"'HEAD'"
op|':'
newline|'\n'
indent|'            '
name|'body'
op|'='
name|'None'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'body'
op|'='
string|"'401 Unauthorized: Temp URL invalid\\n'"
newline|'\n'
dedent|''
name|'return'
name|'HTTPUnauthorized'
op|'('
name|'body'
op|'='
name|'body'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_clean_incoming_headers
dedent|''
name|'def'
name|'_clean_incoming_headers'
op|'('
name|'self'
op|','
name|'env'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Removes any headers from the WSGI environment as per the\n        middleware configuration for incoming requests.\n\n        :param env: The WSGI environment for the request.\n        """'
newline|'\n'
name|'for'
name|'h'
name|'in'
name|'env'
op|'.'
name|'keys'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'remove'
op|'='
name|'h'
name|'in'
name|'self'
op|'.'
name|'incoming_remove_headers'
newline|'\n'
name|'if'
name|'not'
name|'remove'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'p'
name|'in'
name|'self'
op|'.'
name|'incoming_remove_headers_startswith'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'h'
op|'.'
name|'startswith'
op|'('
name|'p'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'remove'
op|'='
name|'True'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'if'
name|'remove'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'h'
name|'in'
name|'self'
op|'.'
name|'incoming_allow_headers'
op|':'
newline|'\n'
indent|'                    '
name|'remove'
op|'='
name|'False'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'remove'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'p'
name|'in'
name|'self'
op|'.'
name|'incoming_allow_headers_startswith'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'h'
op|'.'
name|'startswith'
op|'('
name|'p'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'remove'
op|'='
name|'False'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'if'
name|'remove'
op|':'
newline|'\n'
indent|'                '
name|'del'
name|'env'
op|'['
name|'h'
op|']'
newline|'\n'
nl|'\n'
DECL|member|_clean_outgoing_headers
dedent|''
dedent|''
dedent|''
name|'def'
name|'_clean_outgoing_headers'
op|'('
name|'self'
op|','
name|'headers'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Removes any headers as per the middleware configuration for\n        outgoing responses.\n\n        :param headers: A WSGI start_response style list of headers,\n                        [(\'header1\', \'value), (\'header2\', \'value),\n                         ...]\n        :returns: The same headers list, but with some headers\n                  removed as per the middlware configuration for\n                  outgoing responses.\n        """'
newline|'\n'
name|'headers'
op|'='
name|'HeaderKeyDict'
op|'('
name|'headers'
op|')'
newline|'\n'
name|'for'
name|'h'
name|'in'
name|'headers'
op|'.'
name|'keys'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'remove'
op|'='
name|'h'
name|'in'
name|'self'
op|'.'
name|'outgoing_remove_headers'
newline|'\n'
name|'if'
name|'not'
name|'remove'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'p'
name|'in'
name|'self'
op|'.'
name|'outgoing_remove_headers_startswith'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'h'
op|'.'
name|'startswith'
op|'('
name|'p'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'remove'
op|'='
name|'True'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'if'
name|'remove'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'h'
name|'in'
name|'self'
op|'.'
name|'outgoing_allow_headers'
op|':'
newline|'\n'
indent|'                    '
name|'remove'
op|'='
name|'False'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'remove'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'p'
name|'in'
name|'self'
op|'.'
name|'outgoing_allow_headers_startswith'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'h'
op|'.'
name|'startswith'
op|'('
name|'p'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'remove'
op|'='
name|'False'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'if'
name|'remove'
op|':'
newline|'\n'
indent|'                '
name|'del'
name|'headers'
op|'['
name|'h'
op|']'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'headers'
op|'.'
name|'items'
op|'('
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
string|'"""Returns the WSGI filter for use with paste.deploy."""'
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
name|'methods'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'methods'"
op|','
string|"'GET HEAD PUT'"
op|')'
op|'.'
name|'split'
op|'('
op|')'
newline|'\n'
name|'register_swift_info'
op|'('
string|"'tempurl'"
op|','
name|'methods'
op|'='
name|'methods'
op|')'
newline|'\n'
nl|'\n'
name|'return'
name|'lambda'
name|'app'
op|':'
name|'TempURL'
op|'('
name|'app'
op|','
name|'conf'
op|','
name|'methods'
op|'='
name|'methods'
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
