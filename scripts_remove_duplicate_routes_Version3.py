#!/usr/bin/env python3
"""
Eliminar definiciones duplicadas de confirm_email y resend_confirmation
Mantiene SOLO la primera aparición de cada función en routes.py
Uso: python scripts/remove_duplicate_routes.py path/to/routes.py
"""
import sys
import re
from pathlib import Path

if len(sys.argv) != 2:
    print("Uso: python remove_duplicate_routes.py path/to/routes.py")
    sys.exit(1)

p = Path(sys.argv[1])
if not p.exists():
    print("Archivo no encontrado:", p)
    sys.exit(2)

text = p.read_text(encoding="utf-8")

# Buscamos bloques de funciones por su decorador y nombre
pattern_confirm = re.compile(r'@auth_bp\.route\("/confirm/<token>"\)\s*def\s+confirm_email\([^:]*:\s*.*?(?=(?:@auth_bp\.route\(|\Z))', re.S)
pattern_resend = re.compile(r'@auth_bp\.route\("/resend_confirmation",\s*methods=\[[^\]]*\]\)\s*def\s+resend_confirmation\([^:]*:\s*.*?(?=(?:@auth_bp\.route\(|\Z))', re.S)

def keep_first(pattern, s, name):
    matches = list(pattern.finditer(s))
    if len(matches) <= 1:
        print(f"{name}: {len(matches)} ocurrencia(s) — nada que hacer")
        return s, False
    # Mantener el primer match, eliminar los demás
    first = matches[0]
    pieces = []
    last_end = 0
    # añadir todo hasta el final del primer match
    for i, m in enumerate(matches):
        if i == 0:
            last_end = m.end()
        else:
            # omitimos el bloque duplicado
            pass
    # construir nuevo texto: todo hasta end of first match, luego el resto después del último duplicate
    # encontrar start of last duplicate to splice
    last_duplicate_end = matches[-1].end()
    new_s = s[:last_end] + s[last_duplicate_end:]
    print(f"{name}: encontrado {len(matches)} ocurrencias, eliminadas {len(matches)-1} duplicadas")
    return new_s, True

new_text, changed1 = keep_first(pattern_confirm, text, "confirm_email")
new_text, changed2 = keep_first(pattern_resend, new_text, "resend_confirmation")

if changed1 or changed2:
    bak = p.with_suffix(p.suffix + ".bak")
    bak.write_text(text, encoding="utf-8")
    p.write_text(new_text, encoding="utf-8")
    print(f"Actualizado {p}. Backup en {bak}")
else:
    print("No se realizaron cambios.")
