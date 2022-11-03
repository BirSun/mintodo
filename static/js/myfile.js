document.getElementById('demo').innerHTML = "This was created with Javascript";


 let modalBtns = [...document.querySelectorAll(".button")];
      modalBtns.forEach(function (btn) {
        btn.onclick = function () {
          let modal = btn.getAttribute("data-modal");
          document.getElementById(modal).style.display = "block";
        };
      });
      let closeBtns = [...document.querySelectorAll(".close")];
      closeBtns.forEach(function (btn) {
        btn.onclick = function () {
          let modal = btn.closest(".modal");
          modal.style.display = "none";
        };
      });
      window.onclick = function (event) {
        if (event.target.className === "modal") {
          event.target.style.display = "none";
        }
      };

function update1(){
  select = document.getElementById("picker");
  display = document.getElementById("nam");
  display1 = document.getElementById("info");
  display2 = document.getElementById("category");

  const myArray = select.value.split("-");

  display.value = myArray[0];
  display1.value = myArray[1];
  display2.value = myArray[2];

  }



