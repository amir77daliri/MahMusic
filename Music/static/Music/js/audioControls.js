let audio = document.querySelector('#audio');
let prev = document.querySelector('#prev');
let next = document.querySelector('#next');
let playBtn = document.querySelector('#play-btn');
let stopBtn = document.querySelector('#stop-btn');
let addFavoritBtn = document.querySelector('#add-favorit');
let soundRange = document.querySelector('#sound-range');
let audioDurationRange = document.querySelector('#duration-time');
let unMuteBtn = document.querySelector('#audio-unmute');
let muteBtn = document.querySelector('#audio-mute');
let currentStatus = 'stop';
console.log(audioDurationRange)
function handleSound(){
    let sound = soundRange.value;
    audio.volume = sound;

}

function handlePlay() {
    if(currentStatus === 'stop') {
        currentStatus = 'play';
        playBtn.classList.remove('active');
        stopBtn.classList.add('active');
        audio.play();
    }else if (currentStatus === 'play') {
        currentStatus = 'stop';
        stopBtn.classList.remove('active');
        playBtn.classList.add('active');
        audio.pause();
    }
}

function handleMute() {
    if(!audio.muted){
        audio.muted = true;
        unMuteBtn.classList.remove('active');
        muteBtn.classList.add('active')

    }else {
        audio.muted = false;
        muteBtn.classList.remove('active');
        unMuteBtn.classList.add('active');
    }
}

function handleTime() {
    const time = audioDurationRange.value;

    audio.currentTime = time    
}

setInterval(() => {
    audioDurationRange.value = audio.currentTime;
}, 1000)


audioDurationRange.addEventListener('input', handleTime)
playBtn.addEventListener('click', handlePlay);
stopBtn.addEventListener('click', handlePlay);
unMuteBtn.addEventListener('click', handleMute);
muteBtn.addEventListener('click', handleMute);
soundRange.addEventListener('input', handleSound)
