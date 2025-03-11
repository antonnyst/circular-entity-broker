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

function gen_fluid_button(property, product_id, parent, text_id) {
    let button = document.createElement("button");
    button.innerHTML = "Get " + property;
    button.id = "get"+property;
    button.addEventListener("click", async event => {
        let value = await get_fluid_data(product_id, property)
        let text = document.getElementById(text_id)
        text.textContent = value;
        text.classList.remove("text-hidden");
        button.classList.add("button-hidden");
        fluid_data_dict[property+product_id] = value;
    });
    parent.appendChild(button);    
}

function genStockButton(products, product, match, properties, sortingOrder, choosenHeader){
    // Button sending inputs to broker
    let button = document.createElement("button");
    button.innerHTML = "Current Stock";
    button.id = "getStock";
    button.addEventListener("click", event => {fetchStock(products, product, match, properties, sortingOrder, choosenHeader)});
    document.getElementById("showprops").appendChild(button);    
    }

async function fetchStock(products, product, match, properties, sortingOrder, choosenHeader){
    // First we wanted to work with arrays but for some reason JS created Array-like objects that are relly wonky so we
    // changed for this approch instead
    let stockArr = { values: [] };
    let fluid = [];
    // Get all products
    const values = match.map(async (item) => {
        
        const stockresponse = await fetch(`http://localhost:7100/interrogate?productId=${item.productId}&property=stock`);
        

        const stockValue = await stockresponse.json();
       
        stockArr.values.push(stockValue.value);
       
        fluid.push(stockValue.property);
    });

    // Wait for all fetch calls to complete
    await Promise.all(values);
    getmatch(products, product, match, properties, sortingOrder, choosenHeader, [], stockArr)

}

function genPriceButton(products, product, match, properties, sortingOrder, choosenHeader){
    // Button sending inputs to broker
    let button = document.createElement("button");
    button.innerHTML = "Current Price $";
    button.id = "getPrice";
    button.addEventListener("click", event => {fetchPrice(products, product, match, properties, sortingOrder, choosenHeader)});
    document.getElementById("showprops").appendChild(button);    
    }

async function fetchPrice(products, product, match, properties, sortingOrder, choosenHeader){
    // First we wanted to work with arrays but for some reason JS created Array-like objects that are relly wonky so we
    // changed for this approch instead
    let priceArr = { values: [] };
    
    let fluid = [];
    // Get all products
    const values = match.map(async (item) => {
        const priceresponse = await fetch(`http://localhost:7100/interrogate?productId=${item.productId}&property=price`);
        const priceValue = await priceresponse.json();
        priceArr.values.push(priceValue.value);
        fluid.push(priceValue.property);
    });

    // Wait for all fetch calls to complete
    await Promise.all(values);
    getmatch(products, product, match, properties, sortingOrder, choosenHeader, priceArr, [])

}

async function getFluidData(product) {
    const FluidData = await fetch(`http://localhost:7100/fluid_properties?product=${product}`);
    const retFluidData = await FluidData.json();
    return retFluidData;
}

let fluid_data;
let fluid_data_dict = {}

async function getmatch(products, product, match, properties, sortingOrder, choosenHeader){
    dropdown(products, product);
    var propertiescount = [];
    let thFluid = [];
    var checkprint = false;
    document.getElementById('showprops').innerHTML = "";
    //genStockButton(products, product, match, properties, sortingOrder, choosenHeader);
    //genPriceButton(products, product, match, properties, sortingOrder, choosenHeader);
    //If the product doesn't exist print "No product exists"
    if (match.length == 0) {
        head = document.createElement('h1');
        head.textContent = "No product exists";
        document.getElementById('showprops').appendChild(head);
    
    //If the product exist make a table with property and value
    } else {

        let fluid_data = await getFluidData(product);
        console.log(fluid_data);

        var tbl = document.createElement('table');
        tbl.id = "showtable";
        var trprop = document.createElement('tr');
        //Makes sure that all the columns for properties is getting filled
        for(let i = 0; i < properties.length; i++){
            //Prints out the haders
            if (checkProducts(propertiescount, properties[i].property) && properties[i].property != "company"){
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
        fluid_data.forEach(fluid => {
            let thprop = document.createElement('th');
            thprop.textContent = fluid.property;
            trprop.appendChild(thprop);
        });

        
        tbl.appendChild(trprop);
        match.forEach(obj => {
            if (obj.properties) {
                let trval = document.createElement('tr');
                
                for(let i = 0; i < properties.length; i++){
                
                
                    //loops through all properties of a product
                    obj.properties.forEach(prop => {
                        
                        let tdval = document.createElement('td');
                        //Checks if the product have the property
                        if(prop.property == "company"){
                            checkprint = true;
                        }
                        if(prop.property == properties[i].property && prop.property != "company"){
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

                fluid_data.forEach(fluidData => {
                    let tdval = document.createElement('td');
                    let text_id = "p"+fluidData["property"]+obj["productId"];

                    let text = document.createElement('p');
                    text.className = "text-hidden"
                    text.id = text_id
                   

                    if (fluid_data_dict[fluidData["property"]+obj["productId"]] !== undefined) {
                        text.textContent = fluid_data_dict[fluidData["property"]+obj["productId"]];
                        text.classList.remove("text-hidden");
                    } else {
                        gen_fluid_button(fluidData["property"], obj["productId"], tdval, text_id);
                    }
                    tdval.appendChild(text);           
                    trval.appendChild(tdval);
                });
                
                tbl.appendChild(trval);
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

async function get_fluid_data(product_id, property) {
    const priceresponse = await fetch(`http://localhost:7100/interrogate?productId=${product_id}&property=${property}`);
    const priceValue = await priceresponse.json();
        
    return priceValue["value"]
}