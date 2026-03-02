// Visa Direct - Push Payment Transfer
const validateVisaDirectTransfer = (payload) => {
  if (!payload.amount || payload.amount <= 0) throw new Error("Invalid amount");
  if (payload.amount > VISA_LIMIT) throw new Error("Exceeds Visa Direct limit");
  if (!payload.recipientCardNumber) throw new Error("Recipient Visa card number required");
  if (payload.amount > 10000 && !payload.purposeCode) throw new Error("Purpose code required above RM10000");
  return true;
};

const calculateVisaFee = (amount) => {
  const fee = amount * VISA_FEE_RATE;
  const sst = fee * SST_RATE;
  return { fee: roundFee(fee), sst: roundFee(sst), total: roundFee(fee + sst) };
};

const validateVisaPurposeCode = (code) => {
  const valid = ["PERSONAL", "BUSINESS", "SALARY", "INVESTMENT"];
  if (!valid.includes(code)) throw new Error("Invalid Visa Direct purpose code");
  return true;
};

const VISA_LIMIT = 25000;
const VISA_FEE_RATE = 0.005;
const SST_RATE = 0.06;
