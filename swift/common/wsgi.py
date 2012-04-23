begin_unit
comment|'# Copyright (c) 2010-2012 OpenStack, LLC.'
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
string|'"""WSGI tools for use with swift."""'
newline|'\n'
nl|'\n'
name|'import'
name|'errno'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'signal'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'mimetools'
newline|'\n'
name|'from'
name|'itertools'
name|'import'
name|'chain'
newline|'\n'
nl|'\n'
name|'import'
name|'eventlet'
newline|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'greenio'
op|','
name|'GreenPool'
op|','
name|'sleep'
op|','
name|'wsgi'
op|','
name|'listen'
newline|'\n'
name|'from'
name|'paste'
op|'.'
name|'deploy'
name|'import'
name|'loadapp'
op|','
name|'appconfig'
newline|'\n'
name|'from'
name|'eventlet'
op|'.'
name|'green'
name|'import'
name|'socket'
op|','
name|'ssl'
newline|'\n'
name|'from'
name|'webob'
name|'import'
name|'Request'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'get_logger'
op|','
name|'drop_privileges'
op|','
name|'validate_configuration'
op|','
name|'capture_stdio'
op|','
name|'NullLogger'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|monkey_patch_mimetools
name|'def'
name|'monkey_patch_mimetools'
op|'('
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    mimetools.Message defaults content-type to "text/plain"\n    This changes it to default to None, so we can detect missing headers.\n    """'
newline|'\n'
nl|'\n'
name|'orig_parsetype'
op|'='
name|'mimetools'
op|'.'
name|'Message'
op|'.'
name|'parsetype'
newline|'\n'
nl|'\n'
DECL|function|parsetype
name|'def'
name|'parsetype'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'not'
name|'self'
op|'.'
name|'typeheader'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'type'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'maintype'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'subtype'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'plisttext'
op|'='
string|"''"
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'orig_parsetype'
op|'('
name|'self'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'mimetools'
op|'.'
name|'Message'
op|'.'
name|'parsetype'
op|'='
name|'parsetype'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_socket
dedent|''
name|'def'
name|'get_socket'
op|'('
name|'conf'
op|','
name|'default_port'
op|'='
number|'8080'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Bind socket to bind ip:port in conf\n\n    :param conf: Configuration dict to read settings from\n    :param default_port: port to use if not specified in conf\n\n    :returns : a socket object as returned from socket.listen or\n               ssl.wrap_socket if conf specifies cert_file\n    """'
newline|'\n'
name|'bind_addr'
op|'='
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'bind_ip'"
op|','
string|"'0.0.0.0'"
op|')'
op|','
nl|'\n'
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'bind_port'"
op|','
name|'default_port'
op|')'
op|')'
op|')'
newline|'\n'
name|'address_family'
op|'='
op|'['
name|'addr'
op|'['
number|'0'
op|']'
name|'for'
name|'addr'
name|'in'
name|'socket'
op|'.'
name|'getaddrinfo'
op|'('
name|'bind_addr'
op|'['
number|'0'
op|']'
op|','
nl|'\n'
name|'bind_addr'
op|'['
number|'1'
op|']'
op|','
name|'socket'
op|'.'
name|'AF_UNSPEC'
op|','
name|'socket'
op|'.'
name|'SOCK_STREAM'
op|')'
nl|'\n'
name|'if'
name|'addr'
op|'['
number|'0'
op|']'
name|'in'
op|'('
name|'socket'
op|'.'
name|'AF_INET'
op|','
name|'socket'
op|'.'
name|'AF_INET6'
op|')'
op|']'
op|'['
number|'0'
op|']'
newline|'\n'
name|'sock'
op|'='
name|'None'
newline|'\n'
name|'retry_until'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'+'
number|'30'
newline|'\n'
name|'warn_ssl'
op|'='
name|'False'
newline|'\n'
name|'while'
name|'not'
name|'sock'
name|'and'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'<'
name|'retry_until'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'sock'
op|'='
name|'listen'
op|'('
name|'bind_addr'
op|','
name|'backlog'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'backlog'"
op|','
number|'4096'
op|')'
op|')'
op|','
nl|'\n'
name|'family'
op|'='
name|'address_family'
op|')'
newline|'\n'
name|'if'
string|"'cert_file'"
name|'in'
name|'conf'
op|':'
newline|'\n'
indent|'                '
name|'warn_ssl'
op|'='
name|'True'
newline|'\n'
name|'sock'
op|'='
name|'ssl'
op|'.'
name|'wrap_socket'
op|'('
name|'sock'
op|','
name|'certfile'
op|'='
name|'conf'
op|'['
string|"'cert_file'"
op|']'
op|','
nl|'\n'
name|'keyfile'
op|'='
name|'conf'
op|'['
string|"'key_file'"
op|']'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'socket'
op|'.'
name|'error'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'err'
op|'.'
name|'args'
op|'['
number|'0'
op|']'
op|'!='
name|'errno'
op|'.'
name|'EADDRINUSE'
op|':'
newline|'\n'
indent|'                '
name|'raise'
newline|'\n'
dedent|''
name|'sleep'
op|'('
number|'0.1'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'not'
name|'sock'
op|':'
newline|'\n'
indent|'        '
name|'raise'
name|'Exception'
op|'('
string|"'Could not bind to %s:%s after trying for 30 seconds'"
op|'%'
nl|'\n'
name|'bind_addr'
op|')'
newline|'\n'
dedent|''
name|'sock'
op|'.'
name|'setsockopt'
op|'('
name|'socket'
op|'.'
name|'SOL_SOCKET'
op|','
name|'socket'
op|'.'
name|'SO_REUSEADDR'
op|','
number|'1'
op|')'
newline|'\n'
comment|'# in my experience, sockets can hang around forever without keepalive'
nl|'\n'
name|'sock'
op|'.'
name|'setsockopt'
op|'('
name|'socket'
op|'.'
name|'SOL_SOCKET'
op|','
name|'socket'
op|'.'
name|'SO_KEEPALIVE'
op|','
number|'1'
op|')'
newline|'\n'
name|'sock'
op|'.'
name|'setsockopt'
op|'('
name|'socket'
op|'.'
name|'IPPROTO_TCP'
op|','
name|'socket'
op|'.'
name|'TCP_KEEPIDLE'
op|','
number|'600'
op|')'
newline|'\n'
name|'if'
name|'warn_ssl'
op|':'
newline|'\n'
indent|'        '
name|'ssl_warning_message'
op|'='
string|"'WARNING: SSL should only be enabled for '"
string|"'testing purposes. Use external SSL '"
string|"'termination for a production deployment.'"
newline|'\n'
name|'get_logger'
op|'('
name|'conf'
op|')'
op|'.'
name|'warning'
op|'('
name|'ssl_warning_message'
op|')'
newline|'\n'
name|'print'
name|'_'
op|'('
name|'ssl_warning_message'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'sock'
newline|'\n'
nl|'\n'
nl|'\n'
comment|'# TODO: pull pieces of this out to test'
nl|'\n'
DECL|function|run_wsgi
dedent|''
name|'def'
name|'run_wsgi'
op|'('
name|'conf_file'
op|','
name|'app_section'
op|','
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Loads common settings from conf, then instantiates app and runs\n    the server using the specified number of workers.\n\n    :param conf_file: Path to paste.deploy style configuration file\n    :param app_section: App name from conf file to load config from\n    """'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'conf'
op|'='
name|'appconfig'
op|'('
string|"'config:%s'"
op|'%'
name|'conf_file'
op|','
name|'name'
op|'='
name|'app_section'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|','
name|'e'
op|':'
newline|'\n'
indent|'        '
name|'print'
string|'"Error trying to load config %s: %s"'
op|'%'
op|'('
name|'conf_file'
op|','
name|'e'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'validate_configuration'
op|'('
op|')'
newline|'\n'
nl|'\n'
comment|'# pre-configure logger'
nl|'\n'
name|'log_name'
op|'='
name|'conf'
op|'.'
name|'get'
op|'('
string|"'log_name'"
op|','
name|'app_section'
op|')'
newline|'\n'
name|'if'
string|"'logger'"
name|'in'
name|'kwargs'
op|':'
newline|'\n'
indent|'        '
name|'logger'
op|'='
name|'kwargs'
op|'.'
name|'pop'
op|'('
string|"'logger'"
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'        '
name|'logger'
op|'='
name|'get_logger'
op|'('
name|'conf'
op|','
name|'log_name'
op|','
nl|'\n'
name|'log_to_console'
op|'='
name|'kwargs'
op|'.'
name|'pop'
op|'('
string|"'verbose'"
op|','
name|'False'
op|')'
op|','
name|'log_route'
op|'='
string|"'wsgi'"
op|')'
newline|'\n'
nl|'\n'
comment|'# bind to address and port'
nl|'\n'
dedent|''
name|'sock'
op|'='
name|'get_socket'
op|'('
name|'conf'
op|','
name|'default_port'
op|'='
name|'kwargs'
op|'.'
name|'get'
op|'('
string|"'default_port'"
op|','
number|'8080'
op|')'
op|')'
newline|'\n'
comment|'# remaining tasks should not require elevated privileges'
nl|'\n'
name|'drop_privileges'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'user'"
op|','
string|"'swift'"
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# Ensure the application can be loaded before proceeding.'
nl|'\n'
name|'loadapp'
op|'('
string|"'config:%s'"
op|'%'
name|'conf_file'
op|','
name|'global_conf'
op|'='
op|'{'
string|"'log_name'"
op|':'
name|'log_name'
op|'}'
op|')'
newline|'\n'
nl|'\n'
comment|'# redirect errors to logger and close stdio'
nl|'\n'
name|'capture_stdio'
op|'('
name|'logger'
op|')'
newline|'\n'
nl|'\n'
DECL|function|run_server
name|'def'
name|'run_server'
op|'('
op|')'
op|':'
newline|'\n'
indent|'        '
name|'wsgi'
op|'.'
name|'HttpProtocol'
op|'.'
name|'default_request_version'
op|'='
string|'"HTTP/1.0"'
newline|'\n'
comment|'# Turn off logging requests by the underlying WSGI software.'
nl|'\n'
name|'wsgi'
op|'.'
name|'HttpProtocol'
op|'.'
name|'log_request'
op|'='
name|'lambda'
op|'*'
name|'a'
op|':'
name|'None'
newline|'\n'
comment|'# Redirect logging other messages by the underlying WSGI software.'
nl|'\n'
name|'wsgi'
op|'.'
name|'HttpProtocol'
op|'.'
name|'log_message'
op|'='
name|'lambda'
name|'s'
op|','
name|'f'
op|','
op|'*'
name|'a'
op|':'
name|'logger'
op|'.'
name|'error'
op|'('
string|"'ERROR WSGI: '"
op|'+'
name|'f'
op|'%'
name|'a'
op|')'
newline|'\n'
name|'wsgi'
op|'.'
name|'WRITE_TIMEOUT'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'client_timeout'"
op|')'
name|'or'
number|'60'
op|')'
newline|'\n'
name|'eventlet'
op|'.'
name|'hubs'
op|'.'
name|'use_hub'
op|'('
string|"'poll'"
op|')'
newline|'\n'
name|'eventlet'
op|'.'
name|'patcher'
op|'.'
name|'monkey_patch'
op|'('
name|'all'
op|'='
name|'False'
op|','
name|'socket'
op|'='
name|'True'
op|')'
newline|'\n'
name|'monkey_patch_mimetools'
op|'('
op|')'
newline|'\n'
name|'app'
op|'='
name|'loadapp'
op|'('
string|"'config:%s'"
op|'%'
name|'conf_file'
op|','
nl|'\n'
name|'global_conf'
op|'='
op|'{'
string|"'log_name'"
op|':'
name|'log_name'
op|'}'
op|')'
newline|'\n'
name|'pool'
op|'='
name|'GreenPool'
op|'('
name|'size'
op|'='
number|'1024'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'wsgi'
op|'.'
name|'server'
op|'('
name|'sock'
op|','
name|'app'
op|','
name|'NullLogger'
op|'('
op|')'
op|','
name|'custom_pool'
op|'='
name|'pool'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'socket'
op|'.'
name|'error'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'err'
op|'['
number|'0'
op|']'
op|'!='
name|'errno'
op|'.'
name|'EINVAL'
op|':'
newline|'\n'
indent|'                '
name|'raise'
newline|'\n'
dedent|''
dedent|''
name|'pool'
op|'.'
name|'waitall'
op|'('
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'worker_count'
op|'='
name|'int'
op|'('
name|'conf'
op|'.'
name|'get'
op|'('
string|"'workers'"
op|','
string|"'1'"
op|')'
op|')'
newline|'\n'
comment|'# Useful for profiling [no forks].'
nl|'\n'
name|'if'
name|'worker_count'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'        '
name|'run_server'
op|'('
op|')'
newline|'\n'
name|'return'
newline|'\n'
nl|'\n'
DECL|function|kill_children
dedent|''
name|'def'
name|'kill_children'
op|'('
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Kills the entire process group."""'
newline|'\n'
name|'logger'
op|'.'
name|'error'
op|'('
string|"'SIGTERM received'"
op|')'
newline|'\n'
name|'signal'
op|'.'
name|'signal'
op|'('
name|'signal'
op|'.'
name|'SIGTERM'
op|','
name|'signal'
op|'.'
name|'SIG_IGN'
op|')'
newline|'\n'
name|'running'
op|'['
number|'0'
op|']'
op|'='
name|'False'
newline|'\n'
name|'os'
op|'.'
name|'killpg'
op|'('
number|'0'
op|','
name|'signal'
op|'.'
name|'SIGTERM'
op|')'
newline|'\n'
nl|'\n'
DECL|function|hup
dedent|''
name|'def'
name|'hup'
op|'('
op|'*'
name|'args'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Shuts down the server, but allows running requests to complete"""'
newline|'\n'
name|'logger'
op|'.'
name|'error'
op|'('
string|"'SIGHUP received'"
op|')'
newline|'\n'
name|'signal'
op|'.'
name|'signal'
op|'('
name|'signal'
op|'.'
name|'SIGHUP'
op|','
name|'signal'
op|'.'
name|'SIG_IGN'
op|')'
newline|'\n'
name|'running'
op|'['
number|'0'
op|']'
op|'='
name|'False'
newline|'\n'
nl|'\n'
dedent|''
name|'running'
op|'='
op|'['
name|'True'
op|']'
newline|'\n'
name|'signal'
op|'.'
name|'signal'
op|'('
name|'signal'
op|'.'
name|'SIGTERM'
op|','
name|'kill_children'
op|')'
newline|'\n'
name|'signal'
op|'.'
name|'signal'
op|'('
name|'signal'
op|'.'
name|'SIGHUP'
op|','
name|'hup'
op|')'
newline|'\n'
name|'children'
op|'='
op|'['
op|']'
newline|'\n'
name|'while'
name|'running'
op|'['
number|'0'
op|']'
op|':'
newline|'\n'
indent|'        '
name|'while'
name|'len'
op|'('
name|'children'
op|')'
op|'<'
name|'worker_count'
op|':'
newline|'\n'
indent|'            '
name|'pid'
op|'='
name|'os'
op|'.'
name|'fork'
op|'('
op|')'
newline|'\n'
name|'if'
name|'pid'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'                '
name|'signal'
op|'.'
name|'signal'
op|'('
name|'signal'
op|'.'
name|'SIGHUP'
op|','
name|'signal'
op|'.'
name|'SIG_DFL'
op|')'
newline|'\n'
name|'signal'
op|'.'
name|'signal'
op|'('
name|'signal'
op|'.'
name|'SIGTERM'
op|','
name|'signal'
op|'.'
name|'SIG_DFL'
op|')'
newline|'\n'
name|'run_server'
op|'('
op|')'
newline|'\n'
name|'logger'
op|'.'
name|'notice'
op|'('
string|"'Child %d exiting normally'"
op|'%'
name|'os'
op|'.'
name|'getpid'
op|'('
op|')'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'logger'
op|'.'
name|'notice'
op|'('
string|"'Started child %s'"
op|'%'
name|'pid'
op|')'
newline|'\n'
name|'children'
op|'.'
name|'append'
op|'('
name|'pid'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'pid'
op|','
name|'status'
op|'='
name|'os'
op|'.'
name|'wait'
op|'('
op|')'
newline|'\n'
name|'if'
name|'os'
op|'.'
name|'WIFEXITED'
op|'('
name|'status'
op|')'
name|'or'
name|'os'
op|'.'
name|'WIFSIGNALED'
op|'('
name|'status'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'logger'
op|'.'
name|'error'
op|'('
string|"'Removing dead child %s'"
op|'%'
name|'pid'
op|')'
newline|'\n'
name|'children'
op|'.'
name|'remove'
op|'('
name|'pid'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'OSError'
op|','
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'err'
op|'.'
name|'errno'
name|'not'
name|'in'
op|'('
name|'errno'
op|'.'
name|'EINTR'
op|','
name|'errno'
op|'.'
name|'ECHILD'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'KeyboardInterrupt'
op|':'
newline|'\n'
indent|'            '
name|'logger'
op|'.'
name|'notice'
op|'('
string|"'User quit'"
op|')'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'greenio'
op|'.'
name|'shutdown_safe'
op|'('
name|'sock'
op|')'
newline|'\n'
name|'sock'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
name|'logger'
op|'.'
name|'notice'
op|'('
string|"'Exited'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|WSGIContext
dedent|''
name|'class'
name|'WSGIContext'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    This class provides a means to provide context (scope) for a middleware\n    filter to have access to the wsgi start_response results like the request\n    status and headers.\n    """'
newline|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'wsgi_app'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'app'
op|'='
name|'wsgi_app'
newline|'\n'
comment|'# Results from the last call to self._start_response.'
nl|'\n'
name|'self'
op|'.'
name|'_response_status'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'_response_headers'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'_response_exc_info'
op|'='
name|'None'
newline|'\n'
nl|'\n'
DECL|member|_start_response
dedent|''
name|'def'
name|'_start_response'
op|'('
name|'self'
op|','
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
indent|'        '
string|'"""\n        Saves response info without sending it to the remote client.\n        Uses the same semantics as the usual WSGI start_response.\n        """'
newline|'\n'
name|'self'
op|'.'
name|'_response_status'
op|'='
name|'status'
newline|'\n'
name|'self'
op|'.'
name|'_response_headers'
op|'='
name|'headers'
newline|'\n'
name|'self'
op|'.'
name|'_response_exc_info'
op|'='
name|'exc_info'
newline|'\n'
nl|'\n'
DECL|member|_app_call
dedent|''
name|'def'
name|'_app_call'
op|'('
name|'self'
op|','
name|'env'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Ensures start_response has been called before returning.\n        """'
newline|'\n'
name|'resp'
op|'='
name|'iter'
op|'('
name|'self'
op|'.'
name|'app'
op|'('
name|'env'
op|','
name|'self'
op|'.'
name|'_start_response'
op|')'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'first_chunk'
op|'='
name|'resp'
op|'.'
name|'next'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'StopIteration'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'iter'
op|'('
op|'['
op|']'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
comment|'# We got a first_chunk'
newline|'\n'
indent|'            '
name|'return'
name|'chain'
op|'('
op|'['
name|'first_chunk'
op|']'
op|','
name|'resp'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_get_status_int
dedent|''
dedent|''
name|'def'
name|'_get_status_int'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Returns the HTTP status int from the last called self._start_response\n        result.\n        """'
newline|'\n'
name|'return'
name|'int'
op|'('
name|'self'
op|'.'
name|'_response_status'
op|'.'
name|'split'
op|'('
string|"' '"
op|','
number|'1'
op|')'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_response_header_value
dedent|''
name|'def'
name|'_response_header_value'
op|'('
name|'self'
op|','
name|'key'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"Returns str of value for given header key or None"'
newline|'\n'
name|'for'
name|'h_key'
op|','
name|'val'
name|'in'
name|'self'
op|'.'
name|'_response_headers'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'h_key'
op|'.'
name|'lower'
op|'('
op|')'
op|'=='
name|'key'
op|'.'
name|'lower'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'return'
name|'val'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'None'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|make_pre_authed_request
dedent|''
dedent|''
name|'def'
name|'make_pre_authed_request'
op|'('
name|'env'
op|','
name|'method'
op|'='
name|'None'
op|','
name|'path'
op|'='
name|'None'
op|','
name|'body'
op|'='
name|'None'
op|','
nl|'\n'
name|'headers'
op|'='
name|'None'
op|','
name|'agent'
op|'='
string|"'Swift'"
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Makes a new webob.Request based on the current env but with the\n    parameters specified. Note that this request will be preauthorized.\n\n    :param env: The WSGI environment to base the new request on.\n    :param method: HTTP method of new request; default is from\n                   the original env.\n    :param path: HTTP path of new request; default is from the\n                 original env.\n    :param body: HTTP body of new request; empty by default.\n    :param headers: Extra HTTP headers of new request; None by\n                    default.\n    :param agent: The HTTP user agent to use; default \'Swift\'. You\n                  can put %(orig)s in the agent to have it replaced\n                  with the original env\'s HTTP_USER_AGENT, such as\n                  \'%(orig)s StaticWeb\'. You also set agent to None to\n                  use the original env\'s HTTP_USER_AGENT or \'\' to\n                  have no HTTP_USER_AGENT.\n    :returns: Fresh webob.Request object.\n    """'
newline|'\n'
name|'newenv'
op|'='
name|'make_pre_authed_env'
op|'('
name|'env'
op|','
name|'method'
op|','
name|'path'
op|','
name|'agent'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'headers'
op|':'
newline|'\n'
indent|'        '
name|'headers'
op|'='
op|'{'
op|'}'
newline|'\n'
dedent|''
name|'if'
name|'body'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
op|','
name|'environ'
op|'='
name|'newenv'
op|','
name|'body'
op|'='
name|'body'
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'Request'
op|'.'
name|'blank'
op|'('
name|'path'
op|','
name|'environ'
op|'='
name|'newenv'
op|','
name|'headers'
op|'='
name|'headers'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|make_pre_authed_env
dedent|''
dedent|''
name|'def'
name|'make_pre_authed_env'
op|'('
name|'env'
op|','
name|'method'
op|'='
name|'None'
op|','
name|'path'
op|'='
name|'None'
op|','
name|'agent'
op|'='
string|"'Swift'"
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Returns a new fresh WSGI environment with escalated privileges to\n    do backend checks, listings, etc. that the remote user wouldn\'t\n    be able to accomplish directly.\n\n    :param env: The WSGI environment to base the new environment on.\n    :param method: The new REQUEST_METHOD or None to use the\n                   original.\n    :param path: The new PATH_INFO or None to use the original.\n    :param agent: The HTTP user agent to use; default \'Swift\'. You\n                  can put %(orig)s in the agent to have it replaced\n                  with the original env\'s HTTP_USER_AGENT, such as\n                  \'%(orig)s StaticWeb\'. You also set agent to None to\n                  use the original env\'s HTTP_USER_AGENT or \'\' to\n                  have no HTTP_USER_AGENT.\n    :returns: Fresh WSGI environment.\n    """'
newline|'\n'
name|'newenv'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'name'
name|'in'
op|'('
string|"'eventlet.posthooks'"
op|','
string|"'HTTP_USER_AGENT'"
op|','
nl|'\n'
string|"'PATH_INFO'"
op|','
string|"'QUERY_STRING'"
op|','
string|"'REMOTE_USER'"
op|','
string|"'REQUEST_METHOD'"
op|','
nl|'\n'
string|"'SERVER_NAME'"
op|','
string|"'SERVER_PORT'"
op|','
string|"'SERVER_PROTOCOL'"
op|','
nl|'\n'
string|"'swift.cache'"
op|','
string|"'swift.source'"
op|','
string|"'swift.trans_id'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'name'
name|'in'
name|'env'
op|':'
newline|'\n'
indent|'            '
name|'newenv'
op|'['
name|'name'
op|']'
op|'='
name|'env'
op|'['
name|'name'
op|']'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'method'
op|':'
newline|'\n'
indent|'        '
name|'newenv'
op|'['
string|"'REQUEST_METHOD'"
op|']'
op|'='
name|'method'
newline|'\n'
dedent|''
name|'if'
name|'path'
op|':'
newline|'\n'
indent|'        '
name|'if'
string|"'?'"
name|'in'
name|'path'
op|':'
newline|'\n'
indent|'            '
name|'path'
op|','
name|'query_string'
op|'='
name|'path'
op|'.'
name|'split'
op|'('
string|"'?'"
op|','
number|'1'
op|')'
newline|'\n'
name|'newenv'
op|'['
string|"'QUERY_STRING'"
op|']'
op|'='
name|'query_string'
newline|'\n'
dedent|''
name|'newenv'
op|'['
string|"'PATH_INFO'"
op|']'
op|'='
name|'path'
newline|'\n'
dedent|''
name|'if'
name|'agent'
op|':'
newline|'\n'
indent|'        '
name|'newenv'
op|'['
string|"'HTTP_USER_AGENT'"
op|']'
op|'='
op|'('
nl|'\n'
name|'agent'
op|'%'
op|'{'
string|"'orig'"
op|':'
name|'env'
op|'.'
name|'get'
op|'('
string|"'HTTP_USER_AGENT'"
op|','
string|"''"
op|')'
op|'}'
op|')'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'agent'
op|'=='
string|"''"
name|'and'
string|"'HTTP_USER_AGENT'"
name|'in'
name|'newenv'
op|':'
newline|'\n'
indent|'        '
name|'del'
name|'newenv'
op|'['
string|"'HTTP_USER_AGENT'"
op|']'
newline|'\n'
dedent|''
name|'newenv'
op|'['
string|"'swift.authorize'"
op|']'
op|'='
name|'lambda'
name|'req'
op|':'
name|'None'
newline|'\n'
name|'newenv'
op|'['
string|"'swift.authorize_override'"
op|']'
op|'='
name|'True'
newline|'\n'
name|'newenv'
op|'['
string|"'REMOTE_USER'"
op|']'
op|'='
string|"'.wsgi.pre_authed'"
newline|'\n'
name|'return'
name|'newenv'
newline|'\n'
dedent|''
endmarker|''
end_unit
