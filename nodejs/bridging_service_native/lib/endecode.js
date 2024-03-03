/*
 *   Library for Encrypt and Descrypt String
 *
 * @version 0.1.2
 * @author Vinsha/Bailey
 * @copyright Stratevision 2019
 
 */

const base64 = require("./base64.js");
const md5 = require("md5");

const scrambleBase64 = (string) => {
  const str = string.replace(/=/g, "")
  const splitPoint = 5;
  const line1 = str.substr(0, splitPoint);
  const line2 = str.substr(splitPoint)
  return line2 + line1 + ((line1.length + line2.length) % 2 == 1?"=":"")
};

const unscrambleBase64 = (string) => {
  const str = string.replace(/=/g, "")
  const splitPoint = str.length - 5;
  const line1 = str.substr(0, splitPoint);
  const line2 = str.substr(splitPoint)
  return line2 + line1
};

/**
 * 解密
 * @param {string} data 待解密字串
 * @returns {string} 解密結果
 */
const strdecode = data => {
  let key = md5("650521256");
  let string = base64.decode(unscrambleBase64(data));
  let len = key.length;
  let code = "";
  for (let i = 0; i < string.length; i++) {
    let k = i % len;
    code += String.fromCharCode(string.charCodeAt(i) ^ key.charCodeAt(k));
  }
  return base64.decode(code);
};

/**
 * 加密
 * @param {string} strings 待加密字串
 * @returns {string} 加密結果
 */
const strencode = strings => {
  let key = "59d5435b13db530ad50a4ae44391a2c0";
  let string = base64.encode(strings);
  let len = key.length;
  let code = "";
  for (let i = 0; i < string.length; i++) {
    let k = i % len;
    code += String.fromCharCode(string.charCodeAt(i) ^ key.charCodeAt(k));
  }
  return scrambleBase64(base64.encode(code));
};

module.exports = {
  strdecode,
  strencode
};
