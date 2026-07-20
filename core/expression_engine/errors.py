class OELError(Exception): pass
class LexerError(OELError): pass
class ParseError(OELError): pass
class ResolveError(OELError): pass
class RuntimeError(OELError): pass
class PermissionError(OELError): pass
class SandboxError(OELError): pass