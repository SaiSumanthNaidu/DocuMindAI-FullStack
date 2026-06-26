import re

from .parsers.aadhaar_parser import parse_aadhaar
from .parsers.pan_parser import parse_pan
from .parsers.voter_parser import parse_voter
from .parsers.passport_parser import parse_passport
from .parsers.dl_parser import parse_dl
from .parsers.invoice_parser import parse_invoice


def analyze_document(front_text, back_text=""):

    text = (
        front_text +
        "\n" +
        back_text
    ).upper()

    # Aadhaar

    if (
        "AADHAAR" in text
        or "UIDAI" in text
        or "1947" in text
    ):
        return parse_aadhaar(
            front_text,
            back_text
        )

    # PAN

    if (
        "INCOME TAX" in text
        or "PERMANENT ACCOUNT" in text
        or "INCOME TAX DEPARTMENT" in text
    ):
        return parse_pan(
            front_text,
            back_text
        )

    # Voter

    if (
        "ELECTION" in text
        or "ELECTOR" in text
        or "EPIC" in text
    ):
        return parse_voter(
            front_text,
            back_text
        )

    # Driving License

    if (
        "DRIVING" in text
        or "LICENCE" in text
        or "LICENSE" in text
        or "DATE OF FIRST ISSUE" in text
        or "VALIDITY" in text
        or re.search(
            r"TS\d{10,}",
            text
        )
    ):
        return parse_dl(
            front_text,
            back_text
        )

    # Passport

    if (
        "PASSPORT" in text
        or "P<IND" in text
        or (
            "INDIAN" in text
            and re.search(
                r"[A-Z][0-9]{7}",
                text
            )
        )
    ):
        return parse_passport(
            front_text,
            back_text
        )

    # Invoice

    if (
        "GSTIN" in text
        or "INVOICE" in text
        or "TAX INVOICE" in text
        or "BILL" in text
        or "TOTAL" in text
        or "AMOUNT" in text
    ):
        return parse_invoice(
            front_text,
            back_text
        )

    return {
        "document_type": "Unknown",
        "raw_text_preview": (
            front_text +
            "\n" +
            back_text
        )[:500]
    }