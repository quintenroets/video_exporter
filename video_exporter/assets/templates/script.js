var active = false;
var multiple = false;

var id = 'school-position-' + window.location.href;
var id_done = id + 'done'
var position = window.localStorage.getItem(id);

const defaultImplementation = function(seconds, guide) {
    seconds = seconds < 0 ? 0 : seconds;
    let s = Math.floor(seconds % 60);
    let m = Math.floor(seconds / 60 % 60);
    let h = Math.floor(seconds / 3600);
    const gm = Math.floor(guide / 60 % 60);
    const gh = Math.floor(guide / 3600);

    // handle invalid times
    if (isNaN(seconds) || seconds === Infinity) {
        // '-' is false for all relational operators (e.g. <, >=) so this setting
        // will add the minimum number of fields specified by the guide
        h = m = s = '-';
        }
    // Check if we need to show hours
    h = (h > 0 || gh > 0) ? h + ':' : '';

    // If hours are showing, we may need to add a leading zero.
    // Always show at least one digit of minutes.
    m = (((h || gm >= 10) && m < 10) ? '0' + m : m) + ':';
    // Check if leading zero is need for seconds
    s = (s < 10) ? '0' + s : s;
    return h + m + s;
};
    

function formatTime(seconds, guide){
    let rate = window.localStorage.getItem("videospeed") || 1;
    seconds = seconds / rate;
    guide = guide / rate;
    return defaultImplementation(seconds, guide);
}


videojs.setFormatTime(formatTime)


function setup(video_el){
    var player = videojs(video_el);
    
    if (position){
        var old_onload = window.onload;
    }
    
    player.on('loadedmetadata', function() {
        let ratio = player.videoWidth() / player.videoHeight();
        if (ratio < 4/3 + 0.01){
            let video = document.getElementById(video_id);
            video.className = video.className.replace("vjs-16-9", "vjs-4-3");
            document.getElementsByClassName("videocontent")[0].className = "videocontentsmall";
        }
    });
    
    player.on('seeking', function(t) {
        if (player.scrubbing() && multiple){
            for(var i = 0, max = videos.length; i < max; i++) {
                let other_player = players[i];
                if (other_player != player){
                    other_player.currentTime(player.currentTime());
                }
            }
        }
    });
    
    player.on('pause', function(t) {
        if (multiple && !document.hidden){
            for(var i = 0, max = videos.length; i < max; i++) {
                let other_player = players[i];
                if (other_player != player){
                    other_player.pause();
                }
            }
        }
    });
        
    player.on('play', function() {
        active = true;
        if (!multiple){
            if(!player.isFullscreen()){
                player.requestFullscreen();
            }
        } else {
            for(var i = 0, max = videos.length; i < max; i++) {
                let other_player = players[i];
                if (other_player != player){
                    other_player.play();
                }
            }
        }
        window.localStorage.setItem(id_done, false);
    });

    player.on('ended', function() {
        window.localStorage.setItem(id_done, true);
        if (!multiple){
            player.exitFullscreen();
        }
    });
    return player;
}

var players = [];
videos = document.getElementsByTagName("video");
for(var i = 0, max = videos.length; i < max; i++) 
{
    let player = setup(videos[i]);
    players.push(player);
    if (i>0){
        //player.muted(true);
        multiple = true;
    }
} 
