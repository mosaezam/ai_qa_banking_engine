function validateTransferAmount(amount) {
    if (amount <= 0) {
        throw new Error("Invalid transfer amount");
    }
}

function calculateFTTFee(amount, destinationCountry) {
    if (destinationCountry === "SG") {
        return amount * 0.02;
    }
    return amount * 0.03;
}

function checkTransactionLimit(amount) {
    if (amount > 50000) {
        throw new Error("FTT transaction limit exceeded");
    }
}