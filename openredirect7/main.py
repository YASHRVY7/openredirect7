# openredirect7/main.py

import argparse
import validators
from utils.url_processor import check_open_redirect
from utils.check_internet import check_internet_connection
from includes.helps import banner, display_help
from includes.const import Data
import webbrowser
from colorama import init, Fore, Style
from includes.credential import send_whatsapp_message

init()

def validate_url(url):
    if validators.url(url):
        return True
    else:
        print(f"Invalid URL: {url}")
        return False
    
def main():
    parser = argparse.ArgumentParser(description="Open Redirect Vulnerability Checker")
    parser.add_argument('-u', '--url', type=str, help="URL to check for open redirect vulnerability")
    parser.add_argument('-i', '--input', type=argparse.FileType('r'), help="File containing URLs to check")
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), help="File to save the output results")
    parser.add_argument('-p', '--payloads', nargs='+', type=str, help="Additional payloads to test for open redirect")
    parser.add_argument('-b', '--blog', action='store_true', help='Open Blog to read about Bug')
    args = parser.parse_args()
    banner()

    if not check_internet_connection():
        print("No internet connection. Please check your internet settings.")
        return
    
    if args.blog:
        display_help()
        webbrowser.open(Data.blog)
        return
    
    if args.url:
        if validate_url(args.url):
            print(f"Checking URL: {args.url}")
            vulnerable_payloads = check_open_redirect(args.url, args.payloads if args.payloads else [])
            if vulnerable_payloads:
                result = f"URL: {args.url} is vulnerable to open redirects with payloads: {', '.join(vulnerable_payloads)}"
                if args.output:
                    args.output.write(result + "\n")
                print(result)
                send_whatsapp_message(result)
        else:
            print(Fore.RED + f"Invalid URL: {args.url}"+ Style.RESET_ALL)

    if args.input:
        urls = [url.strip() for url in args.input.readlines()]
        for url in urls:
            if validate_url(url):
                print(f"Checking URL: {url}")
                vulnerable_payloads = check_open_redirect(url, args.payloads if args.payloads else [])
                if vulnerable_payloads:
                    result = f"URL: {url} is vulnerable to open redirects with payloads: {', '.join(vulnerable_payloads)}"
                    if args.output:
                        args.output.write(result + "\n")
                    print(result)
                    send_whatsapp_message(result)
            else:
                print(f"Invalid URL: {url}")

if __name__ == "__main__":
    main()
