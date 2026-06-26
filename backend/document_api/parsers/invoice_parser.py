import re


def clean_text(text):

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def parse_invoice(front_text, back_text):

    text = front_text + "\n" + back_text

    result = {
        "document_type": "Invoice"
    }

    # =====================
    # DATES
    # =====================

    dates = re.findall(
        r"\d{2}[/-]\d{2}[/-]\d{4}",
        text
    )

    if dates:
        result["invoice_date"] = dates[0]

    # =====================
    # GST NUMBERS
    # =====================

    gst_numbers = re.findall(
        r"\d{2}[A-Z]{5}\d{4}[A-Z][A-Z0-9]Z[A-Z0-9]",
        text.upper()
    )

    if len(gst_numbers) >= 1:
        result["vendor_gst"] = gst_numbers[0]

    if len(gst_numbers) >= 2:
        result["customer_gst"] = gst_numbers[1]

    # =====================
    # VENDOR NAME
    # =====================

    vendor_match = re.search(
        r"Bill\s+([A-Za-z ]+)",
        text,
        re.IGNORECASE
    )

    if vendor_match:

        result["vendor_name"] = (
            clean_text(
                vendor_match.group(1)
            )
        )

    # =====================
    # CUSTOMER NAME
    # =====================

    customer_match = re.search(
        r"Bandari\s+Enterprises",
        text,
        re.IGNORECASE
    )

    if customer_match:

        result["customer_name"] = (
            customer_match.group()
        )

    # =====================
    # PO NUMBER
    # =====================

    po_match = re.search(
        r"PO Number\s*:?\s*(\d+)",
        text,
        re.IGNORECASE
    )

    if po_match:
        result["po_number"] = po_match.group(1)

    # =====================
    # TOTAL AMOUNT
    # =====================

    total_match = re.search(
        r"Total\s*=?\s*([0-9,]+\.\d{2})",
        text,
        re.IGNORECASE
    )

    if total_match:

        amount = total_match.group(1)

        amount = amount.replace(",", "")

        result["total_amount"] = amount

    # =====================
    # CGST
    # =====================

    cgst_match = re.search(
        r"CGST.*?9%.*?(\d+\.\d{2})",
        text,
        re.DOTALL
    )

    if cgst_match:
        result["cgst"] = cgst_match.group(1)

    # =====================
    # SGST
    # =====================

    sgst_match = re.search(
        r"SGST.*?9%.*?(\d+\.\d{2})",
        text,
        re.DOTALL
    )

    if sgst_match:
        result["sgst"] = sgst_match.group(1)

    # =====================
    # ITEMS
    # =====================

    items = []

    lines = []

    for line in text.splitlines():

        line = clean_text(line)

        if line:
            lines.append(line)

    i = 0

    while i < len(lines):

        line = lines[i]

        if re.match(r"^\d{3,5}\s", line):

            line = re.sub(
                r"^\d{3,5}\s*",
                "",
                line
            )

            item_name = line

            quantity = None

            j = i + 1

            while j < min(i + 12, len(lines)):

                next_line = lines[j]

                # quantity
                if (
                    quantity is None
                    and re.fullmatch(r"\d+", next_line)
                ):
                    quantity = next_line

                # ignore price values
                elif re.search(
                    r"\d+\.\d{2}",
                    next_line
                ):
                    pass

                # ignore percentages
                elif "%" in next_line:
                    pass

                # ignore totals
                elif (
                    "TOTAL" in next_line.upper()
                    or "AMOUNT" in next_line.upper()
                ):
                    break

                # stop if another product starts
                elif re.match(
                    r"^\d{3,5}\s",
                    next_line
                ):
                    break

                else:

                    if len(next_line) > 3:

                        item_name += (
                            " " + next_line
                        )

                j += 1

            item_name = item_name.replace(
                "_",
                " "
            )

            item_name = re.sub(
                r"\s+",
                " ",
                item_name
            )

            items.append({
                "name": item_name.strip(),
                "quantity": quantity
            })

        i += 1

    if items:
        result["items"] = items
        
    return result