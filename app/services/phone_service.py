import phonenumbers
from phonenumbers import carrier, geocoder, timezone

def analyze_number(number: str):
    try:
        parsed = phonenumbers.parse(number)

        if not phonenumbers.is_valid_number(parsed):
            return {"valid": False}

        return {
            "valid": True,
            "international_format": phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
            ),
            "country": geocoder.description_for_number(parsed, "en"),
            "carrier": carrier.name_for_number(parsed, "en"),
            "timezone": timezone.time_zones_for_number(parsed),
            "line_type": "Mobile" if phonenumbers.number_type(parsed) == 1 else "Other"
        }

    except:
        return {"valid": False}