from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as streamr:
    long_description = streamr.read()

setup(
    name='subdominator',
    version='2.1.0',
    author='D. Sanjai Kumar',
    author_email='bughunterz0047@gmail.com',
    description='Subdominator - An ultimate subdomain enumeration tool for Security Researchers and Bug Bounty Hunters',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RevoltSecurities/Subdominator",
    packages=find_packages(),
    install_requires=[
        'aiofiles>=24.1.0',
        'aiohttp>=3.10.11',
        'appdirs>=1.4.4',
        'art>=6.4',
        'beautifulsoup4>=4.13.3',
        'colorama>=0.4.6',
        'fake_useragent>=2.0.3',
        'httpx>=0.28.1',
        'Jinja2>=3.1.6',
        'prompt_toolkit>=3.0.50',
        'PyYAML>=6.0.2',
        'Requests>=2.32.3',
        'rich>=13.9.4',
        'setuptools>=75.6.0',
        'SQLAlchemy>=2.0.32',
        'tldextract>=5.1.2',
        'weasyprint>=65.0',
        'aiosqlite>=0.21.0',
    ],
    entry_points={
        'console_scripts': [
            'subdominator = subdominator.subdominator:main'
        ]
    },
)
