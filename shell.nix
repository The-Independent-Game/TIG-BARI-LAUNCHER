{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    python3Packages.pip
    python3Packages.pyserial
  ];

  shellHook = ''
    # Crea un ambiente virtuale locale se non esiste
    if [ ! -d .venv ]; then
      echo "Creazione ambiente virtuale..."
      python3 -m venv .venv
    fi

    # Attiva l'ambiente virtuale
    source .venv/bin/activate

    # Installa mpremote se non presente
    if ! command -v mpremote &> /dev/null; then
      echo "Installazione mpremote..."
      pip install --quiet mpremote
    fi

    echo "Ambiente mpremote pronto!"
    echo ""
    echo "Comandi utili:"
    echo "  mpremote connect list          # Lista dispositivi"
    echo "  mpremote ls                    # Lista file sul Pico"
    echo "  mpremote cp file.py :          # Copia file"
    echo "  mpremote cp -r cartella/* :    # Copia cartella"
    echo ""

    # Verifica se ci sono dispositivi ttyACM
    if ls /dev/ttyACM* 2>/dev/null; then
      echo "Dispositivi trovati:"
      ls -l /dev/ttyACM*
    else
      echo "Nessun dispositivo /dev/ttyACM* trovato"
    fi
  '';
}