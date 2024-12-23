# Subdominator - Docker Usage
This README provides instructions for using the **Subdominator** tool inside a Docker container for subdomain enumeration.

## Installation
To build the Docker image, run the following command:

```bash
sudo docker build -t subdominator .
```
This will create the `subdominator` image using the `Dockerfile` in the current directory.

## Docker Commands

### 1. **Subdomain Enumeration for a Single Domain**
To perform subdomain enumeration for a **single domain** and save the output to a file, use:

```bash
sudo docker run --rm -it -v $(pwd):/output subdominator -d redacted.com --output /output/outfile.txt
```

Explanation:
- **`-d redacted.com`**: Specifies the domain for subdomain enumeration.
- **`--output /output/outfile.txt`**: Saves the output to a file. The `$(pwd)` mounts the current working directory to `/output` inside the container.

### 2. **Subdomain Enumeration for a List of Domains**

If you have a **list of root domains** in a file (e.g., `input.txt`) and want to enumerate subdomains for all domains, use the following command:

```bash
sudo docker run --rm -v /home/pugal/tools/Subdominator/input.txt:/input.txt -v /home/pugal/tools/Subdominator/output-directory:/output-directory subdominator -dL /input.txt -oD /output-directory
```

Explanation:
- **`-dL /input.txt`**: Specifies the file containing the list of domains.
- **`-oD /output-directory`**: Specifies the directory to save the output. The directory is mounted from your local machine to the Docker container.

### 3. **Subdomain Enumeration with Output in JSON Format**

If you want to save the output in **JSON format**, use the `-oJ` flag:

```bash
sudo docker run --rm -it -v $(pwd):/output subdominator -d thx.com -oJ /output/outfile.json
```

Explanation:
- **`-d thx.com`**: Specifies the domain for subdomain enumeration.
- **`-oJ /output/outfile.json`**: Saves the output in JSON format.

## Example with Custom Configuration

If you want to specify a custom configuration file for API keys, you can mount the configuration file into the container:

```bash
sudo docker run --rm -v /path/to/config:/custom-config subdominator -cp /custom-config/config.yaml -d example.com --output /output/outfile.txt
```

### Explanation:
- **`-cp /custom-config/config.yaml`**: Specifies the custom path for the configuration file.

## Notes
- Replace `/path/to/config` and `/home/pugal/tools/Subdominator/` with the actual paths on your system.
- Ensure the output directory (`/output` or `/output-directory`) exists on your local machine or Docker will create it inside the container.