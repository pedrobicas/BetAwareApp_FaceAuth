import sys

try:
    import face_recognition
    print("SUCESSO: face_recognition importado.")
except Exception as e:
    print(f"FALHA na importação de face_recognition: {e}")
    sys.exit(1) # Sai se falhar

try:
    from flask import Flask
    print("SUCESSO: Flask importado.")
except Exception as e:
    print(f"FALHA na importação de Flask: {e}")
    sys.exit(1) # Sai se falhar

print("Todas as bibliotecas principais importadas com sucesso. O problema está na execução.")