# -*- coding: utf-8 -*-
"""Load the canonical ``sanskrit-util`` package with a legacy sibling fallback.

The compatibility module intentionally has a different name from the installed
package.  That avoids the old ``sanskrit_util.py`` shim shadowing a real package
on ``sys.path``.
"""
import importlib.util as _ilu
import os as _os

try:
    import sanskrit_util as _mod
except ImportError as _installed_error:
    _here = _os.path.dirname(_os.path.abspath(__file__))
    _pkg_init = _os.path.abspath(_os.path.join(
        _here, '..', '..', 'sanskrit-util', 'py', 'sanskrit_util', '__init__.py'))
    if not _os.path.isfile(_pkg_init):
        raise ImportError(
            "Install sanskrit-util from requirements.txt, or restore the legacy sibling "
            "checkout at %s" % _pkg_init) from _installed_error
    _spec = _ilu.spec_from_file_location('_sanskrit_util_sibling', _pkg_init)
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)

globals().update({_name: getattr(_mod, _name) for _name in _mod.__all__})
__all__ = list(_mod.__all__)
__version__ = getattr(_mod, '__version__', None)
