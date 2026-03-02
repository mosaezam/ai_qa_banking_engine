// Bakong - Recipient Validation (NBC Cambodia)
const validateBakongRecipient = (recipient) => {
  if (!recipient.bakongId) throw new Error("Bakong ID required");
  if (!recipient.bankCode) throw new Error("NBC bank code required");
  if (!recipient.accountNumber) throw new Error("Account number required");
  return true;
};

const validateNBCBankCode = (code) => {
  if (!code || code.length !== 6) throw new Error("Invalid NBC bank code format");
  return checkNBCRegistry(code);
};

const getExchangeRate = (fromCurrency, toCurrency) => {
  if (!fromCurrency || !toCurrency) throw new Error("Both currencies required");
  if (toCurrency !== "KHR" && toCurrency !== "USD") throw new Error("Bakong only supports KHR and USD");
  return fetchBakongRate(fromCurrency, toCurrency);
};

const validateBakongId = (id) => {
  if (!id || id.length < 8) throw new Error("Invalid Bakong ID");
  return id.trim().toLowerCase();
};
