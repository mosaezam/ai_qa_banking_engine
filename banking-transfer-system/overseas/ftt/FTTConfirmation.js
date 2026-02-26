function confirmFTTTransfer(transactionId) {
    if (!transactionId) {
        throw new Error("Transaction ID missing");
    }
    return "FTT Transfer Confirmed";
}