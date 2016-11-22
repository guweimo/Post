/**
 * Created by lyfw2 on 2016/10/27.
 */

window.onload = function () {
    body = document.getElementsByClassName('post-body');
    summary = document.getElementsByClassName('post-summary');
    retract = document.getElementsByClassName('retract');
    max_num = 120;

    for (var i = 0; i < body.length; i++) {
        body[i].style.display = 'none';
        retract[i].style.display = 'none';
        summary[i].style.display = 'block';
        if (body[i].innerText.length > max_num) {
            str = trim(body[i].innerText);
            summary[i].innerHTML = str.substring(0, max_num) + '... ';
        } else {
            summary[i].innerHTML = body[i].innerText;
        }
        a = document.createElement('a');
        a_text = document.createTextNode('显示全部');
        a.appendChild(a_text);
        addClassName(a, 'toggle-expand');
        summary[i].appendChild(a);
    }
    for (var i = 0; i < summary.length; i++) {
        summary[i].index = i;
        summary[i].onclick = function () {
            this.style.display = 'none';
            body[this.index].style.display = 'block';
            retract[this.index].style.display = 'inline-block';
        }
    }
    for (var i = 0; i < retract.length; i++) {
        retract[i].index = i;
        retract[i].onclick = function () {
            this.style.display = 'none';
            body[this.index].style.display = 'none';
            summary[this.index].style.display = 'block';
        }
    }


    function trim(str) {
        return str.replace(new RegExp('(^\\s+)|(\\s+&)'), '');
    }

}

function addClassName(elm, cls) {
    if(!elm.className.match(new RegExp('(\\s|^)' + cls + '(\\s|&)'))) {
        if (elm.className == '') {
            elm.className += cls;
        } else {
            elm.className += ' ' + cls;
        }

    }
}

function removeClassName(elm, cls) {
    if (elm.className.match(new RegExp('(\\s|^)' + cls + '(\\s|&)'))) {
        elm.className = elm.className.replace(new RegExp('(\\s|^)' + cls), '');
    }
}