// Western Union - MTCN Generation and Confirmation
const processWUTransaction = async (payload) => {
  try {
    validateWUTransfer(payload);
    validateWURecipient(payload.recipient);
    await validateWUCompliance(payload);
    const fee = calculateWUFee(payload.amount, payload.destCountry);
    const mtcn = await submitToWUGateway(payload, fee);
    if (!mtcn) throw new Error("MTCN not generated");
    await updateLedger(payload.accountNo, payload.amount + fee.total);
    await logAuditTrail(payload, { mtcn });
    return { status: "SUCCESS", mtcn, fee };
  } catch (error) {
    await logError("WU_FAILED", error, payload);
    throw error;
  }
};

const validateMTCN = (mtcn) => {
  if (!mtcn || mtcn.length !== 10) throw new Error("Invalid MTCN format");
  return true;
};
