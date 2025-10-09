# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Questo è un progetto per **Raspberry Pi Pico 2 W** che implementa un launcher intelligente basato sulla presenza di hardware I2C.

## Architettura

Il progetto utilizza un pattern di **conditional module loading** basato su hardware detection:

- **main.py**: Entry point che esegue la scansione I2C e carica dinamicamente il modulo appropriato
  - Scansiona il bus I2C (GP0=SDA, GP1=SCL) cercando un display all'indirizzo `0x3c`
  - Se il display è presente → importa ed esegue il gioco in `tig_00_bari`
  - Se il display NON è presente → importa ed esegue `tig_01_bari`

- **tig_00_bari.py**: Modulo eseguito quando il display I2C è presente
- **tig_01_bari.py**: Modulo eseguito quando il display I2C NON è presente

## Hardware Configuration

- **Platform**: Raspberry Pi Pico 2 W (MicroPython)
- **I2C Pins**: GP0 (SDA), GP1 (SCL)
- **Display**: I2C display con indirizzo 0x3c (se presente)

## Module Interface

Ogni modulo caricabile deve implementare:
- Una classe principale (es. `TIG00`, `TIG01`) con metodo `go(self)` che contiene la logica del programma
- Una funzione `start()` a livello di modulo che istanzia la classe e chiama `go()`

Esempio:
```python
class TIG00:
    def __init__(self):
        # Inizializzazione
        pass

    def go(self):
        # Logica principale
        print("Game running...")

def start():
    game = TIG00()
    game.go()
```

## Development Workflow

Il progetto usa **VS Code** con l'estensione **MicroPico** per lo sviluppo:

### Upload e Test
1. Connetti il Pico 2 W via USB
2. In VS Code: `Ctrl+Shift+P` → "MicroPico: Connect"
3. Upload del progetto: `Ctrl+Shift+P` → "Upload project to Pico"
4. Reset per eseguire: `Ctrl+Shift+P` → "MicroPico: Reset"

### Debug
- Il REPL integrato in VS Code mostra l'output in tempo reale
- Usa `print()` per debug
- L'output mostra quale modulo è stato caricato in base alla detection I2C

### Common Issues
- **AttributeError su `start()`**: Verificare che `start()` sia definita a livello di modulo, non dentro la classe
- **TypeError su metodi di classe**: Tutti i metodi di istanza devono avere `self` come primo parametro
