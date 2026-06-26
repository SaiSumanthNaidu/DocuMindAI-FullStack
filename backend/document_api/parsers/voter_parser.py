import re


def clean_text(text):

    text = re.sub(
        r"[^A-Za-z0-9 :/\-]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def parse_voter(front_text, back_text):

    text = front_text + "\n" + back_text

    result = {
        "document_type": "Voter ID"
    }

    # =====================
    # EPIC NUMBER
    # =====================

    epic = re.search(
        r"[A-Z]{3}[0-9]{7}",
        text.upper()
    )

    if epic:
        result["epic_number"] = epic.group()

    # =====================
    # DOB
    # =====================

    dates = re.findall(
        r"\d{2}[/-]\d{2}[/-]\d{4}",
        text
    )

    if dates:
        result["dob"] = dates[0]

    # =====================
    # GENDER
    # =====================

    if "MALE" in text.upper():
        result["gender"] = "Male"

    elif "FEMALE" in text.upper():
        result["gender"] = "Female"

    # =====================
    # VOTER REGION
    # =====================

    region_match = re.search(
        r"VOTER_REGION:(.*)",
        front_text,
        re.DOTALL
    )

    if region_match:

        region = region_match.group(1)

        lines = []

        for line in region.splitlines():

            line = clean_text(line)

            if len(line) >= 4:
                lines.append(line)

        # FATHER NAME

        for line in lines:

            if "FATHER" in line.upper():

                if ":" in line:
                    father = line.split(":")[-1]
                else:
                    continue

                father = clean_text(father)

                if len(father.split()) >= 2:
                    result["father_name"] = father

                break

        # NAME

        for line in lines:

            upper = line.upper()

            if (
                "NAME" in upper
                and "FATHER" not in upper
            ):

                if ":" in line:
                    name = line.split(":")[-1]
                else:
                    continue

                name = clean_text(name)

                name = re.sub(
                    r"\bLE\b",
                    "",
                    name,
                    flags=re.IGNORECASE
                ).strip()

                if len(name.split()) >= 2:

                    invalid_words = [
                        "LE",
                        "MALE",
                        "FEMALE",
                        "PHOTO",
                        "CARD",
                        "ELECTOR"
                    ]

                    bad = False

                    for word in invalid_words:

                        if word in name.upper():
                            bad = True

                    if not bad:
                        result["name"] = name

                break

        # Fallback

        if (
            "name" not in result
            and "father_name" in result
        ):

            father_words = (
                result["father_name"]
                .split()
            )

            if len(father_words) >= 3:

                result["name"] = " ".join(
                    father_words[:-1]
                )
    # =====================
    # ADDRESS
    # =====================

    address = re.search(
        r"Address[:\s']*(.*?)(?:Electoral Registration Officer|Download Date|1950)",
        back_text,
        re.IGNORECASE | re.DOTALL
    )

    if address:

        addr = address.group(1)

        addr = re.sub(
            r"\s+",
            " ",
            addr
        )

        addr = re.sub(
            r"[^\w\s,./:\-]",
            "",
            addr
        )

        result["address"] = addr.strip()

    return result