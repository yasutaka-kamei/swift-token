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
string|'""" In-Memory Disk File Interface for Swift Object Server"""'
newline|'\n'
nl|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'hashlib'
newline|'\n'
name|'from'
name|'contextlib'
name|'import'
name|'contextmanager'
newline|'\n'
nl|'\n'
name|'from'
name|'eventlet'
name|'import'
name|'Timeout'
newline|'\n'
name|'from'
name|'six'
name|'import'
name|'moves'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'utils'
name|'import'
name|'Timestamp'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'exceptions'
name|'import'
name|'DiskFileQuarantined'
op|','
name|'DiskFileNotExist'
op|','
name|'DiskFileCollision'
op|','
name|'DiskFileDeleted'
op|','
name|'DiskFileNotOpen'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'request_helpers'
name|'import'
name|'is_sys_meta'
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
name|'from'
name|'swift'
op|'.'
name|'obj'
op|'.'
name|'diskfile'
name|'import'
name|'DATAFILE_SYSTEM_META'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|InMemoryFileSystem
name|'class'
name|'InMemoryFileSystem'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    A very simplistic in-memory file system scheme.\n\n    There is one dictionary mapping a given object name to a tuple. The first\n    entry in the tuble is the cStringIO buffer representing the file contents,\n    the second entry is the metadata dictionary.\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'_filesystem'
op|'='
op|'{'
op|'}'
newline|'\n'
nl|'\n'
DECL|member|get_object
dedent|''
name|'def'
name|'get_object'
op|'('
name|'self'
op|','
name|'name'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Return back an file-like object and its metadata\n\n        :param name: standard object name\n        :return (fp, metadata): fp is `StringIO` in-memory representation\n                                object (or None). metadata is a dictionary\n                                of metadata (or None)\n        """'
newline|'\n'
name|'val'
op|'='
name|'self'
op|'.'
name|'_filesystem'
op|'.'
name|'get'
op|'('
name|'name'
op|')'
newline|'\n'
name|'if'
name|'val'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'fp'
op|','
name|'metadata'
op|'='
name|'None'
op|','
name|'None'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'fp'
op|','
name|'metadata'
op|'='
name|'val'
newline|'\n'
dedent|''
name|'return'
name|'fp'
op|','
name|'metadata'
newline|'\n'
nl|'\n'
DECL|member|put_object
dedent|''
name|'def'
name|'put_object'
op|'('
name|'self'
op|','
name|'name'
op|','
name|'fp'
op|','
name|'metadata'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Store object into memory\n\n        :param name: standard object name\n        :param fp: `StringIO` in-memory representation object\n        :param metadata: dictionary of metadata to be written\n        """'
newline|'\n'
name|'self'
op|'.'
name|'_filesystem'
op|'['
name|'name'
op|']'
op|'='
op|'('
name|'fp'
op|','
name|'metadata'
op|')'
newline|'\n'
nl|'\n'
DECL|member|del_object
dedent|''
name|'def'
name|'del_object'
op|'('
name|'self'
op|','
name|'name'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Delete object from memory\n\n        :param name: standard object name\n        """'
newline|'\n'
name|'del'
name|'self'
op|'.'
name|'_filesystem'
op|'['
name|'name'
op|']'
newline|'\n'
nl|'\n'
DECL|member|get_diskfile
dedent|''
name|'def'
name|'get_diskfile'
op|'('
name|'self'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|','
op|'**'
name|'kwargs'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'return'
name|'DiskFile'
op|'('
name|'self'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
nl|'\n'
DECL|member|pickle_async_update
dedent|''
name|'def'
name|'pickle_async_update'
op|'('
name|'self'
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
string|'"""\n        For now don\'t handle async updates.\n        """'
newline|'\n'
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DiskFileWriter
dedent|''
dedent|''
name|'class'
name|'DiskFileWriter'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    .. note::\n        Sample alternative pluggable on-disk backend implementation.\n\n    Encapsulation of the write context for servicing PUT REST API\n    requests. Serves as the context manager object for DiskFile\'s create()\n    method.\n\n    :param fs: internal file system object to use\n    :param name: standard object name\n    :param fp: `StringIO` in-memory representation object\n    """'
newline|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'fs'
op|','
name|'name'
op|','
name|'fp'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'_filesystem'
op|'='
name|'fs'
newline|'\n'
name|'self'
op|'.'
name|'_name'
op|'='
name|'name'
newline|'\n'
name|'self'
op|'.'
name|'_fp'
op|'='
name|'fp'
newline|'\n'
name|'self'
op|'.'
name|'_upload_size'
op|'='
number|'0'
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
string|'"""\n        Write a chunk of data into the `StringIO` object.\n\n        :param chunk: the chunk of data to write as a string object\n        """'
newline|'\n'
name|'self'
op|'.'
name|'_fp'
op|'.'
name|'write'
op|'('
name|'chunk'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_upload_size'
op|'+='
name|'len'
op|'('
name|'chunk'
op|')'
newline|'\n'
name|'return'
name|'self'
op|'.'
name|'_upload_size'
newline|'\n'
nl|'\n'
DECL|member|put
dedent|''
name|'def'
name|'put'
op|'('
name|'self'
op|','
name|'metadata'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Make the final association in the in-memory file system for this name\n        with the `StringIO` object.\n\n        :param metadata: dictionary of metadata to be written\n        """'
newline|'\n'
name|'metadata'
op|'['
string|"'name'"
op|']'
op|'='
name|'self'
op|'.'
name|'_name'
newline|'\n'
name|'self'
op|'.'
name|'_filesystem'
op|'.'
name|'put_object'
op|'('
name|'self'
op|'.'
name|'_name'
op|','
name|'self'
op|'.'
name|'_fp'
op|','
name|'metadata'
op|')'
newline|'\n'
nl|'\n'
DECL|member|commit
dedent|''
name|'def'
name|'commit'
op|'('
name|'self'
op|','
name|'timestamp'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Perform any operations necessary to mark the object as durable. For\n        mem_diskfile type this is a no-op.\n\n        :param timestamp: object put timestamp, an instance of\n                          :class:`~swift.common.utils.Timestamp`\n        """'
newline|'\n'
name|'pass'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DiskFileReader
dedent|''
dedent|''
name|'class'
name|'DiskFileReader'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""\n    .. note::\n        Sample alternative pluggable on-disk backend implementation.\n\n    Encapsulation of the read context for servicing GET REST API\n    requests. Serves as the context manager object for DiskFile\'s reader()\n    method.\n\n    :param name: object name\n    :param fp: open file object pointer reference\n    :param obj_size: on-disk size of object in bytes\n    :param etag: MD5 hash of object from metadata\n    """'
newline|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'name'
op|','
name|'fp'
op|','
name|'obj_size'
op|','
name|'etag'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'_name'
op|'='
name|'name'
newline|'\n'
name|'self'
op|'.'
name|'_fp'
op|'='
name|'fp'
newline|'\n'
name|'self'
op|'.'
name|'_obj_size'
op|'='
name|'obj_size'
newline|'\n'
name|'self'
op|'.'
name|'_etag'
op|'='
name|'etag'
newline|'\n'
comment|'#'
nl|'\n'
name|'self'
op|'.'
name|'_iter_etag'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'_bytes_read'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'_started_at_0'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'_read_to_eof'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'_suppress_file_closing'
op|'='
name|'False'
newline|'\n'
comment|'#'
nl|'\n'
name|'self'
op|'.'
name|'was_quarantined'
op|'='
string|"''"
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
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_bytes_read'
op|'='
number|'0'
newline|'\n'
name|'self'
op|'.'
name|'_started_at_0'
op|'='
name|'False'
newline|'\n'
name|'self'
op|'.'
name|'_read_to_eof'
op|'='
name|'False'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'_fp'
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
name|'_started_at_0'
op|'='
name|'True'
newline|'\n'
name|'self'
op|'.'
name|'_iter_etag'
op|'='
name|'hashlib'
op|'.'
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
name|'_fp'
op|'.'
name|'read'
op|'('
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
name|'_iter_etag'
op|':'
newline|'\n'
indent|'                        '
name|'self'
op|'.'
name|'_iter_etag'
op|'.'
name|'update'
op|'('
name|'chunk'
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'_bytes_read'
op|'+='
name|'len'
op|'('
name|'chunk'
op|')'
newline|'\n'
name|'yield'
name|'chunk'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'_read_to_eof'
op|'='
name|'True'
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
name|'_suppress_file_closing'
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
name|'_fp'
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
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'chunk'
name|'in'
name|'self'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'length'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'                    '
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
indent|'                        '
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
name|'_suppress_file_closing'
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
DECL|member|app_iter_ranges
dedent|''
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
name|'_suppress_file_closing'
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
name|'_suppress_file_closing'
op|'='
name|'False'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'                    '
name|'self'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
dedent|''
name|'except'
name|'DiskFileQuarantined'
op|':'
newline|'\n'
indent|'                    '
name|'pass'
newline|'\n'
nl|'\n'
DECL|member|_quarantine
dedent|''
dedent|''
dedent|''
dedent|''
name|'def'
name|'_quarantine'
op|'('
name|'self'
op|','
name|'msg'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'was_quarantined'
op|'='
name|'msg'
newline|'\n'
nl|'\n'
DECL|member|_handle_close_quarantine
dedent|''
name|'def'
name|'_handle_close_quarantine'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'self'
op|'.'
name|'_bytes_read'
op|'!='
name|'self'
op|'.'
name|'_obj_size'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_quarantine'
op|'('
nl|'\n'
string|'"Bytes read: %s, does not match metadata: %s"'
op|'%'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'_bytes_read'
op|','
name|'self'
op|'.'
name|'_obj_size'
op|')'
op|')'
newline|'\n'
dedent|''
name|'elif'
name|'self'
op|'.'
name|'_iter_etag'
name|'and'
name|'self'
op|'.'
name|'_etag'
op|'!='
name|'self'
op|'.'
name|'_iter_etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_quarantine'
op|'('
nl|'\n'
string|'"ETag %s and file\'s md5 %s do not match"'
op|'%'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'_etag'
op|','
name|'self'
op|'.'
name|'_iter_etag'
op|'.'
name|'hexdigest'
op|'('
op|')'
op|')'
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
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Close the file. Will handle quarantining file if necessary.\n        """'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'_fp'
op|':'
newline|'\n'
indent|'            '
name|'try'
op|':'
newline|'\n'
indent|'                '
name|'if'
name|'self'
op|'.'
name|'_started_at_0'
name|'and'
name|'self'
op|'.'
name|'_read_to_eof'
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
op|':'
newline|'\n'
indent|'                '
name|'pass'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'_fp'
op|'='
name|'None'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|DiskFile
dedent|''
dedent|''
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
string|'"""\n    .. note::\n\n        Sample alternative pluggable on-disk backend implementation. This\n        example duck-types the reference implementation DiskFile class.\n\n    Manage object files in-memory.\n\n    :param fs: an instance of InMemoryFileSystem\n    :param account: account name for the object\n    :param container: container name for the object\n    :param obj: object name for the object\n    """'
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'fs'
op|','
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'_name'
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
name|'self'
op|'.'
name|'_metadata'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'_fp'
op|'='
name|'None'
newline|'\n'
name|'self'
op|'.'
name|'_filesystem'
op|'='
name|'fs'
newline|'\n'
name|'self'
op|'.'
name|'fragments'
op|'='
name|'None'
newline|'\n'
nl|'\n'
DECL|member|open
dedent|''
name|'def'
name|'open'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Open the file and read the metadata.\n\n        This method must populate the _metadata attribute.\n        :raises DiskFileCollision: on name mis-match with metadata\n        :raises DiskFileDeleted: if it does not exist, or a tombstone is\n                                 present\n        :raises DiskFileQuarantined: if while reading metadata of the file\n                                     some data did pass cross checks\n        """'
newline|'\n'
name|'fp'
op|','
name|'self'
op|'.'
name|'_metadata'
op|'='
name|'self'
op|'.'
name|'_filesystem'
op|'.'
name|'get_object'
op|'('
name|'self'
op|'.'
name|'_name'
op|')'
newline|'\n'
name|'if'
name|'fp'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'DiskFileDeleted'
op|'('
op|')'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'_fp'
op|'='
name|'self'
op|'.'
name|'_verify_data_file'
op|'('
name|'fp'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'_metadata'
op|'='
name|'self'
op|'.'
name|'_metadata'
name|'or'
op|'{'
op|'}'
newline|'\n'
name|'return'
name|'self'
newline|'\n'
nl|'\n'
DECL|member|__enter__
dedent|''
name|'def'
name|'__enter__'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'self'
op|'.'
name|'_metadata'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'DiskFileNotOpen'
op|'('
op|')'
newline|'\n'
dedent|''
name|'return'
name|'self'
newline|'\n'
nl|'\n'
DECL|member|__exit__
dedent|''
name|'def'
name|'__exit__'
op|'('
name|'self'
op|','
name|'t'
op|','
name|'v'
op|','
name|'tb'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'self'
op|'.'
name|'_fp'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_fp'
op|'='
name|'None'
newline|'\n'
nl|'\n'
DECL|member|_quarantine
dedent|''
dedent|''
name|'def'
name|'_quarantine'
op|'('
name|'self'
op|','
name|'name'
op|','
name|'msg'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Quarantine a file; responsible for incrementing the associated logger\'s\n        count of quarantines.\n\n        :param name: name of object to quarantine\n        :param msg: reason for quarantining to be included in the exception\n        :returns: DiskFileQuarantined exception object\n        """'
newline|'\n'
comment|'# for this implementation we simply delete the bad object'
nl|'\n'
name|'self'
op|'.'
name|'_filesystem'
op|'.'
name|'del_object'
op|'('
name|'name'
op|')'
newline|'\n'
name|'return'
name|'DiskFileQuarantined'
op|'('
name|'msg'
op|')'
newline|'\n'
nl|'\n'
DECL|member|_verify_data_file
dedent|''
name|'def'
name|'_verify_data_file'
op|'('
name|'self'
op|','
name|'fp'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Verify the metadata\'s name value matches what we think the object is\n        named.\n\n        :raises DiskFileCollision: if the metadata stored name does not match\n                                   the referenced name of the file\n        :raises DiskFileNotExist: if the object has expired\n        :raises DiskFileQuarantined: if data inconsistencies were detected\n                                     between the metadata and the file-system\n                                     metadata\n        """'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'mname'
op|'='
name|'self'
op|'.'
name|'_metadata'
op|'['
string|"'name'"
op|']'
newline|'\n'
dedent|''
name|'except'
name|'KeyError'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'self'
op|'.'
name|'_quarantine'
op|'('
name|'self'
op|'.'
name|'_name'
op|','
string|'"missing name metadata"'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'mname'
op|'!='
name|'self'
op|'.'
name|'_name'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'DiskFileCollision'
op|'('
string|"'Client path does not match path '"
nl|'\n'
string|"'stored in object metadata'"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'x_delete_at'
op|'='
name|'int'
op|'('
name|'self'
op|'.'
name|'_metadata'
op|'['
string|"'X-Delete-At'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'KeyError'
op|':'
newline|'\n'
indent|'            '
name|'pass'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
comment|'# Quarantine, the x-delete-at key is present but not an'
nl|'\n'
comment|'# integer.'
nl|'\n'
indent|'            '
name|'raise'
name|'self'
op|'.'
name|'_quarantine'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'_name'
op|','
string|'"bad metadata x-delete-at value %s"'
op|'%'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'_metadata'
op|'['
string|"'X-Delete-At'"
op|']'
op|')'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'x_delete_at'
op|'<='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'DiskFileNotExist'
op|'('
string|"'Expired'"
op|')'
newline|'\n'
dedent|''
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'metadata_size'
op|'='
name|'int'
op|'('
name|'self'
op|'.'
name|'_metadata'
op|'['
string|"'Content-Length'"
op|']'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'KeyError'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'self'
op|'.'
name|'_quarantine'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'_name'
op|','
string|'"missing content-length in metadata"'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'ValueError'
op|':'
newline|'\n'
comment|'# Quarantine, the content-length key is present but not an'
nl|'\n'
comment|'# integer.'
nl|'\n'
indent|'            '
name|'raise'
name|'self'
op|'.'
name|'_quarantine'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'_name'
op|','
string|'"bad metadata content-length value %s"'
op|'%'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'_metadata'
op|'['
string|"'Content-Length'"
op|']'
op|')'
op|')'
newline|'\n'
dedent|''
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'fp'
op|'.'
name|'seek'
op|'('
number|'0'
op|','
number|'2'
op|')'
newline|'\n'
name|'obj_size'
op|'='
name|'fp'
op|'.'
name|'tell'
op|'('
op|')'
newline|'\n'
name|'fp'
op|'.'
name|'seek'
op|'('
number|'0'
op|','
number|'0'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'OSError'
name|'as'
name|'err'
op|':'
newline|'\n'
comment|"# Quarantine, we can't successfully stat the file."
nl|'\n'
indent|'            '
name|'raise'
name|'self'
op|'.'
name|'_quarantine'
op|'('
name|'self'
op|'.'
name|'_name'
op|','
string|'"not stat-able: %s"'
op|'%'
name|'err'
op|')'
newline|'\n'
dedent|''
name|'if'
name|'obj_size'
op|'!='
name|'metadata_size'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'self'
op|'.'
name|'_quarantine'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'_name'
op|','
string|'"metadata content-length %s does"'
nl|'\n'
string|'" not match actual object size %s"'
op|'%'
op|'('
nl|'\n'
name|'metadata_size'
op|','
name|'obj_size'
op|')'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'fp'
newline|'\n'
nl|'\n'
DECL|member|get_metadata
dedent|''
name|'def'
name|'get_metadata'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Provide the metadata for an object as a dictionary.\n\n        :returns: object\'s metadata dictionary\n        """'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'_metadata'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'DiskFileNotOpen'
op|'('
op|')'
newline|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'_metadata'
newline|'\n'
nl|'\n'
DECL|member|read_metadata
dedent|''
name|'def'
name|'read_metadata'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Return the metadata for an object.\n\n        :returns: metadata dictionary for an object\n        """'
newline|'\n'
name|'with'
name|'self'
op|'.'
name|'open'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'get_metadata'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|reader
dedent|''
dedent|''
name|'def'
name|'reader'
op|'('
name|'self'
op|','
name|'keep_cache'
op|'='
name|'False'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Return a swift.common.swob.Response class compatible "app_iter"\n        object. The responsibility of closing the open file is passed to the\n        DiskFileReader object.\n\n        :param keep_cache:\n        """'
newline|'\n'
name|'dr'
op|'='
name|'DiskFileReader'
op|'('
name|'self'
op|'.'
name|'_name'
op|','
name|'self'
op|'.'
name|'_fp'
op|','
nl|'\n'
name|'int'
op|'('
name|'self'
op|'.'
name|'_metadata'
op|'['
string|"'Content-Length'"
op|']'
op|')'
op|','
nl|'\n'
name|'self'
op|'.'
name|'_metadata'
op|'['
string|"'ETag'"
op|']'
op|')'
newline|'\n'
comment|'# At this point the reader object is now responsible for'
nl|'\n'
comment|'# the file pointer.'
nl|'\n'
name|'self'
op|'.'
name|'_fp'
op|'='
name|'None'
newline|'\n'
name|'return'
name|'dr'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'contextmanager'
newline|'\n'
DECL|member|create
name|'def'
name|'create'
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
string|'"""\n        Context manager to create a file. We create a temporary file first, and\n        then return a DiskFileWriter object to encapsulate the state.\n\n        :param size: optional initial size of file to explicitly allocate on\n                     disk\n        :raises DiskFileNoSpace: if a size is specified and allocation fails\n        """'
newline|'\n'
name|'fp'
op|'='
name|'moves'
op|'.'
name|'cStringIO'
op|'('
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'yield'
name|'DiskFileWriter'
op|'('
name|'self'
op|'.'
name|'_filesystem'
op|','
name|'self'
op|'.'
name|'_name'
op|','
name|'fp'
op|')'
newline|'\n'
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'del'
name|'fp'
newline|'\n'
nl|'\n'
DECL|member|write_metadata
dedent|''
dedent|''
name|'def'
name|'write_metadata'
op|'('
name|'self'
op|','
name|'metadata'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Write a block of metadata to an object.\n        """'
newline|'\n'
name|'data'
op|','
name|'cur_mdata'
op|'='
name|'self'
op|'.'
name|'_filesystem'
op|'.'
name|'get_object'
op|'('
name|'self'
op|'.'
name|'_name'
op|')'
newline|'\n'
name|'if'
name|'data'
name|'is'
name|'not'
name|'None'
op|':'
newline|'\n'
comment|"# The object exists. Update the new metadata with the object's"
nl|'\n'
comment|'# immutable metadata (e.g. name, size, etag, sysmeta) and store it'
nl|'\n'
comment|'# with the object data.'
nl|'\n'
indent|'            '
name|'immutable_metadata'
op|'='
name|'dict'
op|'('
nl|'\n'
op|'['
op|'('
name|'key'
op|','
name|'val'
op|')'
name|'for'
name|'key'
op|','
name|'val'
name|'in'
name|'cur_mdata'
op|'.'
name|'items'
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
name|'DATAFILE_SYSTEM_META'
nl|'\n'
name|'or'
name|'is_sys_meta'
op|'('
string|"'object'"
op|','
name|'key'
op|')'
op|']'
op|')'
newline|'\n'
name|'metadata'
op|'.'
name|'update'
op|'('
name|'immutable_metadata'
op|')'
newline|'\n'
name|'metadata'
op|'['
string|"'name'"
op|']'
op|'='
name|'self'
op|'.'
name|'_name'
newline|'\n'
name|'self'
op|'.'
name|'_filesystem'
op|'.'
name|'put_object'
op|'('
name|'self'
op|'.'
name|'_name'
op|','
name|'data'
op|','
name|'metadata'
op|')'
newline|'\n'
nl|'\n'
DECL|member|delete
dedent|''
dedent|''
name|'def'
name|'delete'
op|'('
name|'self'
op|','
name|'timestamp'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Perform a delete for the given object in the given container under the\n        given account.\n\n        This creates a tombstone file with the given timestamp, and removes\n        any older versions of the object file.  Any file that has an older\n        timestamp than timestamp will be deleted.\n\n        :param timestamp: timestamp to compare with each file\n        """'
newline|'\n'
name|'fp'
op|','
name|'md'
op|'='
name|'self'
op|'.'
name|'_filesystem'
op|'.'
name|'get_object'
op|'('
name|'self'
op|'.'
name|'_name'
op|')'
newline|'\n'
name|'if'
name|'md'
name|'and'
name|'md'
op|'['
string|"'X-Timestamp'"
op|']'
op|'<'
name|'Timestamp'
op|'('
name|'timestamp'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'_filesystem'
op|'.'
name|'del_object'
op|'('
name|'self'
op|'.'
name|'_name'
op|')'
newline|'\n'
nl|'\n'
dedent|''
dedent|''
op|'@'
name|'property'
newline|'\n'
DECL|member|timestamp
name|'def'
name|'timestamp'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'self'
op|'.'
name|'_metadata'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'DiskFileNotOpen'
op|'('
op|')'
newline|'\n'
dedent|''
name|'return'
name|'Timestamp'
op|'('
name|'self'
op|'.'
name|'_metadata'
op|'.'
name|'get'
op|'('
string|"'X-Timestamp'"
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|variable|data_timestamp
dedent|''
name|'data_timestamp'
op|'='
name|'timestamp'
newline|'\n'
nl|'\n'
DECL|variable|durable_timestamp
name|'durable_timestamp'
op|'='
name|'timestamp'
newline|'\n'
nl|'\n'
DECL|variable|content_type_timestamp
name|'content_type_timestamp'
op|'='
name|'timestamp'
newline|'\n'
nl|'\n'
op|'@'
name|'property'
newline|'\n'
DECL|member|content_type
name|'def'
name|'content_type'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'self'
op|'.'
name|'_metadata'
name|'is'
name|'None'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'DiskFileNotOpen'
op|'('
op|')'
newline|'\n'
dedent|''
name|'return'
name|'self'
op|'.'
name|'_metadata'
op|'.'
name|'get'
op|'('
string|"'Content-Type'"
op|')'
newline|'\n'
dedent|''
dedent|''
endmarker|''
end_unit
