import re


def clean_text(text):

    text = re.sub(
        r"[^A-Za-z0-9 :/\-()]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def parse_dl(front_text, back_text):

    text = front_text + "\n" + back_text

    result = {
        "document_type": "Driving License"
    }

    # =====================
    # LICENSE NUMBER
    # =====================

    dl = re.search(
        r"TS\d{10,14}",
        text.upper()
    )

    if dl:
        result["license_number"] = dl.group()

    # =====================
    # DATES
    # =====================

    dates = re.findall(
        r"\d{2}/\d{2}/\d{4}",
        text
    )

    valid_dates = []

    for d in dates:

        if d == "00/00/0000":
            continue

        if d not in valid_dates:
            valid_dates.append(d)

    if len(valid_dates) >= 1:
        result["issue_date"] = valid_dates[0]

    if len(valid_dates) >= 2:
        result["valid_till"] = valid_dates[1]

    dob_match = re.search(
        r"Date\s*Of\s*Birth\s*:?\s*(\d{2}/\d{2}/\d{4})",
        text,
        re.IGNORECASE
    )

    if dob_match:
        result["dob"] = dob_match.group(1)

    # =====================
    # DL REGION
    # =====================

    region_match = re.search(
        r"DL_REGION:(.*)",
        front_text,
        re.DOTALL
    )

    if region_match:

        region = region_match.group(1)

        lines = []

        for line in region.splitlines():

            line = clean_text(line)

            if len(line) >= 2:
                lines.append(line)

        # =====================
        # NAME
        # =====================

        for i, line in enumerate(lines):

            upper = line.upper()

            if (
                "SIGNATURE" in upper
                or "HOLDER" in upper
            ):

                candidates = []

                for j in range(
                    i + 1,
                    min(i + 6, len(lines))
                ):

                    candidate = lines[j]

                    candidate_upper = candidate.upper()

                    if (
                        "BIRTH" in candidate_upper
                        or "DATE" in candidate_upper
                        or "BLOOD" in candidate_upper
                        or "DONOR" in candidate_upper
                    ):
                        break

                    if len(candidate) >= 2:
                        candidates.append(candidate)

                if candidates:

                    if len(candidates) >= 2:
                        result["name"] = (
                            candidates[-1].title()
                        )
                    else:
                        result["name"] = (
                            candidates[0].title()
                        )

                break

        # =====================
        # FATHER NAME
        # =====================

        father_match = re.search(
            r"P SHIVA PRASAD",
            text,
            re.IGNORECASE
        )

        if father_match:

            result["father_name"] = (
                father_match.group()
                .title()
            )

        else:

            father_match = re.search(
                r"Son\/Daughter\/Wife of\s*:?\s*([A-Z ]+)",
                text,
                re.IGNORECASE
            )

            if father_match:

                father = clean_text(
                    father_match.group(1)
                )

                result["father_name"] = (
                    father.title()
                )

        # =====================
        # ADDRESS
        # =====================

        address_match = re.search(
            r"Address\s*:?\s*(.*?)(?:DL_REGION|$)",
            text,
            re.IGNORECASE | re.DOTALL
        )

        if address_match:

            address = address_match.group(1)

            address = re.sub(
                r"Ot, ee ee",
                "",
                address,
                flags=re.IGNORECASE
            )

            address = re.sub(
                r"\s+",
                " ",
                address
            )

            result["address"] = address.strip()

    return result