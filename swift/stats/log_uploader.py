begin_unit
comment|'# Copyright (c) 2010-2011 OpenStack, LLC.'
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
name|'os'
newline|'\n'
name|'import'
name|'hashlib'
newline|'\n'
name|'import'
name|'time'
newline|'\n'
name|'import'
name|'gzip'
newline|'\n'
name|'import'
name|'re'
newline|'\n'
name|'from'
name|'paste'
op|'.'
name|'deploy'
name|'import'
name|'appconfig'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'internal_proxy'
name|'import'
name|'InternalProxy'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
op|'.'
name|'daemon'
name|'import'
name|'Daemon'
newline|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'utils'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|LogUploader
name|'class'
name|'LogUploader'
op|'('
name|'Daemon'
op|')'
op|':'
newline|'\n'
indent|'    '
string|"'''\n    Given a local directory, a swift account, and a container name, LogParser\n    will upload all files in the local directory to the given account/\n    container.  All but the newest files will be uploaded, and the files' md5\n    sum will be computed. The hash is used to prevent duplicate data from\n    being uploaded multiple times in different files (ex: log lines). Since\n    the hash is computed, it is also used as the uploaded object's etag to\n    ensure data integrity.\n\n    Note that after the file is successfully uploaded, it will be unlinked.\n\n    The given proxy server config is used to instantiate a proxy server for\n    the object uploads.\n    '''"
newline|'\n'
nl|'\n'
DECL|member|__init__
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'uploader_conf'
op|','
name|'plugin_name'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'super'
op|'('
name|'LogUploader'
op|','
name|'self'
op|')'
op|'.'
name|'__init__'
op|'('
name|'uploader_conf'
op|')'
newline|'\n'
name|'log_name'
op|'='
string|"'%s-log-uploader'"
op|'%'
name|'plugin_name'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'='
name|'utils'
op|'.'
name|'get_logger'
op|'('
name|'uploader_conf'
op|','
name|'log_name'
op|','
nl|'\n'
name|'log_route'
op|'='
name|'plugin_name'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'log_dir'
op|'='
name|'uploader_conf'
op|'.'
name|'get'
op|'('
string|"'log_dir'"
op|','
string|"'/var/log/swift/'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'swift_account'
op|'='
name|'uploader_conf'
op|'['
string|"'swift_account'"
op|']'
newline|'\n'
name|'self'
op|'.'
name|'container_name'
op|'='
name|'uploader_conf'
op|'['
string|"'container_name'"
op|']'
newline|'\n'
name|'proxy_server_conf_loc'
op|'='
name|'uploader_conf'
op|'.'
name|'get'
op|'('
string|"'proxy_server_conf'"
op|','
nl|'\n'
string|"'/etc/swift/proxy-server.conf'"
op|')'
newline|'\n'
name|'proxy_server_conf'
op|'='
name|'appconfig'
op|'('
string|"'config:%s'"
op|'%'
name|'proxy_server_conf_loc'
op|','
nl|'\n'
name|'name'
op|'='
string|"'proxy-server'"
op|')'
newline|'\n'
name|'self'
op|'.'
name|'internal_proxy'
op|'='
name|'InternalProxy'
op|'('
name|'proxy_server_conf'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'new_log_cutoff'
op|'='
name|'int'
op|'('
name|'uploader_conf'
op|'.'
name|'get'
op|'('
string|"'new_log_cutoff'"
op|','
string|"'7200'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'unlink_log'
op|'='
name|'uploader_conf'
op|'.'
name|'get'
op|'('
string|"'unlink_log'"
op|','
string|"'True'"
op|')'
op|'.'
name|'lower'
op|'('
op|')'
name|'in'
name|'utils'
op|'.'
name|'TRUE_VALUES'
newline|'\n'
nl|'\n'
comment|'# source_filename_format is deprecated'
nl|'\n'
name|'source_filename_format'
op|'='
name|'uploader_conf'
op|'.'
name|'get'
op|'('
string|"'source_filename_format'"
op|')'
newline|'\n'
name|'source_filename_pattern'
op|'='
name|'uploader_conf'
op|'.'
name|'get'
op|'('
string|"'source_filename_pattern'"
op|')'
newline|'\n'
name|'if'
name|'source_filename_format'
name|'and'
name|'not'
name|'source_filename_pattern'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'warning'
op|'('
name|'_'
op|'('
string|"'source_filename_format is unreliable and '"
nl|'\n'
string|"'deprecated; use source_filename_pattern'"
op|')'
op|')'
newline|'\n'
name|'self'
op|'.'
name|'pattern'
op|'='
name|'self'
op|'.'
name|'convert_glob_to_regex'
op|'('
name|'source_filename_format'
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'pattern'
op|'='
name|'source_filename_pattern'
name|'or'
string|"'%Y%m%d%H'"
newline|'\n'
nl|'\n'
DECL|member|run_once
dedent|''
dedent|''
name|'def'
name|'run_once'
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
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|'"Uploading logs"'
op|')'
op|')'
newline|'\n'
name|'start'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'upload_all_logs'
op|'('
op|')'
newline|'\n'
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|'"Uploading logs complete (%0.2f minutes)"'
op|')'
op|'%'
nl|'\n'
op|'('
op|'('
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'start'
op|')'
op|'/'
number|'60'
op|')'
op|')'
newline|'\n'
nl|'\n'
DECL|member|convert_glob_to_regex
dedent|''
name|'def'
name|'convert_glob_to_regex'
op|'('
name|'self'
op|','
name|'glob'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Make a best effort to support old style config globs\n\n        :param : old style config source_filename_format\n\n        :returns : new style config source_filename_pattern\n        """'
newline|'\n'
name|'pattern'
op|'='
name|'glob'
newline|'\n'
name|'pattern'
op|'='
name|'pattern'
op|'.'
name|'replace'
op|'('
string|"'.'"
op|','
string|"r'\\.'"
op|')'
newline|'\n'
name|'pattern'
op|'='
name|'pattern'
op|'.'
name|'replace'
op|'('
string|"'*'"
op|','
string|"r'.*'"
op|')'
newline|'\n'
name|'pattern'
op|'='
name|'pattern'
op|'.'
name|'replace'
op|'('
string|"'?'"
op|','
string|"r'.?'"
op|')'
newline|'\n'
name|'return'
name|'pattern'
newline|'\n'
nl|'\n'
DECL|member|validate_filename_pattern
dedent|''
name|'def'
name|'validate_filename_pattern'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Validate source_filename_pattern\n\n        :returns : valid regex pattern based on soruce_filename_pattern with\n                   group matches substituded for date fmt markers\n        """'
newline|'\n'
name|'pattern'
op|'='
name|'self'
op|'.'
name|'pattern'
newline|'\n'
name|'markers'
op|'='
op|'{'
nl|'\n'
string|"'%Y'"
op|':'
op|'('
string|"'year'"
op|','
string|"'(?P<year>[0-9]{4})'"
op|')'
op|','
nl|'\n'
string|"'%m'"
op|':'
op|'('
string|"'month'"
op|','
string|"'(?P<month>[0-1][0-9])'"
op|')'
op|','
nl|'\n'
string|"'%d'"
op|':'
op|'('
string|"'day'"
op|','
string|"'(?P<day>[0-3][0-9])'"
op|')'
op|','
nl|'\n'
string|"'%H'"
op|':'
op|'('
string|"'hour'"
op|','
string|"'(?P<hour>[0-2][0-9])'"
op|')'
op|','
nl|'\n'
op|'}'
newline|'\n'
name|'for'
name|'marker'
op|','
op|'('
name|'mtype'
op|','
name|'group'
op|')'
name|'in'
name|'markers'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
indent|'            '
name|'if'
name|'marker'
name|'not'
name|'in'
name|'self'
op|'.'
name|'pattern'
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
string|"'source_filename_pattern much contain a '"
nl|'\n'
string|"'marker %(marker)s to match the '"
nl|'\n'
string|"'%(mtype)s'"
op|')'
op|'%'
op|'{'
string|"'marker'"
op|':'
name|'marker'
op|','
nl|'\n'
string|"'mtype'"
op|':'
name|'mtype'
op|'}'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'pattern'
op|'='
name|'pattern'
op|'.'
name|'replace'
op|'('
name|'marker'
op|','
name|'group'
op|')'
newline|'\n'
dedent|''
name|'return'
name|'pattern'
newline|'\n'
nl|'\n'
DECL|member|get_relpath_to_files_under_log_dir
dedent|''
name|'def'
name|'get_relpath_to_files_under_log_dir'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Look under log_dir recursively and return all filenames as relpaths\n\n        :returns : list of strs, the relpath to all filenames under log_dir\n        """'
newline|'\n'
name|'all_files'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'path'
op|','
name|'dirs'
op|','
name|'files'
name|'in'
name|'os'
op|'.'
name|'walk'
op|'('
name|'self'
op|'.'
name|'log_dir'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'all_files'
op|'.'
name|'extend'
op|'('
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'path'
op|','
name|'f'
op|')'
name|'for'
name|'f'
name|'in'
name|'files'
op|')'
newline|'\n'
dedent|''
name|'return'
op|'['
name|'os'
op|'.'
name|'path'
op|'.'
name|'relpath'
op|'('
name|'f'
op|','
name|'start'
op|'='
name|'self'
op|'.'
name|'log_dir'
op|')'
name|'for'
name|'f'
name|'in'
name|'all_files'
op|']'
newline|'\n'
nl|'\n'
DECL|member|filter_files
dedent|''
name|'def'
name|'filter_files'
op|'('
name|'self'
op|','
name|'all_files'
op|','
name|'pattern'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Filter files based on regex pattern\n\n        :param all_files: list of strs, relpath of the filenames under log_dir\n        :param pattern: regex pattern to match against filenames\n\n        :returns : dict mapping full path of file to match group dict\n        """'
newline|'\n'
name|'filename2match'
op|'='
op|'{'
op|'}'
newline|'\n'
name|'found_match'
op|'='
name|'False'
newline|'\n'
name|'for'
name|'filename'
name|'in'
name|'all_files'
op|':'
newline|'\n'
indent|'            '
name|'match'
op|'='
name|'re'
op|'.'
name|'match'
op|'('
name|'pattern'
op|','
name|'filename'
op|')'
newline|'\n'
name|'if'
name|'match'
op|':'
newline|'\n'
indent|'                '
name|'found_match'
op|'='
name|'True'
newline|'\n'
name|'full_path'
op|'='
name|'os'
op|'.'
name|'path'
op|'.'
name|'join'
op|'('
name|'self'
op|'.'
name|'log_dir'
op|','
name|'filename'
op|')'
newline|'\n'
name|'filename2match'
op|'['
name|'full_path'
op|']'
op|'='
name|'match'
op|'.'
name|'groupdict'
op|'('
op|')'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|"'%(filename)s does not match '"
nl|'\n'
string|"'%(pattern)s'"
op|')'
op|'%'
op|'{'
string|"'filename'"
op|':'
name|'filename'
op|','
nl|'\n'
string|"'pattern'"
op|':'
name|'pattern'
op|'}'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'return'
name|'filename2match'
newline|'\n'
nl|'\n'
DECL|member|upload_all_logs
dedent|''
name|'def'
name|'upload_all_logs'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Match files under log_dir to source_filename_pattern and upload to swift\n        """'
newline|'\n'
name|'pattern'
op|'='
name|'self'
op|'.'
name|'validate_filename_pattern'
op|'('
op|')'
newline|'\n'
name|'if'
name|'not'
name|'pattern'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
name|'_'
op|'('
string|"'Invalid filename_format'"
op|')'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'all_files'
op|'='
name|'self'
op|'.'
name|'get_relpath_to_files_under_log_dir'
op|'('
op|')'
newline|'\n'
name|'filename2match'
op|'='
name|'self'
op|'.'
name|'filter_files'
op|'('
name|'all_files'
op|','
name|'pattern'
op|')'
newline|'\n'
name|'if'
name|'not'
name|'filename2match'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'info'
op|'('
name|'_'
op|'('
string|"'No files in %(log_dir)s match %(pattern)s'"
op|')'
op|'%'
nl|'\n'
op|'{'
string|"'log_dir'"
op|':'
name|'self'
op|'.'
name|'log_dir'
op|','
string|"'pattern'"
op|':'
name|'pattern'
op|'}'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'self'
op|'.'
name|'internal_proxy'
op|'.'
name|'create_container'
op|'('
name|'self'
op|'.'
name|'swift_account'
op|','
nl|'\n'
name|'self'
op|'.'
name|'container_name'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
name|'_'
op|'('
string|"'Unable to create container for '"
nl|'\n'
string|"'%(account)s/%(container)s'"
op|')'
op|'%'
op|'{'
nl|'\n'
string|"'account'"
op|':'
name|'self'
op|'.'
name|'swift_account'
op|','
nl|'\n'
string|"'container'"
op|':'
name|'self'
op|'.'
name|'container_name'
op|'}'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'for'
name|'filename'
op|','
name|'match'
name|'in'
name|'filename2match'
op|'.'
name|'items'
op|'('
op|')'
op|':'
newline|'\n'
comment|"# don't process very new logs"
nl|'\n'
indent|'            '
name|'seconds_since_mtime'
op|'='
name|'time'
op|'.'
name|'time'
op|'('
op|')'
op|'-'
name|'os'
op|'.'
name|'stat'
op|'('
name|'filename'
op|')'
op|'.'
name|'st_mtime'
newline|'\n'
name|'if'
name|'seconds_since_mtime'
op|'<'
name|'self'
op|'.'
name|'new_log_cutoff'
op|':'
newline|'\n'
indent|'                '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|'"Skipping log: %(file)s "'
nl|'\n'
string|'"(< %(cutoff)d seconds old)"'
op|')'
op|'%'
op|'{'
nl|'\n'
string|"'file'"
op|':'
name|'filename'
op|','
nl|'\n'
string|"'cutoff'"
op|':'
name|'self'
op|'.'
name|'new_log_cutoff'
op|'}'
op|')'
newline|'\n'
name|'continue'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'upload_one_log'
op|'('
name|'filename'
op|','
op|'**'
name|'match'
op|')'
newline|'\n'
nl|'\n'
DECL|member|upload_one_log
dedent|''
dedent|''
name|'def'
name|'upload_one_log'
op|'('
name|'self'
op|','
name|'filename'
op|','
name|'year'
op|','
name|'month'
op|','
name|'day'
op|','
name|'hour'
op|')'
op|':'
newline|'\n'
indent|'        '
string|'"""\n        Upload one file to swift\n        """'
newline|'\n'
name|'if'
name|'os'
op|'.'
name|'path'
op|'.'
name|'getsize'
op|'('
name|'filename'
op|')'
op|'=='
number|'0'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|'"Log %s is 0 length, skipping"'
op|')'
op|'%'
name|'filename'
op|')'
newline|'\n'
name|'return'
newline|'\n'
dedent|''
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|'"Processing log: %s"'
op|')'
op|'%'
name|'filename'
op|')'
newline|'\n'
name|'filehash'
op|'='
name|'hashlib'
op|'.'
name|'md5'
op|'('
op|')'
newline|'\n'
name|'already_compressed'
op|'='
name|'True'
name|'if'
name|'filename'
op|'.'
name|'endswith'
op|'('
string|"'.gz'"
op|')'
name|'else'
name|'False'
newline|'\n'
name|'opener'
op|'='
name|'gzip'
op|'.'
name|'open'
name|'if'
name|'already_compressed'
name|'else'
name|'open'
newline|'\n'
name|'f'
op|'='
name|'opener'
op|'('
name|'filename'
op|','
string|"'rb'"
op|')'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'for'
name|'line'
name|'in'
name|'f'
op|':'
newline|'\n'
comment|'# filter out bad lines here?'
nl|'\n'
indent|'                '
name|'filehash'
op|'.'
name|'update'
op|'('
name|'line'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'finally'
op|':'
newline|'\n'
indent|'            '
name|'f'
op|'.'
name|'close'
op|'('
op|')'
newline|'\n'
dedent|''
name|'filehash'
op|'='
name|'filehash'
op|'.'
name|'hexdigest'
op|'('
op|')'
newline|'\n'
comment|'# By adding a hash to the filename, we ensure that uploaded files'
nl|'\n'
comment|'# have unique filenames and protect against uploading one file'
nl|'\n'
comment|'# more than one time. By using md5, we get an etag for free.'
nl|'\n'
name|'target_filename'
op|'='
string|"'/'"
op|'.'
name|'join'
op|'('
op|'['
name|'year'
op|','
name|'month'
op|','
name|'day'
op|','
name|'hour'
op|','
name|'filehash'
op|'+'
string|"'.gz'"
op|']'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'internal_proxy'
op|'.'
name|'upload_file'
op|'('
name|'filename'
op|','
nl|'\n'
name|'self'
op|'.'
name|'swift_account'
op|','
nl|'\n'
name|'self'
op|'.'
name|'container_name'
op|','
nl|'\n'
name|'target_filename'
op|','
nl|'\n'
name|'compress'
op|'='
op|'('
name|'not'
name|'already_compressed'
op|')'
op|')'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'debug'
op|'('
name|'_'
op|'('
string|'"Uploaded log %(file)s to %(target)s"'
op|')'
op|'%'
nl|'\n'
op|'{'
string|"'file'"
op|':'
name|'filename'
op|','
string|"'target'"
op|':'
name|'target_filename'
op|'}'
op|')'
newline|'\n'
name|'if'
name|'self'
op|'.'
name|'unlink_log'
op|':'
newline|'\n'
indent|'                '
name|'os'
op|'.'
name|'unlink'
op|'('
name|'filename'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'logger'
op|'.'
name|'error'
op|'('
name|'_'
op|'('
string|'"ERROR: Upload of log %s failed!"'
op|')'
op|'%'
name|'filename'
op|')'
newline|'\n'
dedent|''
dedent|''
dedent|''
endmarker|''
end_unit
