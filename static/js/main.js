// nav bar
fetch("/static/components/navbar.html")
.then(res => res.text())
.then(data => {
    document.getElementById("navbar").innerHTML = data;
});



// button color active
// main.js
document.addEventListener("DOMContentLoaded", function () {
    if (category) {
      const btns = document.querySelectorAll(".categories button");
      btns.forEach((btn) => {
        if (btn.textContent.trim() === getCategoryName(category)) {
          btn.classList.add("active");
        }
      });
    }
  });
  
  // 카테고리 번호를 이름으로 매핑
  function getCategoryName(id) {
    const map = {
      1: "연애",
      2: "인간관계",
      3: "취업/커리어",
      4: "건강",
      5: "학업",
      6: "취미",
      7: "소비",
      8: "기타"
    };
    return map[id];
  }
  
  

document.addEventListener("DOMContentLoaded", showTopPosts)