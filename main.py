from machine import Pin, I2C
import time
import network
import urequests
import wifi_config
import os
import uhashlib

DEV_MODE = False

def connect_wifi():
    print("WiFi Connections...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        print(f"WiFi already connected IP: {wlan.ifconfig()[0]}")
        return True

    for network_config in wifi_config.WIFI_NETWORKS:
        ssid = network_config["ssid"]
        password = network_config["password"]

        print(f"Trying to connect to {ssid}...")
        wlan.connect(ssid, password)

        timeout = wifi_config.WIFI_TIMEOUT
        while timeout > 0:
            if wlan.isconnected():
                print(f"WiFi connected IP: {wlan.ifconfig()[0]}")
                return True
            time.sleep(1)
            timeout -= 1
            
            print(f"Attendo connessione... ({timeout}s)")


        print(f"Connection timeout {ssid}")
        wlan.disconnect()
        time.sleep(1)

    print("can't connect to WiFi")
    return False

def md5sum(filename):
    """
    Calcola l'MD5 di un file
    Ritorna l'hash MD5 in formato stringa esadecimale, o None se il file non esiste
    """
    try:
        hash_md5 = uhashlib.sha256()  # MicroPython supporta SHA256
        with open(filename, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                hash_md5.update(chunk)
        return ''.join(['{:02x}'.format(b) for b in hash_md5.digest()])
    except Exception as e:
        print(f"Errore calcolo hash di {filename}: {e}")
        return None

def download_file(url, filename):
    """
    Scarica un file da URL e lo salva localmente con download a chunk
    Ritorna True se il download ha successo, False altrimenti
    """
    try:
        print(f"Download di {url}...")
        response = urequests.get(url, timeout=30)

        if response.status_code == 200:
            total_bytes = 0
            with open(filename, 'wb') as f:
                # Download a chunk per evitare problemi di memoria
                while True:
                    chunk = response.raw.read(1024)  # 1KB alla volta
                    if not chunk:
                        break
                    f.write(chunk)
                    total_bytes += len(chunk)
                    if total_bytes % 5120 == 0:  # Feedback ogni 5KB
                        print(f"  {total_bytes} bytes...")

            response.close()
            print(f"File {filename} scaricato: {total_bytes} bytes")
            return True
        else:
            print(f"Errore download: HTTP {response.status_code}")
            response.close()
            return False

    except Exception as e:
        print(f"Errore durante il download: {e}")
        return False

def update_file_if_changed(old_file, new_file):
    """
    Confronta MD5 di due file. Se diversi, sostituisce il vecchio con il nuovo.
    """
    print(f"Verifica aggiornamento: {old_file}...")

    # Calcola MD5 del file vecchio (se esiste)
    old_md5 = md5sum(old_file)

    # Calcola MD5 del file nuovo
    new_md5 = md5sum(new_file)

    if new_md5 is None:
        print("File nuovo non trovato, skip aggiornamento")
        return False

    print(f"SHA256 {old_file}: {old_md5}")
    print(f"SHA256 {new_file}: {new_md5}")

    if old_md5 != new_md5:
        print("File diversi, aggiornamento in corso...")
        try:
            os.remove(old_file)
            os.rename(new_file, old_file)
            print(f"File {old_file} aggiornato con successo")
            return True
        except Exception as e:
            print(f"Errore durante l'aggiornamento: {e}")
            return False
    else:
        print("File identici, nessun aggiornamento necessario")
        # Rimuovi il file temporaneo
        try:
            os.remove(new_file)
        except:
            pass
        return False

def check_i2c_device(address=0x3c):
    """
    Controlla se un dispositivo I2C è presente all'indirizzo specificato
    """
    try:
        # Inizializza I2C (GP4=SDA, GP5=SCL per default su Pico W)
        # Modifica i pin se necessario
        i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

        # Scansiona i dispositivi I2C
        devices = i2c.scan()

        print(f"Dispositivi I2C trovati: {[hex(d) for d in devices]}")

        # Verifica se il dispositivo è presente
        return address in devices

    except Exception as e:
        print(f"Errore durante la scansione I2C: {e}")
        return False

def main():
    print("TIG LAUNCHER ")

    online_mode = False
    online_mode = connect_wifi()
    if not DEV_MODE:
        if online_mode:
            # update TIG00
            github_url = "https://raw.githubusercontent.com/The-Independent-Game/TIG-00-BARI/main/tig_00_bari.py"
            if download_file(github_url, "tig_00_bari.new.py"):
                update_file_if_changed("tig_00_bari.py", "tig_00_bari.new.py")

            # update TIG01
            github_url = "https://raw.githubusercontent.com/The-Independent-Game/TIG-01-BARI/main/tig_01_bari.py"
            if download_file(github_url, "tig_01_bari.new.py"):
                update_file_if_changed("tig_01_bari.py", "tig_01_bari.new.py")
    else:
        print("continue without updates")

    # Attendi un momento per stabilizzare l'I2C
    time.sleep(0.5)

    # Controlla la presenza del display
    if check_i2c_device(0x3c):
        print("Display I2C rilevato all'indirizzo 0x3c")
        print("Caricamento tig-00-bari.py...")
        try:
            import tig_00_bari
            tig_00_bari.start(online_mode)
        except ImportError:
            print("ERRORE: File tig-00-bari.py non trovato!")
    else:
        print("Display I2C NON rilevato")
        print("Caricamento tig-01-bari.py...")
        try:
            import tig_01_bari
            tig_01_bari.start(online_mode)
        except ImportError:
            print("ERRORE: File tig-01-bari.py non trovato!")

if __name__ == "__main__":
    main()
