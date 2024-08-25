#!/bin/bash

# Instalar las dependencias desde el archivo requirements.txt
pip install -r requirements.txt

# Ejecutar el script de monitoreo
python3 monitor_pagina.py
