#!/bin/bash
# Desencripta credenciales - Uso: bash decrypt.sh
read -sp "Clave: " KEY
echo
echo "$KEY" | openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -d -pass "pass:$KEY" -base64 -A -in credenciales.enc
