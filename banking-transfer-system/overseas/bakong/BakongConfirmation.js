function confirmBakongTransfer(transactionId) {
    if (!transactionId) {
        throw new Error("Transaction ID missing");
    }
    return "Bakong Transfer Confirmed";
}