function create_product() {
    var productname = getId("productname").value;
    var url = getId("url").value;
    var description = getId("description").value;
    var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    if(productname== "" || url == "" || description == ""){
        showmsg("Parameter error !!!", "Please complete the parameters !!!", null)
    }
    var xmlhttp = Getxmlhttp();
    xmlhttp.open("POST", add_product_url, true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    var data = "productname=" + productname + "&url=" + url + "&description=" + description + "&csrfmiddlewaretoken=" +
    csrfmiddlewaretoken;
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

function update_product() {
    var product_id = getId("proudct_id").value;
    var productname = getId("productname").value;
    var url = getId("url").value;
    var description = getId("description").value;
    var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    if( product_id == "" || productname== "" || url == "" || description == ""){
        showmsg("Parameter error !!!", "Please complete the parameters !!!", null)
    }
    var xmlhttp = Getxmlhttp();
    xmlhttp.open("POST", product_update_url, true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    var data = "productname=" + productname + "&url=" + url + "&description=" + description + "&csrfmiddlewaretoken=" +
    csrfmiddlewaretoken + "&product_id=" + product_id;
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
