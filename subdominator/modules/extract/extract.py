def filters(results):
    filtered = []
    for result in results:
        source = result["source"]
        subdomains = result["subdomains"]
        if subdomains is not None and subdomains != []:
            filtered.append({
                "source": source,
                "subdomains": [s for s in subdomains if s is not None]
            })
    return filtered
