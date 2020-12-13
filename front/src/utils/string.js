export const fmt = (string, params) => {
  let fmtString = string;

  for (let param in params) {
    fmtString = fmtString.replace(`{${param}}`, params[param]);
  }

  return fmtString;
}
