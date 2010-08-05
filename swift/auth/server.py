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
name|'from'
name|'__future__'
name|'import'
name|'with_statement'
newline|'\n'
name|'import'
name|'errno'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'socket'
newline|'\n'
name|'from'
name|'contextlib'
name|'import'
name|'contextmanager'
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'gmtime'
op|','
name|'strftime'
op|','
name|'time'
newline|'\n'
name|'from'
name|'urllib'
name|'import'
name|'unquote'
op|','
name|'quote'
newline|'\n'
name|'from'
name|'uuid'
name|'import'
name|'uuid4'
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
name|'HTTPBadRequest'
op|','
name|'HTTPNoContent'
op|','
name|'HTTPUnauthorized'
op|','
name|'HTTPServiceUnavailable'
op|','
name|'HTTPNotFound'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'bufferedhttp'
name|'import'
name|'http_connect'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'db'
name|'import'
name|'get_db_connection'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'ring'
name|'import'
name|'Ring'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'get_logger'
op|','
name|'normalize_timestamp'
op|','
name|'split_path'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|AuthController
name|'class'
name|'AuthController'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Sample implementation of an authorization server for development work. This\n    server only implements the basic functionality and isn\'t written for high\n    availability or to scale to thousands (or even hundreds) of requests per\n    second. It is mainly for use by developers working on the rest of the\n    system.\n\n    The design of the auth system was restricted by a couple of existing\n    systems.\n\n    This implementation stores an account name, user name, and password (in\n    plain text!) as well as a corresponding Swift cluster url and account hash.\n    One existing auth system used account, user, and password whereas another\n    used just account and an "API key". Here, we support both systems with\n    their various, sometimes colliding headers.\n\n    The most common use case is by the end user:\n\n    * The user makes a ReST call to the auth server requesting a token and url\n      to use to access the Swift cluster.\n    * The auth system validates the user info and returns a token and url for\n      the user to use with the Swift cluster.\n    * The user makes a ReST call to the Swift cluster using the url given with\n      the token as the X-Auth-Token header.\n    * The Swift cluster makes an ReST call to the auth server to validate the\n      token for the given account hash, caching the result for future requests\n      up to the expiration the auth server returns.\n    * The auth server validates the token / account hash given and returns the\n      expiration for the token.\n    * The Swift cluster completes the user\'s request.\n\n    Another use case is creating a new account:\n\n    * The developer makes a ReST call to create a new account.\n    * The auth server makes ReST calls to the Swift cluster\'s account servers\n      to create a new account on its end.\n    * The auth server records the information in its database.\n\n    A last use case is recreating existing accounts; this is really only useful\n    on a development system when the drives are reformatted quite often but\n    the auth server\'s database is retained:\n\n    * A developer makes an ReST call to have the existing accounts recreated.\n    * For each account in its database, the auth server makes ReST calls to\n      the Swift cluster\'s account servers to create a specific account on its\n      end.\n\n    :param conf: The [auth-server] dictionary of the auth server configuration\n                 file\n    :param ring: Overrides loading the account ring from a file; useful for\n                 testing.\n\n    See the etc/auth-server.conf-sample for information on the possible\n    configuration parameters.\n    """'
newline|'\n'
nl|'\n'
DECL|variable|log_name
name|'log_name'
op|'='
string|"'auth'"
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'conf'
op|','
name|'ring'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'conf'
op|','
name|'self'
op|'.'
name|'log_name'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'swift_dir'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'swift_dir'"
op|','
string|"'/etc/swift'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'default_cluster_url'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'default_cluster_url'"
op|','
string|"'http://127.0.0.1:9000/v1'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'token_life'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'token_life'"
op|','
number|'86400'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'log_headers'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'log_headers'"
op|')'
op|'=='
string|"'True'"
newline|'\n'
name|'if'
name|'ring'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'account_ring'
op|'='
name|'ring'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'account_ring'
op|'='
name|'Ring'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'swift_dir'
op|','
string|"'account.ring.gz'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'db_file'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'swift_dir'
op|','
string|"'auth.db'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'conn'
op|'='
name|'get_db_connection'
op|'('
name|'self'
op|'.'
name|'db_file'
op|','
name|'okay_to_create'
op|'='
name|'True'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''CREATE TABLE IF NOT EXISTS account (\n                                account TEXT, url TEXT, cfaccount TEXT,\n                                user TEXT, password TEXT)'''"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''CREATE INDEX IF NOT EXISTS ix_account_account\n                             ON account (account)'''"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''CREATE TABLE IF NOT EXISTS token (\n                                cfaccount TEXT, token TEXT, created FLOAT)'''"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''CREATE INDEX IF NOT EXISTS ix_token_cfaccount\n                             ON token (cfaccount)'''"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''CREATE INDEX IF NOT EXISTS ix_token_created\n                             ON token (created)'''"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'conn'
op|'.'
name|'commit'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|add_storage_account
dedent|''
name|'def'
name|'add_storage_account'
op|'('
name|'self'
op|','
name|'account_name'
op|'='
string|"''"
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Creates an account within the Swift cluster by making a ReST call to\n        each of the responsible account servers.\n\n        :param account_name: The desired name for the account; if omitted a\n                             UUID4 will be used.\n        :returns: False upon failure, otherwise the name of the account\n                  within the Swift cluster.\n        """'
newline|'\n'
name|'begin'
op|'='
name|'time'
op|'('
op|')'
newline|'\n'
name|'orig_account_name'
op|'='
name|'account_name'
newline|'\n'
name|'if'
name|'not'
name|'account_name'
op|':'
newline|'\n'
indent|'            '
name|'account_name'
op|'='
name|'str'
op|'('
name|'uuid4'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
name|'partition'
op|','
name|'nodes'
op|'='
name|'self'
op|'.'
name|'account_ring'
op|'.'
name|'get_nodes'
op|'('
name|'account_name'
op|')'
newline|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Timestamp'"
op|':'
name|'normalize_timestamp'
op|'('
name|'time'
op|'('
op|')'
op|')'
op|','
nl|'\n'
string|"'x-cf-trans-id'"
op|':'
string|"'tx'"
op|'+'
name|'str'
op|'('
name|'uuid4'
op|'('
op|')'
op|')'
op|'}'
newline|'\n'
name|'statuses'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'node'
name|'in'
name|'nodes'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'conn'
op|'='
name|'None'
newline|'\n'
name|'conn'
op|'='
name|'http_connect'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
name|'node'
op|'['
string|"'device'"
op|']'
op|','
nl|'\n'
name|'partition'
op|','
string|"'PUT'"
op|','
string|"'/'"
op|'+'
name|'account_name'
op|','
name|'headers'
op|')'
newline|'\n'
name|'source'
op|'='
name|'conn'
op|'.'
name|'getresponse'
op|'('
op|')'
newline|'\n'
name|'statuses'
op|'.'
name|'append'
op|'('
name|'source'
op|'.'
name|'status'
op|')'
newline|'\n'
name|'if'
name|'source'
op|'.'
name|'status'
op|'>='
number|'500'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
string|"'ERROR With account server %s:%s/%s: '"
nl|'\n'
string|"'Response %s %s: %s'"
op|'%'
nl|'\n'
op|'('
name|'node'
op|'['
string|"'ip'"
op|']'
op|','
name|'node'
op|'['
string|"'port'"
op|']'
op|','
name|'node'
op|'['
string|"'device'"
op|']'
op|','
nl|'\n'
name|'source'
op|'.'
name|'status'
op|','
name|'source'
op|'.'
name|'reason'
op|','
name|'source'
op|'.'
name|'read'
op|'('
number|'1024'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
name|'conn'
op|'='
name|'None'
newline|'\n'
dedent|''
name|'except'
name|'BaseException'
op|','
name|'err'
op|':'
newline|'\n'
indent|'                '
name|'log_call'
op|'='
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
newline|'\n'
name|'msg'
op|'='
string|"'ERROR With account server '"
string|"'%(ip)s:%(port)s/%(device)s (will retry later): '"
op|'%'
name|'node'
newline|'\n'
name|'if'
name|'isinstance'
op|'('
name|'err'
op|','
name|'socket'
op|'.'
name|'error'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'err'
op|'['
number|'0'
op|']'
op|'=='
name|'errno'
op|'.'
name|'ECONNREFUSED'
op|':'
newline|'\n'
indent|'                        '
name|'log_call'
op|'='
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
newline|'\n'
name|'msg'
op|'+='
string|"'Connection refused'"
newline|'\n'
dedent|''
name|'elif'
name|'err'
op|'['
number|'0'
op|']'
op|'=='
name|'errno'
op|'.'
name|'EHOSTUNREACH'
op|':'
newline|'\n'
indent|'                        '
name|'log_call'
op|'='
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
newline|'\n'
name|'msg'
op|'+='
string|"'Host unreachable'"
newline|'\n'
dedent|''
dedent|''
name|'log_call'
op|'('
name|'msg'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'rv'
op|'='
name|'False'
newline|'\n'
name|'if'
name|'len'
op|'('
op|'['
name|'s'
name|'for'
name|'s'
name|'in'
name|'statuses'
name|'if'
op|'('
number|'200'
op|'<='
name|'s'
op|'<'
number|'300'
op|')'
op|']'
op|')'
op|'>'
name|'len'
op|'('
name|'nodes'
op|')'
op|'/'
number|'2'
op|':'
newline|'\n'
indent|'            '
name|'rv'
op|'='
name|'account_name'
newline|'\n'
dedent|''
name|'return'
name|'rv'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'contextmanager'
newline|'\n'
DECL|member|get_conn
name|'def'
name|'get_conn'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Returns a DB API connection instance to the auth server\'s SQLite\n        database. This is a contextmanager call to be use with the \'with\'\n        statement. It takes no parameters.\n        """'
newline|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'conn'
op|':'
newline|'\n'
comment|'# We go ahead and make another db connection even if this is a'
nl|'\n'
comment|'# reentry call; just in case we had an error that caused self.conn'
nl|'\n'
comment|"# to become None. Even if we make an extra conn, we'll only keep"
nl|'\n'
comment|"# one after the 'with' block."
nl|'\n'
indent|'            '
name|'self'
op|'.'
name|'conn'
op|'='
name|'get_db_connection'
op|'('
name|'self'
op|'.'
name|'db_file'
op|')'
newline|'\n'
dedent|''
name|'conn'
op|'='
name|'self'
op|'.'
name|'conn'
newline|'\n'
name|'self'
op|'.'
name|'conn'
op|'='
name|'None'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'yield'
name|'conn'
newline|'\n'
name|'conn'
op|'.'
name|'rollback'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'conn'
op|'='
name|'conn'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'conn'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'conn'
op|'='
name|'get_db_connection'
op|'('
name|'self'
op|'.'
name|'db_file'
op|')'
newline|'\n'
name|'raise'
name|'err'
newline|'\n'
nl|'\n'
DECL|member|purge_old_tokens
dedent|''
dedent|''
name|'def'
name|'purge_old_tokens'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Removes tokens that have expired from the auth server\'s database. This\n        is called by :func:`validate_token` and :func:`GET` to help keep the\n        database clean.\n        """'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'get_conn'
op|'('
op|')'
name|'as'
name|'conn'
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'DELETE FROM token WHERE created < ?'"
op|','
nl|'\n'
op|'('
name|'time'
op|'('
op|')'
op|'-'
name|'self'
op|'.'
name|'token_life'
op|','
op|')'
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'commit'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|validate_token
dedent|''
dedent|''
name|'def'
name|'validate_token'
op|'('
name|'self'
op|','
name|'token'
op|','
name|'account_hash'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Tests if the given token is a valid token\n\n        :param token: The token to validate\n        :param account_hash: The account hash the token is being used with\n        :returns: TTL if valid, False otherwise\n        """'
newline|'\n'
name|'begin'
op|'='
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'purge_old_tokens'
op|'('
op|')'
newline|'\n'
name|'rv'
op|'='
name|'False'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'get_conn'
op|'('
op|')'
name|'as'
name|'conn'
op|':'
newline|'\n'
indent|'            '
name|'row'
op|'='
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n                SELECT created FROM token\n                WHERE cfaccount = ? AND token = ?'''"
op|','
nl|'\n'
op|'('
name|'account_hash'
op|','
name|'token'
op|')'
op|')'
op|'.'
name|'fetchone'
op|'('
op|')'
newline|'\n'
name|'if'
name|'row'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'created'
op|'='
name|'row'
op|'['
number|'0'
op|']'
newline|'\n'
name|'if'
name|'time'
op|'('
op|')'
op|'-'
name|'created'
op|'>='
name|'self'
op|'.'
name|'token_life'
op|':'
newline|'\n'
indent|'                    '
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n                        DELETE FROM token\n                        WHERE cfaccount = ? AND token = ?'''"
op|','
nl|'\n'
op|'('
name|'account_hash'
op|','
name|'token'
op|')'
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'commit'
op|'('
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'rv'
op|'='
name|'self'
op|'.'
name|'token_life'
op|'-'
op|'('
name|'time'
op|'('
op|')'
op|'-'
name|'created'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
string|"'validate_token(%s, %s, _, _) = %s [%.02f]'"
op|'%'
nl|'\n'
op|'('
name|'repr'
op|'('
name|'token'
op|')'
op|','
name|'repr'
op|'('
name|'account_hash'
op|')'
op|','
name|'repr'
op|'('
name|'rv'
op|')'
op|','
nl|'\n'
name|'time'
op|'('
op|')'
op|'-'
name|'begin'
op|')'
op|')'
newline|'\n'
name|'return'
name|'rv'
newline|'\n'
nl|'\n'
DECL|member|create_account
dedent|''
name|'def'
name|'create_account'
op|'('
name|'self'
op|','
name|'new_account'
op|','
name|'new_user'
op|','
name|'new_password'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Handles the create_account call for developers, used to request\n        an account be created both on a Swift cluster and in the auth server\n        database.\n\n        This will make ReST requests to the Swift cluster\'s account servers\n        to have an account created on its side. The resulting account hash\n        along with the URL to use to access the account, the account name, the\n        user name, and the password is recorded in the auth server\'s database.\n        The url is constructed now and stored separately to support changing\n        the configuration file\'s default_cluster_url for directing new accounts\n        to a different Swift cluster while still supporting old accounts going\n        to the Swift clusters they were created on.\n\n        :param new_account: The name for the new account\n        :param new_user: The name for the new user\n        :param new_password: The password for the new account\n\n        :returns: False if the create fails, storage url if successful\n        """'
newline|'\n'
name|'begin'
op|'='
name|'time'
op|'('
op|')'
newline|'\n'
name|'if'
name|'not'
name|'all'
op|'('
op|'('
name|'new_account'
op|','
name|'new_user'
op|','
name|'new_password'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'False'
newline|'\n'
dedent|''
name|'account_hash'
op|'='
name|'self'
op|'.'
name|'add_storage_account'
op|'('
op|')'
newline|'\n'
name|'if'
name|'not'
name|'account_hash'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
nl|'\n'
string|"'FAILED create_account(%s, %s, _,) [%.02f]'"
op|'%'
nl|'\n'
op|'('
name|'repr'
op|'('
name|'new_account'
op|')'
op|','
name|'repr'
op|'('
name|'new_user'
op|')'
op|','
name|'time'
op|'('
op|')'
op|'-'
name|'begin'
op|')'
op|')'
newline|'\n'
name|'return'
name|'False'
newline|'\n'
dedent|''
name|'url'
op|'='
name|'self'
op|'.'
name|'default_cluster_url'
op|'.'
name|'rstrip'
op|'('
string|"'/'"
op|')'
op|'+'
string|"'/'"
op|'+'
name|'account_hash'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'get_conn'
op|'('
op|')'
name|'as'
name|'conn'
op|':'
newline|'\n'
indent|'            '
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''INSERT INTO account\n                (account, url, cfaccount, user, password)\n                VALUES (?, ?, ?, ?, ?)'''"
op|','
nl|'\n'
op|'('
name|'new_account'
op|','
name|'url'
op|','
name|'account_hash'
op|','
name|'new_user'
op|','
name|'new_password'
op|')'
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'commit'
op|'('
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
nl|'\n'
string|"'SUCCESS create_account(%s, %s, _) = %s [%.02f]'"
op|'%'
nl|'\n'
op|'('
name|'repr'
op|'('
name|'new_account'
op|')'
op|','
name|'repr'
op|'('
name|'new_user'
op|')'
op|','
name|'repr'
op|'('
name|'url'
op|')'
op|','
name|'time'
op|'('
op|')'
op|'-'
name|'begin'
op|')'
op|')'
newline|'\n'
name|'return'
name|'url'
newline|'\n'
nl|'\n'
DECL|member|recreate_accounts
dedent|''
name|'def'
name|'recreate_accounts'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Recreates the accounts from the existing auth database in the Swift\n        cluster. This is useful on a development system when the drives are\n        reformatted quite often but the auth server\'s database is retained.\n\n        :returns: A string indicating accounts and failures\n        """'
newline|'\n'
name|'begin'
op|'='
name|'time'
op|'('
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'get_conn'
op|'('
op|')'
name|'as'
name|'conn'
op|':'
newline|'\n'
indent|'            '
name|'account_hashes'
op|'='
op|'['
name|'r'
op|'['
number|'0'
op|']'
name|'for'
name|'r'
name|'in'
nl|'\n'
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'SELECT cfaccount FROM account'"
op|')'
op|'.'
name|'fetchall'
op|'('
op|')'
op|']'
newline|'\n'
dedent|''
name|'failures'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'i'
op|','
name|'account_hash'
name|'in'
name|'enumerate'
op|'('
name|'account_hashes'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'not'
name|'self'
op|'.'
name|'add_storage_account'
op|'('
name|'account_hash'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'failures'
op|'.'
name|'append'
op|'('
name|'account_hash'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'rv'
op|'='
string|"'%d accounts, failures %s'"
op|'%'
op|'('
name|'len'
op|'('
name|'account_hashes'
op|')'
op|','
name|'repr'
op|'('
name|'failures'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
string|"'recreate_accounts(_, _) = %s [%.02f]'"
op|'%'
nl|'\n'
op|'('
name|'rv'
op|','
name|'time'
op|'('
op|')'
op|'-'
name|'begin'
op|')'
op|')'
newline|'\n'
name|'return'
name|'rv'
newline|'\n'
nl|'\n'
DECL|member|handle_token
dedent|''
name|'def'
name|'handle_token'
op|'('
name|'self'
op|','
name|'request'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Hanles ReST request from Swift to validate tokens\n\n        Valid URL paths:\n            * GET /token/<account-hash>/<token>\n\n        If the HTTP equest returns with a 204, then the token is valid,\n        and the TTL of the token will be available in the X-Auth-Ttl header.\n\n        :param request: webob.Request object\n        """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'_'
op|','
name|'account_hash'
op|','
name|'token'
op|'='
name|'split_path'
op|'('
name|'request'
op|'.'
name|'path'
op|','
name|'minsegs'
op|'='
number|'3'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
op|')'
newline|'\n'
dedent|''
name|'ttl'
op|'='
name|'self'
op|'.'
name|'validate_token'
op|'('
name|'token'
op|','
name|'account_hash'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'ttl'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPNotFound'
op|'('
op|')'
newline|'\n'
dedent|''
name|'return'
name|'HTTPNoContent'
op|'('
name|'headers'
op|'='
op|'{'
string|"'x-auth-ttl'"
op|':'
name|'ttl'
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|member|handle_account_create
dedent|''
name|'def'
name|'handle_account_create'
op|'('
name|'self'
op|','
name|'request'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Handles Rest requests from developers to have an account created.\n\n        Valid URL paths:\n            * PUT /account/<account-name>/<user-name> - create the account\n\n        Valid headers:\n            * X-Auth-Key: <password> (Only required when creating an account)\n\n        If the HTTP request returns with a 204, then the account was created,\n        and the storage url will be available in the X-Storage-Url header.\n\n        :param request: webob.Request object\n        """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'_'
op|','
name|'account_name'
op|','
name|'user_name'
op|'='
name|'split_path'
op|'('
name|'request'
op|'.'
name|'path'
op|','
name|'minsegs'
op|'='
number|'3'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
op|')'
newline|'\n'
dedent|''
name|'if'
string|"'X-Auth-Key'"
name|'not'
name|'in'
name|'request'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
string|"'X-Auth-Key is required'"
op|')'
newline|'\n'
dedent|''
name|'password'
op|'='
name|'request'
op|'.'
name|'headers'
op|'['
string|"'x-auth-key'"
op|']'
newline|'\n'
name|'storage_url'
op|'='
name|'self'
op|'.'
name|'create_account'
op|'('
name|'account_name'
op|','
name|'user_name'
op|','
name|'password'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'storage_url'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPServiceUnavailable'
op|'('
op|')'
newline|'\n'
dedent|''
name|'return'
name|'HTTPNoContent'
op|'('
name|'headers'
op|'='
op|'{'
string|"'x-storage-url'"
op|':'
name|'storage_url'
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|member|handle_account_recreate
dedent|''
name|'def'
name|'handle_account_recreate'
op|'('
name|'self'
op|','
name|'request'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Handles ReST requests from developers to have accounts in the Auth\n        system recreated in Swift. I know this is bad ReST style, but this\n        isn\'t production right? :)\n\n        Valid URL paths:\n            * POST /recreate_accounts\n\n        :param request: webob.Request object\n        """'
newline|'\n'
name|'result'
op|'='
name|'self'
op|'.'
name|'recreate_accounts'
op|'('
op|')'
newline|'\n'
name|'return'
name|'Response'
op|'('
name|'result'
op|','
number|'200'
op|','
name|'request'
op|'='
name|'request'
op|')'
newline|'\n'
nl|'\n'
DECL|member|handle_auth
dedent|''
name|'def'
name|'handle_auth'
op|'('
name|'self'
op|','
name|'request'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Handles ReST requests from end users for a Swift cluster url and auth\n        token. This can handle all the various headers and formats that\n        existing auth systems used, so it\'s a bit of a chameleon.\n\n        Valid URL paths:\n            * GET /v1/<account-name>/auth\n            * GET /auth\n            * GET /v1.0\n\n        Valid headers:\n            * X-Auth-User: <account-name>:<user-name>\n            * X-Auth-Key: <password>\n            * X-Storage-User: [<account-name>:]<user-name>\n                    The [<account-name>:] is only optional here if the\n                    /v1/<account-name>/auth path is used.\n            * X-Storage-Pass: <password>\n\n        The (currently) preferred method is to use /v1.0 path and the\n        X-Auth-User and X-Auth-Key headers.\n\n        :param request: A webob.Request instance.\n        """'
newline|'\n'
name|'pathsegs'
op|'='
name|'split_path'
op|'('
name|'request'
op|'.'
name|'path'
op|','
name|'minsegs'
op|'='
number|'1'
op|','
name|'maxsegs'
op|'='
number|'3'
op|','
name|'rest_with_last'
op|'='
name|'True'
op|')'
newline|'\n'
name|'if'
name|'pathsegs'
op|'['
number|'0'
op|']'
op|'=='
string|"'v1'"
name|'and'
name|'pathsegs'
op|'['
number|'2'
op|']'
op|'=='
string|"'auth'"
op|':'
newline|'\n'
indent|'            '
name|'account'
op|'='
name|'pathsegs'
op|'['
number|'1'
op|']'
newline|'\n'
name|'user'
op|'='
name|'request'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-storage-user'"
op|')'
newline|'\n'
name|'if'
name|'not'
name|'user'
op|':'
newline|'\n'
indent|'                '
name|'user'
op|'='
name|'request'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-auth-user'"
op|')'
newline|'\n'
name|'if'
name|'not'
name|'user'
name|'or'
string|"':'"
name|'not'
name|'in'
name|'user'
op|':'
newline|'\n'
indent|'                    '
name|'return'
name|'HTTPUnauthorized'
op|'('
op|')'
newline|'\n'
dedent|''
name|'account2'
op|','
name|'user'
op|'='
name|'user'
op|'.'
name|'split'
op|'('
string|"':'"
op|','
number|'1'
op|')'
newline|'\n'
name|'if'
name|'account'
op|'!='
name|'account2'
op|':'
newline|'\n'
indent|'                    '
name|'return'
name|'HTTPUnauthorized'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
name|'password'
op|'='
name|'request'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-storage-pass'"
op|')'
newline|'\n'
name|'if'
name|'not'
name|'password'
op|':'
newline|'\n'
indent|'                '
name|'password'
op|'='
name|'request'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-auth-key'"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'elif'
name|'pathsegs'
op|'['
number|'0'
op|']'
name|'in'
op|'('
string|"'auth'"
op|','
string|"'v1.0'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'user'
op|'='
name|'request'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-auth-user'"
op|')'
newline|'\n'
name|'if'
name|'not'
name|'user'
op|':'
newline|'\n'
indent|'                '
name|'user'
op|'='
name|'request'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-storage-user'"
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'user'
name|'or'
string|"':'"
name|'not'
name|'in'
name|'user'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'HTTPUnauthorized'
op|'('
op|')'
newline|'\n'
dedent|''
name|'account'
op|','
name|'user'
op|'='
name|'user'
op|'.'
name|'split'
op|'('
string|"':'"
op|','
number|'1'
op|')'
newline|'\n'
name|'password'
op|'='
name|'request'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-auth-key'"
op|')'
newline|'\n'
name|'if'
name|'not'
name|'password'
op|':'
newline|'\n'
indent|'                '
name|'password'
op|'='
name|'request'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-storage-pass'"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPBadRequest'
op|'('
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'all'
op|'('
op|'('
name|'account'
op|','
name|'user'
op|','
name|'password'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'HTTPUnauthorized'
op|'('
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'purge_old_tokens'
op|'('
op|')'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'get_conn'
op|'('
op|')'
name|'as'
name|'conn'
op|':'
newline|'\n'
indent|'            '
name|'row'
op|'='
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n                SELECT cfaccount, url FROM account\n                WHERE account = ? AND user = ? AND password = ?'''"
op|','
nl|'\n'
op|'('
name|'account'
op|','
name|'user'
op|','
name|'password'
op|')'
op|')'
op|'.'
name|'fetchone'
op|'('
op|')'
newline|'\n'
name|'if'
name|'row'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'HTTPUnauthorized'
op|'('
op|')'
newline|'\n'
dedent|''
name|'cfaccount'
op|'='
name|'row'
op|'['
number|'0'
op|']'
newline|'\n'
name|'url'
op|'='
name|'row'
op|'['
number|'1'
op|']'
newline|'\n'
name|'row'
op|'='
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'SELECT token FROM token WHERE cfaccount = ?'"
op|','
nl|'\n'
op|'('
name|'cfaccount'
op|','
op|')'
op|')'
op|'.'
name|'fetchone'
op|'('
op|')'
newline|'\n'
name|'if'
name|'row'
op|':'
newline|'\n'
indent|'                '
name|'token'
op|'='
name|'row'
op|'['
number|'0'
op|']'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'token'
op|'='
string|"'tk'"
op|'+'
name|'str'
op|'('
name|'uuid4'
op|'('
op|')'
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'execute'
op|'('
string|"'''\n                    INSERT INTO token (cfaccount, token, created)\n                    VALUES (?, ?, ?)'''"
op|','
nl|'\n'
op|'('
name|'cfaccount'
op|','
name|'token'
op|','
name|'time'
op|'('
op|')'
op|')'
op|')'
newline|'\n'
name|'conn'
op|'.'
name|'commit'
op|'('
op|')'
newline|'\n'
dedent|''
name|'return'
name|'HTTPNoContent'
op|'('
name|'headers'
op|'='
op|'{'
string|"'x-auth-token'"
op|':'
name|'token'
op|','
nl|'\n'
string|"'x-storage-token'"
op|':'
name|'token'
op|','
nl|'\n'
string|"'x-storage-url'"
op|':'
name|'url'
op|'}'
op|')'
newline|'\n'
nl|'\n'
DECL|member|handleREST
dedent|''
dedent|''
name|'def'
name|'handleREST'
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
string|'"""\n        Handles routing of ReST requests. This handler also logs all requests.\n\n        :param env: WSGI environment\n        :param start_response: WSGI start_response function\n        """'
newline|'\n'
name|'req'
op|'='
name|'Request'
op|'('
name|'env'
op|')'
newline|'\n'
name|'logged_headers'
op|'='
name|'None'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'log_headers'
op|':'
newline|'\n'
indent|'            '
name|'logged_headers'
op|'='
string|"'\\n'"
op|'.'
name|'join'
op|'('
string|"'%s: %s'"
op|'%'
op|'('
name|'k'
op|','
name|'v'
op|')'
nl|'\n'
name|'for'
name|'k'
op|','
name|'v'
name|'in'
name|'req'
op|'.'
name|'headers'
op|'.'
name|'items'
op|'('
op|')'
op|')'
op|'.'
name|'replace'
op|'('
string|'\'"\''
op|','
string|'"#042"'
op|')'
newline|'\n'
dedent|''
name|'start_time'
op|'='
name|'time'
op|'('
op|')'
newline|'\n'
comment|'# Figure out how to handle the request'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'req'
op|'.'
name|'method'
op|'=='
string|"'GET'"
name|'and'
name|'req'
op|'.'
name|'path'
op|'.'
name|'startswith'
op|'('
string|"'/v1'"
op|')'
name|'or'
name|'req'
op|'.'
name|'path'
op|'.'
name|'startswith'
op|'('
string|"'/auth'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'handler'
op|'='
name|'self'
op|'.'
name|'handle_auth'
newline|'\n'
dedent|''
name|'elif'
name|'req'
op|'.'
name|'method'
op|'=='
string|"'GET'"
name|'and'
name|'req'
op|'.'
name|'path'
op|'.'
name|'startswith'
op|'('
string|"'/token/'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'handler'
op|'='
name|'self'
op|'.'
name|'handle_token'
newline|'\n'
dedent|''
name|'elif'
name|'req'
op|'.'
name|'method'
op|'=='
string|"'PUT'"
name|'and'
name|'req'
op|'.'
name|'path'
op|'.'
name|'startswith'
op|'('
string|"'/account/'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'handler'
op|'='
name|'self'
op|'.'
name|'handle_account_create'
newline|'\n'
dedent|''
name|'elif'
name|'req'
op|'.'
name|'method'
op|'=='
string|"'POST'"
name|'and'
name|'req'
op|'.'
name|'path'
op|'=='
string|"'/recreate_accounts'"
op|':'
newline|'\n'
indent|'                '
name|'handler'
op|'='
name|'self'
op|'.'
name|'handle_account_recreate'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'HTTPBadRequest'
op|'('
name|'request'
op|'='
name|'env'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'response'
op|'='
name|'handler'
op|'('
name|'req'
op|')'
newline|'\n'
dedent|''
name|'except'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'exception'
op|'('
string|"'ERROR Unhandled exception in ReST request'"
op|')'
newline|'\n'
name|'return'
name|'HTTPServiceUnavailable'
op|'('
name|'request'
op|'='
name|'req'
op|')'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
name|'trans_time'
op|'='
string|"'%.4f'"
op|'%'
op|'('
name|'time'
op|'('
op|')'
op|'-'
name|'start_time'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'response'
op|'.'
name|'content_length'
name|'and'
name|'response'
op|'.'
name|'app_iter'
name|'and'
name|'hasattr'
op|'('
name|'response'
op|'.'
name|'app_iter'
op|','
string|"'__len__'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'response'
op|'.'
name|'content_length'
op|'='
name|'sum'
op|'('
name|'map'
op|'('
name|'len'
op|','
name|'response'
op|'.'
name|'app_iter'
op|')'
op|')'
newline|'\n'
dedent|''
name|'the_request'
op|'='
string|"'%s %s'"
op|'%'
op|'('
name|'req'
op|'.'
name|'method'
op|','
name|'quote'
op|'('
name|'unquote'
op|'('
name|'req'
op|'.'
name|'path'
op|')'
op|')'
op|')'
newline|'\n'
name|'if'
name|'req'
op|'.'
name|'query_string'
op|':'
newline|'\n'
indent|'            '
name|'the_request'
op|'='
name|'the_request'
op|'+'
string|"'?'"
op|'+'
name|'req'
op|'.'
name|'query_string'
newline|'\n'
dedent|''
name|'the_request'
op|'+='
string|"' '"
op|'+'
name|'req'
op|'.'
name|'environ'
op|'['
string|"'SERVER_PROTOCOL'"
op|']'
newline|'\n'
name|'client'
op|'='
name|'req'
op|'.'
name|'headers'
op|'.'
name|'get'
op|'('
string|"'x-cluster-client-ip'"
op|')'
newline|'\n'
name|'if'
name|'not'
name|'client'
name|'and'
string|"'x-forwarded-for'"
name|'in'
name|'req'
op|'.'
name|'headers'
op|':'
newline|'\n'
indent|'            '
name|'client'
op|'='
name|'req'
op|'.'
name|'headers'
op|'['
string|"'x-forwarded-for'"
op|']'
op|'.'
name|'split'
op|'('
string|"','"
op|')'
op|'['
number|'0'
op|']'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'client'
op|':'
newline|'\n'
indent|'            '
name|'client'
op|'='
name|'req'
op|'.'
name|'remote_addr'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
nl|'\n'
string|'\'%s - - [%s] "%s" %s %s "%s" "%s" - - - - - - - - - "-" "%s" \''
nl|'\n'
string|'\'"%s" %s\''
op|'%'
op|'('
nl|'\n'
name|'client'
op|','
nl|'\n'
name|'strftime'
op|'('
string|"'%d/%b/%Y:%H:%M:%S +0000'"
op|','
name|'gmtime'
op|'('
op|')'
op|')'
op|','
nl|'\n'
name|'the_request'
op|','
nl|'\n'
name|'response'
op|'.'
name|'status_int'
op|','
nl|'\n'
name|'response'
op|'.'
name|'content_length'
name|'or'
string|"'-'"
op|','
nl|'\n'
name|'req'
op|'.'
name|'referer'
name|'or'
string|"'-'"
op|','
nl|'\n'
name|'req'
op|'.'
name|'user_agent'
name|'or'
string|"'-'"
op|','
nl|'\n'
name|'req'
op|'.'
name|'remote_addr'
op|','
nl|'\n'
name|'logged_headers'
name|'or'
string|"'-'"
op|','
nl|'\n'
name|'trans_time'
op|')'
op|')'
newline|'\n'
name|'return'
name|'response'
op|'('
name|'env'
op|','
name|'start_response'
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
string|'""" Used by the eventlet.wsgi.server """'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'handleREST'
op|'('
name|'env'
op|','
name|'start_response'
op|')'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
