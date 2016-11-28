/**
 * Created by lyfw2 on 2016/10/29.
 */
window.onload = function () {
    sub = document.getElementById('submit');
    password2 = document.getElementById('password2');
    password = document.getElementById('password');
    username = document.getElementById('username');
    email = document.getElementById('email');
    ip_name = 'input-red';
    
    email.onblur = function () {
        checkEmail(this)
    };
    email.onfocus = function () {
        removeClassName(this, ip_name);
        insertText(this, '');
    };
    function checkEmail(elm) {
        reg = /^[\w-]+@[\w-]+(\.[0-9A-Za-z]{2,4}){1,2}$/;
        elm.value = trim(elm.value);
        if (elm.value == '') {
            insertText(elm, '不能为空');
            addClassName(elm, ip_name);
            return false;
        } else if (elm.value.length < 4 || elm.value.length > 64) {
            insertText(elm, '不能少于4位，大于64位');
            addClassName(elm, ip_name);
            return false;
        } else if (reg.test(elm.value)) {
            removeClassName(elm, ip_name);
            insertText(elm, '');
            return true;
        } else {
            insertText(elm, '不符合电子邮箱规范');
            addClassName(elm, ip_name);
            return false;
        }
    }

    username.onblur = function () {
        checkUsername(this);
    };
    username.onfocus = function () {
        insertText(this, '');
        removeClassName(this, ip_name);
    };
    function checkUsername(elm) {
        elm.value = trim(elm.value);
        if (elm.value == '') {
            insertText(elm, '用户名不能为空');
            addClassName(elm, ip_name);
            return false;
        } else if (elm.value.length < 1 || elm.value.length > 32) {
            insertText(elm, '用户名不能少于1位，大于32位');
            addClassName(elm, ip_name);
            return false;
        } else {
            insertText(elm, '');
            removeClassName(elm, ip_name);
            return true;
        }
    }

    password.onblur = function () {
        checkPassword(this);
    };
    password.onfocus = function () {
        insertText(this, '');
        removeClassName(this, ip_name);
    };
    function checkPassword(elm) {
        elm.value = trim(elm.value);
        if (elm.value == '') {
            insertText(elm, '密码不能为空');
            addClassName(elm, ip_name);
            return false;
        } else if (elm.value.length < 5 || elm.value.length > 32) {
            insertText(elm, '密码不能少于5位，多于32位');
            addClassName(elm, ip_name);
            return false;
        } else {
            insertText(elm, '');
            removeClassName(elm, ip_name);
            return true;
        }
    }

    password2.onblur = function () {
        checkConfirmPassowrd(this);
    };
    password2.onfocus = function () {
        insertText(this, '');
        removeClassName(this, ip_name);
    };
    function checkConfirmPassowrd(elm) {
        elm.value = trim(elm.value);
        if (elm.value == '') {
            insertText(elm, '验证密码不能为空');
            addClassName(elm, ip_name);
            return false;
        } else if (elm.value == password.value) {
            insertText(elm, '');
            removeClassName(elm, ip_name);
            return true;
        } else {
            insertText(elm, '两次密码不相同');
            addClassName(elm, ip_name);
            return false;
        }
    }

    sub.onclick = function () {
        if (checkEmail(email) & checkUsername(username) & checkPassword(password) & checkConfirmPassowrd(password2)) {
            return true;
        }
        return false;
    };

    
};

function createElement(elm, content) {
    e = document.createElement('p');
    e.className = 'help-block';
    text = document.createTextNode(content);
    e.appendChild(text);
    e.style.color = 'red';
    elm.parentNode.appendChild(e);
}

function insertText(elm, content) {
    if (!hasElement(elm)) {
        createElement(elm, content);
    } else {
        p = elm.parentNode.getElementsByClassName('help-block')[0];
        p.innerHTML = content;
    }
}


function hasElement(elm) {
    nodes = elm.parentNode.childNodes;
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].nodeName == 'P') {
            return true;
        }
    }
    return false;
}

function addClassName(elm, name) {
    if (!elm.className.match(new RegExp('(\\s|^)' + name + '(\\s|$)'))) {
        if (elm.className == '') {
            elm.className = name;
        } else {
            elm.className += ' ' + name;
        }
    }
}

function removeClassName(elm, name) {
    if (elm.className.match(new RegExp('(\\s|^)' + name + '(\\s|$)'))) {
        elm.className = elm.className.replace(new RegExp('(\\s|^)' + name), '');
    }
}

function trim(value) {
    return value.replace(new RegExp('(^\\s+)|(\\s+$)'), '');
}