import requests
from concurrent.futures import ThreadPoolExecutor
import time

# ৬০+ হাই-কোয়ালিটি লাইভ সোর্স (যেগুলো প্রতি ৫-১০ মিনিটে আপডেট হয়)
SOURCES = [
    # TheSpeedX (High Traffic)
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
    # Monosans (Very Clean)
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt"
]

live_proxies = []

def check_fb(proxy):
    # সব প্রোটোকল ট্রাই করা হবে
    for proto in ['http', 'socks4', 'socks5']:
        try:
            proxy_dict = {"http": f"{proto}://{proxy}", "https": f"{proto}://{proxy}"}
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
            
            # ফেসবুক মোবাইল এন্ডপয়েন্ট চেক (ফাস্ট এবং একুরেট)
            r = requests.get("https://m.facebook.com/", proxies=proxy_dict, headers=headers, timeout=4)
            
            if r.status_code == 200 and "facebook.com" in r.url:
                live_proxies.append(f"{proto}://{proxy}")
                return # সফল হলে পরের প্রোটোকল চেক করার দরকার নেই
        except:
            continue

def main():
    print("Fetching 60+ sources...")
    raw_list = []
    for url in SOURCES:
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                raw_list.extend(res.text.splitlines())
        except: continue
    
    unique_list = list(set([p.strip() for p in raw_list if ":" in p]))
    print(f"Total Unique Scraped: {len(unique_list)}. Testing for Facebook...")

    # ৩০০ থ্রেড দিয়ে ফাস্ট চেক
    with ThreadPoolExecutor(max_workers=150) as executor:
        executor.map(check_fb, unique_list)

    # রেজাল্ট সেভ
    with open("live_proxies.txt", "w") as f:
        f.write("\n".join(live_proxies))
    
    print(f"Update Done! Saved {len(live_proxies)} Facebook proxies.")

if __name__ == "__main__":
    main()


