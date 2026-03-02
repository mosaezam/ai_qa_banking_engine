// EIPO - Beneficiary and SWIFT Validation
const validateEIPOBeneficiary = (beneficiary) => {
  if (!beneficiary.accountNumber) throw new Error("Beneficiary account required");
  if (!beneficiary.bankCode) throw new Error("Bank code required");
  if (!beneficiary.swiftBIC) throw new Error("SWIFT/BIC code required for EIPO");
  return validateSWIFTCode(beneficiary.swiftBIC);
};

const validateSWIFTCode = (swift) => {
  const swiftRegex = /^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$/;
  if (!swiftRegex.test(swift)) throw new Error("Invalid SWIFT/BIC format");
  return true;
};

const validatePurposeCode = (code) => {
  const validCodes = ["TRADE", "SALARY", "INVESTMENT", "PERSONAL", "EDUCATION", "MEDICAL"];
  if (!validCodes.includes(code)) throw new Error(`Invalid purpose code: ${code}`);
  return true;
};

const validateEIPOSanctions = async (beneficiary) => {
  const result = await checkOFACSanctions(beneficiary.name, beneficiary.country);
  if (result.hit) throw new Error("Beneficiary flagged in OFAC sanctions list");
  return true;
};
