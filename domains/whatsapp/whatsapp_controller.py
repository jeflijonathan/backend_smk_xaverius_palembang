from fastapi import status
from common.base.baseController import BaseController
from config.whatsapp.whatsapp import wa_service
from domains.whatsapp.dto.whatsapp_dto import SendMessageDTO


class WhatsAppController(BaseController, prefix="/whatsapp", tags=["WhatsApp"]):

    @classmethod
    def register_routes(cls):
        @cls.router.get("/status", status_code=status.HTTP_200_OK)
        def get_status():
            try:
                # Start service automatically if not running
                if not wa_service._thread or not wa_service._thread.is_alive():
                    wa_service.start()

                status_data = wa_service.get_account_status()
                status_data["qr_code"] = wa_service.qr_code_base64

                return cls.handle_success(
                    data=status_data,
                    message="WhatsApp status retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/send", status_code=status.HTTP_200_OK)
        def send_message(payload: SendMessageDTO):
            try:
                wa_service.send_text_message(payload.to_phone, payload.message)
                return cls.handle_success(
                    message="Message sent successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error),
                                 status_code=status.HTTP_400_BAD_REQUEST)

        @cls.router.post("/logout", status_code=status.HTTP_200_OK)
        def logout():
            try:
                wa_service.logout()
                return cls.handle_success(
                    message="WhatsApp logged out successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error),
                                 status_code=status.HTTP_400_BAD_REQUEST)


WhatsAppController.register_routes()
