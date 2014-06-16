import re

try:
    import setuptools
except ImportError:
    import distutils.core
    setup = distutils.core.setup
else:
    setup = setuptools.setup


setup(
    name='coblr',
    version=(re
             .compile(r".*__version__ = '(.*?)'", re.S)
             .match(open('coblr.py').read())
             .group(1)),
    url='https://github.com/cieplak/coblr/',
    author='coblr',
    author_email='coblr@example.com',
    description='Cobbles together a db from spreadsheets',
    py_modules=['coblr'],
    package_data={'': ['LICENSE']},
    include_package_data=True,
    tests_require=[
        'nose==1.3.3',
    ],
    install_requires=[
        'click==2.1',
        'wsgiref==0.1.2',
        'SQLAlchemy==0.9.4',
        'psycopg2==2.5.3',
    ],
    test_suite='tests',
)
