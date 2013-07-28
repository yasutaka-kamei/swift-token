begin_unit
comment|'# Copyright (c) 2010-2013 OpenStack, LLC.'
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
string|'"""General object server functions."""'
newline|'\n'
nl|'\n'
name|'import'
name|'cPickle'
name|'as'
name|'pickle'
newline|'\n'
name|'import'
name|'errno'
newline|'\n'
name|'import'
name|'hashlib'
newline|'\n'
name|'import'
name|'logging'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'uuid'
newline|'\n'
name|'from'
name|'gettext'
name|'import'
name|'gettext'
name|'as'
name|'_'
newline|'\n'
name|'from'
name|'os'
op|'.'
name|'path'
name|'import'
name|'basename'
op|','
name|'dirname'
op|','
name|'join'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'exceptions'
name|'import'
name|'PathNotDir'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'lock_path'
op|','
name|'renamer'
op|','
name|'write_pickle'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|variable|PICKLE_PROTOCOL
name|'PICKLE_PROTOCOL'
op|'='
number|'2'
newline|'\n'
DECL|variable|ONE_WEEK
name|'ONE_WEEK'
op|'='
number|'604800'
newline|'\n'
DECL|variable|HASH_FILE
name|'HASH_FILE'
op|'='
string|"'hashes.pkl'"
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|quarantine_renamer
name|'def'
name|'quarantine_renamer'
op|'('
name|'device_path'
op|','
name|'corrupted_file_path'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    In the case that a file is corrupted, move it to a quarantined\n    area to allow replication to fix it.\n\n    :params device_path: The path to the device the corrupted file is on.\n    :params corrupted_file_path: The path to the file you want quarantined.\n\n    :returns: path (str) of directory the file was moved to\n    :raises OSError: re-raises non errno.EEXIST / errno.ENOTEMPTY\n                     exceptions from rename\n    """'
newline|'\n'
name|'from_dir'
op|'='
name|'dirname'
op|'('
name|'corrupted_file_path'
op|')'
newline|'\n'
name|'to_dir'
op|'='
name|'join'
op|'('
name|'device_path'
op|','
string|"'quarantined'"
op|','
string|"'objects'"
op|','
name|'basename'
op|'('
name|'from_dir'
op|')'
op|')'
newline|'\n'
name|'invalidate_hash'
op|'('
name|'dirname'
op|'('
name|'from_dir'
op|')'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'renamer'
op|'('
name|'from_dir'
op|','
name|'to_dir'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'OSError'
op|','
name|'e'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'e'
op|'.'
name|'errno'
name|'not'
name|'in'
op|'('
name|'errno'
op|'.'
name|'EEXIST'
op|','
name|'errno'
op|'.'
name|'ENOTEMPTY'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raise'
newline|'\n'
dedent|''
name|'to_dir'
op|'='
string|'"%s-%s"'
op|'%'
op|'('
name|'to_dir'
op|','
name|'uuid'
op|'.'
name|'uuid4'
op|'('
op|')'
op|'.'
name|'hex'
op|')'
newline|'\n'
name|'renamer'
op|'('
name|'from_dir'
op|','
name|'to_dir'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'to_dir'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|hash_suffix
dedent|''
name|'def'
name|'hash_suffix'
op|'('
name|'path'
op|','
name|'reclaim_age'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Performs reclamation and returns an md5 of all (remaining) files.\n\n    :param reclaim_age: age in seconds at which to remove tombstones\n    :raises PathNotDir: if given path is not a valid directory\n    :raises OSError: for non-ENOTDIR errors\n    """'
newline|'\n'
name|'md5'
op|'='
name|'hashlib'
op|'.'
name|'md5'
op|'('
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'path_contents'
op|'='
name|'sorted'
op|'('
name|'os'
op|'.'
name|'listdir'
op|'('
name|'path'
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'OSError'
op|','
name|'err'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'err'
op|'.'
name|'errno'
name|'in'
op|'('
name|'errno'
op|'.'
name|'ENOTDIR'
op|','
name|'errno'
op|'.'
name|'ENOENT'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'PathNotDir'
op|'('
op|')'
newline|'\n'
dedent|''
name|'raise'
newline|'\n'
dedent|''
name|'for'
name|'hsh'
name|'in'
name|'path_contents'
op|':'
newline|'\n'
indent|'        '
name|'hsh_path'
op|'='
name|'join'
op|'('
name|'path'
op|','
name|'hsh'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'files'
op|'='
name|'os'
op|'.'
name|'listdir'
op|'('
name|'hsh_path'
op|')'
newline|'\n'
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
op|'=='
name|'errno'
op|'.'
name|'ENOTDIR'
op|':'
newline|'\n'
indent|'                '
name|'partition_path'
op|'='
name|'dirname'
op|'('
name|'path'
op|')'
newline|'\n'
name|'objects_path'
op|'='
name|'dirname'
op|'('
name|'partition_path'
op|')'
newline|'\n'
name|'device_path'
op|'='
name|'dirname'
op|'('
name|'objects_path'
op|')'
newline|'\n'
name|'quar_path'
op|'='
name|'quarantine_renamer'
op|'('
name|'device_path'
op|','
name|'hsh_path'
op|')'
newline|'\n'
name|'logging'
op|'.'
name|'exception'
op|'('
nl|'\n'
name|'_'
op|'('
string|"'Quarantined %s to %s because it is not a directory'"
op|')'
op|'%'
nl|'\n'
op|'('
name|'hsh_path'
op|','
name|'quar_path'
op|')'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'raise'
newline|'\n'
dedent|''
name|'if'
name|'len'
op|'('
name|'files'
op|')'
op|'=='
number|'1'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'files'
op|'['
number|'0'
op|']'
op|'.'
name|'endswith'
op|'('
string|"'.ts'"
op|')'
op|':'
newline|'\n'
comment|'# remove tombstones older than reclaim_age'
nl|'\n'
indent|'                '
name|'ts'
op|'='
name|'files'
op|'['
number|'0'
op|']'
op|'.'
name|'rsplit'
op|'('
string|"'.'"
op|','
number|'1'
op|')'
op|'['
number|'0'
op|']'
newline|'\n'
name|'if'
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'float'
op|'('
name|'ts'
op|')'
op|')'
op|'>'
name|'reclaim_age'
op|':'
newline|'\n'
indent|'                    '
name|'os'
op|'.'
name|'unlink'
op|'('
name|'join'
op|'('
name|'hsh_path'
op|','
name|'files'
op|'['
number|'0'
op|']'
op|')'
op|')'
newline|'\n'
name|'files'
op|'.'
name|'remove'
op|'('
name|'files'
op|'['
number|'0'
op|']'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'elif'
name|'files'
op|':'
newline|'\n'
indent|'            '
name|'files'
op|'.'
name|'sort'
op|'('
name|'reverse'
op|'='
name|'True'
op|')'
newline|'\n'
name|'meta'
op|'='
name|'data'
op|'='
name|'tomb'
op|'='
name|'None'
newline|'\n'
name|'for'
name|'filename'
name|'in'
name|'list'
op|'('
name|'files'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'not'
name|'meta'
name|'and'
name|'filename'
op|'.'
name|'endswith'
op|'('
string|"'.meta'"
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'meta'
op|'='
name|'filename'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'data'
name|'and'
name|'filename'
op|'.'
name|'endswith'
op|'('
string|"'.data'"
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'data'
op|'='
name|'filename'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'tomb'
name|'and'
name|'filename'
op|'.'
name|'endswith'
op|'('
string|"'.ts'"
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'tomb'
op|'='
name|'filename'
newline|'\n'
dedent|''
name|'if'
op|'('
name|'filename'
op|'<'
name|'tomb'
name|'or'
comment|'# any file older than tomb'
nl|'\n'
name|'filename'
op|'<'
name|'data'
name|'or'
comment|'# any file older than data'
nl|'\n'
op|'('
name|'filename'
op|'.'
name|'endswith'
op|'('
string|"'.meta'"
op|')'
name|'and'
nl|'\n'
name|'filename'
op|'<'
name|'meta'
op|')'
op|')'
op|':'
comment|'# old meta'
newline|'\n'
indent|'                    '
name|'os'
op|'.'
name|'unlink'
op|'('
name|'join'
op|'('
name|'hsh_path'
op|','
name|'filename'
op|')'
op|')'
newline|'\n'
name|'files'
op|'.'
name|'remove'
op|'('
name|'filename'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'if'
name|'not'
name|'files'
op|':'
newline|'\n'
indent|'            '
name|'os'
op|'.'
name|'rmdir'
op|'('
name|'hsh_path'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'filename'
name|'in'
name|'files'
op|':'
newline|'\n'
indent|'            '
name|'md5'
op|'.'
name|'update'
op|'('
name|'filename'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'os'
op|'.'
name|'rmdir'
op|'('
name|'path'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'OSError'
op|':'
newline|'\n'
indent|'        '
name|'pass'
newline|'\n'
dedent|''
name|'return'
name|'md5'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|invalidate_hash
dedent|''
name|'def'
name|'invalidate_hash'
op|'('
name|'suffix_dir'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Invalidates the hash for a suffix_dir in the partition\'s hashes file.\n\n    :param suffix_dir: absolute path to suffix dir whose hash needs\n                       invalidating\n    """'
newline|'\n'
nl|'\n'
name|'suffix'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'basename'
op|'('
name|'suffix_dir'
op|')'
newline|'\n'
name|'partition_dir'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'dirname'
op|'('
name|'suffix_dir'
op|')'
newline|'\n'
name|'hashes_file'
op|'='
name|'join'
op|'('
name|'partition_dir'
op|','
name|'HASH_FILE'
op|')'
newline|'\n'
name|'with'
name|'lock_path'
op|'('
name|'partition_dir'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'open'
op|'('
name|'hashes_file'
op|','
string|"'rb'"
op|')'
name|'as'
name|'fp'
op|':'
newline|'\n'
indent|'                '
name|'hashes'
op|'='
name|'pickle'
op|'.'
name|'load'
op|'('
name|'fp'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'suffix'
name|'in'
name|'hashes'
name|'and'
name|'not'
name|'hashes'
op|'['
name|'suffix'
op|']'
op|':'
newline|'\n'
indent|'                '
name|'return'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
dedent|''
name|'hashes'
op|'['
name|'suffix'
op|']'
op|'='
name|'None'
newline|'\n'
name|'write_pickle'
op|'('
name|'hashes'
op|','
name|'hashes_file'
op|','
name|'partition_dir'
op|','
name|'PICKLE_PROTOCOL'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|get_hashes
dedent|''
dedent|''
name|'def'
name|'get_hashes'
op|'('
name|'partition_dir'
op|','
name|'recalculate'
op|'='
name|'None'
op|','
name|'do_listdir'
op|'='
name|'False'
op|','
nl|'\n'
name|'reclaim_age'
op|'='
name|'ONE_WEEK'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Get a list of hashes for the suffix dir.  do_listdir causes it to mistrust\n    the hash cache for suffix existence at the (unexpectedly high) cost of a\n    listdir.  reclaim_age is just passed on to hash_suffix.\n\n    :param partition_dir: absolute path of partition to get hashes for\n    :param recalculate: list of suffixes which should be recalculated when got\n    :param do_listdir: force existence check for all hashes in the partition\n    :param reclaim_age: age at which to remove tombstones\n\n    :returns: tuple of (number of suffix dirs hashed, dictionary of hashes)\n    """'
newline|'\n'
nl|'\n'
name|'hashed'
op|'='
number|'0'
newline|'\n'
name|'hashes_file'
op|'='
name|'join'
op|'('
name|'partition_dir'
op|','
name|'HASH_FILE'
op|')'
newline|'\n'
name|'modified'
op|'='
name|'False'
newline|'\n'
name|'force_rewrite'
op|'='
name|'False'
newline|'\n'
name|'hashes'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'mtime'
op|'='
op|'-'
number|'1'
newline|'\n'
nl|'\n'
name|'if'
name|'recalculate'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'        '
name|'recalculate'
op|'='
op|'['
op|']'
newline|'\n'
nl|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'with'
name|'open'
op|'('
name|'hashes_file'
op|','
string|"'rb'"
op|')'
name|'as'
name|'fp'
op|':'
newline|'\n'
indent|'            '
name|'hashes'
op|'='
name|'pickle'
op|'.'
name|'load'
op|'('
name|'fp'
op|')'
newline|'\n'
dedent|''
name|'mtime'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'getmtime'
op|'('
name|'hashes_file'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'        '
name|'do_listdir'
op|'='
name|'True'
newline|'\n'
name|'force_rewrite'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'if'
name|'do_listdir'
op|':'
newline|'\n'
indent|'        '
name|'for'
name|'suff'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'partition_dir'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'len'
op|'('
name|'suff'
op|')'
op|'=='
number|'3'
op|':'
newline|'\n'
indent|'                '
name|'hashes'
op|'.'
name|'setdefault'
op|'('
name|'suff'
op|','
name|'None'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'modified'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'hashes'
op|'.'
name|'update'
op|'('
op|'('
name|'hash_'
op|','
name|'None'
op|')'
name|'for'
name|'hash_'
name|'in'
name|'recalculate'
op|')'
newline|'\n'
name|'for'
name|'suffix'
op|','
name|'hash_'
name|'in'
name|'hashes'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'not'
name|'hash_'
op|':'
newline|'\n'
indent|'            '
name|'suffix_dir'
op|'='
name|'join'
op|'('
name|'partition_dir'
op|','
name|'suffix'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'hashes'
op|'['
name|'suffix'
op|']'
op|'='
name|'hash_suffix'
op|'('
name|'suffix_dir'
op|','
name|'reclaim_age'
op|')'
newline|'\n'
name|'hashed'
op|'+='
number|'1'
newline|'\n'
dedent|''
name|'except'
name|'PathNotDir'
op|':'
newline|'\n'
indent|'                '
name|'del'
name|'hashes'
op|'['
name|'suffix'
op|']'
newline|'\n'
dedent|''
name|'except'
name|'OSError'
op|':'
newline|'\n'
indent|'                '
name|'logging'
op|'.'
name|'exception'
op|'('
name|'_'
op|'('
string|"'Error hashing suffix'"
op|')'
op|')'
newline|'\n'
dedent|''
name|'modified'
op|'='
name|'True'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'modified'
op|':'
newline|'\n'
indent|'        '
name|'with'
name|'lock_path'
op|'('
name|'partition_dir'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'force_rewrite'
name|'or'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'hashes_file'
op|')'
name|'or'
name|'os'
op|'.'
name|'path'
op|'.'
name|'getmtime'
op|'('
name|'hashes_file'
op|')'
op|'=='
name|'mtime'
op|':'
newline|'\n'
indent|'                '
name|'write_pickle'
op|'('
nl|'\n'
name|'hashes'
op|','
name|'hashes_file'
op|','
name|'partition_dir'
op|','
name|'PICKLE_PROTOCOL'
op|')'
newline|'\n'
name|'return'
name|'hashed'
op|','
name|'hashes'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'get_hashes'
op|'('
name|'partition_dir'
op|','
name|'recalculate'
op|','
name|'do_listdir'
op|','
nl|'\n'
name|'reclaim_age'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'hashed'
op|','
name|'hashes'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
