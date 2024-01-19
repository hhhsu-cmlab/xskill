// state variables
let msg = [];

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

    document.getElementById("ok").addEventListener("click", () => {
        recordStage();
    })
});

function recordStage() {
    var cur_start = document.getElementById('start').textContent;
    var cur_end = document.getElementById('end').textContent;

    msg.push({
        'start': parseFloat(cur_start, 10),
        'end': parseFloat(cur_end, 10),
    });

    new_time_str = `(${cur_start}, ${cur_end})`;
    document.getElementById("timestamps-display").innerHTML += new_time_str + " ";
    
    document.getElementById("content").value = JSON.stringify(msg);

    document.getElementById('start').textContent = cur_end;
}

