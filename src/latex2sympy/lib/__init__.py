import platform

if platform.system() == 'Linux':  # pragma: no cover
    from latex2sympy.lib.linux.latex2antlrJson import parseToJson, LATEXLexerToken
elif platform.system() == 'Darwin':  # pragma: no cover
    if platform.machine() == 'arm64':  # pragma: no cover
        from latex2sympy.lib.macOS.arm64.latex2antlrJson import parseToJson, LATEXLexerToken
    else:
        from latex2sympy.lib.macOS.x86_64.latex2antlrJson import parseToJson, LATEXLexerToken
else:  # pragma: no cover
    raise Exception(platform.system() + ' platform not supported')
