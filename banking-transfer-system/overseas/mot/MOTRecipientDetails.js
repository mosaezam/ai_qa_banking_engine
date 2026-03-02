// MOT - Overseas Recipient Validation
const validateMOTRecipient = (recipient) => {
  if (!recipient.swiftCode) throw new Error("SWIFT code required for overseas transfer");
  if (!recipient.bankName) throw new Error("Beneficiary bank name required");
  if (!recipient.country) throw new Error("Destination country required");
  return true;
};

const validateIBAN = (iban) => {
  if (!iban || iban.length < 15) throw new Error("Invalid IBAN format");
  return iban.replace(/\s/g, '').toUpperCase();
};

const validateSWIFTCode = (swift) => {
  const swiftRegex = /^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$/;
  if (!swiftRegex.test(swift)) throw new Error("Invalid SWIFT/BIC format");
  return true;
};

const getExchangeRate = (fromCurrency, toCurrency) => {
  if (!fromCurrency || !toCurrency) throw new Error("Currency required");
  return fetchBNMRate(fromCurrency, toCurrency);
};
