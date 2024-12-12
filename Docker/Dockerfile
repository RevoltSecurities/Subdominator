FROM python:3.11-slim
WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y git
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir tldextract aiofiles>=23.2.1 aiohttp>=3.9.4 appdirs>=1.4.4 httpx>=0.27.2 art>=6.1 beautifulsoup4>=4.11.1 colorama>=0.4.6 fake_useragent>=1.5.0 PyYAML>=6.0.1 Requests>=2.31.0 rich>=13.7.1 urllib3>=1.26.18
RUN pip install git+https://github.com/RevoltSecurities/Subdominator

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["subdominator"]