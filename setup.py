from setuptools import setup, find_packages

setup(
    name='subdominator',
    version='1.0.5',
    author='D. Sanjai Kumar',
    author_email='bughunterz0047@gmail.com',
    description='Subdominator - An ultimate subdomain enumeration tool',
    packages=find_packages(),
    install_requires=[
        'censys==2.2.9',
        'colorama==0.4.6',
        'httpx==0.25.2',
        'plyer==2.1.0',
        'pywebio==1.8.2',
        'requests==2.31.0',
        'argparse==1.4.0'
    ],
    entry_points={
        'console_scripts': [
            'subdominator = subdominator.subdominator:main'
        ]
    },
)

