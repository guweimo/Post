/**
 * Created by lyfw2 on 2016/10/31.
 */


window.onload = function () {
    var upload_input = document.getElementsByClassName('upload_pic')[0];
    var upload_reset = document.getElementsByClassName('upload-reset')[0];
    if (typeof FileReader === 'undefined') {
        upload_input.setAttribute('disabled', 'disabled');
    } else {
        upload_input.addEventListener('change', readFile, false);
    }

    function readFile() {
        var file = this.files[0];
        if (!/image\/\w+/.test(file.type)) {
            alert('文件必须为图片');
            return false;
        }
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function(e) {
            var image = new Image();
            image.src = e.target.result;
            var max=200;
            image.onload = function(){
                var canvas = document.getElementById("cvs");
                var ctx = canvas.getContext("2d");
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(image, 0, 0, 200, 200);
            };
        }
    }

    upload_reset.onclick = function() {
        var canvas = document.getElementById("cvs");
        var ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
};

