function getData(page) {
    var xmlhttp = Getxmlhttp();
    xmlhttp.open("GET", search_log_api_url + "?page=" + page, true);
    xmlhttp.send();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState==4){
            if (xmlhttp.status==200){
                var data = toJson(xmlhttp.responseText);
                var logs = data["logs"];
                createtable(logs);
                createPagebar(data["page"], data["paginator"]);
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
        td_btu.addEventListener("click", function () {
            alert(i);
        });

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

function createPagebar(now_page, pages_vaul) {
    var ul = getId("page-ul");
    // Previous
    var previous_li = document.createElement("li");
    var previous_a = document.createElement("a");
    if(now_page == 1){
        previous_li.className = "page-item disabled";
    }else {
        previous_li.className = "page-item";
        previous_a.href = search_log_url + "?page=" + (now_page - 1);
    }
    previous_a.className = "page-link";
    previous_a.innerText = "Previous";
    previous_li.appendChild(previous_a);
    ul.appendChild(previous_li);
    // next
    var next_li = document.createElement("li");
    var next_a = document.createElement("a");
    if(now_page == pages_vaul[pages_vaul.length - 1]){
        next_li.className = "page-item disabled";
    }else {
        next_li.className = "page-item";
        next_a.href = search_log_url + "?page=" + (now_page + 1);
    }
    next_a.className = "page-link";
    next_a.innerText = "Next";
    next_li.appendChild(next_a);

    for(var i = 0; i < pages_vaul.length; i++){
        var li = document.createElement("li");
        var a = document.createElement("a");
        if(now_page == pages_vaul[i]){
            li.className = "page-item active";
        }else {
            li.className = "page-item";
        }
        a.className = "page-link";
        a.href = search_log_url + "?page=" + pages_vaul[i];
        a.innerText = pages_vaul[i];
        li.appendChild(a);
        ul.appendChild(li);
    }
    ul.appendChild(next_li);
}

function remoceChilds(node){
    var childs = node.childNodes;
    for (var i=0; i<childs.length; i++){
        node.removeChild(childs[i]);
    }
}

window.onload = function(){
    getData(window.location.search.substr(6));
};
