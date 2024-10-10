def filters(results):
    filtered = []
    for subdomains in results:
        if subdomains is None:
            subdomains = []
        for subdomain in subdomains:
            if subdomain is not None:
                filtered.append(subdomain)
    return sorted(set(filtered))
