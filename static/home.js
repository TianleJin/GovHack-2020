// prettier-ignore
const med = [[218, 893, 4220.5,	14050.5, 24563.5,	32743.5, 39582, 45656.5, 62060, 140897,	272347.5, 276766.5, 188741.5],
[1299, 3885, 9569, 18885, 28684.5, 37451.5, 45414, 54997, 73032.5, 105045.5, 145830, 185190, 155186],
[3014, 11515, 25591, 44037, 62674, 80083, 96402, 113099, 136006, 156636, 169983, 234170, 302287],
[10853, 16492, 46624, 77835, 114056, 152008, 191468, 236722, 294607, 349273, 410292, 579115, 654138],
[20766, 6931, 52895, 108952, 166696, 231523, 308285, 411255, 569072, 816497, 1021877, 1245259, 1259708]]

// prettier-ignore
const maxsup = [[265, 926, 4886, 16018, 25597, 34597, 45698, 53843, 70741, 153549, 273103, 287182, 194374],
[1480, 4042, 10854, 22572, 32927, 38786, 46813, 58280, 77767, 112336, 153022, 190888, 165593],
[3169, 11646, 25930, 45220, 63891, 82221, 102769, 122389, 146524, 164446, 169995, 246254, 312854],
[18273, 22340, 48582, 80154, 115460, 155567, 198743, 244881, 307104, 356512, 443566, 649387, 665255],
[38586, 10418, 65597, 117364, 175727, 244928, 322471, 426415, 590476, 830835, 1055104, 1263161, 1356455]]

// prettier-ignore
const minsup = [[171, 860, 3555, 12083, 23530, 30890, 33466, 37470, 53379, 128245, 271592, 266351, 183109],
[1118, 3728, 8284, 15198, 24442, 36117, 44015, 51714, 68298, 97755, 138638, 179492, 144779],
[2859, 11385, 25253, 42855, 61458, 77945, 90036, 103809, 125488, 148827, 169972, 222086, 291721],
[3433, 10644, 44667, 75516, 112653, 148449, 184193, 228563, 282111, 342035, 377019, 508844, 643021],
[2947, 3444, 40193, 100540, 157665, 218119, 294099, 396095, 547668, 802159, 988651, 1227357, 1162961]]

const SUPER_DATA = { minsup, maxsup, med };
/*
columns are age brackets
[<18, 18-24, 25-29, 30-34, 35-39, 40-44, 45-49, 50-54, 55-59, 60-64, 65-69, 70-74, 75+]
[ 0     1      2      3      4      5      6      7      8      9      10     11   12 ]

25 30 35 40 45 50 55 60
0  1   2  3  4

rows are income brackets
a. $18,200 or less
b. $18,201 to $37,000
c. $37,001 to $87,000
d. $87,001 to $180,000
e. $180,001 or more
*/

function getCol(val) {
  if (val < 18) {
    return 0;
  } else if (val < 25) {
    return 1;
  }
  ans = 5 * Math.floor(val / 5);
  ans -= 25;
  ans = ans / 5;
  return Math.min(12, ans + 2);
}

function getRow(val) {
  if (val < 18200) {
    return 0;
  } else if (val < 37000) {
    return 1;
  } else if (val < 87000) {
    return 2;
  } else if (val < 180000) {
    return 3;
  } else {
    return 4;
  }
}

function updateInput(val, el) {
  document.getElementById(el + "-disp").innerHTML = val;
  calculate();
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

  var fv = Math.max(0, drawAmount * (1 + (ROI - INFLATION - 0.0085)) ** n - fees);

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

  document.getElementById("penalty").innerHTML =
    "<strong>$" + Math.round(fv).toLocaleString() + "</strong>";
  document.getElementById("target").innerHTML =
    "<strong>" + remaining + " years</strong>";
  document.getElementById("endBalance").innerHTML =
    "<strong>$" + Math.round(endBalance).toLocaleString() + "</strong>";

  var healthMin = Math.round(
    SUPER_DATA.minsup[getRow(income)][getCol(currAge)] / 2
  );
  var healthMax = SUPER_DATA.maxsup[getRow(income)][getCol(currAge)] * 2;
  document.getElementById("healthlow").innerHTML =
    "$" + healthMin.toLocaleString();
  document.getElementById("healthhigh").innerHTML =
    "$" + healthMax.toLocaleString();

  pct = Math.max(
    1,
    Math.min(99, (100 * currBalance) / (healthMin + healthMax))
  );
  document.getElementById("marker").style.left = pct + "%";

  var numPlanes = Math.round(fv / 3000);
  var node = document.getElementById("planes");
  node.innerHTML =
    "<h5>In retirement, this will cost you ~" + numPlanes + " holidays</h5>";

  var plane = document.createElement("img");
  plane.src = "static/img/plane.png";
  plane.style = "height: 35px; padding: 3px;"
  for (var i = 0; i < numPlanes; i++) {
    node.appendChild(plane.cloneNode(true));
  }

  document.getElementById("feedback").classList.add("show");
}
