// author: elloit
// date: 2018-6-1 儿童节快乐 :)
// email: imelloit@gmail.com

// 三个方法
function ObjforId(id) {
    return document.getElementById(id);
}

function ObjsforName(name) {
    return document.getElementsByName(name);
}

function ObjsforClassname(classname) {
    return document.getElementsByClassName(classname)
}

// 创建Ajax对象
function getXmlHttp() {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp=new XMLHttpRequest();
    }
    else{
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xmlhttp;
}

// 检查提交的数据是否合乎规范
function checkdata() {
    var title = jobdata.title.value;
    var desc = jobdata.desc.value;
    var dst_port = jobdata.dst_port.value;
    var src_port = jobdata.src_port.value;
    var ip = jobdata.ip.value;
    var networkcard = jobdata.networkcard.value;
    if (title=="" | desc=="" | dst_port=="" | src_port=="" | ip=="" | networkcard==""){
        alert("请将数据补充完整");
    }else {
        var ip_check = ip.split("/");
        if (! checkip(ip_check[0])){
            alert("ip范围错误");
        }else if(ip_check[1] != 24 & ip_check[1] != 26){
            alert("ip范围错误");
        }else if (! checknumber(dst_port)){
            alert("请输入正确目的端口");
        }else if(! checknumber(src_port)){
            alert("请输入正确源端口");
        }else {
            submit_create(title, desc, dst_port, src_port, ip, networkcard);
        }
    }
}

// 提交创建的数据
function submit_create(title, desc, dst_port, src_port, ip, networkcard) {
    var xmlhttp = getXmlHttp();
    xmlhttp.open("POST", submit_create_url, true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    data = "title=" + title + "&desc=" + desc + "&dst_port=" + dst_port + "&src_port=" + src_port + "&ip=" + ip +
        "&networkcard=" + networkcard + "&csrfmiddlewaretoken=" + jobdata.csrfmiddlewaretoken.value;
    xmlhttp.send(data);
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            msg = toJson(xmlhttp.responseText);
            if (msg.msg == 0){
                alert("端口错误");
            }else if(msg.msg == 1){
                var td_title = document.createElement("td");
                var td_dst_port = document.createElement("td");
                var td_src_port = document.createElement("td");
                var td_ip = document.createElement("td");
                var td_network = document.createElement("td");
                var td_locatip = document.createElement("td");
                var td_create_time = document.createElement("td");
                var td_status = document.createElement("td");
                var td_progress_rate = document.createElement("td");
                var tr = document.createElement("tr");
                td_title.innerText = msg.data[1];
                td_dst_port.innerText = msg.data[2];
                td_src_port.innerText = msg.data[3];
                td_ip.innerText = msg.data[4];
                td_network.innerText = msg.data[5];
                td_locatip.innerText = msg.data[6];
                td_create_time.innerText = msg.data[7];
                switch (msg.data[8]){
                    case 0:
                        td_status.innerHTML = "<span class='text-info'>就绪</span>";
                        td_progress_rate.innerHTML = "<button class='btn btn-info' onclick='runjob("+ msg.data[0] + "," + td_status + "," + td_progress_rate+")'>点击开始</button>";
                        break;
                    case 1:
                        td_status.innerHTML = "<span class='text-warning'>执行中</span>";
                        td_progress_rate.innerHTML = '<div class="progress">\n' +
                            '                            <div class="progress-bar bg-danger" style="width:'+ msg.data[9] +'%"></div>\n' +
                            '                        </div>';
                        break;
                    case 2:
                        td_status.innerHTML = "<span class='text-success'>完成</span>";
                        td_progress_rate.innerHTML = '<div class="progress">\n' +
                            '                            <div class="progress-bar bg-danger" style="width:100%"></div>\n' +
                            '                        </div>';
                        break;
                }
                tr.appendChild(td_title);
                tr.appendChild(td_dst_port);
                tr.appendChild(td_src_port);
                tr.appendChild(td_ip);
                tr.appendChild(td_network);
                tr.appendChild(td_locatip);
                tr.appendChild(td_create_time);
                tr.appendChild(td_status);
                tr.appendChild(td_progress_rate);
                tr.innerHTML += "<input name='job_uuid' type='hidden' value='"+ msg.data[0] +"'>"
                var jobtable = ObjforId("jobtable");
                jobtable.innerHTML = '';
                jobtable.append(tr);
                $("#myModal").modal('hide');
            }

        }
    }
}

// 执行任务
function runjob(uuid,statues, process) {
    alert(uuid);
    alert(statues);
    alert(process);
}

// 检验ip
function checkip(ip) {
    var reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
    return reg.test(ip);
}

// 检验数字
function checknumber(number) {
    var reg = /^([0-9]|[1-9]\d|[1-9]\d{2}|[1-9]\d{3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$/;
    return reg.test(number);
}

//字符串转 json对象
function toJson(str) {
    var json = (new Function("return" + str))();
    return json;
}