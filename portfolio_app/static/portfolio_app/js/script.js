const mediaQuery = window.matchMedia("(max-width: 768px)");

let animationRunning = false;
let dots = [];
let animationId = null;

function startAnimation() {
  if (animationRunning) return;
  animationRunning = true;

  const DOT_COUNT = 16;

  for (let i = 0; i < DOT_COUNT; i++) {
    const el = document.createElement("div");
    el.className = "dot";

    el.style.background =
      "linear-gradient(135deg,rgba(255,255,255,0.35),rgba(255,255,255,0.1))";
    el.style.backdropFilter = "blur(8px)";
    el.style.border = "1px solid rgba(255,255,255,0.35)";
    el.style.boxShadow =
      "0 0 12px rgba(255,255,255,0.45), inset 0 0 6px rgba(255,255,255,0.25)";

    el.style.width = "12px";
    el.style.height = "12px";
    el.style.borderRadius = "50%";
    el.style.position = "fixed";

    document.body.appendChild(el);
    dots.push({ el, x: innerWidth / 2, y: innerHeight / 2 });
  }

  let mouseX = innerWidth / 2,
    mouseY = innerHeight / 2;

  window.addEventListener("mousemove", (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  function animate() {
    let prevX = mouseX,
      prevY = mouseY;

    dots.forEach((d, i) => {
      d.x += (prevX - d.x) * (0.18 + i * 0.01);
      d.y += (prevY - d.y) * (0.18 + i * 0.01);
      d.el.style.left = d.x + "px";
      d.el.style.top = d.y + "px";
      prevX = d.x;
      prevY = d.y;
    });

    animationId = requestAnimationFrame(animate);
  }

  animate();
}

function stopAnimation() {
  animationRunning = false;
  cancelAnimationFrame(animationId);

  dots.forEach((d) => d.el.remove());
  dots = [];
}

// Initial check
if (!mediaQuery.matches) {
  startAnimation();
}

// Listen for screen size change
mediaQuery.addEventListener("change", (e) => {
  if (e.matches) {
    // Mobile
    stopAnimation();
  } else {
    // Desktop
    startAnimation();
  }
});


document.addEventListener("DOMContentLoaded", function () {

    const buttons = document.querySelectorAll(".tab-button");
    const panels = document.querySelectorAll(".skills-panels .panel");

    buttons.forEach(btn => {
        btn.addEventListener("click", () => {

            document.querySelector(".tab-button.active")?.classList.remove("active");
            btn.classList.add("active");

            const category = btn.dataset.category;

            panels.forEach(p => {
                p.classList.remove("active");

                if (p.dataset.panel === category) {
                    p.classList.add("active");
                }
            });

        });
    });

});


// ----Details---------

let slideIndex = 0;
const slides = document.querySelectorAll('.slide');

function showSlide(n) {
    slides.forEach(s => s.classList.remove('active'));
    slides[n].classList.add('active');
    slideIndex = n;
}

// Previous/Next buttons
function changeSlide(n) {
    slideIndex += n;
    if(slideIndex >= slides.length) slideIndex = 0;
    if(slideIndex < 0) slideIndex = slides.length - 1;
    showSlide(slideIndex);
}

// Swap top media when a thumbnail is clicked
function changeMainMedia(url, type) {
    const container = document.querySelector('.top-media-container');
    container.innerHTML = ''; 

    if(type === 'image') {
        const img = document.createElement('img');
        img.src = url;
        img.className = 'project-media';
        container.appendChild(img);
    } else if(type === 'video') {
        const video = document.createElement('video');
        video.className = 'project-media';
        video.controls = true;

        const source = document.createElement('source');
        source.src = url;
        source.type = 'video/mp4';
        video.appendChild(source);

        container.appendChild(video);
    }
}


// log In
function openLogin() {
    document.getElementById('loginModal').style.display = 'block';
}

function closeLogin() {
    document.getElementById('loginModal').style.display = 'none';
}

window.onclick = function(e) {
    const modal = document.getElementById('loginModal');
    if (e.target === modal) {
        modal.style.display = 'none';
    }
};
