import requests
from concurrent.futures import ThreadPoolExecutor
import time

# এখানে সেরা সোর্সগুলো দেওয়া হলো (একাধিক লিঙ্ক একসাথে)
SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/proxies.txt",
    "https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt"
]

live_proxies = []

def check_proxy(proxy):
    """খুব দ্রুত প্রক্সি চেক করার ফাংশন"""
    try:
        # ৩ সেকেন্ডের টাইমআউট সেট করা হয়েছে যাতে দ্রুত হয়
        r = requests.get("http://google.com", 
                         proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, 
                         timeout=3)
        if r.status_code == 200:
            live_proxies.append(proxy)
            print(f"[LIVE] {proxy}")
    except:
        pass

def main():
    print("Fetching proxies from GitHub...")
    all_raw = []
    for url in SOURCES:
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                all_raw.extend(res.text.splitlines())
        except:
            continue
    
    unique_proxies = list(set(all_raw))
    print(f"Total found: {len(unique_proxies)}. Checking speed...")

    # ৫০টি থ্রেড একসাথে কাজ করবে (খুবই ফাস্ট)
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(check_proxy, unique_proxies[:500]) # প্রথম ৫০০টি চেক করবে

    # ফাইলে সেভ করা
    with open("live_proxies.txt", "w") as f:
        f.write("\n".join(live_proxies))
    
    print(f"Update Done! Live: {len(live_proxies)}")

if __name__ == "__main__":
    main()
