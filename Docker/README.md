# Subdominator - Docker Usage
This guide provides instructions for using **Subdominator v3.0.0** inside a Docker container for high-performance subdomain enumeration.

## 🚀 Installation
To build the Docker image, run the following command from the **project root**:

```bash
docker build -t subdominator -f Docker/Dockerfile .
```

## 🛠 Docker Commands

### 1. **Basic Enumeration**
Scan a **single domain** and save the output to your local machine:

```bash
docker run --rm -it -v $(pwd):/output subdominator -d example.com -o /output/results.txt
```

### 2. **Deep Recon (Recursive)**
Perform a recursive scan with a depth of 2 and generate an HTML report:

```bash
docker run --rm -it -v $(pwd):/output subdominator -d example.com -rd 2 -oh /output/report.html
```

### 3. **Bulk Enumeration**
If you have a list of domains in `input.txt`, mount the file and an output directory:

```bash
docker run --rm -v $(pwd)/input.txt:/input.txt -v $(pwd)/results:/results subdominator -dL /input.txt -oD /results
```

### 4. **Using Custom Configuration**
To use your local API keys and configuration, mount your config directory:

```bash
docker run --rm -v ~/.config/Subdominator:/config subdominator -cp /config/provider-config.yaml -d example.com
```

## 💡 Key Flags for Docker
- **`-d`**: Target domain.
- **`-rd`**: Recursion depth.
- **`-oh`**: Generate a high-quality HTML report.
- **`-j`**: Output JSONL stream to stdout.
- **`-o`**: Save findings to a specific file.
- **`-sd`**: Persist findings to the container's database (or mount one using `-v`).

## 📝 Notes
- Always use absolute paths or `$(pwd)` when mounting volumes for input/output files.
- Ensure your output paths within the command (e.g., `-o /output/file.txt`) match the container's mount point.
