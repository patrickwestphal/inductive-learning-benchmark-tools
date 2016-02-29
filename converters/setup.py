try:
    from setuptools import setup
except ImportError:
    from distutils import setup

config = {
    'description': 'Collection of scripts for converting datasets to RDF',
    'author': 'Patrick Westphal',
    'url':
        'https://github.com/patrickwestphal/inductive-learning-benchmark-tools',
    'download_url':
        'https://github.com/patrickwestphal/inductive-learning-benchmark-tools',
    'author_email': 'patrick.westphal@informatik.uni-leipzig.de',
    'version': '0.0.1',
    'tests_require': [
    ],
    'install_requires': [
        'pyparsing==2.0.3',
        'rdflib==4.2.1'
    ],
    'packages': ['datasets', 'predicates_file', 'prolog', 'sdf', 'utils'],
    'scripts': [
        'bin/alzheimer2rdf',
        'bin/germancreditdata2prolog',
        'bin/germancreditdata2rdf',
        'bin/glassidentification2prolog',
        'bin/glassidentification2rdf',
        'bin/iris2prolog',
        'bin/iris2rdf',
        'bin/predfile2prolog',
        'bin/predfile2rdf',
        'bin/sdf2prolog',
        'bin/sdf2rdf',
        'bin/wine2prolog',
        'bin/wine2rdf'
    ],
    'name': 'conversion-scripts'
}

setup(**config)
