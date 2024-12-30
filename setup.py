from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as streamr:
    long_description = streamr.read()

setup(
    name='subdominator',
    version='2.0.0',
    author='D. Sanjai Kumar',
    author_email='bughunterz0047@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RevoltSecurities/Subdominator",
    description='Subdominator - An ultimate subdomain enumeration tool for Security Researchers and Bug Bounty Hunters',
    packages=find_packages(),
    install_requires=[
        'aiofiles>=23.2.1',
        'aiohttp>=3.9.4',
        'appdirs>=1.4.4',
        'art>=6.1',
        'httpx>=0.27.2',
        'fake_useragent>=1.5.0',
        'beautifulsoup4>=4.11.1',
        'PyYAML>=6.0.1',
        'Requests>=2.31.0',
        'rich>=13.7.1',
        'urllib3>=1.26.18',
        'tldextract>=5.1.2',
        'colorama>=0.4.6'
    ],
    entry_points={
        'console_scripts': [
            'subdominator = subdominator.subdominator:main'
        ]
    },
)
