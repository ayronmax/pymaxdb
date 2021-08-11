from setuptools import setup, find_packages

with open(file='README.md',  mode='r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name = 'pymaxdb',
    version = '1.1.7',
    author = 'Alexinaldo Costa',
    author_email = 'ayronmax@gmail.com',
    packages = find_packages(),
    description = 'Projeto que visa padronizar a comunicação com alguns bancos de dados',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/ayronmax/pymaxdb',
    project_urls = {
        'Código fonte': 'https://github.com/ayronmax/pymaxdb',
        'Download': 'https://github.com/ayronmax/pymaxdb/archive/master.zip'
    },
    license = 'MIT',
    keywords = 'ODBC PostgreSQL DBMaker Firebird SQLServer',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Database'
    ],
    install_requires = [
        'psycopg2==2.8.4',
        'pyodbc==4.0.27',
        'fdb==2.0.1'
    ]    
)