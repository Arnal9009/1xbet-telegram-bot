# Telegram принимает только http/https в URL кнопок — используем сайты банков
BANK_URLS: dict[str, str | None] = {
    "MBank":       "https://mbank.kg",
    "Bakai":       "https://bakai.kg",
    "Optima Bank": "https://optimabank.kg",
    "MegaPay":     "https://megapay.kg",
    "Simbank":     "https://simbank.kg",
    "DemirBank":   "https://demirbank.kg",
    "O!Bank":      "https://obank.kg",
}


def get_bank_url(bank: str) -> str | None:
    return BANK_URLS.get(bank)
