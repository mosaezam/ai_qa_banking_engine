// FTT - Recipient Account Validation
const validateFTTRecipient = (recipient) => {
  if (!recipient.accountNumber) throw new Error("Account number required");
  if (!recipient.bankCode) throw new Error("Bank code required");
  if (!recipient.accountName) throw new Error("Account name required for FTT");
  return true;
};

const validateDuitNowId = (id, idType) => {
  const validTypes = ["MOBILE", "NRIC", "PASSPORT", "BUSINESS_REG", "VIRTUAL_ACCOUNT"];
  if (!validTypes.includes(idType)) throw new Error("Invalid DuitNow ID type");
  if (!id) throw new Error("DuitNow ID value required");
  return true;
};

const lookupAccountName = async (accountNo, bankCode) => {
  const result = await fetchAccountProxy(accountNo, bankCode);
  if (!result) throw new Error("Account not found in interbank directory");
  return result.accountName;
};

const validateIBFTBank = (bankCode) => {
  if (!bankCode || bankCode.length !== 4) throw new Error("Invalid bank code format");
  return checkIBFTDirectory(bankCode);
};
