from setuptools import setup

setup(
    name='matilda',
    version='2.0.0',
    packages=['matilda'],
    url='http://tools.wmflabs.org/matilda/',
    license='MIT License',
    author='Kunal Mehta',
    author_email='legoktm@gmail.com',
    description='Tool to allow mass-edits on Wikidata',
    install_requires=[
        'mwparserfromhell',
        'simplejson',
        'wdapi',
    ],
    test_suite='tests',
)
