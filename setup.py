from setuptools import setup

setup(
    name='polarityserv',
    version='0.1dev',
    packages=[
        'polarity_server',
        'polarity_server.shell_deployment',
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
        'pexpect',
    ],
    python_requires='~=3.6',
)
