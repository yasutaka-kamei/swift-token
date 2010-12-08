begin_unit
comment|'#!/usr/bin/python'
nl|'\n'
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
name|'setuptools'
name|'import'
name|'setup'
op|','
name|'find_packages'
newline|'\n'
name|'from'
name|'setuptools'
op|'.'
name|'command'
op|'.'
name|'sdist'
name|'import'
name|'sdist'
newline|'\n'
name|'import'
name|'os'
newline|'\n'
name|'import'
name|'subprocess'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
name|'import'
name|'__version__'
name|'as'
name|'version'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|local_sdist
name|'class'
name|'local_sdist'
op|'('
name|'sdist'
op|')'
op|':'
newline|'\n'
indent|'    '
string|'"""Customized sdist hook - builds the ChangeLog file from VC first"""'
newline|'\n'
nl|'\n'
DECL|member|run
name|'def'
name|'run'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'os'
op|'.'
name|'path'
op|'.'
name|'isdir'
op|'('
string|"'.bzr'"
op|')'
op|':'
newline|'\n'
comment|"# We're in a bzr branch"
nl|'\n'
nl|'\n'
indent|'            '
name|'log_cmd'
op|'='
name|'subprocess'
op|'.'
name|'Popen'
op|'('
op|'['
string|'"bzr"'
op|','
string|'"log"'
op|','
string|'"--gnu"'
op|']'
op|','
nl|'\n'
name|'stdout'
op|'='
name|'subprocess'
op|'.'
name|'PIPE'
op|')'
newline|'\n'
name|'changelog'
op|'='
name|'log_cmd'
op|'.'
name|'communicate'
op|'('
op|')'
op|'['
number|'0'
op|']'
newline|'\n'
name|'with'
name|'open'
op|'('
string|'"ChangeLog"'
op|','
string|'"w"'
op|')'
name|'as'
name|'changelog_file'
op|':'
newline|'\n'
indent|'                '
name|'changelog_file'
op|'.'
name|'write'
op|'('
name|'changelog'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'sdist'
op|'.'
name|'run'
op|'('
name|'self'
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|variable|name
dedent|''
dedent|''
name|'name'
op|'='
string|"'swift'"
newline|'\n'
nl|'\n'
name|'setup'
op|'('
nl|'\n'
DECL|variable|name
name|'name'
op|'='
name|'name'
op|','
nl|'\n'
DECL|variable|version
name|'version'
op|'='
name|'version'
op|','
nl|'\n'
DECL|variable|description
name|'description'
op|'='
string|"'Swift'"
op|','
nl|'\n'
DECL|variable|license
name|'license'
op|'='
string|"'Apache License (2.0)'"
op|','
nl|'\n'
DECL|variable|author
name|'author'
op|'='
string|"'OpenStack, LLC.'"
op|','
nl|'\n'
DECL|variable|author_email
name|'author_email'
op|'='
string|"'openstack-admins@lists.launchpad.net'"
op|','
nl|'\n'
DECL|variable|url
name|'url'
op|'='
string|"'https://launchpad.net/swift'"
op|','
nl|'\n'
DECL|variable|packages
name|'packages'
op|'='
name|'find_packages'
op|'('
name|'exclude'
op|'='
op|'['
string|"'test'"
op|','
string|"'bin'"
op|']'
op|')'
op|','
nl|'\n'
DECL|variable|test_suite
name|'test_suite'
op|'='
string|"'nose.collector'"
op|','
nl|'\n'
DECL|variable|cmdclass
name|'cmdclass'
op|'='
op|'{'
string|"'sdist'"
op|':'
name|'local_sdist'
op|'}'
op|','
nl|'\n'
DECL|variable|classifiers
name|'classifiers'
op|'='
op|'['
nl|'\n'
string|"'Development Status :: 4 - Beta'"
op|','
nl|'\n'
string|"'License :: OSI Approved :: Apache Software License'"
op|','
nl|'\n'
string|"'Operating System :: POSIX :: Linux'"
op|','
nl|'\n'
string|"'Programming Language :: Python :: 2.6'"
op|','
nl|'\n'
string|"'Environment :: No Input/Output (Daemon)'"
op|','
nl|'\n'
op|']'
op|','
nl|'\n'
DECL|variable|install_requires
name|'install_requires'
op|'='
op|'['
op|']'
op|','
comment|'# removed for better compat'
nl|'\n'
DECL|variable|scripts
name|'scripts'
op|'='
op|'['
nl|'\n'
string|"'bin/st'"
op|','
string|"'bin/swift-account-auditor'"
op|','
nl|'\n'
string|"'bin/swift-account-audit'"
op|','
string|"'bin/swift-account-reaper'"
op|','
nl|'\n'
string|"'bin/swift-account-replicator'"
op|','
string|"'bin/swift-account-server'"
op|','
nl|'\n'
string|"'bin/swift-auth-add-user'"
op|','
nl|'\n'
string|"'bin/swift-auth-recreate-accounts'"
op|','
string|"'bin/swift-auth-server'"
op|','
nl|'\n'
string|"'bin/swift-auth-update-reseller-prefixes'"
op|','
nl|'\n'
string|"'bin/swift-container-auditor'"
op|','
nl|'\n'
string|"'bin/swift-container-replicator'"
op|','
nl|'\n'
string|"'bin/swift-container-server'"
op|','
string|"'bin/swift-container-updater'"
op|','
nl|'\n'
string|"'bin/swift-drive-audit'"
op|','
string|"'bin/swift-get-nodes'"
op|','
nl|'\n'
string|"'bin/swift-init'"
op|','
string|"'bin/swift-object-auditor'"
op|','
nl|'\n'
string|"'bin/swift-object-info'"
op|','
nl|'\n'
string|"'bin/swift-object-replicator'"
op|','
nl|'\n'
string|"'bin/swift-object-server'"
op|','
nl|'\n'
string|"'bin/swift-object-updater'"
op|','
string|"'bin/swift-proxy-server'"
op|','
nl|'\n'
string|"'bin/swift-ring-builder'"
op|','
string|"'bin/swift-stats-populate'"
op|','
nl|'\n'
string|"'bin/swift-stats-report'"
op|','
nl|'\n'
string|"'bin/swift-bench'"
op|','
nl|'\n'
string|"'bin/swift-log-uploader'"
op|','
nl|'\n'
string|"'bin/swift-log-stats-collector'"
op|','
nl|'\n'
string|"'bin/swift-account-stats-logger'"
op|','
nl|'\n'
string|"'bin/swauth-add-account'"
op|','
string|"'bin/swauth-add-user'"
op|','
nl|'\n'
string|"'bin/swauth-delete-account'"
op|','
string|"'bin/swauth-delete-user'"
op|','
nl|'\n'
string|"'bin/swauth-list'"
op|','
string|"'bin/swauth-prep'"
op|','
string|"'bin/swauth-set-account-service'"
op|','
nl|'\n'
string|"'bin/swift-auth-to-swauth'"
op|','
nl|'\n'
op|']'
op|','
nl|'\n'
DECL|variable|entry_points
name|'entry_points'
op|'='
op|'{'
nl|'\n'
string|"'paste.app_factory'"
op|':'
op|'['
nl|'\n'
string|"'proxy=swift.proxy.server:app_factory'"
op|','
nl|'\n'
string|"'object=swift.obj.server:app_factory'"
op|','
nl|'\n'
string|"'container=swift.container.server:app_factory'"
op|','
nl|'\n'
string|"'account=swift.account.server:app_factory'"
op|','
nl|'\n'
string|"'auth=swift.auth.server:app_factory'"
op|','
nl|'\n'
op|']'
op|','
nl|'\n'
string|"'paste.filter_factory'"
op|':'
op|'['
nl|'\n'
string|"'auth=swift.common.middleware.auth:filter_factory'"
op|','
nl|'\n'
string|"'swauth=swift.common.middleware.swauth:filter_factory'"
op|','
nl|'\n'
string|"'healthcheck=swift.common.middleware.healthcheck:filter_factory'"
op|','
nl|'\n'
string|"'memcache=swift.common.middleware.memcache:filter_factory'"
op|','
nl|'\n'
string|"'ratelimit=swift.common.middleware.ratelimit:filter_factory'"
op|','
nl|'\n'
string|"'cname_lookup=swift.common.middleware.cname_lookup:filter_factory'"
op|','
nl|'\n'
string|"'catch_errors=swift.common.middleware.catch_errors:filter_factory'"
op|','
nl|'\n'
string|"'domain_remap=swift.common.middleware.domain_remap:filter_factory'"
op|','
nl|'\n'
op|']'
op|','
nl|'\n'
op|'}'
op|','
nl|'\n'
op|')'
newline|'\n'
endmarker|''
end_unit
