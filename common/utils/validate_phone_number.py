import re
import phonenumbers
from typing import Optional


def validate_international_phone(value: Optional[str]) -> Optional[str]:
    if value is None or value.strip() == "":
        return value

    cleaned = re.sub(r"[\s\-]", "", value)

    if cleaned.startswith("08"):
        cleaned = "+62" + cleaned[1:]

    try:
        parsed_number = phonenumbers.parse(cleaned, None)

        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Nomor telepon tidak valid untuk kode negara tersebut.")

        return phonenumbers.format_number(
            parsed_number, phonenumbers.PhoneNumberFormat.E164
        )

    except phonenumbers.NumberParseException:
        raise ValueError(
            "Format nomor telepon internasional tidak dikenali (Gunakan tanda + di depan)."
        )
