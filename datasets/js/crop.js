// state variables
let msg = [];
let start = 0;

window.addEventListener('load', function () {

    // Get the video element by its ID
    var video = document.getElementById("main-video");

    // Update the current time display whenever the time is updated
    video.addEventListener("timeupdate", function () {
        var endTag = document.getElementById('end');
        endTag.textContent = video.currentTime.toFixed(2);
    });

    /*
    var player = videojs('main-video');

    // Get the total number of frames in the video
    player.on('loadedmetadata', function () {
        var totalFrames = player.duration() * player.videoWidth();
        document.getElementById('frame-slider').max = totalFrames;
    });

    // Update the slider value based on video time
    player.on('timeupdate', function () {
        var currentFrame = Math.floor(player.currentTime() * player.videoWidth());
        document.getElementById('frame-slider').value = currentFrame;
    });

    // Update the video frame based on slider value
    document.getElementById('frame-slider').addEventListener('input', function () {
        var frameNumber = this.value;
        var timeInSeconds = frameNumber / player.videoWidth();
        player.currentTime(timeInSeconds);
    });
    */


});

function recordStage() {
    var light = document.querySelector('input[name="light"]:checked').value;
    var drawer = document.querySelector('input[name="drawer"]:checked').value;
    var cur_start = document.getElementById('start').textContent;
    cur_start = parseInt(cur_start, 10);
    var cur_end = document.getElementById('end').textContent;
    cur_end = parseInt(cur_end, 10);

    msg.push({
        'start': cur_start,
        'end': cur_end,
        'light': light,
        'drawer': drawer,
    });

    console.log(msg);

    setStart(cur_start);
}

function setStart(st) {
    start = st;
    document.getElementById('start').textContent = start;
}

