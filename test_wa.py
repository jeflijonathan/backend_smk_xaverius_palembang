import time
from config.whatsapp.whatsapp import wa_service

print("Starting WA Service...")
wa_service.start()

for i in range(15):
    status = wa_service.get_account_status()
    print(f"[{i}] Status: is_connected={status['is_connected']}, qr_code_length={len(wa_service.qr_code_base64) if wa_service.qr_code_base64 else 0}")
    if wa_service.qr_code_base64:
        print("QR Code generated successfully!")
        break
    time.sleep(2)
