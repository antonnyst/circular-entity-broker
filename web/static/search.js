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

function getmatch(products, product, match, properties, sortingOrder, choosenHeader){
    dropdown(products, product);
    var propertiescount = [];
    var checkprint = false;
    
    //If the product doesn't exist print "No product exists"
    if(match.length == 0){
        head = document.createElement('h1');
        head.textContent = "No product exists";
        document.getElementById('showprops').appendChild(head);
    
    //If the product exist make a table with property and value
    }else{
        var tbl = document.createElement('table');
        tbl.id = "showtable";
        var trprop = document.createElement('tr');
        //Makes sure that all the columns for properties is getting filled
        for(let i = 0; i < properties.length; i++){
            //Prints out the haders
            if (checkProducts(propertiescount, properties[i].property)){
                if(choosenHeader == properties[i].property){
                    if(sortingOrder % 2 == 0){
                        var thprop = document.createElement('th');
        
                        thprop.textContent = properties[i].property + "▼";
                        thprop.addEventListener("click", () => sortingResult(products, product, match, properties, properties[i], sortingOrder));
                        trprop.appendChild(thprop);
                        propertiescount.push(properties);
                    }else{
                        var thprop = document.createElement('th');
        
                        thprop.textContent = properties[i].property + "▲";
                        thprop.addEventListener("click", () => sortingResult(products, product, match, properties, properties[i], sortingOrder));
                        trprop.appendChild(thprop);
                        propertiescount.push(properties);
                    }
                }else{
                    var thprop = document.createElement('th');
        
                    thprop.textContent = properties[i].property;
                    thprop.addEventListener("click", () => sortingResult(products, product, match, properties, properties[i], sortingOrder));
                    trprop.appendChild(thprop);
                    propertiescount.push(properties);
                }
               
            }
            
        }
        tbl.appendChild(trprop);
        match.forEach(obj => {
            if (obj.properties) {
                var trval = document.createElement('tr');

                for(var i = 0; i < properties.length; i++){
                    checkprint = false;
                    
                    //loops through all properties of a product
                    obj.properties.forEach(prop => {
                        var tdval = document.createElement('td');
                        //Checks if the product have the property
                        if(prop.property == properties[i].property){
                            if(prop.value == ""){
                                tdval.textContent = "";
                                checkprint = true;
                            }else{
                                tdval.textContent = prop.value;
                                checkprint = true;
                            }
        
                            trval.appendChild(tdval);
                        }
                    });
                    //If it doesn't have the property we make an empty column
                    if(checkprint == false){
                        var tdval = document.createElement('td');
                        tdval.textContent = "";
                        trval.appendChild(tdval);
                    }
                   
                }
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

function sortingResult(products, product, match, properties, properval, sortingOrder){
    if(sortingOrder % 2 == 0){
        //sorting descending
        const sortedDescending = match.sort((a, b) => {
            if(properval.valueType == "string"){
                var propertyA = a.properties.find(props => props.property == properval.property).value;
                var propertyB = b.properties.find(props => props.property == properval.property).value;
                return propertyA.localeCompare(propertyB);
            }else if(properval.valueType == "float"){
                var propertyA = parseFloat(a.properties.find(props => props.property == properval.property).value);
                var propertyB = parseFloat(b.properties.find(props => props.property == properval.property).value);
                return propertyA-propertyB;
            }
        
        });
        sortingOrder++;
        document.getElementById('showprops').innerHTML = "";
        getmatch(products, product, sortedDescending, properties, sortingOrder, properval.property);
    }else{
        //Sorting ascending
        const sortedAscending = match.sort((a, b) => {
            if(properval.valueType == "string"){
                var propertyA = a.properties.find(props => props.property == properval.property).value;
                var propertyB = b.properties.find(props => props.property == properval.property).value;
                return propertyB.localeCompare(propertyA);
            }else if(properval.valueType == "float"){
                var propertyA = parseFloat(a.properties.find(props => props.property == properval.property).value);
                var propertyB = parseFloat(b.properties.find(props => props.property == properval.property).value);
                return propertyB-propertyA;
            }
            
        });
        sortingOrder++;
        document.getElementById('showprops').innerHTML = "";
        getmatch(products, product, sortedAscending, properties, sortingOrder, properval.property);
    }
    
}