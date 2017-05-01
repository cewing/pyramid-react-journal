import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'alembic',
    'pygments',
    'pyramid',
    'pyramid_exclog',
    'pyramid_jinja2',
    'ipython',
    'pyramid_ipython',
    'paginate_sqlalchemy',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'wtforms',
    'velruse',
    'markdown',
    'psycopg2'
]

setup(name='learning-journal',
      version='0.1',
      description='A Group Learning Journal built with Pyramid and React.js',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Cris Ewing, Nicholas Hunt-Walker',
      author_email='cris@crisewing.com, nhuntwalker@gmail.com',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='learning_journal',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = learning_journal:main
      [console_scripts]
      initialize_db = learning_journal.scripts.initializedb:main
      """,
      )
