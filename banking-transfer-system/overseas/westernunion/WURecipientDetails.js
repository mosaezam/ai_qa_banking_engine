// Western Union - Recipient and Compliance Validation
const validateWURecipient = (recipient) => {
  if (!recipient.firstName || !recipient.lastName) throw new Error("Full name required");
  if (!recipient.country) throw new Error("Destination country required");
  if (!recipient.idType || !recipient.idNumber) throw new Error("Recipient ID required for WU compliance");
  return true;
};

const validateWUCompliance = (payload) => {
  if (!payload.purposeOfTransfer) throw new Error("Purpose of transfer required");
  return checkOFACSanctions(payload.recipientName, payload.country);
};

const validateOFAC = (name, country) => {
  if (!name || !country) throw new Error("Name and country required for OFAC screening");
  return fetchOFACScreening(name, country);
};

const validateWUPurposeCode = (purpose) => {
  const valid = ["FAMILY_SUPPORT", "EDUCATION", "MEDICAL", "BUSINESS", "GIFT"];
  if (!valid.includes(purpose)) throw new Error("Invalid WU purpose code");
  return true;
};
