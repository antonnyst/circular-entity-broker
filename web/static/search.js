"https://code.jquery.com/jquery-3.5.1.min.js"

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
    var inp = 0;
    var currentprod = [];
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
                    
                    input.id = inp;
                    inp++;
                    document.getElementById('showprops').appendChild(input); 
                    currentprod.push(key);
                }
            }
            //Button for searching and going back
            var elem2 = document.createElement('button');
            elem2.innerHTML = "Search";    
            prot = returnPrototype(properties, product);
            elem2.addEventListener("click", event => { sendProperties(currentprod, inp) });
            document.getElementById('showprops').appendChild(elem2);

            var elem2 = document.createElement('button');
            elem2.innerHTML = "Back";    
            elem2.addEventListener("click", event => { initiate(properties) });
            document.getElementById('showprops').appendChild(elem2);
        return;
        }
    }
}

function sendProperties(prod, inp){
    var properties = {}
    for(var i = 0; i < inp; i++){
        properties[prod[i]] = document.getElementById(i).value;
    }
    propertJ = JSON.stringify(properties);

    $.ajax({
       type: 'POST',
       contentType: 'application/json',
       data: JSON.stringify(propertJ),
       url: '/results',
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