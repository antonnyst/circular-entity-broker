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
        label.innerHTML = properties[i];   
        label.id = i; 

        var input = document.createElement("input");
        input.className = "dropdown-text";
        input.type = "text";
        input.id = properties[i];
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

    matchvalue = [];
    var tbl = document.createElement('table');
    tbl.id = "showtable";
    //If the product doesn't exist print "Finns ingen sådan produkt"
    if(match.length == 0){
        head = document.createElement('h1');
        head.textContent = "Finns ingen sådan produkt";
        document.getElementById('showprops').appendChild(head);
    
    //If the product exist make a table with property and value
    }else{
        var i = 1
        var trhead = document.createElement('tr');
        var thprop = document.createElement('th');
        var thval = document.createElement('th');

        thprop.textContent = "property";
        thval.textContent = "value";
        trhead.appendChild(thprop);
        trhead.appendChild(thval);
        tbl.appendChild(trhead)
        match.forEach(obj => {
            if (obj.properties) {
                var tr = document.createElement('tr');
                var tdprop = document.createElement('th');
                var tdval = document.createElement('th');
                tdprop.textContent = "Company";
                tdval.textContent = i;

                tr.appendChild(tdprop);
                tr.appendChild(tdval);
                tbl.appendChild(tr);

                i++;
                obj.properties.forEach(prop => {
                    var tr = document.createElement('tr');
                    var tdprop = document.createElement('td');
                    var tdval = document.createElement('td');
                    tdprop.textContent = prop.property;
                    tdval.textContent = prop.value;

                    tr.appendChild(tdprop);
                    tr.appendChild(tdval);
                    tbl.appendChild(tr)
                    matchvalue.push(prop.value)
                });
            }
        });
        document.getElementById('showprops').appendChild(tbl);
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
    var inputprops = {}
    for(var i = 0; i < properties.length; i++){
        if(document.getElementById(properties[i]).value != ''){
            inputprops[properties[i]] = document.getElementById(properties[i]).value;
        }
    }
    if (Object.keys(inputprops).length === 0) {
        alert('You need to input a value');
        return;
    }
    
    $.ajax({
        url: '/resultprop',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ 'data': inputprops }),
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
