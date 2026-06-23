import zipfile
import concurrent.futures
import os
import sys

def try_password(zip_filepath, password):
    """Bitta parolni tekshirish funksiyasi"""
    try:
        with zipfile.ZipFile(zip_filepath) as zip_file:
            zip_file.extractall(pwd=bytes(password, 'utf-8'))
            return password
    except:
        return None

def brute_force_zip(zip_filepath, wordlist_path, max_workers=10):
    if not os.path.exists(zip_filepath) or not os.path.exists(wordlist_path):
        print("[-] Xato: Fayl yoki lug'at topilmadi!")
        return

    print(f"[*] Brute-force boshlandi ({max_workers} ta oqimda)...")
    
    # Parollarni lug'atdan o'qish
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
        passwords = [line.strip() for line in f]

    # Multithreading yordamida tezkor tekshirish
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Har bir parolni alohida oqimga topshirish
        results = executor.map(lambda p: try_password(zip_filepath, p), passwords)
        
        for result in results:
            if result:
                print(f"\n[+] PAROL TOPILDI: {result}")
                # Dasturni to'xtatish
                executor.shutdown(wait=False)
                sys.exit(0)
                
    print("\n[-] Afsus, lug'atdagi hech bir parol tushmadi.")

if __name__ == "__main__":
    ZIP_FILE = "yashirin_fayl.zip"
    WORDLIST = "rockyou.txt"
    THREADS = 20  # Kompyuter quvvatiga qarab oshirish mumkin
    
    brute_force_zip(ZIP_FILE, WORDLIST, max_workers=THREADS)
  
