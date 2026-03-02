// Bakong - Confirmation and NBC Submission
const processBakongTransaction = async (payload) => {
  try {
    validateBakongTransfer(payload);
    validateBakongRecipient(payload.recipient);
    const fee = calculateBakongFee(payload.amount);
    const result = await submitToNBCGateway(payload, fee);
    if (!result.referenceNo) throw new Error("NBC reference not generated");
    await updateLedger(payload.accountNo, payload.amount + fee.total);
    await logAuditTrail(payload, result);
    return { status: "SUCCESS", referenceNo: result.referenceNo, fee };
  } catch (error) {
    await logError("BAKONG_FAILED", error, payload);
    throw error;
  }
};

const validateBakongLimit = (amount, dailyUsed) => {
  if (amount + dailyUsed > BAKONG_LIMIT) throw new Error("Daily limit exceeded");
  return true;
};
