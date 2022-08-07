"""
    Setup file for python-cpuid.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.3.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
from setuptools import Extension, setup

if __name__ == "__main__":

    cpuid_module = Extension(
        "cpuid.bindings",
        sources=["src/cpuid/cpuid_bindings.c"],
    )
    try:
        setup(
            use_scm_version={"version_scheme": "no-guess-dev"},
            ext_modules=[cpuid_module],
        )
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
