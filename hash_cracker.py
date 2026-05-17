import argparse
import hashlib
import sys
import os
import threading
from concurrent.futures import ThreadPoolExecutor

found_event = threading.Event()
cracked_password = None

def detect_hash_type(hash_string):
    hash_len = len(hash_string)
    if hash_len == 32:
        return 'md5'
    elif hash_len == 40:
        return 'sha1'
    elif hash_len == 64:
        return 'sha256'
    elif hash_len == 128:
        return 'sha512'
    else:
        return None

def check_password(password, target_hash, hash_type):
    global cracked_password
    
    if found_event.is_set():
        return

    password = password.strip()
    if hash_type == 'md5':
        hashed = hashlib.md5(password.encode()).hexdigest()
    elif hash_type == 'sha1':
        hashed = hashlib.sha1(password.encode()).hexdigest()
    elif hash_type == 'sha256':
        hashed = hashlib.sha256(password.encode()).hexdigest()
    elif hash_type == 'sha512':
        hashed = hashlib.sha512(password.encode()).hexdigest()
    
    if hashed == target_hash:
        cracked_password = password
        found_event.set()

def main():
    parser = argparse.ArgumentParser(description="Advanced Safe Hash Cracker by Sergio")
    parser.add_argument("-t", "--target", help="The target hash string to crack", required=True)
    parser.add_argument("-w", "--wordlist", help="Path to the wordlist file", required=True)
    parser.add_argument("--threads", type=int, help="Number of concurrent threads (default: 20)", default=20)
    
    args = parser.parse_args()
    
    target_hash = args.target.lower()
    
    hash_type = detect_hash_type(target_hash)
    if not hash_type:
        print("[!] Error: Unsupported or invalid hash length.")
        sys.exit(1)
        
    print("-" * 60)
    print(f"[*] Target Hash : {target_hash}")
    print(f"[*] Detected Type: {hash_type.upper()}")
    print(f"[*] Threads Count: {args.threads}")
    print(f"[*] Status       : Memory-Safe Cracking in progress...")
    print("-" * 60)
    
    if not os.path.exists(args.wordlist):
        print(f"[!] Error: Wordlist file '{args.wordlist}' not found.")
        sys.exit(1)
        
    try:
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            with open(args.wordlist, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    if found_event.is_set():
                        break 
                    executor.submit(check_password, line, target_hash, hash_type)
                    
    except KeyboardInterrupt:
        print("\n[!] Process interrupted by user. Exiting cleanly...")
        sys.exit(0)
            
    if found_event.is_set():
        print(f"\n[+] SUCCESS: Hash Cracked!")
        print(f"[+] Password Found: {cracked_password}")
    else:
        print("\n[-] Failure: Password not found in the provided wordlist.")

if __name__ == "__main__":
    main()