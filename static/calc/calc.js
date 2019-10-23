var fromMMR = document.getElementById("input-mmr-from");
var toMMR = document.getElementById("input-mmr-to");
var rangeSlider = document.getElementById("slider");
var rangeBullet = document.getElementById("slider-label");
var priceDiv = document.getElementById("price");
var priceHidden =  document.getElementById("price_hidden");
var is_core =  document.getElementById("cbx");
var is_quick =  document.getElementById("cdx");


var PRICELIST = [
    [1,     500,    1.50],
    [501,   1000,   1.54],
    [1001,  1500,   1.60],
    [1501,  2500,   1.70],
    [2501,  3500,   2.30],
    [3501,  4000,   3.04],
    [4001,  4500,   3.74],
    [4501,  4900,   5.25],
    [4901,  5000,   6.00],
    [5001,  5100,   7.50],
    [5101,  5200,   8.10],
    [5201,  5300,   8.90],
    [5301,  5400,   9.50],
    [5401,  5500,   10.90],
    [5501,  5600,   14.44],
    [5601,  5700,   16.36],
    [5701,  5800,   17.98],
    [5801,  5900,   20.20],
    [5901,  6000,   25.04],
];

fromMMR.oninput= changeFromMMR;
toMMR.oninput = changeToMMR;
rangeSlider.oninput = changeSlider;
is_core.oninput = changeTypeBoost;
is_quick.oninput = changeQuick;
is_quick.value = "off";
changeSlider();


function changeTypeBoost(e) {
    if (is_core.checked != true) {
        is_core.value = "off";
        changePrice();
    }
    else {
        is_core.value = "on";
        changePrice();
    }
}

function changeQuick(e) {
    if (is_quick.checked != true) {
        is_quick.value = "off";
        changePrice();
    }
    else {
        is_quick.value = "on";
        changePrice();
    }
    console.log(is_quick.value);
}

function changeFromMMR(e) {
  var v = +fromMMR.value;

  if (v < 0)
    fromMMR.value = 1;
  if (v > 5975)
    fromMMR.value = 5975;

  rangeSlider.max = 6000 - v;
  toMMR.value = +rangeSlider.value + v;
  changeLabel();
  changeTypeBoost();
  changePrice();

  if (v < 0 || v > 5975)
    return false;
}

function changeToMMR(e) {
  var v = +toMMR.value;

  rangeSlider.value= v - fromMMR.value;
  changeLabel();
  changeTypeBoost();
  changePrice();

  if (v < 1 || v > 6000)
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
  changeTypeBoost();
  changePrice();
}


function changePrice() {
   var from = +fromMMR.value;
    var to = +toMMR.value;

    var price = 0;
    for (var i=from; i<=to; i++) {
        for (var j of PRICELIST) {
            if (i > j[0] && i < j[1]) {
                if (is_quick.value == "on" & is_core.value == "on") {
                    price += (j[2]*1.25*1.2);
                    break;
                }
                else if (is_quick.value == "off" & is_core.value == "on"){
                    price += (j[2]*1.25);
                    break;
                }
                else if (is_quick.value == "on" & is_core.value == "off"){
                    price += (j[2]*1.20);
                    break;
                }
                else if(is_quick.value == "off" & is_core.value == "off"){
                    price += (j[2]);
                    break;
                }
            }
        }
    }
    priceDiv.innerText = Math.round(price);
    priceHidden.value = Math.round(price);
}



