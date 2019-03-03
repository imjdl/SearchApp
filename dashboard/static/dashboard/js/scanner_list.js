function getData() {
    var xmlhttp = Getxmlhttp();
    xmlhttp.open("GET", scanner_list_api,true);
    xmlhttp.send();
    xmlhttp.onreadystatechange = function () {
        if(xmlhttp.readyState == 4){
            if(xmlhttp.status == 200){
                var datas = toJson(xmlhttp.responseText);
                createNode(datas["datas"])
            }
        }
    }
}

function createNode(datas){
    var out_div = getId("scanner-list");
    var all_div = document.createElement("div");
    console.log(datas.length);
    for(var i=0; i< datas.length; i++){
        var i_logo = document.createElement("i");
        if(datas[i].status == 0) {
            all_div.className = "panel panel-primary";
            i_logo.className = "fa fa-close fa-5x";
        }else if (datas[i].status == 1){
            all_div.className = "panel panel-green";
            i_logo.className = "fa fa-smile-o fa-5x";
        }else if (datas[i].status == 2) {
            all_div.className = "panel panel-red";
            i_logo.className = "fa fa-chain-broken fa-5x";
        }
        var head_div = document.createElement("div");
        head_div.className = "panel-heading";

        var row_div = document.createElement("div");
        row_div.className = "row";

        var col_xs_2 = document.createElement("div");
        col_xs_2.className = "col-xs-2";
        col_xs_2.appendChild(i_logo);
        var col_xs_10_text_right = document.createElement("div");
        col_xs_10_text_right.className = "col-xs-10 text-right";
        var div_info = document.createElement("div");
        var span_ip = document.createElement("span");
        span_ip.className = "badge badge-info";
        span_ip.style = "font-size: 20px";
        span_ip.innerText = datas[i].ip;
        var span_port = document.createElement("span");
        span_port.className = "badge badge-info";
        span_port.style = "font-size: 20px";
        span_port.innerText = datas[i].port;
        div_info.appendChild(span_ip);
        div_info.appendChild(span_port);
        div_info.appendChild(document.createElement("hr"));
        var div_oper = document.createElement("div");
        var btn_close = document.createElement("button");
        var btn_restart = document.createElement("button");
        var btn_start = document.createElement("button");
        var btn_flush = document.createElement("button");
        btn_close.className = "btn btn-info btn-outline-info";
        btn_close.innerText = "关闭";
        btn_restart.className = "btn btn-warning btn-outline-info";
        btn_restart.innerText = "重启";
        btn_start.className = "btn btn-default btn-outline-info";
        btn_start.innerText = "开启";
        btn_flush.className = "btn btn-default btn-outline-dark";
        btn_flush.innerText = "刷新";
        div_oper.appendChild(btn_close);
        div_oper.appendChild(btn_restart);
        div_oper.appendChild(btn_start);
        div_oper.appendChild(btn_flush);
        col_xs_10_text_right.appendChild(div_info);
        col_xs_10_text_right.appendChild(div_oper);
        row_div.appendChild(col_xs_2);
        row_div.appendChild(col_xs_10_text_right);
        head_div.appendChild(row_div);
        all_div.appendChild(head_div);
        var a = document.createElement("a");
        var div_footer = document.createElement("div");
        div_footer.className = "panel-footer";
        var span_left = document.createElement("span");
        span_left.className = "pull-left";
        var span_right = document.createElement("span");
        span_right.className = "pull-right";
        var i_circle_right = document.createElement("i");
        i_circle_right.className = "fa fa-arrow-circle-right";
        span_right.appendChild(i_circle_right);
        var div_clearfix = document.createElement("div");
        div_clearfix.className = "clearfix";
        div_footer.appendChild(span_left);
        div_footer.appendChild(span_right);
        div_footer.appendChild(div_clearfix);
        a.appendChild(div_footer);
        all_div.appendChild(a);
    }
    out_div.appendChild(all_div);
}

window.onload = function () {
    getData();
};
