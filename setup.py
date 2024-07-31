from setuptools import setup, find_packages
import platform

install_requires = [
    'flask',
    'flask_sqlalchemy',
    'flask_login',
    'flasgger',
    'gunicorn'
    'psycopg2-binary'
    # Add other common dependencies here
]

if platform.system() == 'Windows':
    install_requires.append('pywin32==306')

setup(
    name='flask_app',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
)
