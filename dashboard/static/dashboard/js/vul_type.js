function create_vul_type() {
    var typename = getId("typename").value;
    var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    if(typename== ""){
        showmsg("Parameter error !!!", "Please complete the parameters !!!", null)
    }
    var xmlhttp = Getxmlhttp();
    xmlhttp.open("POST", vul_add_url, true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    var data = "typename=" + typename + "&csrfmiddlewaretoken=" + csrfmiddlewaretoken;
    xmlhttp.send(data);
    xmlhttp.onreadystatechange = function(){
        if (xmlhttp.readyState==4){
            var res = toJson(xmlhttp.responseText);
            if (xmlhttp.status==200){
                 showmsg("Type added successfully!!!", res["info"], function () {
                     window.location.reload();
                 });
            }else {
                showmsg("Type addition failed!!!", res["info"], null);
            }
        }
    };
}