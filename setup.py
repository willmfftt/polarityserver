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
        'argparse==1.4.0',
        'flask==0.12.2',
        'flask-jsonpify==1.5.0',
        'flask-restful==0.3.6',
        'jsonpickle==0.9.6',
        'pexpect==4.4.0',
        'polarity',
    ],
    python_requires='~=3.6',
)
