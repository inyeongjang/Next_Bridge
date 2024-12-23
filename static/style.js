/*document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("background-container");

    const images = [
    "url('/static/img/background_img(1).png')",
    "url('/static/img/background_img(2).png')",
    "url('/static/img/background_img(3).png')",
    ];

    let currentIndex = 0;

    function changeBackgroundImage() {
      container.style.backgroundImage = images[currentIndex];
      container.style.backgroundSize = "cover";
      container.style.backgroundPosition = "center";
      currentIndex = (currentIndex + 1) % images.length;
    }

    setInterval(changeBackgroundImage, 3000);
    changeBackgroundImage();
  });
  */
  /* ----------- 이미지 변환 ---------- */

  
      // 모든 .nav-link에 클릭 이벤트 추가
      document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(event) {
            // 모든 .nav-link에서 active 클래스 제거
            document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active'));
            
            // 클릭된 링크에 active 클래스 추가
            this.classList.add('active');
        });
    });
  /* ----------- 클릭 시 색 변환  ---------- */