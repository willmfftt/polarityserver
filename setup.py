from setuptools import setup

setup(
    name='polarityserv',
    version='0.1dev',
    packages=[
        'polarity_server',
    ],
    license='',
    author='William Moffitt',
    author_email='wmoffitt@cybrtalk.com',
    description='',
    entry_points={
        'console_scripts': [
            'polarityserv = polarity_server.__main__:main',
        ],
    },
    install_requires=[
    ],
    python_requires='~=3.6',
)
