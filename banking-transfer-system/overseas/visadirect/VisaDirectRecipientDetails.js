// Visa Direct - Recipient Card Validation
const validateVisaCard = (cardNumber) => {
  if (!cardNumber || cardNumber.length !== 16) throw new Error("Invalid Visa card number");
  if (!luhnCheck(cardNumber)) throw new Error("Card failed Luhn validation");
  return true;
};

const getCardCountry = async (cardNumber) => {
  const bin = cardNumber.substring(0, 6);
  const result = await lookupBIN(bin);
  if (!result) throw new Error("BIN lookup failed");
  return result.country;
};

const validateVisaNetwork = async (cardNumber) => {
  const eligible = await checkVisaDirectEligibility(cardNumber);
  if (!eligible) throw new Error("Card not eligible for Visa Direct push payment");
  return true;
};

const maskCardNumber = (cardNumber) => {
  return "*".repeat(12) + cardNumber.slice(-4);
};
