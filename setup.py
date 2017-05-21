from setuptools import setup

setup(
    name='fresh_tomatoes',
    packages=['fresh_tomatoes'],
    include_package_data=True,
    install_requires=[
        'flask~=0.12',
        'flask-bootstrap~=3.3.7',
        'flask-sqlalchemy~=2.2',
        'flask-wtf~=0.14.2',
        'pyyaml~=3.12',
        'requests~=2.12.4',
    ],
)
