// FTT - Fund Transfer & Transaction (DuitNow / IBFT)
const validateFTTTransfer = (payload) => {
  if (!payload.amount || payload.amount <= 0) throw new Error("Invalid transfer amount");
  if (payload.amount > FTT_DAILY_LIMIT) throw new Error("Exceeds FTT daily limit");
  if (!payload.recipientAccount) throw new Error("Recipient account required");
  return true;
};

const calculateFTTFee = (amount, transferType) => {
  const feeMap = { DUITNOW: 0, IBFT: 0.50, RENTAS: 2.00 };
  const fee = feeMap[transferType] || 0;
  const sst = fee > 0 ? fee * SST_RATE : 0;
  return { fee: roundFee(fee), sst: roundFee(sst), total: roundFee(fee + sst) };
};

const validateFTTLimit = (amount, segment) => {
  const limits = { STANDARD: 50000, PREMIER: 100000 };
  const limit = limits[segment] || limits.STANDARD;
  if (amount > limit) throw new Error(`Exceeds ${segment} daily limit of RM${limit}`);
  return true;
};

const FTT_DAILY_LIMIT = 100000;
const SST_RATE = 0.06;
