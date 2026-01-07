import requests
import threading

# সোর্স লিস্ট (এখানে আরও লিঙ্ক যোগ করা যাবে)
SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/proxies.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt"
]

live_proxies = []

def check_proxy(proxy):
    try:
        # প্রক্সি চেক করার জন্য httpbin ব্যবহার
        r = requests.get("https://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=5)
        if r.status_code == 200:
            live_proxies.append(proxy)
    except:
        pass

def start_update():
    all_raw = []
    for url in SOURCES:
        try:
            res = requests.get(url)
            all_raw.extend(res.text.splitlines())
        except: continue
    
    # ডুপ্লিকেট বাদ দিয়ে প্রথম ১০০টি চেক করা (টাইম লিমিটের জন্য)
    unique_proxies = list(set(all_raw))[:100]
    
    threads = []
    for p in unique_proxies:
        t = threading.Thread(target=check_proxy, args=(p,))
        threads.append(t)
        t.start()
    
    for t in threads: t.join()
    
    with open("live_proxies.txt", "w") as f:
        f.write("\n".join(live_proxies))

if __name__ == "__main__":
    start_update()