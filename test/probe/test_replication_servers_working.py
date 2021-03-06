begin_unit
comment|'#!/usr/bin/python -u'
nl|'\n'
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
name|'from'
name|'unittest'
name|'import'
name|'main'
newline|'\n'
name|'from'
name|'uuid'
name|'import'
name|'uuid4'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'shutil'
newline|'\n'
nl|'\n'
name|'from'
name|'swiftclient'
name|'import'
name|'client'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'obj'
op|'.'
name|'diskfile'
name|'import'
name|'get_data_dir'
newline|'\n'
nl|'\n'
name|'from'
name|'test'
op|'.'
name|'probe'
op|'.'
name|'common'
name|'import'
name|'ReplProbeTest'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'readconf'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|collect_info
name|'def'
name|'collect_info'
op|'('
name|'path_list'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Recursive collect dirs and files in path_list directory.\n\n    :param path_list: start directory for collecting\n    :return files_list, dir_list: tuple of included\n    directories and files\n    """'
newline|'\n'
name|'files_list'
op|'='
op|'['
op|']'
newline|'\n'
name|'dir_list'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'path'
name|'in'
name|'path_list'
op|':'
newline|'\n'
indent|'        '
name|'temp_files_list'
op|'='
op|'['
op|']'
newline|'\n'
name|'temp_dir_list'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'root'
op|','
name|'dirs'
op|','
name|'files'
name|'in'
name|'os'
op|'.'
name|'walk'
op|'('
name|'path'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'temp_files_list'
op|'+='
name|'files'
newline|'\n'
name|'temp_dir_list'
op|'+='
name|'dirs'
newline|'\n'
dedent|''
name|'files_list'
op|'.'
name|'append'
op|'('
name|'temp_files_list'
op|')'
newline|'\n'
name|'dir_list'
op|'.'
name|'append'
op|'('
name|'temp_dir_list'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'files_list'
op|','
name|'dir_list'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|find_max_occupancy_node
dedent|''
name|'def'
name|'find_max_occupancy_node'
op|'('
name|'dir_list'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Find node with maximum occupancy.\n\n    :param list_dir: list of directories for each node.\n    :return number: number node in list_dir\n    """'
newline|'\n'
name|'count'
op|'='
number|'0'
newline|'\n'
name|'number'
op|'='
number|'0'
newline|'\n'
name|'length'
op|'='
number|'0'
newline|'\n'
name|'for'
name|'dirs'
name|'in'
name|'dir_list'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'length'
op|'<'
name|'len'
op|'('
name|'dirs'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'length'
op|'='
name|'len'
op|'('
name|'dirs'
op|')'
newline|'\n'
name|'number'
op|'='
name|'count'
newline|'\n'
dedent|''
name|'count'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'return'
name|'number'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestReplicatorFunctions
dedent|''
name|'class'
name|'TestReplicatorFunctions'
op|'('
name|'ReplProbeTest'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Class for testing replicators and replication servers.\n\n    By default configuration - replication servers not used.\n    For testing separate replication servers servers need to change\n    ring\'s files using set_info command or new ring\'s files with\n    different port values.\n    """'
newline|'\n'
nl|'\n'
DECL|member|test_main
name|'def'
name|'test_main'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
comment|'# Create one account, container and object file.'
nl|'\n'
comment|'# Find node with account, container and object replicas.'
nl|'\n'
comment|'# Delete all directories and files from this node (device).'
nl|'\n'
comment|'# Wait 60 seconds and check replication results.'
nl|'\n'
comment|'# Delete directories and files in objects storage without'
nl|'\n'
comment|'# deleting file "hashes.pkl".'
nl|'\n'
comment|'# Check, that files not replicated.'
nl|'\n'
comment|'# Delete file "hashes.pkl".'
nl|'\n'
comment|'# Check, that all files were replicated.'
nl|'\n'
indent|'        '
name|'path_list'
op|'='
op|'['
op|']'
newline|'\n'
name|'data_dir'
op|'='
name|'get_data_dir'
op|'('
name|'self'
op|'.'
name|'policy'
op|')'
newline|'\n'
comment|'# Figure out where the devices are'
nl|'\n'
name|'for'
name|'node_id'
name|'in'
name|'range'
op|'('
number|'1'
op|','
number|'5'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'conf'
op|'='
name|'readconf'
op|'('
name|'self'
op|'.'
name|'configs'
op|'['
string|"'object-server'"
op|']'
op|'['
name|'node_id'
op|']'
op|')'
newline|'\n'
name|'device_path'
op|'='
name|'conf'
op|'['
string|"'app:object-server'"
op|']'
op|'['
string|"'devices'"
op|']'
newline|'\n'
name|'for'
name|'dev'
name|'in'
name|'self'
op|'.'
name|'object_ring'
op|'.'
name|'devs'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'dev'
op|'['
string|"'port'"
op|']'
op|'=='
name|'int'
op|'('
name|'conf'
op|'['
string|"'app:object-server'"
op|']'
op|'['
string|"'bind_port'"
op|']'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'device'
op|'='
name|'dev'
op|'['
string|"'device'"
op|']'
newline|'\n'
dedent|''
dedent|''
name|'path_list'
op|'.'
name|'append'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'device_path'
op|','
name|'device'
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# Put data to storage nodes'
nl|'\n'
dedent|''
name|'container'
op|'='
string|"'container-%s'"
op|'%'
name|'uuid4'
op|'('
op|')'
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
name|'container'
op|','
nl|'\n'
name|'headers'
op|'='
op|'{'
string|"'X-Storage-Policy'"
op|':'
nl|'\n'
name|'self'
op|'.'
name|'policy'
op|'.'
name|'name'
op|'}'
op|')'
newline|'\n'
nl|'\n'
name|'obj'
op|'='
string|"'object-%s'"
op|'%'
name|'uuid4'
op|'('
op|')'
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
name|'container'
op|','
name|'obj'
op|','
string|"'VERIFY'"
op|')'
newline|'\n'
nl|'\n'
comment|'# Get all data file information'
nl|'\n'
op|'('
name|'files_list'
op|','
name|'dir_list'
op|')'
op|'='
name|'collect_info'
op|'('
name|'path_list'
op|')'
newline|'\n'
name|'num'
op|'='
name|'find_max_occupancy_node'
op|'('
name|'dir_list'
op|')'
newline|'\n'
name|'test_node'
op|'='
name|'path_list'
op|'['
name|'num'
op|']'
newline|'\n'
name|'test_node_files_list'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'files'
name|'in'
name|'files_list'
op|'['
name|'num'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'not'
name|'files'
op|'.'
name|'endswith'
op|'('
string|"'.pending'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'test_node_files_list'
op|'.'
name|'append'
op|'('
name|'files'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'test_node_dir_list'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'d'
name|'in'
name|'dir_list'
op|'['
name|'num'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'not'
name|'d'
op|'.'
name|'startswith'
op|'('
string|"'tmp'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'test_node_dir_list'
op|'.'
name|'append'
op|'('
name|'d'
op|')'
newline|'\n'
comment|'# Run all replicators'
nl|'\n'
dedent|''
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'replicators'
op|'.'
name|'start'
op|'('
op|')'
newline|'\n'
nl|'\n'
comment|'# Delete some files'
nl|'\n'
name|'for'
name|'directory'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'test_node'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'shutil'
op|'.'
name|'rmtree'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'test_node'
op|','
name|'directory'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'os'
op|'.'
name|'listdir'
op|'('
name|'test_node'
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# We will keep trying these tests until they pass for up to 60s'
nl|'\n'
name|'begin'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'                '
op|'('
name|'new_files_list'
op|','
name|'new_dir_list'
op|')'
op|'='
name|'collect_info'
op|'('
op|'['
name|'test_node'
op|']'
op|')'
newline|'\n'
nl|'\n'
name|'try'
op|':'
newline|'\n'
comment|'# Check replicate files and dir'
nl|'\n'
indent|'                    '
name|'for'
name|'files'
name|'in'
name|'test_node_files_list'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'files'
name|'in'
name|'new_files_list'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'for'
name|'dir'
name|'in'
name|'test_node_dir_list'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'dir'
name|'in'
name|'new_dir_list'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
dedent|''
name|'break'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'begin'
op|'>'
number|'60'
op|':'
newline|'\n'
indent|'                        '
name|'raise'
newline|'\n'
dedent|''
name|'time'
op|'.'
name|'sleep'
op|'('
number|'1'
op|')'
newline|'\n'
nl|'\n'
comment|'# Check behavior by deleting hashes.pkl file'
nl|'\n'
dedent|''
dedent|''
name|'for'
name|'directory'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'test_node'
op|','
name|'data_dir'
op|')'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'input_dir'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
nl|'\n'
name|'test_node'
op|','
name|'data_dir'
op|','
name|'directory'
op|')'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'if'
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
nl|'\n'
name|'test_node'
op|','
name|'data_dir'
op|','
name|'directory'
op|','
name|'input_dir'
op|')'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'shutil'
op|'.'
name|'rmtree'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
nl|'\n'
name|'test_node'
op|','
name|'data_dir'
op|','
name|'directory'
op|','
name|'input_dir'
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# We will keep trying these tests until they pass for up to 60s'
nl|'\n'
dedent|''
dedent|''
dedent|''
name|'begin'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'for'
name|'directory'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
nl|'\n'
name|'test_node'
op|','
name|'data_dir'
op|')'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'for'
name|'input_dir'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
nl|'\n'
name|'test_node'
op|','
name|'data_dir'
op|','
name|'directory'
op|')'
op|')'
op|':'
newline|'\n'
indent|'                            '
name|'self'
op|'.'
name|'assertFalse'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'isdir'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'test_node'
op|','
name|'data_dir'
op|','
nl|'\n'
name|'directory'
op|','
string|"'/'"
op|','
name|'input_dir'
op|')'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'break'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'begin'
op|'>'
number|'60'
op|':'
newline|'\n'
indent|'                        '
name|'raise'
newline|'\n'
dedent|''
name|'time'
op|'.'
name|'sleep'
op|'('
number|'1'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'for'
name|'directory'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'test_node'
op|','
name|'data_dir'
op|')'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'os'
op|'.'
name|'remove'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
nl|'\n'
name|'test_node'
op|','
name|'data_dir'
op|','
name|'directory'
op|','
string|"'hashes.pkl'"
op|')'
op|')'
newline|'\n'
nl|'\n'
comment|'# We will keep trying these tests until they pass for up to 60s'
nl|'\n'
dedent|''
name|'begin'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
op|'('
name|'new_files_list'
op|','
name|'new_dir_list'
op|')'
op|'='
name|'collect_info'
op|'('
op|'['
name|'test_node'
op|']'
op|')'
newline|'\n'
nl|'\n'
comment|'# Check replicate files and dirs'
nl|'\n'
name|'for'
name|'files'
name|'in'
name|'test_node_files_list'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'files'
name|'in'
name|'new_files_list'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'for'
name|'directory'
name|'in'
name|'test_node_dir_list'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'assertTrue'
op|'('
name|'directory'
name|'in'
name|'new_dir_list'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
dedent|''
name|'break'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'begin'
op|'>'
number|'60'
op|':'
newline|'\n'
indent|'                        '
name|'raise'
newline|'\n'
dedent|''
name|'time'
op|'.'
name|'sleep'
op|'('
number|'1'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'replicators'
op|'.'
name|'stop'
op|'('
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
dedent|''
dedent|''
dedent|''
name|'if'
name|'__name__'
op|'=='
string|"'__main__'"
op|':'
newline|'\n'
indent|'    '
name|'main'
op|'('
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
