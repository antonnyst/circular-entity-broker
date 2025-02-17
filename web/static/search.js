function initiate(products){
    //Calls for dropdown which makes the dropdown bar
    var product = "select your choice";
    dropdown(products, product);
    h1 = document.createElement('h1');
    h1.innerHTML = "Choose your product from the dropdown bar";
    document.getElementById('showall').appendChild(h1);
}

function initiateProperties(products, properties, product){
    dropdown(products, product);
    //Creating labels and input fields for properties
    for(var i = 0; i < properties.length; i++){
        var container = document.createElement('div');
        container.className = "disp";

        var label = document.createElement('label');
        label.className = "dropdown";
        label.innerHTML = properties[i].property;   
        label.id = i; 

        var input = document.createElement("input");
        input.className = "dropdown-text";
        input.type = "text";
        input.id = properties[i].property;
        container.appendChild(label);
        container.appendChild(input);
        document.getElementById('showprops').appendChild(container); 

    }
    //Button sending inputs to broker
    var button = document.createElement('button');
    button.innerHTML = "Search";    
    button.id = "search"
    button.addEventListener("click", event => { sendProperties(properties, product)});
    document.getElementById('showprops').appendChild(button);

}

function getmatch(products, product, match){
    dropdown(products, product);
    var check = 0;
    //If the product doesn't exist print "Finns ingen sådan produkt"
    if(match.length == 0){
        head = document.createElement('h1');
        head.textContent = "Finns ingen sådan produkt";
        document.getElementById('showprops').appendChild(head);
    
    //If the product exist make a table with property and value
    }else{
        match.forEach(obj => {
            if (obj.properties) {
                var tbl = document.createElement('table');
                tbl.id = "showtable";

                var trprop = document.createElement('tr');
                if(check == 0){
                    obj.properties.forEach(prop => {
                        var thprop = document.createElement('th');
    
                        thprop.textContent = prop.property;
    
                        trprop.appendChild(thprop);
                        
                    });
                    tbl.appendChild(trprop);
                    check++;
                }
                
                
                var trval = document.createElement('tr');
                obj.properties.forEach(prop => {
                    var tdval = document.createElement('td');

                    tdval.textContent = prop.value;

                    trval.appendChild(tdval);
                    
                });
                tbl.appendChild(trval);
                document.getElementById('showprops').appendChild(tbl);
            }
        });
    }
}


//Sends selected product to resultprod with get request
function redirect(){
    selectElement = document.getElementById("dropId").value;
    $.ajax({
        url: '/resultprod',
        type: 'GET',
        data: { product: selectElement},
        success: function(response) {
            window.location.href = "/search";
        }, error: function() {
            // On failure, show an alert
            alert('Choose a product');
        }
     });   
}


//Sends value for all properties to resultprop with POST request
function sendProperties(properties){
    var inputprops = {};
    var valueType = [];
    for(var i = 0; i < properties.length; i++){
        if(document.getElementById(properties[i].property).value != ''){
            inputprops[properties[i].property] = document.getElementById(properties[i].property).value;
            valueType.push(properties[i].valueType);
        }
    }
    console.log(valueType)
    if (Object.keys(inputprops).length === 0) {
        alert('You need to input a value');
        return;
    }
    
    $.ajax({
        url: '/resultprop',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ 'data': inputprops, 'valueType': valueType}),
        success: function(response) {
            window.location.href = "/compare";
        }
     });   
}

//Checking if product already has been rendered
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

//Creates the dropdown bar for all pages
function dropdown(products, product){
    var count = [];
    document.getElementById('showall').innerHTML = ""
    var selectList = document.createElement("select");
    selectList.id = "dropId";

    var option = document.createElement("option");
    text = document.createTextNode(product);
    option.appendChild(text);
    selectList.appendChild(option);
    count.push(product)

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
    var button = document.createElement('button');
    button.innerHTML = "Get properties";    
    button.addEventListener("click", event => { redirect()});
    document.getElementById('showall').appendChild(button);
}
