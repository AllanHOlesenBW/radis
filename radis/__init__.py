# -*- coding: utf-8 -*-
"""

Summary
-------

RADIS

A code to simulate infrared spectra of molecules::

                *(((((((
                 ((((((((((((              ,(((((
                 ((((((((((((((((/   *((((((((((*
                  ((((((((((((((((( ((((((((((((
                      (((((((( (((((((((((((
                         *
                       @@  *@@       ..  /@@
                  @@&  @@  *@@       @@  /@@  @@%
              @@  @@&  @@  *@@  @@&  @@  /@@  @@%  @@
              @@  @@&  @@  *@@  @@&  @@  /@@  @@%  @@
              @@  @@&  @@  *@@  @@&  @@  /@@  @@%  @@  (@
         ,@   @@  @@&  @@  *@@  @@&  @@  /@@  @@%  @@
         @@   @@  @@&  @@  ,.
                                    ,%&&&&&&&&&&&&&&&&&&&
          &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
           &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
             &&&&&&&&&&&&&&&&@@@@@@&@@@&&&@@@&&&&&&&&
               &&&&&&&&&&&&&&&@@@@@@&&&&&&&&&&&&&&&
                 &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
                   &&&&&&&&&&&&&&&&&&&&&&&&&&&.
                       &&&&&&&&&&&&&&&&&&&
                               .**.
                                &&&,
                                 &&

See Source code [1]_, Documentation [2]_, Package [3]_

Notes
-----

RADIS is nonequilibrium emission and absorption line-by-line code, for use by
infrared spectroscopic that want to compare line databases, or experimentalist
that want to fit their experimental line-of-sight spectra.

Written as a general purpose radiative solver, the code is built around the HITRAN,
HITEMP and CDSD databases for molecules in their electronic ground state. Energy
levels are read from tabulated databases or calculated from Dunham developments.
Boltzmann, Treanor, and state specific vibrational distributions can be
generated. A modular architecture makes it possible to add new species without
modifications to the core code. Thus far, CO2, CO are featured for non-equilibrium
calculations, and all species present in the HITRAN database are featured for
equilibrium calculations. To fit experimental spectra, RADIS includes a line
survey tool, an interface with a look-up database to improve fitting convergence
times, and a multi-slab module with a radiative transfer equation solver to
reproduce line-of-sight experiments. Validation cases against existing spectral
codes and experimental results from various plasma sources are presented.

The code will soon be available under under GNU General Public
License v3.0

References
----------

.. [1] Source code: `GitHub repository <https://github.com/radis/radis>`__

.. [2] Online Documentation: `Readthedocs.io <https://radis.readthedocs.io/en/latest/?badge=latest>`__

.. [3] Install as a package: `PyPi project <https://pypi.python.org/pypi/radis>`__

"""

import os

from .misc.config import get_config
from .misc.utils import Chdir as _chdir
from .misc.utils import getProjectRoot

# %% Config files

# @dev: refactor in progress.
# So far there are config files in ~/radis.json (for databanks), global variables
# here, and a radis/config.json file.
# Everything should be merged in a user JSON file ~/radis.json (json) overriding
# the default one.

config = get_config()
"""dict: RADIS configuration parameters

Notes
-----

refactor in progress.
So far there are config files in ~/radis.json (for databanks), global variables
here, and a radis/config.json file.
Everything should be merged in a user JSON file ~/radis.json (json) overriding
the default one.
"""


# %% Global constants
from .params import (
    AUTO_UPDATE_DATABASE,
    AUTO_UPDATE_SPEC,
    DEBUG_MODE,
    GRIDPOINTS_PER_LINEWIDTH_ERROR_THRESHOLD,
    GRIDPOINTS_PER_LINEWIDTH_WARN_THRESHOLD,
    OLDEST_COMPATIBLE_VERSION,
    USE_CYTHON,
)

# %% Version


def get_version(verbose=False, add_git_number=True):
    """Reads `__version.txt__
    <https://github.com/radis/radis/blob/master/radis/__version__.txt>`__ and
    retrieve version number. If ``add_git_number``, also appends Git commit
    number if we're on a gitted session.

    Examples
    --------

    ::

        import radis
        print(radis.get_version())
        >>> '0.9.17'
    """

    # First get version
    with open(os.path.join(getProjectRoot(), "__version__.txt")) as version_file:
        version = version_file.read().strip()

    # Now get git info
    if add_git_number:
        import subprocess
        import sys

        cd = _chdir(os.path.dirname(__file__))
        try:
            label = subprocess.check_output("git describe", stderr=subprocess.DEVNULL)
        except:
            if verbose:
                print("couldnt get git version: {0}".format(sys.exc_info()[1]))
            # probably not a git session. drop
        else:
            commit = label.decode().strip().split("-")[-1]
            version = version + "-" + commit
        finally:
            cd.__del__()

    return version


__version__ = get_version(add_git_number=False)


from .db import *  # database of molecules
from .io import *  # input / output
from .lbl import *  # line-by-line module
from .levels import *  # rovibrational energies and partition functions
from .los import *  # line-of-sight module
from .phys import *  # conversion functions, blackbody objects
from .spectrum import *  # Spectrum object
from .test import *  # test
from .tools import *  # slit, database, line survey, etc.
