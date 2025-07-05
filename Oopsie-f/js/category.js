const params = new URLSearchParams(window.location.search);
const category = params.get("type");

// 버튼 색 변경 함수
document.addEventListener("DOMContentLoaded", function () {
  if (category) {
    const btns = document.querySelectorAll(".categories button");
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

document.addEventListener("DOMContentLoaded", function () {
  const params = new URLSearchParams(window.location.search);
  const sort = params.get("sort") || "popular"; // 기본값 popular

  const sortBtns = document.querySelectorAll(".order button");
  sortBtns.forEach((btn) => {
    if (btn.textContent.trim() === (sort === "popular" ? "인기순" : "최신순")) {
      btn.classList.add("active");
    }
  });
});
