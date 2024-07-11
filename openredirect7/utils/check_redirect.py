import requests
from urllib.parse import urlparse, urljoin
from colorama import init, Fore, Style
from includes.credential import send_whatsapp_message

# Initialize colorama
init()

def is_vulnerable(url, redirection_url):
    parsed_url = urlparse(url)
    additional_params = ['redirect', 'next', 'r', 'dest', 'destination']

    for param in additional_params:
        full_url = urljoin(url, f"{parsed_url.path}{param}?url={redirection_url}")
        print(f"Checking URL: {full_url}")

        try:
            response = requests.get(full_url, allow_redirects=False)
            
            if response.status_code >= 300:
                if response.headers.get('Location') == redirection_url:
                    print(Fore.RED + f"Found vulnerability: {url} can be redirected to {redirection_url} using parameter '{param}'" + Style.RESET_ALL)
                    print(Fore.RED + f"Response URL: {response.url}" + Style.RESET_ALL)
                    return True
                else:
                    send_whatsapp_message(f"No vulnerability found with parameter '{param}' for URL: {url}")
                    print(Fore.GREEN + f"No vulnerability found with parameter '{param}'" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + f"No redirection with parameter '{param}'" + Style.RESET_ALL)

        except requests.RequestException as e:
            print(Fore.RED + f"Error checking URL {url}: {e}" + Style.RESET_ALL)
    
    return False





