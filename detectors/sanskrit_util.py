# -*- coding: utf-8 -*-
"""Compatibility shim — the canonical SLP1/IAST/Devanāgarī transliteration lives in the
shared `sanskrit-util` package, so this repo does not carry its own copy.

Re-exports the sibling package (GitHub/sanskrit-util) by relative path, so
`from sanskrit_util import to_slp1, deva_to_iast, ...` works unchanged. Implementation,
tests and golden vectors live in ../../sanskrit-util/.

If you relocate this repo away from the GitHub-root layout, install the package instead
and delete this shim:  pip install -e <path>/sanskrit-util/py
"""
import importlib.util as _ilu
import os as _os

_here = _os.path.dirname(_os.path.abspath(__file__))
_pkg_init = _os.path.abspath(_os.path.join(_here, '..', '..', 'sanskrit-util', 'py', 'sanskrit_util', '__init__.py'))

if not _os.path.exists(_pkg_init):
    raise ImportError(
        "shared 'sanskrit-util' package not found at %s — restore the sibling repo or run "
        "`pip install -e <path>/sanskrit-util/py` (then you can delete this shim)." % _pkg_init
    )

_spec = _ilu.spec_from_file_location('_sanskrit_util_shared', _pkg_init)
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

globals().update({_k: getattr(_mod, _k) for _k in _mod.__all__})
__all__ = list(_mod.__all__)
__version__ = getattr(_mod, '__version__', None)
