import time
from stem import Signal
from stem.control import Controller

def renew_tor_ip(port=9051, password=None):
    try:
        with Controller.from_port(port=port) as c:
            c.authenticate(password=password or "")
            c.signal(Signal.NEWNYM)
            time.sleep(5)
            print("[+] Tor circuit renewed")
    except Exception as e:
        print(f"[!] Tor renewal failed: {e}")