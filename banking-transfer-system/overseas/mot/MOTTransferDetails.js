// MOT - Maybank Overseas Transfer (SWIFT Wire)
const validateMOTTransfer = (payload) => {
  if (!payload.amount || payload.amount <= 0) throw new Error("Invalid transfer amount");
  if (payload.amount > MOT_DAILY_LIMIT) throw new Error("Exceeds MOT daily limit");
  if (!payload.currency) throw new Error("Destination currency required");
  if (!payload.recipientAccount) throw new Error("Recipient account required");
  return true;
};

const calculateMOTFee = (amount, currency) => {
  const serviceFee = 10.00;
  const sst = serviceFee * SST_RATE;
  return { serviceFee: roundFee(serviceFee), sst: roundFee(sst), total: roundFee(serviceFee + sst) };
};

const validateMOTAmount = (amount) => {
  if (amount <= 0) throw new Error("Amount must be positive");
  if (amount > MOT_DAILY_LIMIT) throw new Error("Exceeds overseas transfer limit");
  return true;
};

const MOT_DAILY_LIMIT = 50000;
const SST_RATE = 0.06;
