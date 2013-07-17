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
string|'""" Disk File Interface for Swift Object Server"""'
newline|'\n'
nl|'\n'
name|'from'
name|'__future__'
name|'import'
name|'with_statement'
newline|'\n'
name|'import'
name|'cPickle'
name|'as'
name|'pickle'
newline|'\n'
name|'import'
name|'errno'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'traceback'
newline|'\n'
name|'from'
name|'hashlib'
name|'import'
name|'md5'
newline|'\n'
name|'from'
name|'tempfile'
name|'import'
name|'mkstemp'
newline|'\n'
name|'from'
name|'contextlib'
name|'import'
name|'contextmanager'
newline|'\n'
nl|'\n'
name|'from'
name|'xattr'
name|'import'
name|'getxattr'
op|','
name|'setxattr'
newline|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'Timeout'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'mkdirs'
op|','
name|'normalize_timestamp'
op|','
name|'storage_directory'
op|','
name|'hash_path'
op|','
name|'renamer'
op|','
name|'fallocate'
op|','
name|'fsync'
op|','
name|'fdatasync'
op|','
name|'drop_buffer_cache'
op|','
name|'ThreadPool'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'exceptions'
name|'import'
name|'DiskFileError'
op|','
name|'DiskFileNotExist'
op|','
name|'DiskFileCollision'
op|','
name|'DiskFileNoSpace'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'obj'
op|'.'
name|'base'
name|'import'
name|'invalidate_hash'
op|','
name|'quarantine_renamer'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'swob'
name|'import'
name|'multi_range_iterator'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|variable|PICKLE_PROTOCOL
name|'PICKLE_PROTOCOL'
op|'='
number|'2'
newline|'\n'
DECL|variable|METADATA_KEY
name|'METADATA_KEY'
op|'='
string|"'user.swift.metadata'"
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|read_metadata
name|'def'
name|'read_metadata'
op|'('
name|'fd'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Helper function to read the pickled metadata from an object file.\n\n    :param fd: file descriptor to load the metadata from\n\n    :returns: dictionary of metadata\n    """'
newline|'\n'
name|'metadata'
op|'='
string|"''"
newline|'\n'
name|'key'
op|'='
number|'0'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'        '
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'            '
name|'metadata'
op|'+='
name|'getxattr'
op|'('
name|'fd'
op|','
string|"'%s%s'"
op|'%'
op|'('
name|'METADATA_KEY'
op|','
op|'('
name|'key'
name|'or'
string|"''"
op|')'
op|')'
op|')'
newline|'\n'
name|'key'
op|'+='
number|'1'
newline|'\n'
dedent|''
dedent|''
name|'except'
name|'IOError'
op|':'
newline|'\n'
indent|'        '
name|'pass'
newline|'\n'
dedent|''
name|'return'
name|'pickle'
op|'.'
name|'loads'
op|'('
name|'metadata'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|function|write_metadata
dedent|''
name|'def'
name|'write_metadata'
op|'('
name|'fd'
op|','
name|'metadata'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Helper function to write pickled metadata for an object file.\n\n    :param fd: file descriptor to write the metadata\n    :param metadata: metadata to write\n    """'
newline|'\n'
name|'metastr'
op|'='
name|'pickle'
op|'.'
name|'dumps'
op|'('
name|'metadata'
op|','
name|'PICKLE_PROTOCOL'
op|')'
newline|'\n'
name|'key'
op|'='
number|'0'
newline|'\n'
name|'while'
name|'metastr'
op|':'
newline|'\n'
indent|'        '
name|'setxattr'
op|'('
name|'fd'
op|','
string|"'%s%s'"
op|'%'
op|'('
name|'METADATA_KEY'
op|','
name|'key'
name|'or'
string|"''"
op|')'
op|','
name|'metastr'
op|'['
op|':'
number|'254'
op|']'
op|')'
newline|'\n'
name|'metastr'
op|'='
name|'metastr'
op|'['
number|'254'
op|':'
op|']'
newline|'\n'
name|'key'
op|'+='
number|'1'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DiskWriter
dedent|''
dedent|''
name|'class'
name|'DiskWriter'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Encapsulation of the write context for servicing PUT REST API\n    requests. Serves as the context manager object for DiskFile\'s writer()\n    method.\n    """'
newline|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'disk_file'
op|','
name|'fd'
op|','
name|'tmppath'
op|','
name|'threadpool'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'disk_file'
op|'='
name|'disk_file'
newline|'\n'
name|'self'
op|'.'
name|'fd'
op|'='
name|'fd'
newline|'\n'
name|'self'
op|'.'
name|'tmppath'
op|'='
name|'tmppath'
newline|'\n'
name|'self'
op|'.'
name|'upload_size'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'last_sync'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'threadpool'
op|'='
name|'threadpool'
newline|'\n'
nl|'\n'
DECL|member|write
dedent|''
name|'def'
name|'write'
op|'('
name|'self'
op|','
name|'chunk'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Write a chunk of data into the temporary file.\n\n        :param chunk: the chunk of data to write as a string object\n        """'
newline|'\n'
nl|'\n'
DECL|function|_write_entire_chunk
name|'def'
name|'_write_entire_chunk'
op|'('
name|'chunk'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'while'
name|'chunk'
op|':'
newline|'\n'
indent|'                '
name|'written'
op|'='
name|'os'
op|'.'
name|'write'
op|'('
name|'self'
op|'.'
name|'fd'
op|','
name|'chunk'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'upload_size'
op|'+='
name|'written'
newline|'\n'
name|'chunk'
op|'='
name|'chunk'
op|'['
name|'written'
op|':'
op|']'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'threadpool'
op|'.'
name|'run_in_thread'
op|'('
name|'_write_entire_chunk'
op|','
name|'chunk'
op|')'
newline|'\n'
nl|'\n'
comment|'# For large files sync every 512MB (by default) written'
nl|'\n'
name|'diff'
op|'='
name|'self'
op|'.'
name|'upload_size'
op|'-'
name|'self'
op|'.'
name|'last_sync'
newline|'\n'
name|'if'
name|'diff'
op|'>='
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'bytes_per_sync'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'threadpool'
op|'.'
name|'force_run_in_thread'
op|'('
name|'fdatasync'
op|','
name|'self'
op|'.'
name|'fd'
op|')'
newline|'\n'
name|'drop_buffer_cache'
op|'('
name|'self'
op|'.'
name|'fd'
op|','
name|'self'
op|'.'
name|'last_sync'
op|','
name|'diff'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'last_sync'
op|'='
name|'self'
op|'.'
name|'upload_size'
newline|'\n'
nl|'\n'
DECL|member|put
dedent|''
dedent|''
name|'def'
name|'put'
op|'('
name|'self'
op|','
name|'metadata'
op|','
name|'extension'
op|'='
string|"'.data'"
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Finalize writing the file on disk, and renames it from the temp file\n        to the real location.  This should be called after the data has been\n        written to the temp file.\n\n        :param metadata: dictionary of metadata to be written\n        :param extension: extension to be used when making the file\n        """'
newline|'\n'
name|'assert'
name|'self'
op|'.'
name|'tmppath'
name|'is'
name|'not'
name|'None'
newline|'\n'
name|'timestamp'
op|'='
name|'normalize_timestamp'
op|'('
name|'metadata'
op|'['
string|"'X-Timestamp'"
op|']'
op|')'
newline|'\n'
name|'metadata'
op|'['
string|"'name'"
op|']'
op|'='
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'name'
newline|'\n'
nl|'\n'
DECL|function|finalize_put
name|'def'
name|'finalize_put'
op|'('
op|')'
op|':'
newline|'\n'
comment|'# Write the metadata before calling fsync() so that both data and'
nl|'\n'
comment|'# metadata are flushed to disk.'
nl|'\n'
indent|'            '
name|'write_metadata'
op|'('
name|'self'
op|'.'
name|'fd'
op|','
name|'metadata'
op|')'
newline|'\n'
comment|'# We call fsync() before calling drop_cache() to lower the amount'
nl|'\n'
comment|'# of redundant work the drop cache code will perform on the pages'
nl|'\n'
comment|'# (now that after fsync the pages will be all clean).'
nl|'\n'
name|'fsync'
op|'('
name|'self'
op|'.'
name|'fd'
op|')'
newline|'\n'
comment|'# From the Department of the Redundancy Department, make sure'
nl|'\n'
comment|'# we call drop_cache() after fsync() to avoid redundant work'
nl|'\n'
comment|'# (pages all clean).'
nl|'\n'
name|'drop_buffer_cache'
op|'('
name|'self'
op|'.'
name|'fd'
op|','
number|'0'
op|','
name|'self'
op|'.'
name|'upload_size'
op|')'
newline|'\n'
name|'invalidate_hash'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'dirname'
op|'('
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'datadir'
op|')'
op|')'
newline|'\n'
comment|'# After the rename completes, this object will be available for'
nl|'\n'
comment|'# other requests to reference.'
nl|'\n'
name|'renamer'
op|'('
name|'self'
op|'.'
name|'tmppath'
op|','
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'datadir'
op|','
nl|'\n'
name|'timestamp'
op|'+'
name|'extension'
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
name|'self'
op|'.'
name|'threadpool'
op|'.'
name|'force_run_in_thread'
op|'('
name|'finalize_put'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'disk_file'
op|'.'
name|'metadata'
op|'='
name|'metadata'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DiskFile
dedent|''
dedent|''
name|'class'
name|'DiskFile'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    Manage object files on disk.\n\n    :param path: path to devices on the node\n    :param device: device name\n    :param partition: partition on the device the object lives in\n    :param account: account name for the object\n    :param container: container name for the object\n    :param obj: object name for the object\n    :param keep_data_fp: if True, don\'t close the fp, otherwise close it\n    :param disk_chunk_size: size of chunks on file reads\n    :param bytes_per_sync: number of bytes between fdatasync calls\n    :param iter_hook: called when __iter__ returns a chunk\n    :param threadpool: thread pool in which to do blocking operations\n\n    :raises DiskFileCollision: on md5 collision\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'path'
op|','
name|'device'
op|','
name|'partition'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|','
nl|'\n'
name|'logger'
op|','
name|'keep_data_fp'
op|'='
name|'False'
op|','
name|'disk_chunk_size'
op|'='
number|'65536'
op|','
nl|'\n'
name|'bytes_per_sync'
op|'='
op|'('
number|'512'
op|'*'
number|'1024'
op|'*'
number|'1024'
op|')'
op|','
name|'iter_hook'
op|'='
name|'None'
op|','
nl|'\n'
name|'threadpool'
op|'='
name|'None'
op|','
name|'obj_dir'
op|'='
string|"'objects'"
op|','
nl|'\n'
name|'disallowed_metadata_keys'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'disk_chunk_size'
op|'='
name|'disk_chunk_size'
newline|'\n'
name|'self'
op|'.'
name|'bytes_per_sync'
op|'='
name|'bytes_per_sync'
newline|'\n'
name|'self'
op|'.'
name|'iter_hook'
op|'='
name|'iter_hook'
newline|'\n'
name|'self'
op|'.'
name|'name'
op|'='
string|"'/'"
op|'+'
string|"'/'"
op|'.'
name|'join'
op|'('
op|'('
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
op|')'
newline|'\n'
name|'name_hash'
op|'='
name|'hash_path'
op|'('
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'datadir'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
nl|'\n'
name|'path'
op|','
name|'device'
op|','
name|'storage_directory'
op|'('
name|'obj_dir'
op|','
name|'partition'
op|','
name|'name_hash'
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'device_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'path'
op|','
name|'device'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'tmpdir'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'path'
op|','
name|'device'
op|','
string|"'tmp'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'='
name|'logger'
newline|'\n'
name|'self'
op|'.'
name|'disallowed_metadata_keys'
op|'='
name|'disallowed_metadata_keys'
newline|'\n'
name|'self'
op|'.'
name|'metadata'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'self'
op|'.'
name|'meta_file'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'data_file'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'fp'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'iter_etag'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'started_at_0'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'read_to_eof'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'quarantined_dir'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'keep_cache'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'suppress_file_closing'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'threadpool'
op|'='
name|'threadpool'
name|'or'
name|'ThreadPool'
op|'('
name|'nthreads'
op|'='
number|'0'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'self'
op|'.'
name|'datadir'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
dedent|''
name|'files'
op|'='
name|'sorted'
op|'('
name|'os'
op|'.'
name|'listdir'
op|'('
name|'self'
op|'.'
name|'datadir'
op|')'
op|','
name|'reverse'
op|'='
name|'True'
op|')'
newline|'\n'
name|'for'
name|'afile'
name|'in'
name|'files'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'afile'
op|'.'
name|'endswith'
op|'('
string|"'.ts'"
op|')'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'data_file'
op|'='
name|'self'
op|'.'
name|'meta_file'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'metadata'
op|'='
op|'{'
string|"'deleted'"
op|':'
name|'True'
op|'}'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'if'
name|'afile'
op|'.'
name|'endswith'
op|'('
string|"'.meta'"
op|')'
name|'and'
name|'not'
name|'self'
op|'.'
name|'meta_file'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'meta_file'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'datadir'
op|','
name|'afile'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'afile'
op|'.'
name|'endswith'
op|'('
string|"'.data'"
op|')'
name|'and'
name|'not'
name|'self'
op|'.'
name|'data_file'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'data_file'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'datadir'
op|','
name|'afile'
op|')'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'if'
name|'not'
name|'self'
op|'.'
name|'data_file'
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'fp'
op|'='
name|'open'
op|'('
name|'self'
op|'.'
name|'data_file'
op|','
string|"'rb'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'metadata'
op|'='
name|'read_metadata'
op|'('
name|'self'
op|'.'
name|'fp'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'keep_data_fp'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'close'
op|'('
name|'verify_file'
op|'='
name|'False'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'meta_file'
op|':'
newline|'\n'
indent|'            '
name|'with'
name|'open'
op|'('
name|'self'
op|'.'
name|'meta_file'
op|')'
name|'as'
name|'mfp'
op|':'
newline|'\n'
indent|'                '
name|'for'
name|'key'
name|'in'
name|'self'
op|'.'
name|'metadata'
op|'.'
name|'keys'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'key'
op|'.'
name|'lower'
op|'('
op|')'
name|'not'
name|'in'
name|'self'
op|'.'
name|'disallowed_metadata_keys'
op|':'
newline|'\n'
indent|'                        '
name|'del'
name|'self'
op|'.'
name|'metadata'
op|'['
name|'key'
op|']'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'metadata'
op|'.'
name|'update'
op|'('
name|'read_metadata'
op|'('
name|'mfp'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'if'
string|"'name'"
name|'in'
name|'self'
op|'.'
name|'metadata'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'self'
op|'.'
name|'metadata'
op|'['
string|"'name'"
op|']'
op|'!='
name|'self'
op|'.'
name|'name'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
name|'_'
op|'('
string|"'Client path %(client)s does not match '"
nl|'\n'
string|"'path stored in object metadata %(meta)s'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'client'"
op|':'
name|'self'
op|'.'
name|'name'
op|','
nl|'\n'
string|"'meta'"
op|':'
name|'self'
op|'.'
name|'metadata'
op|'['
string|"'name'"
op|']'
op|'}'
op|')'
newline|'\n'
name|'raise'
name|'DiskFileCollision'
op|'('
string|"'Client path does not match path '"
nl|'\n'
string|"'stored in object metadata'"
op|')'
newline|'\n'
nl|'\n'
DECL|member|__iter__
dedent|''
dedent|''
dedent|''
name|'def'
name|'__iter__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Returns an iterator over the data file."""'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'dropped_cache'
op|'='
number|'0'
newline|'\n'
name|'read'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'started_at_0'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'read_to_eof'
op|'='
name|'False'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'fp'
op|'.'
name|'tell'
op|'('
op|')'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'started_at_0'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'iter_etag'
op|'='
name|'md5'
op|'('
op|')'
newline|'\n'
dedent|''
name|'while'
name|'True'
op|':'
newline|'\n'
indent|'                '
name|'chunk'
op|'='
name|'self'
op|'.'
name|'threadpool'
op|'.'
name|'run_in_thread'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'fp'
op|'.'
name|'read'
op|','
name|'self'
op|'.'
name|'disk_chunk_size'
op|')'
newline|'\n'
name|'if'
name|'chunk'
op|':'
newline|'\n'
indent|'                    '
name|'if'
name|'self'
op|'.'
name|'iter_etag'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'iter_etag'
op|'.'
name|'update'
op|'('
name|'chunk'
op|')'
newline|'\n'
dedent|''
name|'read'
op|'+='
name|'len'
op|'('
name|'chunk'
op|')'
newline|'\n'
name|'if'
name|'read'
op|'-'
name|'dropped_cache'
op|'>'
op|'('
number|'1024'
op|'*'
number|'1024'
op|')'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'_drop_cache'
op|'('
name|'self'
op|'.'
name|'fp'
op|'.'
name|'fileno'
op|'('
op|')'
op|','
name|'dropped_cache'
op|','
nl|'\n'
name|'read'
op|'-'
name|'dropped_cache'
op|')'
newline|'\n'
name|'dropped_cache'
op|'='
name|'read'
newline|'\n'
dedent|''
name|'yield'
name|'chunk'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'iter_hook'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'iter_hook'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'read_to_eof'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'_drop_cache'
op|'('
name|'self'
op|'.'
name|'fp'
op|'.'
name|'fileno'
op|'('
op|')'
op|','
name|'dropped_cache'
op|','
nl|'\n'
name|'read'
op|'-'
name|'dropped_cache'
op|')'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'not'
name|'self'
op|'.'
name|'suppress_file_closing'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|app_iter_range
dedent|''
dedent|''
dedent|''
name|'def'
name|'app_iter_range'
op|'('
name|'self'
op|','
name|'start'
op|','
name|'stop'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Returns an iterator over the data file for range (start, stop)"""'
newline|'\n'
name|'if'
name|'start'
name|'or'
name|'start'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'fp'
op|'.'
name|'seek'
op|'('
name|'start'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'stop'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'length'
op|'='
name|'stop'
op|'-'
name|'start'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'length'
op|'='
name|'None'
newline|'\n'
dedent|''
name|'for'
name|'chunk'
name|'in'
name|'self'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'length'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'                '
name|'length'
op|'-='
name|'len'
op|'('
name|'chunk'
op|')'
newline|'\n'
name|'if'
name|'length'
op|'<'
number|'0'
op|':'
newline|'\n'
comment|'# Chop off the extra:'
nl|'\n'
indent|'                    '
name|'yield'
name|'chunk'
op|'['
op|':'
name|'length'
op|']'
newline|'\n'
name|'break'
newline|'\n'
dedent|''
dedent|''
name|'yield'
name|'chunk'
newline|'\n'
nl|'\n'
DECL|member|app_iter_ranges
dedent|''
dedent|''
name|'def'
name|'app_iter_ranges'
op|'('
name|'self'
op|','
name|'ranges'
op|','
name|'content_type'
op|','
name|'boundary'
op|','
name|'size'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Returns an iterator over the data file for a set of ranges"""'
newline|'\n'
name|'if'
name|'not'
name|'ranges'
op|':'
newline|'\n'
indent|'            '
name|'yield'
string|"''"
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'suppress_file_closing'
op|'='
name|'True'
newline|'\n'
name|'for'
name|'chunk'
name|'in'
name|'multi_range_iterator'
op|'('
nl|'\n'
name|'ranges'
op|','
name|'content_type'
op|','
name|'boundary'
op|','
name|'size'
op|','
nl|'\n'
name|'self'
op|'.'
name|'app_iter_range'
op|')'
op|':'
newline|'\n'
indent|'                    '
name|'yield'
name|'chunk'
newline|'\n'
dedent|''
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'suppress_file_closing'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|_handle_close_quarantine
dedent|''
dedent|''
dedent|''
name|'def'
name|'_handle_close_quarantine'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Check if file needs to be quarantined"""'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'get_data_file_size'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'DiskFileError'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'quarantine'
op|'('
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'except'
name|'DiskFileNotExist'
op|':'
newline|'\n'
indent|'            '
name|'return'
newline|'\n'
nl|'\n'
dedent|''
name|'if'
name|'self'
op|'.'
name|'iter_etag'
name|'and'
name|'self'
op|'.'
name|'started_at_0'
name|'and'
name|'self'
op|'.'
name|'read_to_eof'
name|'and'
string|"'ETag'"
name|'in'
name|'self'
op|'.'
name|'metadata'
name|'and'
name|'self'
op|'.'
name|'iter_etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
op|'!='
name|'self'
op|'.'
name|'metadata'
op|'.'
name|'get'
op|'('
string|"'ETag'"
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'quarantine'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|close
dedent|''
dedent|''
name|'def'
name|'close'
op|'('
name|'self'
op|','
name|'verify_file'
op|'='
name|'True'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Close the file. Will handle quarantining file if necessary.\n\n        :param verify_file: Defaults to True. If false, will not check\n                            file to see if it needs quarantining.\n        """'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'fp'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'verify_file'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'_handle_close_quarantine'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
name|'except'
op|'('
name|'Exception'
op|','
name|'Timeout'
op|')'
op|','
name|'e'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
name|'_'
op|'('
nl|'\n'
string|"'ERROR DiskFile %(data_file)s in '"
nl|'\n'
string|"'%(data_dir)s close failure: %(exc)s : %(stack)'"
op|')'
op|','
nl|'\n'
op|'{'
string|"'exc'"
op|':'
name|'e'
op|','
string|"'stack'"
op|':'
string|"''"
op|'.'
name|'join'
op|'('
name|'traceback'
op|'.'
name|'format_stack'
op|'('
op|')'
op|')'
op|','
nl|'\n'
string|"'data_file'"
op|':'
name|'self'
op|'.'
name|'data_file'
op|','
string|"'data_dir'"
op|':'
name|'self'
op|'.'
name|'datadir'
op|'}'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'fp'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'fp'
op|'='
name|'None'
newline|'\n'
nl|'\n'
DECL|member|is_deleted
dedent|''
dedent|''
dedent|''
name|'def'
name|'is_deleted'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Check if the file is deleted.\n\n        :returns: True if the file doesn\'t exist or has been flagged as\n                  deleted.\n        """'
newline|'\n'
name|'return'
name|'not'
name|'self'
op|'.'
name|'data_file'
name|'or'
string|"'deleted'"
name|'in'
name|'self'
op|'.'
name|'metadata'
newline|'\n'
nl|'\n'
DECL|member|is_expired
dedent|''
name|'def'
name|'is_expired'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Check if the file is expired.\n\n        :returns: True if the file has an X-Delete-At in the past\n        """'
newline|'\n'
name|'return'
op|'('
string|"'X-Delete-At'"
name|'in'
name|'self'
op|'.'
name|'metadata'
name|'and'
nl|'\n'
name|'int'
op|'('
name|'self'
op|'.'
name|'metadata'
op|'['
string|"'X-Delete-At'"
op|']'
op|')'
op|'<='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|')'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'contextmanager'
newline|'\n'
DECL|member|writer
name|'def'
name|'writer'
op|'('
name|'self'
op|','
name|'size'
op|'='
name|'None'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Context manager to write a file. We create a temporary file first, and\n        then return a DiskWriter object to encapsulate the state.\n\n        :param size: optional initial size of file to explicitly allocate on\n                     disk\n        :raises DiskFileNoSpace: if a size is specified and allocation fails\n        """'
newline|'\n'
name|'if'
name|'not'
name|'os'
op|'.'
name|'path'
op|'.'
name|'exists'
op|'('
name|'self'
op|'.'
name|'tmpdir'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'mkdirs'
op|'('
name|'self'
op|'.'
name|'tmpdir'
op|')'
newline|'\n'
dedent|''
name|'fd'
op|','
name|'tmppath'
op|'='
name|'mkstemp'
op|'('
name|'dir'
op|'='
name|'self'
op|'.'
name|'tmpdir'
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'size'
name|'is'
name|'not'
name|'None'
name|'and'
name|'size'
op|'>'
number|'0'
op|':'
newline|'\n'
indent|'                '
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'fallocate'
op|'('
name|'fd'
op|','
name|'size'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'OSError'
op|':'
newline|'\n'
indent|'                    '
name|'raise'
name|'DiskFileNoSpace'
op|'('
op|')'
newline|'\n'
dedent|''
dedent|''
name|'yield'
name|'DiskWriter'
op|'('
name|'self'
op|','
name|'fd'
op|','
name|'tmppath'
op|','
name|'self'
op|'.'
name|'threadpool'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'os'
op|'.'
name|'close'
op|'('
name|'fd'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'OSError'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'os'
op|'.'
name|'unlink'
op|'('
name|'tmppath'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'OSError'
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|put_metadata
dedent|''
dedent|''
dedent|''
name|'def'
name|'put_metadata'
op|'('
name|'self'
op|','
name|'metadata'
op|','
name|'tombstone'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Short hand for putting metadata to .meta and .ts files.\n\n        :param metadata: dictionary of metadata to be written\n        :param tombstone: whether or not we are writing a tombstone\n        """'
newline|'\n'
name|'extension'
op|'='
string|"'.ts'"
name|'if'
name|'tombstone'
name|'else'
string|"'.meta'"
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'writer'
op|'('
op|')'
name|'as'
name|'writer'
op|':'
newline|'\n'
indent|'            '
name|'writer'
op|'.'
name|'put'
op|'('
name|'metadata'
op|','
name|'extension'
op|'='
name|'extension'
op|')'
newline|'\n'
nl|'\n'
DECL|member|unlinkold
dedent|''
dedent|''
name|'def'
name|'unlinkold'
op|'('
name|'self'
op|','
name|'timestamp'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Remove any older versions of the object file.  Any file that has an\n        older timestamp than timestamp will be deleted.\n\n        :param timestamp: timestamp to compare with each file\n        """'
newline|'\n'
name|'timestamp'
op|'='
name|'normalize_timestamp'
op|'('
name|'timestamp'
op|')'
newline|'\n'
nl|'\n'
DECL|function|_unlinkold
name|'def'
name|'_unlinkold'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'fname'
name|'in'
name|'os'
op|'.'
name|'listdir'
op|'('
name|'self'
op|'.'
name|'datadir'
op|')'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'fname'
op|'<'
name|'timestamp'
op|':'
newline|'\n'
indent|'                    '
name|'try'
op|':'
newline|'\n'
indent|'                        '
name|'os'
op|'.'
name|'unlink'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'datadir'
op|','
name|'fname'
op|')'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'OSError'
op|','
name|'err'
op|':'
comment|'# pragma: no cover'
newline|'\n'
indent|'                        '
name|'if'
name|'err'
op|'.'
name|'errno'
op|'!='
name|'errno'
op|'.'
name|'ENOENT'
op|':'
newline|'\n'
indent|'                            '
name|'raise'
newline|'\n'
dedent|''
dedent|''
dedent|''
dedent|''
dedent|''
name|'self'
op|'.'
name|'threadpool'
op|'.'
name|'run_in_thread'
op|'('
name|'_unlinkold'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_drop_cache
dedent|''
name|'def'
name|'_drop_cache'
op|'('
name|'self'
op|','
name|'fd'
op|','
name|'offset'
op|','
name|'length'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""Method for no-oping buffer cache drop method."""'
newline|'\n'
name|'if'
name|'not'
name|'self'
op|'.'
name|'keep_cache'
op|':'
newline|'\n'
indent|'            '
name|'drop_buffer_cache'
op|'('
name|'fd'
op|','
name|'offset'
op|','
name|'length'
op|')'
newline|'\n'
nl|'\n'
DECL|member|quarantine
dedent|''
dedent|''
name|'def'
name|'quarantine'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        In the case that a file is corrupted, move it to a quarantined\n        area to allow replication to fix it.\n\n        :returns: if quarantine is successful, path to quarantined\n                  directory otherwise None\n        """'
newline|'\n'
name|'if'
name|'not'
op|'('
name|'self'
op|'.'
name|'is_deleted'
op|'('
op|')'
name|'or'
name|'self'
op|'.'
name|'quarantined_dir'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'quarantined_dir'
op|'='
name|'self'
op|'.'
name|'threadpool'
op|'.'
name|'run_in_thread'
op|'('
nl|'\n'
name|'quarantine_renamer'
op|','
name|'self'
op|'.'
name|'device_path'
op|','
name|'self'
op|'.'
name|'data_file'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'increment'
op|'('
string|"'quarantines'"
op|')'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'quarantined_dir'
newline|'\n'
nl|'\n'
DECL|member|get_data_file_size
dedent|''
dedent|''
name|'def'
name|'get_data_file_size'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Returns the os.path.getsize for the file.  Raises an exception if this\n        file does not match the Content-Length stored in the metadata. Or if\n        self.data_file does not exist.\n\n        :returns: file size as an int\n        :raises DiskFileError: on file size mismatch.\n        :raises DiskFileNotExist: on file not existing (including deleted)\n        """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'file_size'
op|'='
number|'0'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'data_file'
op|':'
newline|'\n'
indent|'                '
name|'file_size'
op|'='
name|'self'
op|'.'
name|'threadpool'
op|'.'
name|'run_in_thread'
op|'('
nl|'\n'
name|'os'
op|'.'
name|'path'
op|'.'
name|'getsize'
op|','
name|'self'
op|'.'
name|'data_file'
op|')'
newline|'\n'
name|'if'
string|"'Content-Length'"
name|'in'
name|'self'
op|'.'
name|'metadata'
op|':'
newline|'\n'
indent|'                    '
name|'metadata_size'
op|'='
name|'int'
op|'('
name|'self'
op|'.'
name|'metadata'
op|'['
string|"'Content-Length'"
op|']'
op|')'
newline|'\n'
name|'if'
name|'file_size'
op|'!='
name|'metadata_size'
op|':'
newline|'\n'
indent|'                        '
name|'raise'
name|'DiskFileError'
op|'('
nl|'\n'
string|"'Content-Length of %s does not match file size '"
nl|'\n'
string|"'of %s'"
op|'%'
op|'('
name|'metadata_size'
op|','
name|'file_size'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'file_size'
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
op|'!='
name|'errno'
op|'.'
name|'ENOENT'
op|':'
newline|'\n'
indent|'                '
name|'raise'
newline|'\n'
dedent|''
dedent|''
name|'raise'
name|'DiskFileNotExist'
op|'('
string|"'Data File does not exist.'"
op|')'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
