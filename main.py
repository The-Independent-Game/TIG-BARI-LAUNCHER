from machine import Pin, I2C
import time

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
    """
    Funzione principale: decide quale file eseguire
    """
    print("TIG SAVONA LAUNCHER - Avvio...")

    # Attendi un momento per stabilizzare l'I2C
    time.sleep(0.5)

    # Controlla la presenza del display
    if check_i2c_device(0x3c):
        print("Display I2C rilevato all'indirizzo 0x3c")
        print("Caricamento tig-00-bari.py...")
        try:
            import tig_00_bari
            tig_00_bari.start()
        except ImportError:
            print("ERRORE: File tig-00-bari.py non trovato!")
    else:
        print("Display I2C NON rilevato")
        print("Caricamento tig-01-bari.py...")
        try:
            import tig_01_bari
            tig_01_bari.start()
        except ImportError:
            print("ERRORE: File tig-01-bari.py non trovato!")

if __name__ == "__main__":
    main()
