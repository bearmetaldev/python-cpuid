.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/python-cpuid.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/python-cpuid
    .. image:: https://readthedocs.org/projects/python-cpuid/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://python-cpuid.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/python-cpuid/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/python-cpuid
    .. image:: https://img.shields.io/pypi/v/python-cpuid.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/python-cpuid/
    .. image:: https://img.shields.io/conda/vn/conda-forge/python-cpuid.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/python-cpuid
    .. image:: https://pepy.tech/badge/python-cpuid/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/python-cpuid
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/python-cpuid

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

============
python-cpuid
============


    Call cpuid from Python code.


This module provides C bindings to call the `cpuid` instruction from Python code.
Simply pass a MSR ID and the `cpuid` function will return the result as a tuple representing
the eax, ebx, ecx and edx registers as integers.

.. code-block::

    from cpuid import cpuid

    msr = 0x80000000    # example value
    eax, ebx, ecx, edx = cpuid(msr)

CPU features
============

In addition to the raw `cpuid` functionality, this library provides helpers for commonly used
CPUID registers.

.. _pyscaffold-notes:

.. code-block::

    from cpuid.features import prcessor_features, secure_encryption_info, vendor

    vendor()   # returns the result of cpuid(0) as bytes, ex: b"GenuineIntel"
    features = processor_features()    # A class with all the fields of cpuid(1)
    secure_encryption_features = secure_encryption_info()   # AMD secure encryption features

Feel free to add more CPUID registers! You can find the specification in official Intel
and AMD docs like this one: https://www.amd.com/system/files/TechDocs/24594.pdf.

Why?
====

Other projects already provide this functionality. To the best of our knowledge:

* `PyCPUID <https://github.com/ngnpope/pycpuid>_` is not compatible with Python 3.
  An `open PR <https://github.com/ngnpope/pycpuid/pull/4>`_ from 2015 proposes an upgrade.
* `cpuid.py <https://github.com/flababah/cpuid.py>`_ looks fun, but ultimately is machine
  code injection. We wanted something more auditable.

Notes
=====

We do not (yet) provide binary wheel distributions for this package, because of the added
complexity of shipping compiled libraries for Linux. You will require GCC to compile
the package for your system.

This project has been set up using PyScaffold 4.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
