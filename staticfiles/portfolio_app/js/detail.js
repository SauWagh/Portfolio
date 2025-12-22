let slideIndex = 0;
const slides = document.querySelectorAll('.slide');

function showSlide(n) {
    slides.forEach(s => s.classList.remove('active'));
    slides[n].classList.add('active');
    slideIndex = n;
}

function changeSlide(n) {
    slideIndex += n;
    if(slideIndex >= slides.length) slideIndex = 0;
    if(slideIndex < 0) slideIndex = slides.length - 1;
    showSlide(slideIndex);
}

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
