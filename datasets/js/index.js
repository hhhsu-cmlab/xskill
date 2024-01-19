window.addEventListener('load', function () {
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

});

