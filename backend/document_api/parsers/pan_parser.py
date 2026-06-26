import re

def fix_pan_name(name):

    corrections = {
        "AANDARU": "BANDARU",
        "SANDARU": "BANDARU"
    }

    words = name.split()

    if words:

        first = words[0].upper()

        if first in corrections:
            words[0] = corrections[first]

    return " ".join(words)

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


def parse_pan(front_text, back_text=""):

    text = front_text + "\n" + back_text

    result = {
        "document_type": "PAN Card"
    }

    # PAN Number

    pan_match = re.search(
        r"[A-Z]{5}[0-9]{4}[A-Z]",
        text.upper()
    )

    if pan_match:
        result["pan_number"] = pan_match.group()

    # DOB

    dob_match = re.search(
        r"\d{2}[/-]\d{2}[/-]\d{4}",
        text
    )

    if dob_match:
        result["dob"] = dob_match.group()

    # ======================
    # PAN REGION
    # ======================

    region_match = re.search(
        r"PAN_REGION:(.*)",
        text,
        re.DOTALL
    )

    if region_match:

        region_text = region_match.group(1)

    else:

        region_text = text

    lines = []

    for line in region_text.splitlines():

        line = clean_text(line)
        line = fix_pan_name(line)

        if len(line) >= 4:

            lines.append(line)

    candidates = []

    invalid_words = [
        "INCOME",
        "TAX",
        "DEPARTMENT",
        "GOVT",
        "INDIA",
        "CARD",
        "ACCOUNT",
        "PERMANENT",
        "DATE",
        "SIGNATURE",
        "SIONATURE",
        "FATHER",
        "NAME"
    ]

    for line in lines:

        upper = line.upper()

        invalid = False

        for word in invalid_words:

            if word in upper:
                invalid = True
                break

        if invalid:
            continue

        words = line.split()

        if len(words) < 2:
            continue

        if len(words) > 5:
            continue

        short_words = 0

        for word in words:

            if len(word) <= 2:
                short_words += 1

        if short_words >= 2:
            continue
        
        if words[0] in ["U", "J"]:
            continue
        candidates.append(line)

    # Remove duplicates

    unique = []

    for item in candidates:

        if item not in unique:

            unique.append(item)

    if len(unique) >= 1:
        result["name"] = unique[0]

    if len(unique) >= 2:
        result["father_name"] = unique[1]

    return result