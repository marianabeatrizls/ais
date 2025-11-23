import subprocess
import socket
import time
# IMPORTA O DECODER
from ais_decoder import (
    parse_nmea_sentence,
    ais_payload_to_bits,
    decode_position_report
)
print("Iniciando AIS-catcher...")
ais_process = subprocess.Popen(
    ["AIS-catcher", "-f", "162.0M", "-u", "127.0.0.1", "10110"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(2)
UDP_IP = "127.0.0.1"
UDP_PORT = 10110
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print("AIS iniciado. Aguardando mensagens...\n")
# LISTA DE REGISTROS AIS DECODIFICADOS
ais_log = []  # cada item será: (timestamp_local, dict_dados)
try:
    while True:
        data, addr = sock.recvfrom(4096)
        msg = data.decode(errors="ignore").strip()
        # Verifica se é mensagem NMEA de AIS
        if not msg.startswith("!AIVDM"):
            continue
        try:
            # 1) Extrai o payload NMEA
            payload = parse_nmea_sentence(msg)
            # 2) Converte para bits
            bits = ais_payload_to_bits(payload)
            # 3) Decodifica mensagem AIS tipo 1
            decoded = decode_position_report(bits)
            # 4) Filtra apenas as mensagens tipo 1
            if decoded["message_id"] != 1:
                continue
            # 5) Adiciona timestamp da recepção
            t_local = time.time()
            ais_log.append((t_local, decoded))
            print("\n=== AIS RECEBIDO ===")
            print("Timestamp local:", t_local)
            for k, v in decoded.items():
                print(f"{k}: {v}")
        except Exception as e:
            print("Erro ao decodificar:", e)
            continue
except KeyboardInterrupt:
    print("\nEncerrando...")
finally:
    ais_process.terminate()
    ais_process.wait()
    print("AIS-catcher finalizado.")