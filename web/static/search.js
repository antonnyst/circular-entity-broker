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

function genPriceButton(products, product, match, properties){
    // Button sending inputs to broker
    let button = document.createElement("button");
    button.innerHTML = "Current Price";
    button.id = "getPrice";
    button.addEventListener("click", event => {fetchPrice(products, product, match, properties)});
    document.getElementById("showprops").appendChild(button);    
    }

async function fetchPrice(products, product, match, properties, sortingOrder, choosenHeader){
    // First we wanted to work with arrays but for some reason JS created Array-like objects that are relly wonky so we
    // changed for this approch instead
    let priceArr = { values: [] };
    let stockArr = { values: [] };
    let fluid = [];
    // Get all products
    console.log(match);
    const response = await fetch(`http://localhost:7100/interrogate?productId=${match[0].productId}&property=price`);
    //const response = await fetch("http://127.0.0.1:5000/products");
    console.log(response);
    const data = await response.json();
    const values = data.map(async (item) => {
        const urlFetch = await fetch(`http://127.0.0.1:5000/api/fluid_data?pid=${item.id}`);
        const fluidData = await urlFetch.json();
        // Add price and stock to their respective arrays
        const keys = Object.keys(fluidData); 
        priceArr.values.push(fluidData.price);
        stockArr.values.push(fluidData.stock);
        fluid.push(keys);
    });

    // Wait for all fetch calls to complete
    await Promise.all(values);
    getmatch(products, product, match, properties, sortingOrder, choosenHeader, priceArr, stockArr, fluid[0])

}

function getmatch(products, product, match, properties, sortingOrder, choosenHeader, price, stock, fluid){
    dropdown(products, product);
    var propertiescount = [];
    var checkprint = false;
    genPriceButton(products, product, match, properties, sortingOrder, choosenHeader);
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
        if(typeof(fluid) != "undefined"){
            fluid.forEach(fluidCat => {
                let thprop = document.createElement('th');
                thprop.textContent = fluidCat;
                trprop.appendChild(thprop);
            })
        }

        tbl.appendChild(trprop);
        match.forEach(obj => {
            if (obj.properties) {
                let trval = document.createElement('tr');
                
                for(let i = 0; i < properties.length; i++){
                   
                   
                    //loops through all properties of a product
                    obj.properties.forEach(prop => {
                        let tdval = document.createElement('td');
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
                        let tdval = document.createElement('td');
                        tdval.textContent = "";
                        trval.appendChild(tdval);
                    }
                }
                
                if(typeof(price) != "undefined" || typeof(stock) != "undefined"){
                    let count = 0;
                    let tdPrice = document.createElement('td');
                    let tdStock = document.createElement('td');
                    if (Array.isArray(price.values)) {
                        price.values.forEach(value => {
                            tdPrice.textContent = value;
                            console.log(value)
                            
                        });
                        price.values.pop();

                      } else {
                        console.log("price.values is not an array");
                      }
                      if (Array.isArray(stock.values)) {
                        stock.values.forEach(stock_value => {
                            tdStock.textContent = stock_value;
                            
                        });
                        stock.values.pop();

                      } else {
                        console.log("stock.values is not an array");
                      }
                      
                    
                    console.log("Why does aobe command not execute???");

                //tdval.textContent = price[i];
                //trval.appendChild(tdval);
                //tdval.textContent = stock[i];
                //trval.appendChild(tdval);
                trval.appendChild(tdPrice);
                trval.appendChild(tdStock);
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

function redirectSearchBar(selectElementSearch, products){
    let compMatch = false;
    let goodValue = selectElementSearch.toLowerCase(); // Fixes case sensisitivity
    products.forEach(prod =>{
        if(selectElementSearch != "" && goodValue == prod){
            compMatch = true;
            $.ajax({
                url: '/resultprod',
                type: 'GET',
                data: { product: goodValue},
                success: function(response) {
                    window.location.href = "/search";
                }, error: function() {
                    // On failure, show an alert
                    alert('Choose a product');
                }
            });   
        }
    });
    if(compMatch == false){
        alert("no such product");
    }
    
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
    let searchbar = document.createElement('input');
    let buttonSearch = document.createElement('button');
    buttonSearch.id = "searchRes";
    buttonSearch.innerHTML = "search for product";
    document.getElementById("showall").appendChild(selectList)  
    //Button for searching and going back
    var button = document.createElement('button');
    button.innerHTML = "Get properties";    
    button.addEventListener("click", event => { redirect()});
    buttonSearch.addEventListener("click", event => { redirectSearchBar(searchbar.value, products)});
    document.getElementById('showall').appendChild(button);
    document.getElementById('showall').appendChild(searchbar);
    document.getElementById('showall').appendChild(buttonSearch);
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