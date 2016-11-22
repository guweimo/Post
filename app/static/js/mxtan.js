/**
 * Created by lyfw2 on 2016/10/26.
 */

window.onload = function() {
    sbt = document.getElementById('submit');
    subject = document.getElementById('subject');
    body = document.getElementById('body');
    submit.onclick = function () {
        if(subject.value == '' && body.innerText == '') {
            createP(subject);
            createP(body);
            return false
        }
    }

    function createP(elm) {
        name = 'input-red'
        p = document.createElement('p');
        p.className = 'help-block';
        text = document.createTextNode('不能为空');
        p.appendChild(text);
        p.style.color = 'red';
        if (!hasChildNode(elm)) {
            elm.parentNode.appendChild(p);
        } else {
            hl = document.getElementsByClassName('help-block')[0];
            hl.innerHTML = '不能为空';
        }
        addClassName(elm, name);
    }



    function hasChildNode(elm) {
        cNodes = elm.parentNode.childNodes;
        for(var i = 0; i < cNodes.length; i++) {
            if (cNodes[i].nodeName == 'P') {
                return true
            }
        }
        return false
    }

    

}


function addClassName(elm, name) {
    if (!elm.className.match(new RegExp('(\\s|^)' + name + '(\\s|&)'))) {
        if (elm.className == '') {
            elm.className = name;
        } else {
            elm.className += ' ' + name;
        }
    }
}

function removeClassName(elm, name) {
    if (elm.className.match(new RegExp('(\\s|^)' + name + '(\\s|&)'))) {
        elm.className = elm.className.replace(new RegExp('(\\s|^)' + name), '');
    }
}