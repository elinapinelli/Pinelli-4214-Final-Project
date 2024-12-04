
// function updateTotal() {
//     var quantity = document.getElementById("quantity").value;
//     var price = parseFloat(document.getElementById("product-price").dataset.price); // Safely get price from a data attribute
//     var total = price * quantity;
//     document.getElementById("total-price").textContent = total.toFixed(2); // Update the total price
// }

//IMPORTANT NOTE: I did this function in order t show that I can do this method as well
function create_product_card(product){
    let div_str=`<div class="product-card">
                <img src="${product.image }" alt="{{ product.title }}">
                <h3>${ product.title }</h3>
                <p>Price: ${ product.price } €</p>
                <a href="/product/${ product.id }" class="btn btn-primary">View Details</a>
            </div>`
    return document.createRange().createContextualFragment(div_str)//i convert the str into an html element
}

// the funtion that will fill the categories and sub categories 
function categories_subcategories() {
    let product_div=document.getElementById("product-list")
    let categories_ul=document.getElementById("categories_ul")
    let subcategories_ul=document.getElementById("subcategories_ul")
    let li_all=document.createElement("li")
    let li_all_but=document.createElement("button")
    li_all_but.className="dropdown-item"
    li_all_but.textContent="All"
    li_all_but.addEventListener("click",function(){//the All button of Categories is pressed
        product_div.innerHTML=""//i empty the div that has my products
        document.getElementById("sel_cat").textContent="All" 
        let sub_category=document.getElementById("sel_sub_cat").textContent //textConent in order to take what i selected not the p
        if(sub_category==="All"){
            for(let product of products_l){
                //i fill the empty div with product cards
                product_div.appendChild(create_product_card(product))
            }
        }
        else{
            for(let product of products_l){
                //if the user has clicked the ALL from Categories and also has ckicked a sub category, not all
                if(product.sub_category===sub_category){
                    //i fill the empty div with product cards
                    product_div.appendChild(create_product_card(product))
                }
            }
        }
        
    })
    li_all.appendChild(li_all_but)
    categories_ul.appendChild(li_all)

    let li_all2=document.createElement("li")
    let li_all_but2=document.createElement("button")
    li_all_but2.className="dropdown-item"
    li_all_but2.textContent="All"
    li_all_but2.addEventListener("click",function(){//the All button of Sub Categories is pressed
        product_div.innerHTML=""//i empty the div that has my products
        document.getElementById("sel_sub_cat").textContent="All" 
        let category=document.getElementById("sel_cat").textContent //textConent in order to take what i selected not the p
        if(category==="All"){
            for(let product of products_l){
                //i fill the empty div with product cards
                product_div.appendChild(create_product_card(product))
            }
        }
        else{
            for(let product of products_l){
                //if the user has clicked the ALL from Categories and also has ckicked a sub category, not all
                if(product.category===category){
                    //i fill the empty div with product cards
                    product_div.appendChild(create_product_card(product))
                }
            }
        }

    })
    li_all2.appendChild(li_all_but2)
    subcategories_ul.appendChild(li_all2)

    let unique_categories=[]
    let unique_subcategories=[]
    for(let product of products_l){//when i put the data to javascript i named it products_l
        //if the category of the product it is not in the unique categories
        if(!unique_categories.includes(product.category)){
            //in order not to put 2 or 3 times the same category i do push
            unique_categories.push(product.category)
            let li=document.createElement("li")
            let li_but=document.createElement("button")
            li_but.className="dropdown-item"
            li_but.textContent=product.category
            li_but.addEventListener("click",function(){//some button of Categories is pressed(not All)
                product_div.innerHTML=""//i empty the div that has my products
                document.getElementById("sel_cat").textContent=product.category 
                let sub_category=document.getElementById("sel_sub_cat").textContent //textConent in order to take what i selected not the p
                if(sub_category==="All"){
                    for(let product_cat of products_l){
                        //only the products from the category the user clicked
                        if(product.category===product_cat.category){
                            //i fill the empty div with product cards
                            product_div.appendChild(create_product_card(product_cat))
                        }
                        
                    }
                }
                else{
                    for(let product_cat of products_l){
                        if(product_cat.sub_category===sub_category && product.category===product_cat.category ){// i keep both category and sub category
                            //i fill the empty div with product cards
                            product_div.appendChild(create_product_card(product_cat))
                        }
                    }
                }
            })
            li.appendChild(li_but)
            categories_ul.appendChild(li)
        }
         //if the category of the product it is not in the unique categorie
        if(!unique_subcategories.includes(product.sub_category)){
            unique_subcategories.push(product.sub_category)
            let li=document.createElement("li")
            let li_but=document.createElement("button")
            li_but.className="dropdown-item"
            li_but.textContent=product.sub_category
            li_but.addEventListener("click",function(){
                product_div.innerHTML=""//i empty the div that has my products
                document.getElementById("sel_sub_cat").textContent= product.sub_category
                let category=document.getElementById("sel_cat").textContent //textConent in order to take what i selected not the p
                if(category==="All"){
                    for(let product_sub of products_l){
                        if(product.sub_category===product_sub.sub_category){//i fill the empty div with product cards
                            product_div.appendChild(create_product_card(product_sub))

                        }
                    
                    }
                }
                else{
                    for(let product_sub of products_l){
                        if(product_sub.category===category && product.sub_category===product_sub.sub_category){// i keep both category and sub category
                            //i fill the empty div with product cards
                            product_div.appendChild(create_product_card(product_sub))
                        }
                    }
                }
            })
            li.appendChild(li_but)
            subcategories_ul.appendChild(li)

        }
    }
}

window.onload=function(){

    categories_subcategories()
}