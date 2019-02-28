function getData() {
    var xmlhttp = Getxmlhttp();
    xmlhttp.open("GET", search_log_api_url, true);
    xmlhttp.send();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState==4){
            if (xmlhttp.status==200){
                var logs = toJson(xmlhttp.responseText)["logs"];
                createtable(logs);
            }
        }
    }
}

function createtable(logs) {
    tbody = getId("search_log_table_tbody");
    for(var i = 0; i< logs.length; i++){
        log = logs[i];
        var tr = document.createElement("tr");
        var td_id = document.createElement("td");
        var td_ip = document.createElement("td");
        var td_date = document.createElement("td");
        var td_content = document.createElement("td");
        var td_operater = document.createElement("td");

        var td_btu = document.createElement("button");
        td_btu.innerText = "删除";
        td_btu.className = "btn btn-danger";

        td_id.innerText = log["id"];
        td_ip.innerText = log["ip"];
        td_date.innerText = log["date"];
        td_content.innerText = log["content"];
        td_operater.appendChild(td_btu);
        tr.appendChild(td_id);
        tr.appendChild(td_ip);
        tr.appendChild(td_content);
        tr.appendChild(td_date);
        tr.appendChild(td_operater);
        tbody.appendChild(tr);
    }
}
getData();