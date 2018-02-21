from setuptools import setup

setup(
    name='polarityserv',
    version='0.1dev',
    packages=[
        'polarity_server',
        'polarity_server.app',
        'polarity_server.objects',
        'polarity_server.persistence',
        'polarity_server.rest',
        'polarity_server.shell_deployment',
        'polarity_server.tasks',
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
        'argparse',
        'flask',
        'flask-jsonpify',
        'flask-restful',
        'jsonpickle',
        'pexpect',
        'polarity',
    ],
    python_requires='~=3.6',
)
