// nav bar
fetch("/static/components/navbar.html")
.then(res => res.text())
.then(data => {
    document.getElementById("navbar").innerHTML = data;
});

// data
const posts = [
    { category: "연애", title: "남자친구랑 싸웠어요", like: 30 },
    { category: "연애", title: "짝사랑 끝냈어요", like: 50 },
    { category: "연애", title: "첫 데이트 조언 부탁해요", like: 40 },
    { category: "취업", title: "면접 후기 공유합니다", like: 60 },
    { category: "취업", title: "이력서 작성 꿀팁", like: 45 },
    { category: "취업", title: "취업 성공했어요!", like: 80 }
  ];
  
// top3 Posts
function showTopPosts() {
    const container = document.querySelector(".post");
    container.innerHTML = "";

    const categories = [...new Set(posts.map(p => p.category))];

    categories.forEach(category => {
        const topPosts = posts
          .filter(p => p.category === category)
          .sort((a, b) => b.like - a.like)
          .slice(0, 3);

        const section = document.createElement("div");

        const categoryName = document.createElement("p");
        categoryName.textContent = `${category}`;
        categoryName.classList.add("categoryName");

        section.appendChild(categoryName);

        const list = document.createElement("div");
        list.classList.add("post-list")
        
        topPosts.forEach(post => {
            const item = document.createElement("div");
            item.textContent = `${post.title}`;
            item.classList.add("post-item");
            list.appendChild(item);
        });
        section.appendChild(list);
        container.appendChild(section);
    });
}

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