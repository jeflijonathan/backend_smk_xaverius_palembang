import threading
import io
import qrcode
import base64
import sys
from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv, PairStatusEv, QREv, event
from neonize.utils.jid import build_jid

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass


class WhatsAppService:
    def __init__(self, db_path: str = "whatsapp_session.sqlite3"):
        self.db_path = db_path
        self.client: NewClient = None
        self.qr_code_base64: str = None
        self.is_connected: bool = False
        self._thread: threading.Thread = None

        # Penampung informasi akun yang terhubung
        self.user_jid: str = None
        self.user_phone: str = None
        self.user_name: str = None

    def _set_account_info(self):
        """Ambil data akun setelah terhubung"""
        try:
            me = self.client.get_me()
            if me:
                jid = me.JID
                # JID adalah protobuf object, bukan string biasa
                # Field 'User' berisi nomor HP, 'Server' berisi domain
                if hasattr(jid, 'User'):
                    self.user_phone = str(jid.User)
                    self.user_jid = f"{jid.User}@{jid.Server}" if hasattr(jid, 'Server') else str(jid.User)
                else:
                    # fallback: konversi ke string dan ambil bagian sebelum @
                    jid_str = str(jid)
                    self.user_phone = jid_str.split("@")[0].split('"')[1] if '"' in jid_str else jid_str.split("@")[0]
                    self.user_jid = jid_str

                self.user_name = getattr(me, "PushName", None) or getattr(me, "Name", None) or "WhatsApp User"
                print(f"⚡ [WhatsApp] Account info: {self.user_name} ({self.user_phone})")
        except Exception as e:
            print(f"[WhatsApp] Failed to fetch account info: {e}")

    def _setup_events(self):
        @self.client.event(ConnectedEv)
        def on_connected(_: NewClient, __: ConnectedEv):
            """Fired on reconnect (session already exists)"""
            self.is_connected = True
            self.qr_code_base64 = None
            self._set_account_info()
            print(f"⚡ [WhatsApp] Reconnected successfully as {self.user_name} ({self.user_phone})")

        @self.client.event(PairStatusEv)
        def on_pair_status(_: NewClient, pair_status: PairStatusEv):
            """Fired after QR code scan. Status 200 means success."""
            print(f"[DEBUG] on_pair_status fired. ID={pair_status.ID}, Status={pair_status.Status}, Error={pair_status.Error}")
            # Jika pairing berhasil (error kosong = sukses)
            if not pair_status.Error or pair_status.Error == "":
                self.is_connected = True
                self.qr_code_base64 = None
                # Ambil info akun setelah jeda singkat (client masih proses pairing)
                import time
                time.sleep(2)
                self._set_account_info()
                print(f"⚡ [WhatsApp] Paired and connected as {self.user_name} ({self.user_phone})")
            else:
                print(f"[WhatsApp] Pairing failed: {pair_status.Error}")

        def on_qr_callback(_: NewClient, data_qr: bytes):
            print(f"[DEBUG] QR callback fired.")
            try:
                self.qr_code_base64 = self._generate_qr_base64(data_qr)
                print("⚡ [WhatsApp] New QR Code base64 generated successfully")
            except Exception as e:
                print(f"[ERROR] Failed to generate base64 QR: {e}")

        # Override default QR handler in neonize
        self.client.event.qr(on_qr_callback)

        @self.client.event(MessageEv)
        def on_message(client: NewClient, message: MessageEv):
            self._handle_incoming_message(client, message)

    def _generate_qr_base64(self, qr_str) -> str:
        import segno
        # qr_str can be bytes or str, segno handles both
        qr = segno.make_qr(qr_str)
        buffered = io.BytesIO()
        qr.save(buffered, kind="png", scale=10, border=4)
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def _handle_incoming_message(self, client: NewClient, message: MessageEv):
        text = message.Message.conversation or message.Message.extendedTextMessage.text
        if text == "ping":
            client.reply_message("pong", message)

    def start(self):
        if self._thread and self._thread.is_alive():
            print("[WhatsApp] Client is already running.")
            return

        def run_client():
            self.client = NewClient(self.db_path)
            self._setup_events()
            self.client.connect()

        self._thread = threading.Thread(target=run_client, daemon=True)
        self._thread.start()

    def stop(self):
        """Hentikan koneksi WhatsApp saat server shutdown."""
        print("[WhatsApp] Stopping WhatsApp service...")
        # Langsung reset state tanpa menunggu graceful disconnect
        # (thread adalah daemon, OS akan kill otomatis saat process mati)
        self.is_connected = False
        self.qr_code_base64 = None
        self.client = None
        print("[WhatsApp] WhatsApp service stopped.")

    def get_account_status(self) -> dict:
        """Mengembalikan status koneksi beserta informasi akun"""
        return {
            "is_connected": self.is_connected,
            "user": {
                "name": self.user_name,
                "phone": self.user_phone,
                "jid": self.user_jid
            } if self.is_connected else None
        }

    def logout(self):
        """Memutus koneksi dan logout dari perangkat"""
        if not self.is_connected or not self.client:
            raise Exception("WhatsApp client is not connected.")

        try:
            self.client.logout()
        except Exception as e:
            print(f"[WhatsApp] Error during logout call: {e}")
        finally:
            self.is_connected = False
            self.qr_code_base64 = None
            self.user_jid = None
            self.user_phone = None
            self.user_name = None
            self.client = None
            print("🚪 [WhatsApp] Logged out successfully.")

    def send_text_message(self, to_phone: str, message_text: str):
        if not self.is_connected or not self.client:
            raise Exception("WhatsApp client is not connected yet.")

        # Bersihkan nomor HP dari karakter tidak valid
        formatted_phone = to_phone.replace("+", "").replace("-", "").replace(" ", "").strip()

        # Buat JID object (bukan string) sesuai yang dibutuhkan neonize
        jid = build_jid(formatted_phone)

        self.client.send_message(jid, message_text)


wa_service = WhatsAppService()
