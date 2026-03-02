// EIPO - Electronic Interbank Payment Order
const validateEIPOTransfer = (payload) => {
  if (!payload.amount || payload.amount <= 0) throw new Error("Invalid EIPO amount");
  if (payload.amount > EIPO_LIMIT) throw new Error("Exceeds EIPO transaction limit");
  if (!payload.beneficiaryBank) throw new Error("Beneficiary bank required");
  if (!payload.purposeCode) throw new Error("Purpose code required for EIPO");
  if (!payload.chargeType) throw new Error("Charge type OUR/SHA/BEN required");
  return true;
};

const calculateEIPOCharges = (amount, chargeType) => {
  const rates = { OUR: 0.003, SHA: 0.0015, BEN: 0 };
  const fee = amount * (rates[chargeType] || rates.SHA);
  const sst = fee * SST_RATE;
  return { fee: roundFee(fee), sst: roundFee(sst), chargeType };
};

const validateChargeType = (chargeType) => {
  const valid = ["OUR", "SHA", "BEN"];
  if (!valid.includes(chargeType)) throw new Error("Invalid charge type — must be OUR, SHA or BEN");
  return true;
};

const EIPO_LIMIT = 100000;
const SST_RATE = 0.06;
