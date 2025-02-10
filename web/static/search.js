//When no 
function initiate(products){
    const count = [];
    document.getElementById('showprops').innerHTML = ""
    var selectList = document.createElement("select");
    selectList.id = "dropId";
    var option = document.createElement("option"),
    text = document.createTextNode("Choose your product");
    option.appendChild(text);
    selectList.appendChild(option);
    for(var j = 0; j < products.length; j++){
        //Checks if button already exists, so we don't create several
        if(checkProducts(count, products[j])){
            option = document.createElement( 'option' );
            option.value = products[j];
            text = document.createTextNode(products[j]);
            option.appendChild(text);
            selectList.appendChild(option);
            count.push(products[j])
        }
    } 
    document.getElementById("showall").appendChild(selectList)  
    //Button for searching and going back
    var elem2 = document.createElement('button');
    elem2.innerHTML = "Get properties";    
    elem2.addEventListener("click", event => { redirect()});
    document.getElementById('showprops').appendChild(elem2);
}

function initiateProperties(products, properties){
    const count = [];
    console.log(properties[0])
    document.getElementById('showall').innerHTML = ""
    var selectList = document.createElement("select");
    selectList.id = "dropId";
    var option = document.createElement("option");
    text = document.createTextNode(properties[0]);
    option.appendChild(text);
    selectList.appendChild(option);
    count.push(properties[0]);
    for(var j = 0; j < products.length; j++){
        //Checks if button already exists, so we don't create several
        if(checkProducts(count, products[j])){
            option = document.createElement( 'option' );
            option.value = products[j];
            text = document.createTextNode(products[j]);
            option.appendChild(text);
            selectList.appendChild(option);
            count.push(products[j])
        }
    } 
    for(var i = 1; i < properties.length; i++){
        var elem2 = document.createElement('label');
        elem2.className = "dropdown";
        elem2.innerHTML = properties[i];    
        document.getElementById('showprops').appendChild(elem2);

        var input = document.createElement("input");
        input.className = "dropdown-text";
        input.type = "text";
        input.id = properties[i];
        document.getElementById('showprops').appendChild(input); 
    }
    document.getElementById("showall").appendChild(selectList)  
    //Button for searching and going back
    var elem2 = document.createElement('button');
    elem2.innerHTML = "Get properties";    
    elem2.addEventListener("click", event => { redirect()});
    document.getElementById('showall').appendChild(elem2);

    document.getElementById("showall").appendChild(selectList)  
    //Button for searching and going back
    var elem2 = document.createElement('button');
    elem2.innerHTML = "Search";    
    elem2.addEventListener("click", event => { sendProperties(properties)});
    document.getElementById('showprops').appendChild(elem2);

}

//Creates labels and input boxes under the button for searching
function redirect(){
    selectElement = document.getElementById("dropId").value;
    $.ajax({
        url: '/resprod',
        type: 'POST',
        data: { 'data': selectElement },
     });
     window.location.href = "/search"
}

function sendProperties(properties){
    inputprops = []
    for(var i = 1; i < properties.length; i++){
        if(document.getElementById(properties[i]) != null){
            inputprops.push(document.getElementById(properties[i]).value);
        }else{
            inputprops.push("");
        }
    }
    jsinputprops = JSON.stringify(inputprops);
    $.ajax({
        url: '/resprop',
        type: 'POST',
        contentType: 'application/json',
        data: jsinputprops,
     });
}


function checkProducts(count, value){
    if (count.length != 0){
        for(i = 0; i < count.length; i++){
            if(value == count[i]){
                return false;
            }
        }
        return true;
    }
    return true;
}