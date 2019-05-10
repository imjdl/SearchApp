function create_poc() {
    editor.save();
    var poc_name = getId("pocname").value;
    var keywords = getId("keywords").value;
    var description = getId("description").value;
    var product = getId("product").value;
    var vul = getId("vul").value;
    var date = getId("date").value;
    var code = window.btoa(window.encodeURIComponent(getId("code").value));
    var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    if(poc_name == "" || keywords == "" || description == "" || product == "" || vul == "" || date == "" || code == ""){
        showmsg("Parameter error !!!", "Please complete the parameters !!!", null)
    }else if(product == "-------" || vul == "-------"){
        showmsg("Parameter error !!!", "Please complete the parameters !!!", null)
    }else {
        var xmlhttp = Getxmlhttp();
        xmlhttp.open("POST", poc_url, true);
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        var data = "poc_name=" + poc_name + "&keywords=" + keywords + "&description=" + description + "&csrfmiddlewaretoken=" +
        csrfmiddlewaretoken + "&product=" + product + "&vul=" + vul + "&date=" + date + "&code=" + code;
        xmlhttp.send(data);
        xmlhttp.onreadystatechange = function(){
            if (xmlhttp.readyState==4){
                var res = toJson(xmlhttp.responseText);
                if (xmlhttp.status==200){
                     showmsg("Product added successfully!!!", res["info"], function () {
                         window.location.reload();
                     });
                }else {
                    showmsg("Product addition failed!!!", res["info"], null);
                }
            }
        };
    }

}

function update_poc() {
    editor.save();
    var poc_id = getId("poc_id").value;
    var poc_name = getId("pocname").value;
    var keywords = getId("keywords").value;
    var description = getId("description").value;
    var product = getId("product").value;
    var vul = getId("vul").value;
    var date = getId("date").value;
    var code = window.btoa(window.encodeURIComponent(getId("code").value));
    var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    console.log(poc_id, poc_name, keywords, description, product, vul, date, code);
    if(poc_id == "" ||poc_name == "" || keywords == "" || description == "" || product == "" || vul == "" || date == "" || code == ""){
        console.log(123123123);
        showmsg("Parameter error !!!", "Please complete the parameters !!!", null)
    }else if(product == "-------" || vul == "-------"){
        showmsg("Parameter error !!!", "Please complete the parameters !!!", null)
    }else {
        var xmlhttp = Getxmlhttp();
        xmlhttp.open("POST", poc_edit_url, true);
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        var data = "poc_id=" + poc_id + "&poc_name=" + poc_name + "&keywords=" + keywords + "&description=" +
            description + "&csrfmiddlewaretoken=" + csrfmiddlewaretoken + "&product=" + product + "&vul=" +
            vul + "&date=" + date + "&code=" + code;
        xmlhttp.send(data);
        xmlhttp.onreadystatechange = function(){
            if (xmlhttp.readyState==4){
                var res = toJson(xmlhttp.responseText);
                if (xmlhttp.status==200){
                     showmsg("Product added successfully!!!", res["info"], function () {
                         window.location.reload();
                     });
                }else {
                    showmsg("Product addition failed!!!", res["info"], null);
                }
            }
        };
    }
}

function run_poc(poc_id) {
    var xmlhttp = Getxmlhttp();
    xmlhttp.open("GET", poc_run_url + "?poc_id=" + poc_id, true);
    xmlhttp.send(data);
    xmlhttp.onreadystatechange = function(){
        if (xmlhttp.readyState==4){
            var res = toJson(xmlhttp.responseText);
            if (xmlhttp.status==200){
                showmsg("Product run successfully!!!", res["info"], function () {
                         window.location.reload();
                });
            }else {
                    showmsg("Product run failed!!!", res["info"], null);
            }
        }
    };
}

function delete_poc(poc_id) {
    var xmlhttp = Getxmlhttp();
    xmlhttp.open("GET", poc_del_url + "?poc_id=" + poc_id, true);
    xmlhttp.send(data);
    xmlhttp.onreadystatechange = function(){
        if (xmlhttp.readyState==4){
            var res = toJson(xmlhttp.responseText);
            if (xmlhttp.status==200){
                showmsg("Product delete successfully!!!", res["info"], function () {
                         window.location.reload();
                });
            }else {
                    showmsg("Product delete failed!!!", res["info"], null);
            }
        }
    };
}
