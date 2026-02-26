function validateTransferAmount(amount) {
    if (amount <= 0) {
        throw new Error("Invalid transfer amount");
    }
}

function calculateBakongFee(amount) {
    return amount * 0.025;
}

function checkDailyLimit(amount) {
    if (amount > 30000) {
        throw new Error("Bakong daily transfer limit exceeded");
    }
}
