//add to cart
///去串store.html的class=update-cart


var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		var quantity = parseInt(this.dataset.quantity)
		console.log('productId:', productId, 'Action:', action, 'quantity', quantity)
		console.log('USER:', user)

        if (user == 'AnonymousUser'){ ///django當無user的時候會自動給這個值
            addCookieItem(productId, action, quantity)

        }else{
            updateUserOrder(productId, action, quantity)
        }

	})
}


/// cookie，去讓沒有登陸的使用者依然記得他之前點過的選項
function addCookieItem(productId, action, quantity){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':quantity}

		}else{
			cart[productId]['quantity'] += quantity
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= quantity

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"

	location.reload()
}


function updateUserOrder(productId, action, quantity){
    console.log('User is authenticated, sending data...')

	    var url = '/updateitem/' ///去使用url.py update的網址

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			},
			body:JSON.stringify({'productId':productId, 'action':action, 'quantity': quantity})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}


///串view.heml add, minus

function addFunction(){
    var qty = parseInt(document.getElementById('quantity').value)
    if (qty < 10){
    qty += 1
    document.getElementById('quantity').value = qty;
    }

}

function minusFunction(){
    var qty = parseInt(document.getElementById('quantity').value)
    if (qty > 0){
    qty -= 1
    document.getElementById('quantity').value = qty;
    }

}

var viewupdateBtns = document.getElementsByClassName('view-update-cart')

for (i = 0; i < viewupdateBtns.length; i++) {
	viewupdateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		var quantity = parseInt(document.getElementById('quantity').value)
		console.log('productId:', productId, 'Action:', action, 'quantity:', quantity)
		console.log('USER:', user)

        if (user == 'AnonymousUser'){ ///django當無user的時候會自動給這個值
            addCookieItem(productId, action, quantity)

        }else{
            updateUserOrder(productId, action, quantity)
        }

	})
}
