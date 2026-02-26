function validateRecipientID(idNumber) {
    if (!idNumber) {
        throw new Error("Recipient ID required");
    }
}

function validateRecipientName(name) {
    if (!name || name.length < 3) {
        throw new Error("Invalid recipient name");
    }
}