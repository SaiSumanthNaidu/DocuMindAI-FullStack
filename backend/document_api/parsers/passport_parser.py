import re


def parse_passport(front_text, back_text):

    text = (
        front_text +
        "\n" +
        back_text
    )

    result = {
        "document_type": "Passport"
    }

    # Passport Number

    passport = re.search(
        r"[A-Z][0-9]{7}",
        text.upper()
    )

    if passport:
        result["passport_number"] = passport.group()

    # DOB

    dates = re.findall(
        r"\d{2}[/-]\d{2}[/-]\d{4}",
        text
    )

    if dates:
        result["dob"] = dates[0]

    # Nationality

    if "INDIAN" in text.upper():
        result["nationality"] = "Indian"

    # Name from MRZ

    mrz = re.search(
        r"P<IND([A-Z<]+)",
        text.upper()
    )

    if mrz:

        mrz_text = mrz.group(1)

        mrz_text = mrz_text.replace(
            "<<",
            " "
        )

        mrz_text = mrz_text.replace(
            "<",
            " "
        )

        words = mrz_text.split()

        clean_words = []

        for word in words:

            if len(word) <= 1:
                continue

            if "CCC" in word:
                continue

            clean_words.append(word)

        if len(clean_words) >= 2:

            surname = clean_words[0]

            given_names = clean_words[1:]

            # Remove trailing single OCR characters

            if len(given_names[-1]) == 1:
                given_names.pop()

            # Remove ending K caused by OCR

            if given_names:

                if (
                    len(given_names[-1]) > 3
                    and given_names[-1].endswith("K")
                ):
                    given_names[-1] = (
                        given_names[-1][:-1]
                    )

            result["surname"] = surname.title()

            result["name"] = (
                " ".join(given_names)
            ).title()

    return result