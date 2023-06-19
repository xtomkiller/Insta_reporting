import requests
from termcolor import colored
from pyfiglet import Figlet

def check_proxy(proxy):
    try:
        response = requests.get('https://www.google.com', proxies={'http': proxy, 'https': proxy}, timeout=5)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        pass
    return False

def test_proxies():
    try:
        response = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=5000')
        proxies = response.text.splitlines()

        total_proxies = len(proxies)
        checked_proxies = 0
        verified_proxies = 0
        not_working_proxies = 0

        figlet = Figlet(font='big')
        banner = colored(figlet.renderText('Normal Proxy X'), 'blue')
        developer = colored('Trusted Hacker', 'cyan')
        print(f'{banner}\nDeveloped by {developer}\n')

        print(colored(f'Total proxies to check: {total_proxies}', 'yellow'))

        for idx, proxy in enumerate(proxies, start=1):
            checked_proxies += 1
            if check_proxy(proxy):
                verified_proxies += 1
                with open('/home/hacker/Desktop/my/Insta_reporting/data/proxies.txt', 'a') as file:
                    file.write(proxy + '\n')
                print(colored(f'{idx}. Proxy {proxy.ljust(20)} is working', 'green'))
            else:
                not_working_proxies += 1
                print(colored(f'{idx}. Proxy {proxy.ljust(20)} is not working', 'red'))

        print(colored(f'Total proxies checked: {checked_proxies}', 'yellow'))
        print(colored(f'Verified proxies: {verified_proxies}', 'green'))
        print(colored(f'Not working proxies: {not_working_proxies}', 'red'))

        if verified_proxies > 0:
            print('Verified proxies saved to proxies_verify.txt')

    except KeyboardInterrupt:
        print('Script interrupted.')

    finally:
        print('Exiting...')
        print(colored(f'Total proxies to check: {total_proxies}', 'yellow'))
        print(colored(f'Total proxies checked: {checked_proxies}', 'yellow'))
        print(colored(f'Verified proxies: {verified_proxies}', 'green'))
        print(colored(f'Not working proxies: {not_working_proxies}', 'red'))
        exit()

test_proxies()
