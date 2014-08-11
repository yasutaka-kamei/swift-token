begin_unit
comment|'#!/usr/bin/python -u'
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
name|'sys'
newline|'\n'
name|'import'
name|'itertools'
newline|'\n'
name|'import'
name|'uuid'
newline|'\n'
name|'from'
name|'optparse'
name|'import'
name|'OptionParser'
newline|'\n'
name|'from'
name|'urlparse'
name|'import'
name|'urlparse'
newline|'\n'
name|'import'
name|'random'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'manager'
name|'import'
name|'Manager'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'utils'
op|','
name|'ring'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'storage_policy'
name|'import'
name|'POLICIES'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'http'
name|'import'
name|'HTTP_NOT_FOUND'
newline|'\n'
nl|'\n'
name|'from'
name|'swiftclient'
name|'import'
name|'client'
op|','
name|'get_auth'
op|','
name|'ClientException'
newline|'\n'
nl|'\n'
DECL|variable|TIMEOUT
name|'TIMEOUT'
op|'='
number|'60'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|meta_command
name|'def'
name|'meta_command'
op|'('
name|'name'
op|','
name|'bases'
op|','
name|'attrs'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Look for attrs with a truthy attribute __command__ and add them to an\n    attribute __commands__ on the type that maps names to decorated methods.\n    The decorated methods\' doc strings also get mapped in __docs__.\n\n    Also adds a method run(command_name, *args, **kwargs) that will\n    execute the method mapped to the name in __commands__.\n    """'
newline|'\n'
name|'commands'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'docs'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'for'
name|'attr'
op|','
name|'value'
name|'in'
name|'attrs'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'getattr'
op|'('
name|'value'
op|','
string|"'__command__'"
op|','
name|'False'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'commands'
op|'['
name|'attr'
op|']'
op|'='
name|'value'
newline|'\n'
comment|'# methods have always have a __doc__ attribute, sometimes empty'
nl|'\n'
name|'docs'
op|'['
name|'attr'
op|']'
op|'='
op|'('
name|'getattr'
op|'('
name|'value'
op|','
string|"'__doc__'"
op|','
name|'None'
op|')'
name|'or'
nl|'\n'
string|"'perform the %s command'"
op|'%'
name|'attr'
op|')'
op|'.'
name|'strip'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
name|'attrs'
op|'['
string|"'__commands__'"
op|']'
op|'='
name|'commands'
newline|'\n'
name|'attrs'
op|'['
string|"'__docs__'"
op|']'
op|'='
name|'docs'
newline|'\n'
nl|'\n'
DECL|function|run
name|'def'
name|'run'
op|'('
name|'self'
op|','
name|'command'
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
name|'return'
name|'self'
op|'.'
name|'__commands__'
op|'['
name|'command'
op|']'
op|'('
name|'self'
op|','
op|'*'
name|'args'
op|','
op|'**'
name|'kwargs'
op|')'
newline|'\n'
dedent|''
name|'attrs'
op|'.'
name|'setdefault'
op|'('
string|"'run'"
op|','
name|'run'
op|')'
newline|'\n'
name|'return'
name|'type'
op|'('
name|'name'
op|','
name|'bases'
op|','
name|'attrs'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|command
dedent|''
name|'def'
name|'command'
op|'('
name|'f'
op|')'
op|':'
newline|'\n'
indent|'    '
name|'f'
op|'.'
name|'__command__'
op|'='
name|'True'
newline|'\n'
name|'return'
name|'f'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|BrainSplitter
dedent|''
name|'class'
name|'BrainSplitter'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|variable|__metaclass__
indent|'    '
name|'__metaclass__'
op|'='
name|'meta_command'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'url'
op|','
name|'token'
op|','
name|'container_name'
op|'='
string|"'test'"
op|','
name|'object_name'
op|'='
string|"'test'"
op|','
nl|'\n'
name|'server_type'
op|'='
string|"'container'"
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'url'
op|'='
name|'url'
newline|'\n'
name|'self'
op|'.'
name|'token'
op|'='
name|'token'
newline|'\n'
name|'self'
op|'.'
name|'account'
op|'='
name|'utils'
op|'.'
name|'split_path'
op|'('
name|'urlparse'
op|'('
name|'url'
op|')'
op|'.'
name|'path'
op|','
number|'2'
op|','
number|'2'
op|')'
op|'['
number|'1'
op|']'
newline|'\n'
name|'self'
op|'.'
name|'container_name'
op|'='
name|'container_name'
newline|'\n'
name|'self'
op|'.'
name|'object_name'
op|'='
name|'object_name'
newline|'\n'
name|'server_list'
op|'='
op|'['
string|"'%s-server'"
op|'%'
name|'server_type'
op|']'
name|'if'
name|'server_type'
name|'else'
op|'['
string|"'all'"
op|']'
newline|'\n'
name|'self'
op|'.'
name|'servers'
op|'='
name|'Manager'
op|'('
name|'server_list'
op|')'
newline|'\n'
name|'policies'
op|'='
name|'list'
op|'('
name|'POLICIES'
op|')'
newline|'\n'
name|'random'
op|'.'
name|'shuffle'
op|'('
name|'policies'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'policies'
op|'='
name|'itertools'
op|'.'
name|'cycle'
op|'('
name|'policies'
op|')'
newline|'\n'
nl|'\n'
name|'o'
op|'='
name|'object_name'
name|'if'
name|'server_type'
op|'=='
string|"'object'"
name|'else'
name|'None'
newline|'\n'
name|'c'
op|'='
name|'container_name'
name|'if'
name|'server_type'
name|'in'
op|'('
string|"'object'"
op|','
string|"'container'"
op|')'
name|'else'
name|'None'
newline|'\n'
name|'part'
op|','
name|'nodes'
op|'='
name|'ring'
op|'.'
name|'Ring'
op|'('
nl|'\n'
string|"'/etc/swift/%s.ring.gz'"
op|'%'
name|'server_type'
op|')'
op|'.'
name|'get_nodes'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'account'
op|','
name|'c'
op|','
name|'o'
op|')'
newline|'\n'
name|'node_ids'
op|'='
op|'['
name|'n'
op|'['
string|"'id'"
op|']'
name|'for'
name|'n'
name|'in'
name|'nodes'
op|']'
newline|'\n'
name|'if'
name|'all'
op|'('
name|'n_id'
name|'in'
name|'node_ids'
name|'for'
name|'n_id'
name|'in'
op|'('
number|'0'
op|','
number|'1'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'primary_numbers'
op|'='
op|'('
number|'1'
op|','
number|'2'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'handoff_numbers'
op|'='
op|'('
number|'3'
op|','
number|'4'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'primary_numbers'
op|'='
op|'('
number|'3'
op|','
number|'4'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'handoff_numbers'
op|'='
op|'('
number|'1'
op|','
number|'2'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
op|'@'
name|'command'
newline|'\n'
DECL|member|start_primary_half
name|'def'
name|'start_primary_half'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        start servers 1 & 2\n        """'
newline|'\n'
name|'tuple'
op|'('
name|'self'
op|'.'
name|'servers'
op|'.'
name|'start'
op|'('
name|'number'
op|'='
name|'n'
op|')'
name|'for'
name|'n'
name|'in'
name|'self'
op|'.'
name|'primary_numbers'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'command'
newline|'\n'
DECL|member|stop_primary_half
name|'def'
name|'stop_primary_half'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        stop servers 1 & 2\n        """'
newline|'\n'
name|'tuple'
op|'('
name|'self'
op|'.'
name|'servers'
op|'.'
name|'stop'
op|'('
name|'number'
op|'='
name|'n'
op|')'
name|'for'
name|'n'
name|'in'
name|'self'
op|'.'
name|'primary_numbers'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'command'
newline|'\n'
DECL|member|start_handoff_half
name|'def'
name|'start_handoff_half'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        start servers 3 & 4\n        """'
newline|'\n'
name|'tuple'
op|'('
name|'self'
op|'.'
name|'servers'
op|'.'
name|'start'
op|'('
name|'number'
op|'='
name|'n'
op|')'
name|'for'
name|'n'
name|'in'
name|'self'
op|'.'
name|'handoff_numbers'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'command'
newline|'\n'
DECL|member|stop_handoff_half
name|'def'
name|'stop_handoff_half'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        stop servers 3 & 4\n        """'
newline|'\n'
name|'tuple'
op|'('
name|'self'
op|'.'
name|'servers'
op|'.'
name|'stop'
op|'('
name|'number'
op|'='
name|'n'
op|')'
name|'for'
name|'n'
name|'in'
name|'self'
op|'.'
name|'handoff_numbers'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'command'
newline|'\n'
DECL|member|put_container
name|'def'
name|'put_container'
op|'('
name|'self'
op|','
name|'policy_index'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        put container with next storage policy\n        """'
newline|'\n'
name|'policy'
op|'='
name|'self'
op|'.'
name|'policies'
op|'.'
name|'next'
op|'('
op|')'
newline|'\n'
name|'if'
name|'policy_index'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'policy'
op|'='
name|'POLICIES'
op|'.'
name|'get_by_index'
op|'('
name|'int'
op|'('
name|'policy_index'
op|')'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'policy'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'ValueError'
op|'('
string|"'Unknown policy with index %s'"
op|'%'
name|'policy'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'headers'
op|'='
op|'{'
string|"'X-Storage-Policy'"
op|':'
name|'policy'
op|'.'
name|'name'
op|'}'
newline|'\n'
name|'client'
op|'.'
name|'put_container'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
name|'self'
op|'.'
name|'container_name'
op|','
nl|'\n'
name|'headers'
op|'='
name|'headers'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'command'
newline|'\n'
DECL|member|delete_container
name|'def'
name|'delete_container'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        delete container\n        """'
newline|'\n'
name|'client'
op|'.'
name|'delete_container'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
name|'self'
op|'.'
name|'container_name'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'command'
newline|'\n'
DECL|member|put_object
name|'def'
name|'put_object'
op|'('
name|'self'
op|','
name|'headers'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        issue put for zero byte test object\n        """'
newline|'\n'
name|'client'
op|'.'
name|'put_object'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
name|'self'
op|'.'
name|'container_name'
op|','
nl|'\n'
name|'self'
op|'.'
name|'object_name'
op|','
name|'headers'
op|'='
name|'headers'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'command'
newline|'\n'
DECL|member|delete_object
name|'def'
name|'delete_object'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        issue delete for test object\n        """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'client'
op|'.'
name|'delete_object'
op|'('
name|'self'
op|'.'
name|'url'
op|','
name|'self'
op|'.'
name|'token'
op|','
name|'self'
op|'.'
name|'container_name'
op|','
nl|'\n'
name|'self'
op|'.'
name|'object_name'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ClientException'
name|'as'
name|'err'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'err'
op|'.'
name|'http_status'
op|'!='
name|'HTTP_NOT_FOUND'
op|':'
newline|'\n'
indent|'                '
name|'raise'
newline|'\n'
nl|'\n'
DECL|variable|parser
dedent|''
dedent|''
dedent|''
dedent|''
name|'parser'
op|'='
name|'OptionParser'
op|'('
string|"'%prog [options] '"
nl|'\n'
string|"'<command>[:<args>[,<args>...]] [<command>...]'"
op|')'
newline|'\n'
name|'parser'
op|'.'
name|'usage'
op|'+='
string|"'\\n\\nCommands:\\n\\t'"
op|'+'
string|"'\\n\\t'"
op|'.'
name|'join'
op|'('
string|'"%s - %s"'
op|'%'
op|'('
name|'name'
op|','
name|'doc'
op|')'
name|'for'
name|'name'
op|','
name|'doc'
name|'in'
nl|'\n'
name|'BrainSplitter'
op|'.'
name|'__docs__'
op|'.'
name|'items'
op|'('
op|')'
op|')'
newline|'\n'
name|'parser'
op|'.'
name|'add_option'
op|'('
string|"'-c'"
op|','
string|"'--container'"
op|','
name|'default'
op|'='
string|"'container-%s'"
op|'%'
name|'uuid'
op|'.'
name|'uuid4'
op|'('
op|')'
op|','
nl|'\n'
name|'help'
op|'='
string|"'set container name'"
op|')'
newline|'\n'
name|'parser'
op|'.'
name|'add_option'
op|'('
string|"'-o'"
op|','
string|"'--object'"
op|','
name|'default'
op|'='
string|"'object-%s'"
op|'%'
name|'uuid'
op|'.'
name|'uuid4'
op|'('
op|')'
op|','
nl|'\n'
name|'help'
op|'='
string|"'set object name'"
op|')'
newline|'\n'
name|'parser'
op|'.'
name|'add_option'
op|'('
string|"'-s'"
op|','
string|"'--server_type'"
op|','
name|'default'
op|'='
string|"'container'"
op|','
nl|'\n'
name|'help'
op|'='
string|"'set server type'"
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|main
name|'def'
name|'main'
op|'('
op|')'
op|':'
newline|'\n'
indent|'    '
name|'options'
op|','
name|'commands'
op|'='
name|'parser'
op|'.'
name|'parse_args'
op|'('
op|')'
newline|'\n'
name|'if'
name|'not'
name|'commands'
op|':'
newline|'\n'
indent|'        '
name|'parser'
op|'.'
name|'print_help'
op|'('
op|')'
newline|'\n'
name|'return'
string|"'ERROR: must specify at least one command'"
newline|'\n'
dedent|''
name|'for'
name|'cmd_args'
name|'in'
name|'commands'
op|':'
newline|'\n'
indent|'        '
name|'cmd'
op|'='
name|'cmd_args'
op|'.'
name|'split'
op|'('
string|"':'"
op|','
number|'1'
op|')'
op|'['
number|'0'
op|']'
newline|'\n'
name|'if'
name|'cmd'
name|'not'
name|'in'
name|'BrainSplitter'
op|'.'
name|'__commands__'
op|':'
newline|'\n'
indent|'            '
name|'parser'
op|'.'
name|'print_help'
op|'('
op|')'
newline|'\n'
name|'return'
string|"'ERROR: unknown command %s'"
op|'%'
name|'cmd'
newline|'\n'
dedent|''
dedent|''
name|'url'
op|','
name|'token'
op|'='
name|'get_auth'
op|'('
string|"'http://127.0.0.1:8080/auth/v1.0'"
op|','
nl|'\n'
string|"'test:tester'"
op|','
string|"'testing'"
op|')'
newline|'\n'
name|'brain'
op|'='
name|'BrainSplitter'
op|'('
name|'url'
op|','
name|'token'
op|','
name|'options'
op|'.'
name|'container'
op|','
name|'options'
op|'.'
name|'object'
op|','
nl|'\n'
name|'options'
op|'.'
name|'server_type'
op|')'
newline|'\n'
name|'for'
name|'cmd_args'
name|'in'
name|'commands'
op|':'
newline|'\n'
indent|'        '
name|'parts'
op|'='
name|'cmd_args'
op|'.'
name|'split'
op|'('
string|"':'"
op|','
number|'1'
op|')'
newline|'\n'
name|'command'
op|'='
name|'parts'
op|'['
number|'0'
op|']'
newline|'\n'
name|'if'
name|'len'
op|'('
name|'parts'
op|')'
op|'>'
number|'1'
op|':'
newline|'\n'
indent|'            '
name|'args'
op|'='
name|'utils'
op|'.'
name|'list_from_csv'
op|'('
name|'parts'
op|'['
number|'1'
op|']'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'args'
op|'='
op|'('
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'brain'
op|'.'
name|'run'
op|'('
name|'command'
op|','
op|'*'
name|'args'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ClientException'
name|'as'
name|'e'
op|':'
newline|'\n'
indent|'            '
name|'print'
string|"'**WARNING**: %s raised %s'"
op|'%'
op|'('
name|'command'
op|','
name|'e'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'print'
string|"'STATUS'"
op|'.'
name|'join'
op|'('
op|'['
string|"'*'"
op|'*'
number|'25'
op|']'
op|'*'
number|'2'
op|')'
newline|'\n'
name|'brain'
op|'.'
name|'servers'
op|'.'
name|'status'
op|'('
op|')'
newline|'\n'
name|'sys'
op|'.'
name|'exit'
op|'('
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
name|'if'
name|'__name__'
op|'=='
string|'"__main__"'
op|':'
newline|'\n'
indent|'    '
name|'sys'
op|'.'
name|'exit'
op|'('
name|'main'
op|'('
op|')'
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit