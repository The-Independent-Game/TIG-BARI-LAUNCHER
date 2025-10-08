# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Questo è un progetto per **Raspberry Pi Pico 2 W** che implementa un launcher intelligente basato sulla presenza di hardware I2C.

## Architettura

Il progetto utilizza un pattern di **conditional module loading** basato su hardware detection:

- **main.py**: Entry point che esegue la scansione I2C e carica dinamicamente il modulo appropriato
  - Scansiona il bus I2C (GP0=SDA, GP1=SCL) cercando un display all'indirizzo `0x3c`
  - Se il display è presente → importa ed esegue `tig_00_bari.start()`
  - Se il display NON è presente → importa ed esegue `tig_01_bari.start()`

- **tig_00_bari.py**: Modulo eseguito quando il display I2C è presente
- **tig_01_bari.py**: Modulo eseguito quando il display I2C NON è presente

## Hardware Configuration

- **Platform**: Raspberry Pi Pico 2 W (MicroPython)
- **I2C Pins**: GP0 (SDA), GP1 (SCL)
- **Display**: I2C display con indirizzo 0x3c (se presente)

## Module Interface

Ogni modulo caricabile deve implementare una funzione `start()` che viene chiamata da `main.py` dopo l'import.
