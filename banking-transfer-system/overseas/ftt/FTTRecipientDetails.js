function validateRecipientName(name) {
    if (!name || name.length < 3) {
        throw new Error("Invalid recipient name");
    }
}

function validateRecipientAccount(accountNumber) {
    if (!accountNumber || accountNumber.length < 8) {
        throw new Error("Invalid account number");
    }
}