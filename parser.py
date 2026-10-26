import xml.etree.ElementTree as ET

import requests

URL = "https://www.cbr.ru/scripts/XML_daily.asp"


def get_rates():
    resp = requests.get(URL, timeout=15)
    resp.raise_for_status()
    resp.encoding = "windows-1251"  # ЦБ отдаёт XML в windows-1251
    root = ET.fromstring(resp.text)

    rates = {}
    for valute in root.findall("Valute"):
        char_code = valute.findtext("CharCode")
        if char_code in ("USD", "EUR"):
            value = valute.findtext("Value").replace(",", ".")
            rates[char_code] = float(value)
    return rates


if __name__ == "__main__":
    rates = get_rates()
    for code in ("USD", "EUR"):
        print(f"{code}: {rates.get(code, 'не найден')}")
