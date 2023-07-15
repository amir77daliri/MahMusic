let slides = document.querySelectorAll('.slide')
let points = document.querySelector('.points')
points = Array.from(points.children)

let currentSlide = 0;
points.forEach((point, index) => {
    point.addEventListener('click', e => {
        currentSlide = index;
        removeActive();
        points[index].classList.add('active')
        showSlide(index)
    })
})


function removeActive() {
    for(let i=0; i< points.length;i++){
        points[i].classList.remove('active')
    }
}

function showSlide(index) {
    let item;
    for(item=0; item<slides.length;item++){
        slides[item].classList.remove('active')

    }
    removeActive()
    slides[index].classList.add('active')
    points[index].classList.add('active')
}

function changeSlide() {
    currentSlide += 1;
    if(currentSlide > 2) {
        currentSlide = 0;
    }
    showSlide(currentSlide)    
}

setInterval(changeSlide, 3000);