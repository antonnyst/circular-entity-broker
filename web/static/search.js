//Makes buttons for all products
function initiate(properties){
    const count = [];
    document.getElementById('showprops').innerHTML = ""
    for(var j = 0; j < properties.length; j++){
        const property = JSON.parse(properties[j]);
        for (const key in property) {
            if(key == "product"){
                //Checks if button already exists, so we don't create several
                if(checkProducts(count, property[key])){

                    //Creates the button and add an listener to it
                    var elem2 = document.createElement('button');
                    elem2.innerHTML = property[key];    
                    elem2.className = "list"
                    elem2.addEventListener("click", event => { changeValue(properties, property[key]) });
                    document.getElementById('showprops').appendChild(elem2);
                    count.push(property[key])
                }
            }
        }   
    }
}

//Creates labels and input boxes under the button for searching
function changeValue(properties, product){
    const count = [];
    for(var j = 0; j < properties.length; j++){
        const property = JSON.parse(properties[j]);
        if(property.product == product){
            document.getElementById("showprops").innerHTML = "";
            for (const key in property) {
                if(key == "product"){
                    if(checkProducts(count, property[key])){
                        //Creates the button for just the one property
                        var elem2 = document.createElement('button');
                        elem2.innerHTML = property[key];    
                        elem2.className = "list"
                        elem2.addEventListener("click", event => { changeValue(properties, property[key]) });
                        document.getElementById('showprops').appendChild(elem2);
                        count.push(property[key])
                    }
                }else{
                    //Creates labels and textfields
                    var elem2 = document.createElement('label');
                    elem2.className = "dropdown";
                    elem2.innerHTML = key;    
                    document.getElementById('showprops').appendChild(elem2);

                    var input = document.createElement("input");
                    input.className = "dropdown-text";
                    input.type = "text";

                    input.id = property[key];
                    document.getElementById('showprops').appendChild(input); 
                }
            }
            //Button for searching and going back
            var elem2 = document.createElement('button');
            elem2.innerHTML = "Search";    
            prot = returnPrototype(properties, product);
            elem2.addEventListener("click", event => { CompareProperties(prot) });
            document.getElementById('showprops').appendChild(elem2);

            var elem2 = document.createElement('button');
            elem2.innerHTML = "Back";    
            elem2.addEventListener("click", event => { initiate(properties) });
            document.getElementById('showprops').appendChild(elem2);
        return;
        }
    }
}

function CompareProperties(properties){
    input = []
    const props = properties[0];
    for(prop in props){
        if(props != "product" && document.getElementById(props[prop]) != null){
            input.push(document.getElementById(props[prop]).value);
        }
    }
    for(var i = 0; i < properties.length; i++){
        const property = properties[i];
        count = 0;
        for (const key in property) {
            input[count];
            if(key != "product"){
                if(input[count].toLowerCase() != property[key].toLowerCase() && input[count] != ""){
                    break;
                }
                count++;
                if(count == Object.keys(property).length - 1){
                    return location.href = 'http://127.0.0.1:7300/' + property.manufacturer;
                }
            }

        }
    }
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

function returnPrototype(properties, product){
    const prot = [];
    for(var j = 0; j < properties.length; j++){
        const property = JSON.parse(properties[j]);
        if(property.product == product){
            for (const key in property) {
                if(key == "product"){
                    const property = JSON.parse(properties[j]);
                    prot.push(property);
                }
            }
        }
    }
    return prot;
}