function Getxmlhttp() {
    var xmlhttp;
    if (window.XMLHttpRequest) {
    //  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
    xmlhttp=new XMLHttpRequest();
    } else{
    // IE6, IE5 浏览器执行代码
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xmlhttp;
}

function getId(id) {
    return document.getElementById(id);
}

function toJson(str) {
    var json = (new Function("return" + str))();
    return json;
}

function showmsg(title, body, fun) {
    getId("myModalLabel").innerText = title;
    getId("myModalbody").innerText = body;
    $('#myModal').modal('toggle');
    $('#myModal').on('hidden.bs.modal',fun)
}
