def filters(results):
    filtered = []
    for subdomains in results:
        if subdomains is None:
            continue
        for subdomain in subdomains:
            filtered.append(subdomain)
    return sorted(set(filtered))
