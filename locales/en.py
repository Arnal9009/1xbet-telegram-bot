texts = {
    "choose_language": "Please select a language:",

    "main_menu": "🏠 <b>Main Menu</b>\nChoose a section:",
    "btn_topup": "💵 Top Up Account",
    "btn_withdraw": "💳 Withdraw Funds",
    "btn_rules": "📜 Terms of Use",
    "btn_change_lang": "🌐 Change Language",
    "btn_las_vegas": "🎰 Las Vegas",
    "las_vegas_wip": "🎰 This section is under development. Coming soon!",

    "rules": (
        "📜 <b>Terms of Use</b>\n\n"
        "• Minimum top-up amount: <b>100 som</b>\n"
        "• Maximum top-up amount: <b>100,000 som</b>\n"
        "• After creating an order you have <b>15 minutes</b> to pay\n"
        "• Operator processing time: <b>5–15 minutes</b>\n"
        "• 1xBet ID: digits only, 8–9 characters\n"
        "• Receipt accepted as: photo (JPG/PNG), PDF"
    ),

    "captcha_topup": "🤖 Bot check.\nSelect the emoji: 🚗",
    "captcha_withdraw": "🤖 Confirm you are not a robot.\nTap the emoji: 🥮",
    "captcha_wrong": "❌ Wrong answer, please try again.",

    "enter_1xbet_id": (
        "🆔 Enter your 1xBet account ID:\n"
        "<i>(Digits only, e.g.: 12345678)</i>"
    ),
    "invalid_id": "❌ Invalid ID format. Enter 6 to 12 digits.",
    "confirm_id": (
        "👤 Check your 1xBet ID:\n\n"
        "ID: <b>{id}</b>\n\n"
        "Is everything correct?"
    ),
    "btn_confirm_yes": "🟢 Yes, continue",
    "btn_confirm_no": "🔴 Re-enter ID",

    "enter_amount": (
        "💰 Enter the top-up amount:\n\n"
        "📌 Minimum amount: <b>{min} som</b>\n"
        "📌 Maximum amount: <b>{max} som</b>"
    ),
    "invalid_amount": "❌ Enter an amount between {min} and {max} som.",

    "select_bank": "🏛 Select a bank for payment:",

    "order_created": (
        "📄 Order <b>#{order_id}</b> created\n\n"
        "💰 Amount: <b>{amount} som</b>\n"
        "🏛 Bank: <b>{bank}</b>\n"
        "🆔 1xBet ID: <b>{xbet_id}</b>\n\n"
        "⏳ You have <b>15 minutes</b> to complete the payment.\n\n"
        "📎 After payment, please send your receipt (photo or PDF) in this chat!"
    ),
    "btn_pay": "💳 Pay via {bank}",

    "receipt_accepted": (
        "⏳ Your receipt has been received!\n\n"
        "Order <b>#{order_id}</b> has been sent to the operator.\n"
        "Processing usually takes 5 to 15 minutes."
    ),

    "topup_approved": "✅ Your 1xBet balance has been topped up!",
    "topup_rejected_wrong_id": "❌ Order declined: incorrect 1xBet ID.",
    "topup_rejected_no_payment": "❌ Order declined: payment not found.",

    "upload_qr": (
        "📲 Generate a QR code in your banking app and send a screenshot.\n\n"
        "<i>ELQR supported (MBank, Bakai, etc.)</i>"
    ),
    "qr_received": "✅ QR code received. Now enter your 1xBet ID.",

    "withdraw_instruction": (
        "ID: <b>{id}</b>\n\n"
        "📍 Open the 1xBet app:\n"
        "1. Settings\n"
        "2. Withdraw from account\n"
        "3. Cash\n"
        "4. Enter withdrawal amount\n"
        "5. City: <b>Bishkek</b>\n"
        "6. Street: <b>TopKassa (24/7)</b>\n"
        "7. Confirm\n"
        "8. Get code\n"
        "9. Send the code to this bot\n\n"
        "Need help? {operator}"
    ),
    "enter_withdraw_code": "💳 Enter the withdrawal code from the 1xBet app/website:",

    "withdraw_accepted": (
        "⏳ Your withdrawal request has been accepted!\n\n"
        "The operator will verify the details and transfer funds to your QR code."
    ),
    "withdraw_approved": "✅ Funds have been transferred to your card!",
    "withdraw_rejected_wrong_code": "❌ Order declined: invalid withdrawal code.",

    "btn_back": "⬅️ Back to menu",
}
