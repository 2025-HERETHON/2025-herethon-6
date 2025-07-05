const params = new URLSearchParams(window.location.search);
const category = params.get("type");

// 버튼 색 변경 함수
document.addEventListener("DOMContentLoaded", function () {
    if (category) {
      const btns = document.querySelectorAll(".categories button")
      btns.forEach((btn) => {
        if (btn.textContent.trim() === category) {
            btn.classList.add("active");
        }
      });
    }


// nav bar 
fetch("../components/navbar.html")
    .then((res) => res.text())
    .then((data) => {
    document.getElementById("navbar").innerHTML = data;
    });
});