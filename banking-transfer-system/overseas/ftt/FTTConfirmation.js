// FTT - Confirmation and RENTAS/DuitNow Submission
const processFTTTransaction = async (payload) => {
  try {
    validateFTTTransfer(payload);
    validateFTTRecipient(payload.recipient);
    validateFTTLimit(payload.amount, payload.customerSegment);
    const fee = calculateFTTFee(payload.amount, payload.transferType);
    const result = await submitToPaymentGateway(payload, fee);
    if (!result.transactionId) throw new Error("Transaction ID not returned");
    await updateLedger(payload.accountNo, payload.amount + fee.total);
    await logAuditTrail(payload, result);
    return { status: "SUCCESS", transactionId: result.transactionId, fee };
  } catch (error) {
    await logError("FTT_FAILED", error, payload);
    throw error;
  }
};

const validateFTTDuplicateSubmission = (payload, recentTransactions) => {
  const duplicate = recentTransactions.find(t =>
    t.amount === payload.amount &&
    t.recipient === payload.recipient.accountNumber &&
    Date.now() - t.timestamp < 60000
  );
  if (duplicate) throw new Error("Duplicate transaction detected within 60 seconds");
  return true;
};
