function updateInput(val, el) {
  document.getElementById(el + "-disp").innerHTML = val;
}

function calculate() {
  const INFLATION = 0.04;
  const ROI = 0.075;
  const SUPER_CONTRIB = 0.12;
  const FEE = 74;
  const TAX = 0.07;

  var drawAmount = document.getElementById("draw-amount").value;
  var currAge = document.getElementById("my-age").value;
  var retAge = document.getElementById("ret-age").value;
  var income = document.getElementById("income").value;
  var currBalance = parseFloat(document.getElementById("curr-super").value);
  var tgtBalance = parseFloat(document.getElementById("tgt-ret").value);

  const n = retAge - currAge;

  var fees = 0;
  for (var i = 0; i < n; i++) {
    fees = fees + FEE * (1 - INFLATION) ** i;
  }

  var fv = drawAmount * (1 + (ROI - INFLATION - 0.0085)) ** n - fees;

  var contrib = income * SUPER_CONTRIB;

  var curr = currBalance;
  var remaining = 0;
  while (curr < tgtBalance) {
    curr = curr * (1 + ROI - INFLATION - 0.0085);
    curr += contrib - FEE;
    remaining++;
  }

  var endBalance = currBalance;
  for (var i = 0; i < n; i++) {
    endBalance = endBalance * (1 + ROI - INFLATION - 0.0085);
    endBalance += contrib - FEE;
  }

  console.log(fv); // how much final super will decrease by
  console.log(remaining); // how many years to reach target
  console.log(endBalance); // final super balance at given retirement age

  document.getElementById("penalty").innerHTML =
    "<strong>$" + Math.round(fv) + "</strong>";
  document.getElementById("target").innerHTML =
    "<strong>" + remaining + " years</strong>";
  document.getElementById("endBalance").innerHTML =
    "<strong>$" + Math.round(endBalance) + "</strong>";

  document.getElementById("feedback").classList.toggle("show");
}
