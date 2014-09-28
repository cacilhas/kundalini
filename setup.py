from distutils.core import setup
from os import path

readme = path.join(path.dirname(__file__), 'README.md')
if path.exists(readme):
    with open(readme) as fd:
        long_description = fd.read()

else:
    long_description = None


setup(
    name             = 'kundalini',
    version          = '0.1',
    license          = 'BSD 3-Clausule License',
    platforms        = 'any',
    url              = 'https://bitbucket.org/cacilhas/kundalini',
    download_url     = 'https://bitbucket.org/cacilhas/kundalini/branch/master',
    py_modules       = ['kundalini'],
    author           = 'Rodrigo Arĥimedeς ℳontegasppa ℭacilhας',
    author_email     = 'batalema@cacilhas.info',
    description      = 'LÖVE-like PyGame API',
    long_description = long_description,
    install_requires = ['pygame>=1.9.1'],
    classifiers      = [
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
