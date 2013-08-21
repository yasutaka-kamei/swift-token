begin_unit
comment|'# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.'
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
name|'import'
name|'pbr'
op|'.'
name|'version'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|variable|_version_info
name|'_version_info'
op|'='
name|'pbr'
op|'.'
name|'version'
op|'.'
name|'VersionInfo'
op|'('
string|"'swift'"
op|')'
newline|'\n'
DECL|variable|__version__
name|'__version__'
op|'='
name|'_version_info'
op|'.'
name|'release_string'
op|'('
op|')'
newline|'\n'
DECL|variable|__canonical_version__
name|'__canonical_version__'
op|'='
name|'_version_info'
op|'.'
name|'version_string'
op|'('
op|')'
newline|'\n'
endmarker|''
end_unit
