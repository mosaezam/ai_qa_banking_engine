// Western Union - Transfer Details
const validateWUTransfer = (payload) => {
  if (!payload.amount || payload.amount <= 0) throw new Error("Invalid amount");
  if (payload.amount > WU_LIMIT) throw new Error("Exceeds WU transaction limit");
  if (!payload.senderDetails) throw new Error("Sender details required");
  if (payload.amount >= 3000 && !payload.sourceOfFunds) throw new Error("Source of funds required above RM3000");
  return true;
};

const calculateWUFee = (amount, destCountry) => {
  const baseFee = getWUFeeSchedule(destCountry, amount);
  const sst = baseFee * SST_RATE;
  return { fee: roundFee(baseFee), sst: roundFee(sst), total: roundFee(baseFee + sst) };
};

const validateWUDailyLimit = (amount, dailyUsed) => {
  if (amount + dailyUsed > WU_DAILY_LIMIT) throw new Error("WU daily limit of RM20000 exceeded");
  return true;
};

const WU_LIMIT = 10000;
const WU_DAILY_LIMIT = 20000;
const SST_RATE = 0.06;
