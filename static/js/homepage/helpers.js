export function str2Object (str) {
  if (!str || typeof str === 'undefined') {
    return {};
  }

  const jsonStr = str.replaceAll("'", '"').replace(/(\w+:)|(\w+ :)/g, function(matchedStr) {
    return '"' + matchedStr.substring(0, matchedStr.length - 1) + '":';
  });

  return JSON.parse(jsonStr); //converts to a regular object
};
