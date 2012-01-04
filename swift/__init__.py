begin_unit
name|'import'
name|'gettext'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|class|Version
name|'class'
name|'Version'
op|'('
name|'object'
op|')'
op|':'
newline|'\n'
DECL|member|__init__
indent|'    '
name|'def'
name|'__init__'
op|'('
name|'self'
op|','
name|'canonical_version'
op|','
name|'final'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'self'
op|'.'
name|'canonical_version'
op|'='
name|'canonical_version'
newline|'\n'
name|'self'
op|'.'
name|'final'
op|'='
name|'final'
newline|'\n'
nl|'\n'
dedent|''
op|'@'
name|'property'
newline|'\n'
DECL|member|pretty_version
name|'def'
name|'pretty_version'
op|'('
name|'self'
op|')'
op|':'
newline|'\n'
indent|'        '
name|'if'
name|'self'
op|'.'
name|'final'
op|':'
newline|'\n'
indent|'            '
name|'return'
name|'self'
op|'.'
name|'canonical_version'
newline|'\n'
dedent|''
name|'else'
op|':'
newline|'\n'
indent|'            '
name|'return'
string|"'%s-dev'"
op|'%'
op|'('
name|'self'
op|'.'
name|'canonical_version'
op|','
op|')'
newline|'\n'
nl|'\n'
nl|'\n'
DECL|variable|_version
dedent|''
dedent|''
dedent|''
name|'_version'
op|'='
name|'Version'
op|'('
string|"'1.4.6'"
op|','
name|'False'
op|')'
newline|'\n'
DECL|variable|__version__
name|'__version__'
op|'='
name|'_version'
op|'.'
name|'pretty_version'
newline|'\n'
DECL|variable|__canonical_version__
name|'__canonical_version__'
op|'='
name|'_version'
op|'.'
name|'canonical_version'
newline|'\n'
nl|'\n'
name|'gettext'
op|'.'
name|'install'
op|'('
string|"'swift'"
op|')'
newline|'\n'
endmarker|''
end_unit
