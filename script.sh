#!/bin/bash

# Iniciar cargo build em background
cargo build &

# Iniciar ngrok em background
ngrok http -hostname=boss-squirrel-instantly.ngrok-free.app 8000 &

# Esperar todos os processos terminarem
wait