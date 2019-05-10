function create_zmap_task() {
    // 获取base info
    var scanners = getId("scanners").value;
    var name = getId("name").value;
    var task_name = getId("task_name").value;
    var enable = getId("enable").value;
    var description = getId("description").value;
    var every = getId("every").value;
    var period = getId("period").value;
    var minute = getId("minute").value;
    var hour = getId("hour").value;
    var dayofweek = getId("dayofweek").value;
    var dayofmonth = getId("dayofmonth").value;
    var monthofyear = getId("monthofyear").value;
    var timezone = getId("timezone").value;
    var one_of_task = getId("one_of_task").value;
    var port = getId("port").value;
    var cidr = getId("cidr").value;
    var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    var xmlhttp = Getxmlhttp();
    xmlhttp.open("POST", create_zmap_task_url, true);
    var data = "scanners_id=" + scanners + "&name=" + name + "&task_name=" + task_name + "&enable=" + enable + "&desc="
    + description + "&every=" + every + "&period=" + period + "&minute=" + minute + "&hour=" + hour + "&dayofweek="  +
        dayofweek + "&dayofmonth=" + dayofmonth + "&monthofyear=" + monthofyear + "&timezone=" + timezone + "&one_of_task=" +
        one_of_task + "&port=" + port + "&cidr=" + cidr + "&csrfmiddlewaretoken=" + csrfmiddlewaretoken;
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send(data);
    xmlhttp.onreadystatechange = function(){
        if (xmlhttp.readyState==4){
            var res = toJson(xmlhttp.responseText);
            if (xmlhttp.status==200){
                showmsg("任务创建成功", "可在任务里表中查看", function () {
                    window.location.reload();
                });
            }else {
                showmsg("任务创建失败", res["info"]);
            }
        }
    };
}

function create_nmap_task() {
    var scanners = getId("scanners").value;
    var name = getId("name").value;
    var enable = getId("enable").value;
    var description = getId("description").value;
    var every = getId("every").value;
    var period = getId("period").value;
    var minute = getId("minute").value;
    var hour = getId("hour").value;
    var dayofweek = getId("dayofweek").value;
    var dayofmonth = getId("dayofmonth").value;
    var monthofyear = getId("monthofyear").value;
    var timezone = getId("timezone").value;
    var one_of_task = getId("one_of_task").value;
    var type = getId("type").value;
    var datas = getId("datas").value;
    var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    console.log(scanners, name, enable, description, every, period, minute, hour, dayofmonth, dayofweek, monthofyear,
        timezone, one_of_task, type, data, csrfmiddlewaretoken);
    var xmlhttp = Getxmlhttp();
    xmlhttp.open("POST", create_nmap_task_url, true);
    var data = "scanners_id=" + scanners + "&name=" + name + "&enable=" + enable + "&desc="
    + description + "&every=" + every + "&period=" + period + "&minute=" + minute + "&hour=" + hour + "&dayofweek="  +
        dayofweek + "&dayofmonth=" + dayofmonth + "&monthofyear=" + monthofyear + "&timezone=" + timezone + "&one_of_task=" +
        one_of_task + "&type=" + type + "&datas=" + datas + "&csrfmiddlewaretoken=" + csrfmiddlewaretoken;
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send(data);
    xmlhttp.onreadystatechange = function(){
        if (xmlhttp.readyState==4){
            var res = toJson(xmlhttp.responseText);
            if (xmlhttp.status==200){
                showmsg("任务创建成功", "可在任务里表中查看", function () {
                    window.location.reload();
                });
            }else {
                showmsg("任务创建失败", res["info"]);
            }
        }
    };
}

