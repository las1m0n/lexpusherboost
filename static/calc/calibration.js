var rangeSlider = document.getElementById("slider");
var rangeBullet = document.getElementById("slider-label");
var priceDiv = document.getElementById("price");
var priceHidden =  document.getElementById("price_hidden");
var fromMMR = document.getElementById("input-mmr-from");


var PRICELIST = [
    [1,     1000,   900],
    [1001,  2000,   900],
    [2001,  3000,   1100],
    [3001,  4000,   1100],
    [4001,  5000,   1150],
    [5001,  5500,   1300],
];

fromMMR.oninput = changeFromMMR;
rangeSlider.oninput = changeSlider;
changeFromMMR();
changeSlider();

function changeFromMMR(e) {
  var v = +fromMMR.value;

  if (v < 0)
    fromMMR.value = 1;
  if (v > 5499)
    fromMMR.value = 5499;

  rangeSlider.value = +fromMMR.value;
  changePrice();
  if (v < 0 || v > 5500)
    return false;
}

function changeSlider() {
  fromMMR.value = +rangeSlider.value;
  changePrice();
}

function changePrice() {
    var from = +fromMMR.value;

    var price = 0;
    for (var j of PRICELIST) {
        if (from >= j[0] && from <= j[1]) {
                price = +j[2];
                break;
            }
        }
    priceDiv.innerText = Math.round(price) + " ₽";
    priceHidden.value = Math.round(price);
}



