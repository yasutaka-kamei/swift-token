begin_unit
comment|'#!/usr/bin/python -u'
nl|'\n'
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
name|'import'
name|'unittest'
newline|'\n'
name|'from'
name|'os'
name|'import'
name|'kill'
newline|'\n'
name|'from'
name|'signal'
name|'import'
name|'SIGTERM'
newline|'\n'
name|'from'
name|'subprocess'
name|'import'
name|'call'
op|','
name|'Popen'
newline|'\n'
name|'from'
name|'time'
name|'import'
name|'sleep'
newline|'\n'
name|'from'
name|'uuid'
name|'import'
name|'uuid4'
newline|'\n'
nl|'\n'
name|'from'
name|'swift'
op|'.'
name|'common'
name|'import'
name|'client'
op|','
name|'direct_client'
newline|'\n'
nl|'\n'
name|'from'
name|'test'
op|'.'
name|'probe'
op|'.'
name|'common'
name|'import'
name|'kill_pids'
op|','
name|'reset_environment'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|TestObjectHandoff
name|'class'
name|'TestObjectHandoff'
op|'('
name|'unittest'
op|'.'
name|'TestCase'
op|')'
op|':'
newline|'\n'
nl|'\n'
DECL|member|setUp
indent|'    '
name|'def'
name|'setUp'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'pids'
op|','
name|'self'
op|'.'
name|'port2server'
op|','
name|'self'
op|'.'
name|'account_ring'
op|','
name|'self'
op|'.'
name|'container_ring'
op|','
name|'self'
op|'.'
name|'object_ring'
op|','
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
name|'account'
op|'='
name|'reset_environment'
op|'('
op|')'
newline|'\n'
nl|'\n'
DECL|member|tearDown
dedent|''
name|'def'
name|'tearDown'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'kill_pids'
op|'('
name|'self'
op|'.'
name|'pids'
op|')'
newline|'\n'
nl|'\n'
DECL|member|test_main
dedent|''
name|'def'
name|'test_main'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
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
op|')'
newline|'\n'
name|'apart'
op|','
name|'anodes'
op|'='
name|'self'
op|'.'
name|'account_ring'
op|'.'
name|'get_nodes'
op|'('
name|'self'
op|'.'
name|'account'
op|')'
newline|'\n'
nl|'\n'
name|'cpart'
op|','
name|'cnodes'
op|'='
name|'self'
op|'.'
name|'container_ring'
op|'.'
name|'get_nodes'
op|'('
name|'self'
op|'.'
name|'account'
op|','
name|'container'
op|')'
newline|'\n'
name|'cnode'
op|'='
name|'cnodes'
op|'['
number|'0'
op|']'
newline|'\n'
name|'obj'
op|'='
string|"'object-%s'"
op|'%'
name|'uuid4'
op|'('
op|')'
newline|'\n'
name|'opart'
op|','
name|'onodes'
op|'='
name|'self'
op|'.'
name|'object_ring'
op|'.'
name|'get_nodes'
op|'('
nl|'\n'
name|'self'
op|'.'
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
name|'onode'
op|'='
name|'onodes'
op|'['
number|'0'
op|']'
newline|'\n'
name|'kill'
op|'('
name|'self'
op|'.'
name|'pids'
op|'['
name|'self'
op|'.'
name|'port2server'
op|'['
name|'onode'
op|'['
string|"'port'"
op|']'
op|']'
op|']'
op|','
name|'SIGTERM'
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
name|'odata'
op|'='
name|'client'
op|'.'
name|'get_object'
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
op|')'
op|'['
op|'-'
number|'1'
op|']'
newline|'\n'
name|'if'
name|'odata'
op|'!='
string|"'VERIFY'"
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'Object GET did not return VERIFY, instead it '"
nl|'\n'
string|"'returned: %s'"
op|'%'
name|'repr'
op|'('
name|'odata'
op|')'
op|')'
newline|'\n'
comment|'# Kill all primaries to ensure GET handoff works'
nl|'\n'
dedent|''
name|'for'
name|'node'
name|'in'
name|'onodes'
op|'['
number|'1'
op|':'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'kill'
op|'('
name|'self'
op|'.'
name|'pids'
op|'['
name|'self'
op|'.'
name|'port2server'
op|'['
name|'node'
op|'['
string|"'port'"
op|']'
op|']'
op|']'
op|','
name|'SIGTERM'
op|')'
newline|'\n'
dedent|''
name|'odata'
op|'='
name|'client'
op|'.'
name|'get_object'
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
op|')'
op|'['
op|'-'
number|'1'
op|']'
newline|'\n'
name|'if'
name|'odata'
op|'!='
string|"'VERIFY'"
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'Object GET did not return VERIFY, instead it '"
nl|'\n'
string|"'returned: %s'"
op|'%'
name|'repr'
op|'('
name|'odata'
op|')'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'node'
name|'in'
name|'onodes'
op|'['
number|'1'
op|':'
op|']'
op|':'
newline|'\n'
indent|'            '
name|'self'
op|'.'
name|'pids'
op|'['
name|'self'
op|'.'
name|'port2server'
op|'['
name|'node'
op|'['
string|"'port'"
op|']'
op|']'
op|']'
op|'='
name|'Popen'
op|'('
op|'['
nl|'\n'
string|"'swift-object-server'"
op|','
nl|'\n'
string|"'/etc/swift/object-server/%d.conf'"
op|'%'
nl|'\n'
op|'('
op|'('
name|'node'
op|'['
string|"'port'"
op|']'
op|'-'
number|'6000'
op|')'
op|'/'
number|'10'
op|')'
op|']'
op|')'
op|'.'
name|'pid'
newline|'\n'
dedent|''
name|'sleep'
op|'('
number|'2'
op|')'
newline|'\n'
comment|"# We've indirectly verified the handoff node has the object, but let's"
nl|'\n'
comment|'# directly verify it.'
nl|'\n'
name|'another_onode'
op|'='
name|'self'
op|'.'
name|'object_ring'
op|'.'
name|'get_more_nodes'
op|'('
name|'opart'
op|')'
op|'.'
name|'next'
op|'('
op|')'
newline|'\n'
name|'odata'
op|'='
name|'direct_client'
op|'.'
name|'direct_get_object'
op|'('
name|'another_onode'
op|','
name|'opart'
op|','
nl|'\n'
name|'self'
op|'.'
name|'account'
op|','
name|'container'
op|','
name|'obj'
op|')'
op|'['
op|'-'
number|'1'
op|']'
newline|'\n'
name|'if'
name|'odata'
op|'!='
string|"'VERIFY'"
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'Direct object GET did not return VERIFY, instead '"
nl|'\n'
string|"'it returned: %s'"
op|'%'
name|'repr'
op|'('
name|'odata'
op|')'
op|')'
newline|'\n'
dedent|''
name|'objs'
op|'='
op|'['
name|'o'
op|'['
string|"'name'"
op|']'
name|'for'
name|'o'
name|'in'
nl|'\n'
name|'client'
op|'.'
name|'get_container'
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
op|')'
op|'['
number|'1'
op|']'
op|']'
newline|'\n'
name|'if'
name|'obj'
name|'not'
name|'in'
name|'objs'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'Container listing did not know about object'"
op|')'
newline|'\n'
dedent|''
name|'for'
name|'cnode'
name|'in'
name|'cnodes'
op|':'
newline|'\n'
indent|'            '
name|'objs'
op|'='
op|'['
name|'o'
op|'['
string|"'name'"
op|']'
name|'for'
name|'o'
name|'in'
nl|'\n'
name|'direct_client'
op|'.'
name|'direct_get_container'
op|'('
name|'cnode'
op|','
name|'cpart'
op|','
nl|'\n'
name|'self'
op|'.'
name|'account'
op|','
name|'container'
op|')'
op|'['
number|'1'
op|']'
op|']'
newline|'\n'
name|'if'
name|'obj'
name|'not'
name|'in'
name|'objs'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'Exception'
op|'('
nl|'\n'
string|"'Container server %s:%s did not know about object'"
op|'%'
nl|'\n'
op|'('
name|'cnode'
op|'['
string|"'ip'"
op|']'
op|','
name|'cnode'
op|'['
string|"'port'"
op|']'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'pids'
op|'['
name|'self'
op|'.'
name|'port2server'
op|'['
name|'onode'
op|'['
string|"'port'"
op|']'
op|']'
op|']'
op|'='
name|'Popen'
op|'('
op|'['
nl|'\n'
string|"'swift-object-server'"
op|','
nl|'\n'
string|"'/etc/swift/object-server/%d.conf'"
op|'%'
nl|'\n'
op|'('
op|'('
name|'onode'
op|'['
string|"'port'"
op|']'
op|'-'
number|'6000'
op|')'
op|'/'
number|'10'
op|')'
op|']'
op|')'
op|'.'
name|'pid'
newline|'\n'
name|'sleep'
op|'('
number|'2'
op|')'
newline|'\n'
name|'exc'
op|'='
name|'False'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'direct_client'
op|'.'
name|'direct_get_object'
op|'('
name|'onode'
op|','
name|'opart'
op|','
name|'self'
op|'.'
name|'account'
op|','
nl|'\n'
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'exc'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'exc'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'Previously downed object server had test object'"
op|')'
newline|'\n'
comment|"# Run the extra server last so it'll remove its extra partition"
nl|'\n'
dedent|''
name|'ps'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'n'
name|'in'
name|'onodes'
op|':'
newline|'\n'
indent|'            '
name|'ps'
op|'.'
name|'append'
op|'('
name|'Popen'
op|'('
op|'['
string|"'swift-object-replicator'"
op|','
nl|'\n'
string|"'/etc/swift/object-server/%d.conf'"
op|'%'
nl|'\n'
op|'('
op|'('
name|'n'
op|'['
string|"'port'"
op|']'
op|'-'
number|'6000'
op|')'
op|'/'
number|'10'
op|')'
op|','
string|"'once'"
op|']'
op|')'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'p'
name|'in'
name|'ps'
op|':'
newline|'\n'
indent|'            '
name|'p'
op|'.'
name|'wait'
op|'('
op|')'
newline|'\n'
dedent|''
name|'call'
op|'('
op|'['
string|"'swift-object-replicator'"
op|','
nl|'\n'
string|"'/etc/swift/object-server/%d.conf'"
op|'%'
nl|'\n'
op|'('
op|'('
name|'another_onode'
op|'['
string|"'port'"
op|']'
op|'-'
number|'6000'
op|')'
op|'/'
number|'10'
op|')'
op|','
string|"'once'"
op|']'
op|')'
newline|'\n'
name|'odata'
op|'='
name|'direct_client'
op|'.'
name|'direct_get_object'
op|'('
name|'onode'
op|','
name|'opart'
op|','
name|'self'
op|'.'
name|'account'
op|','
nl|'\n'
name|'container'
op|','
name|'obj'
op|')'
op|'['
op|'-'
number|'1'
op|']'
newline|'\n'
name|'if'
name|'odata'
op|'!='
string|"'VERIFY'"
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'Direct object GET did not return VERIFY, instead '"
nl|'\n'
string|"'it returned: %s'"
op|'%'
name|'repr'
op|'('
name|'odata'
op|')'
op|')'
newline|'\n'
dedent|''
name|'exc'
op|'='
name|'False'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'direct_client'
op|'.'
name|'direct_get_object'
op|'('
name|'another_onode'
op|','
name|'opart'
op|','
name|'self'
op|'.'
name|'account'
op|','
nl|'\n'
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'exc'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'exc'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'Handoff object server still had test object'"
op|')'
newline|'\n'
nl|'\n'
comment|'# Because POST has changed to a COPY by default, POSTs will succeed on all up'
nl|'\n'
comment|'# nodes now if at least one up node has the object.'
nl|'\n'
comment|"#       kill(self.pids[self.port2server[onode['port']]], SIGTERM)"
nl|'\n'
comment|'#       client.post_object(self.url, self.token, container, obj,'
nl|'\n'
comment|"#                          headers={'x-object-meta-probe': 'value'})"
nl|'\n'
comment|'#       oheaders = client.head_object(self.url, self.token, container, obj)'
nl|'\n'
comment|"#       if oheaders.get('x-object-meta-probe') != 'value':"
nl|'\n'
comment|"#           raise Exception('Metadata incorrect, was %s' % repr(oheaders))"
nl|'\n'
comment|'#       exc = False'
nl|'\n'
comment|'#       try:'
nl|'\n'
comment|'#           direct_client.direct_get_object(another_onode, opart, self.account,'
nl|'\n'
comment|'#                                           container, obj)'
nl|'\n'
comment|'#       except Exception:'
nl|'\n'
comment|'#           exc = True'
nl|'\n'
comment|'#       if not exc:'
nl|'\n'
comment|"#           raise Exception('Handoff server claimed it had the object when '"
nl|'\n'
comment|"#                           'it should not have it')"
nl|'\n'
comment|"#       self.pids[self.port2server[onode['port']]] = Popen(["
nl|'\n'
comment|"#           'swift-object-server',"
nl|'\n'
comment|"#           '/etc/swift/object-server/%d.conf' %"
nl|'\n'
comment|"#           ((onode['port'] - 6000) / 10)]).pid"
nl|'\n'
comment|'#       sleep(2)'
nl|'\n'
comment|'#       oheaders = direct_client.direct_get_object(onode, opart, self.account,'
nl|'\n'
comment|'#                                                   container, obj)[0]'
nl|'\n'
comment|"#       if oheaders.get('x-object-meta-probe') == 'value':"
nl|'\n'
comment|"#           raise Exception('Previously downed object server had the new '"
nl|'\n'
comment|"#                           'metadata when it should not have it')"
nl|'\n'
comment|"#       # Run the extra server last so it'll remove its extra partition"
nl|'\n'
comment|'#       ps = []'
nl|'\n'
comment|'#       for n in onodes:'
nl|'\n'
comment|"#           ps.append(Popen(['swift-object-replicator',"
nl|'\n'
comment|"#                            '/etc/swift/object-server/%d.conf' %"
nl|'\n'
comment|"#                            ((n['port'] - 6000) / 10), 'once']))"
nl|'\n'
comment|'#       for p in ps:'
nl|'\n'
comment|'#           p.wait()'
nl|'\n'
comment|"#       call(['swift-object-replicator',"
nl|'\n'
comment|"#             '/etc/swift/object-server/%d.conf' %"
nl|'\n'
comment|"#             ((another_onode['port'] - 6000) / 10), 'once'])"
nl|'\n'
comment|'#       oheaders = direct_client.direct_get_object(onode, opart, self.account,'
nl|'\n'
comment|'#                                                   container, obj)[0]'
nl|'\n'
comment|"#       if oheaders.get('x-object-meta-probe') != 'value':"
nl|'\n'
comment|'#           raise Exception('
nl|'\n'
comment|"#               'Previously downed object server did not have the new metadata')"
nl|'\n'
nl|'\n'
dedent|''
name|'kill'
op|'('
name|'self'
op|'.'
name|'pids'
op|'['
name|'self'
op|'.'
name|'port2server'
op|'['
name|'onode'
op|'['
string|"'port'"
op|']'
op|']'
op|']'
op|','
name|'SIGTERM'
op|')'
newline|'\n'
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
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
name|'exc'
op|'='
name|'False'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'client'
op|'.'
name|'head_object'
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
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'exc'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'exc'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'Regular object HEAD was still successful'"
op|')'
newline|'\n'
dedent|''
name|'objs'
op|'='
op|'['
name|'o'
op|'['
string|"'name'"
op|']'
name|'for'
name|'o'
name|'in'
nl|'\n'
name|'client'
op|'.'
name|'get_container'
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
op|')'
op|'['
number|'1'
op|']'
op|']'
newline|'\n'
name|'if'
name|'obj'
name|'in'
name|'objs'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'Container listing still knew about object'"
op|')'
newline|'\n'
dedent|''
name|'for'
name|'cnode'
name|'in'
name|'cnodes'
op|':'
newline|'\n'
indent|'            '
name|'objs'
op|'='
op|'['
name|'o'
op|'['
string|"'name'"
op|']'
name|'for'
name|'o'
name|'in'
nl|'\n'
name|'direct_client'
op|'.'
name|'direct_get_container'
op|'('
nl|'\n'
name|'cnode'
op|','
name|'cpart'
op|','
name|'self'
op|'.'
name|'account'
op|','
name|'container'
op|')'
op|'['
number|'1'
op|']'
op|']'
newline|'\n'
name|'if'
name|'obj'
name|'in'
name|'objs'
op|':'
newline|'\n'
indent|'                '
name|'raise'
name|'Exception'
op|'('
nl|'\n'
string|"'Container server %s:%s still knew about object'"
op|'%'
nl|'\n'
op|'('
name|'cnode'
op|'['
string|"'ip'"
op|']'
op|','
name|'cnode'
op|'['
string|"'port'"
op|']'
op|')'
op|')'
newline|'\n'
dedent|''
dedent|''
name|'self'
op|'.'
name|'pids'
op|'['
name|'self'
op|'.'
name|'port2server'
op|'['
name|'onode'
op|'['
string|"'port'"
op|']'
op|']'
op|']'
op|'='
name|'Popen'
op|'('
op|'['
nl|'\n'
string|"'swift-object-server'"
op|','
nl|'\n'
string|"'/etc/swift/object-server/%d.conf'"
op|'%'
nl|'\n'
op|'('
op|'('
name|'onode'
op|'['
string|"'port'"
op|']'
op|'-'
number|'6000'
op|')'
op|'/'
number|'10'
op|')'
op|']'
op|')'
op|'.'
name|'pid'
newline|'\n'
name|'sleep'
op|'('
number|'2'
op|')'
newline|'\n'
name|'direct_client'
op|'.'
name|'direct_get_object'
op|'('
name|'onode'
op|','
name|'opart'
op|','
name|'self'
op|'.'
name|'account'
op|','
name|'container'
op|','
nl|'\n'
name|'obj'
op|')'
newline|'\n'
comment|"# Run the extra server last so it'll remove its extra partition"
nl|'\n'
name|'ps'
op|'='
op|'['
op|']'
newline|'\n'
name|'for'
name|'n'
name|'in'
name|'onodes'
op|':'
newline|'\n'
indent|'            '
name|'ps'
op|'.'
name|'append'
op|'('
name|'Popen'
op|'('
op|'['
string|"'swift-object-replicator'"
op|','
nl|'\n'
string|"'/etc/swift/object-server/%d.conf'"
op|'%'
nl|'\n'
op|'('
op|'('
name|'n'
op|'['
string|"'port'"
op|']'
op|'-'
number|'6000'
op|')'
op|'/'
number|'10'
op|')'
op|','
string|"'once'"
op|']'
op|')'
op|')'
newline|'\n'
dedent|''
name|'for'
name|'p'
name|'in'
name|'ps'
op|':'
newline|'\n'
indent|'            '
name|'p'
op|'.'
name|'wait'
op|'('
op|')'
newline|'\n'
dedent|''
name|'call'
op|'('
op|'['
string|"'swift-object-replicator'"
op|','
nl|'\n'
string|"'/etc/swift/object-server/%d.conf'"
op|'%'
nl|'\n'
op|'('
op|'('
name|'another_onode'
op|'['
string|"'port'"
op|']'
op|'-'
number|'6000'
op|')'
op|'/'
number|'10'
op|')'
op|','
string|"'once'"
op|']'
op|')'
newline|'\n'
name|'exc'
op|'='
name|'False'
newline|'\n'
name|'try'
op|':'
newline|'\n'
indent|'            '
name|'direct_client'
op|'.'
name|'direct_get_object'
op|'('
name|'another_onode'
op|','
name|'opart'
op|','
name|'self'
op|'.'
name|'account'
op|','
nl|'\n'
name|'container'
op|','
name|'obj'
op|')'
newline|'\n'
dedent|''
name|'except'
name|'Exception'
op|':'
newline|'\n'
indent|'            '
name|'exc'
op|'='
name|'True'
newline|'\n'
dedent|''
name|'if'
name|'not'
name|'exc'
op|':'
newline|'\n'
indent|'            '
name|'raise'
name|'Exception'
op|'('
string|"'Handoff object server still had the object'"
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
name|'unittest'
op|'.'
name|'main'
op|'('
op|')'
newline|'\n'
dedent|''
endmarker|''
end_unit
