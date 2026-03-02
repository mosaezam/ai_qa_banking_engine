// Bakong - Cross Border Transfer Details (Cambodia)
const validateBakongTransfer = (payload) => {
  if (!payload.amount || payload.amount <= 0) throw new Error("Invalid transfer amount");
  if (payload.amount > BAKONG_LIMIT) throw new Error("Exceeds Bakong daily limit");
  if (!payload.currency) throw new Error("Currency required for Bakong transfer");
  return true;
};

const calculateBakongFee = (amount) => {
  const fee = amount * FEE_RATE;
  const sst = fee * SST_RATE;
  return { fee: roundFee(fee), sst: roundFee(sst), total: roundFee(fee + sst) };
};

const validateBakongAmount = (amount, currency) => {
  if (currency === "KHR" && amount < MIN_KHR) throw new Error("Minimum KHR amount not met");
  if (amount <= 0) throw new Error("Amount must be positive");
  return true;
};

const BAKONG_LIMIT = 50000;
const FEE_RATE = 0.005;
const SST_RATE = 0.06;
const MIN_KHR = 4000;
