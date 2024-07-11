from .check_redirect import is_vulnerable

def check_open_redirect(url, payloads=None):
    default_url = [
        "http://evil.com",
        "https://malicious-site.com",
        "https://www.whitelisteddomain.tld@google.com",
        "https://localdomain.pw"
    ]
    
    if payloads is None:
        payloads = []

    all_payloads = default_url + payloads
    
    vulnerable_payloads = []
    for payload in all_payloads:
        print(f"Testing payload: {payload}")
        if is_vulnerable(url, payload):
            vulnerable_payloads.append(payload)
    
    return vulnerable_payloads
