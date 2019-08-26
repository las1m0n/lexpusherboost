var mmr = document.getElementById("mmr");
var corr =  document.getElementById("correction");
var screen =  document.getElementById("screen");

mmr.oninput= changeMMR;
screen.oninput = changeScreen;


function changeMMR(e) {
  console.log(mmr.value);
  var v = mmr.value;

  if (v == ""){
    corr.innerText = "Недопустимое значение";
    corr.innerHTML = "<p>Недопустимое значение</p>";
  }
  else{
    corr.innerHTML = "<p></p>";
    corr.innerText = "";
  }
}

function changeScreen(e) {
  console.log(screen.value);
  var v = screen.value;

  if (v == ""){
    corr.innerText = "Недопустимое значение";
    corr.innerHTML = "<p>Недопустимое значение</p>";
  }
  else{
    corr.innerHTML = "<p></p>";
  }
}




