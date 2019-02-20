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

//获取表单中所有的input元素
function getElements(formId) {
    var form = document.getElementById(formId);
    var elements = new Array();
    var tagElements = form.getElementsByTagName('input');
    for (var j = 0; j < tagElements.length; j++){
         elements.push(tagElements[j]);

    }
    return elements;
}

function ParseDatas(elements) {
    var datas = new Array();
    for(var i=0; i<elements.length; i++){
        var data = new Array();
        data.push(elements[i].name);
        data.push(elements[i].value);
        datas.push(data);
    }
    return datas;
}

function makedata(array) {
    var data = "";
    for(var i=0; i<array.length; i++){
        if (i == array.length -1){
            data += array[i][0] + "=" + array[i][1];
        }else {
            data += array[i][0] + "=" + array[i][1] + "&";
        }
    }
    return data;
}

function create_scanner() {
    // 获取表单数据
    // scanner base
    scanner_elements = ParseDatas(getElements("form-scanner-base"));

    es_elements = ParseDatas(getElements("form-es"));

    borker_elements = ParseDatas(getElements("form-borker"));
    var borker_type = new Array();
    borker_type.push("borker-type");
    borker_type.push(getId("borker-type").options[getId("borker-type").selectedIndex].value);
    borker_elements.push(borker_type);

    backend_elements = ParseDatas(getElements("form-backend"));
    var backend_type = new Array();
    backend_type.push("backend-type");
    backend_type.push(getId("backend-type").options[getId("backend-type").selectedIndex].value);
    backend_type.push(backend_type);
    backend_elements.push(backend_type);

    // xmlhttp
    var xmlhttp = Getxmlhttp();
    xmlhttp.open("POST", create_scanner_url, true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    var data = makedata(scanner_elements) + "&" + makedata(es_elements) + "&" + makedata(borker_elements) + "&"
        + makedata(backend_elements);
    xmlhttp.send(data);
    xmlhttp.onreadystatechange = function(){
        if (xmlhttp.readyState==4 && xmlhttp.status==200){
            // document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
            console.log("asdasd");
        }
    };
    console.log(create_scanner_url);
    console.log(data);
}