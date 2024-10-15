import platform

if platform.system() == "Linux":  # pragma: no cover
    from latex2sympy.lib.linux.latex2antlrJson import LATEXLexerToken, parseToJson
elif platform.system() == "Darwin":  # pragma: no cover
    from latex2sympy.lib.macOS.latex2antlrJson import (  # noqa: F401
        LATEXLexerToken,
        parseToJson,
    )
else:  # pragma: no cover
    raise Exception(platform.system() + " platform not supported")
