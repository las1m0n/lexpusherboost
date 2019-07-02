var fromMMR = document.getElementById("input-mmr-from");
var toMMR = document.getElementById("input-mmr-to");
var rangeSlider = document.getElementById("slider");
var rangeBullet = document.getElementById("slider-label");
var priceDiv = document.getElementById("price");

var PRICELIST = [
    [1,     500,    1.50],
    [501,   1000,   1.54],
    [1001,  1500,   1.54],
    [1501,  2500,   1.70],
    [2501,  3500,   2.20],
    [3501,  4000,   3.04],
    [4001,  4500,   3.74],
    [4501,  4900,   5.25],
    [4901,  5000,   6.00],
    [5001,  5100,   7.50],
    [5101,  5200,   8.10],
    [5201,  5300,   8.90],
    [5301,  5400,   9.50],
    [5401,  5500,   1.080],
    [5501,  5600,   1.450],
    [5601,  5700,   1.590],
    [5701,  5800,   1.795],
    [5801,  5900,   1.975],
    [5901,  6000,   2.250],
];

fromMMR.oninput= changeFromMMR;
toMMR.oninput = changeToMMR;
rangeSlider.oninput = changeSlider;
changeSlider();


function changeFromMMR(e) {
    console.log(fromMMR.value);
  var v = +fromMMR.value;

  if (v < 0)
    fromMMR.value = 1;
  if (v > 6475)
    fromMMR.value = 6475;

  rangeSlider.max = 6500 - v;
  toMMR.value = +rangeSlider.value + v;
  changeLabel();
  changePrice();

  if (v < 0 || v > 6475)
    return false;
}

function changeToMMR(e) {
  var v = +toMMR.value;

  if (v < 1)
    toMMR.value = 1;
  if (v > 6500)
    toMMR.value = 6500;

  rangeSlider.value= v - fromMMR.value;
  console.log(rangeSlider.value);
  changeLabel();
  changePrice();

  if (v < 1 || v > 6500)
    return false;

}


function changeLabel() {
  var v = +rangeSlider.value;
  rangeBullet.innerHTML = "+" + v;
  rangeBullet.style.left = (v / (rangeSlider.max - rangeSlider.min) * 100) + "%";
}

function changeSlider() {
  var v = +rangeSlider.value;
  toMMR.value = +fromMMR.value + v;
  changeLabel();
  changePrice();
}

function changePrice() {
    var from = +fromMMR.value;
    var to = +toMMR.value;

    var price = 0;
    for (var i=from; i<=to; i++) {
        for (var j of PRICELIST) {
            if (i > j[0]) {
                price += j[2];
                break;
            }
        }
    }

    priceDiv.innerText = price + " ₽";
}



