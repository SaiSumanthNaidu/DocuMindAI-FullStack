import re


def clean_text(text):

    text = re.sub(
        r"[^A-Za-z ]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip().title()


def parse_aadhaar(front_text, back_text):

    text = front_text + "\n" + back_text

    result = {
        "document_type": "Aadhaar Card"
    }

    # Aadhaar Number

    number_text = text.replace("\n", " ")

    aadhaar_match = re.search(
        r"\d{4}\s\d{4}\s\d{4}",
        number_text
    )

    if not aadhaar_match:

        aadhaar_match = re.search(
            r"\d{12}",
            number_text
        )

    if aadhaar_match:

        number = aadhaar_match.group()

        if len(number) == 12:

            number = (
                number[:4]
                + " "
                + number[4:8]
                + " "
                + number[8:]
            )

        result["aadhaar_number"] = number

    
    # Gender

    if "MALE" in text.upper():
        result["gender"] = "Male"

    elif "FEMALE" in text.upper():
        result["gender"] = "Female"

    # DOB

    dob_match = re.search(
        r"\d{2}[/-]\d{2}[/-]\d{4}",
        text
    )

    if dob_match:
        result["dob"] = dob_match.group()

    # Address

    address_match = re.search(
        r"Address[:\s]*(.*?)(?:1947|UIDAI|HELP)",
        back_text,
        re.IGNORECASE | re.DOTALL
    )

    if address_match:

        address = address_match.group(1)

        address = re.sub(
            r"\b[eE]{2,}\b",
            "",
            address
        )

        address = re.sub(
            r"\s+",
            " ",
            address
        )

        result["address"] = address[:250].strip()

        address_lines = address.split(",")

        if len(address_lines) >= 1:

            father = address_lines[0].strip()

            if len(father.split()) >= 2:
                result["father_name"] = father.title()

    # AADHAAR REGION

    region_match = re.search(
        r"AADHAAR_REGION:(.*)",
        front_text,
        re.DOTALL
    )

    if region_match:

        region = region_match.group(1)

        candidates = []

        for line in region.splitlines():

            line = clean_text(line)

            upper = line.upper()

            if len(line) < 5:
                continue

            if (
                "DOB" in upper
                or "MALE" in upper
                or "FEMALE" in upper
                or "AADHAAR" in upper
                or "PROOF" in upper
                or "CITIZENSHIP" in upper
                or "DATE" in upper
                or "XML" in upper
                or "QR" in upper
                or "AUTHENTICATION" in upper
            ):
                continue

            words = line.split()

            if len(words) < 2:
                continue

            if len(words) > 4:
                continue

            valid_words = 0

            for word in words:

                if len(word) >= 3:
                    valid_words += 1

            if valid_words >= 2:
                candidates.append(line)

        for candidate in candidates:

            upper = candidate.upper()

            if (
                "SAI" in upper
                or "KUMAR" in upper
                or "RAO" in upper
                or "DEVI" in upper
                or "REDDY" in upper
                or "SUMANTH" in upper
            ):
                result["name"] = candidate
                break

        if "name" not in result and candidates:
            result["name"] = candidates[-1]

    return result