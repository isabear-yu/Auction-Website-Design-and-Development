let product_filter = "all"

function getProducts()
{
	modified_url = "/LuxuryAuction/refresh-products/" + product_filter
	$.ajax({
		url: modified_url,
		dataType: "json",
		success: updatePage,
		error: updateError
	});
}

function setFilter(filter)
{
	product_filter = filter
	console.log("filter is set to: ", product_filter)
}

//Should probably include some kind of error checking here
function updatePage(response) {
	updateProducts(response)
}

function updateError(response)
{
	console.log("Error")
}

function updateProducts(products)
{
	counter = 0
	$(products).each(function() {
		product_id=this.id
		if(document.getElementById(product_id) == null)
		{
			let formatted_date = (new Date(this.starting_time)).toLocaleDateString()
			let formatted_time = (new Date(this.starting_time)).toLocaleTimeString()
			let formatted_start = formatted_time + " " + formatted_date
			let element_string = ('<td>' +
				'<div class="ProductHomePage" id="' +
				this.id +
				'">' +
				this.title +
				'<br>' +
				'<img src="/luxuryauction/media/bluebelle1.jpg" >' +
				'<br>' +
				'Category: ' +
				this.category +
				'<br>' +
				'Starting Price: $' +
				this.starting_bid +
				'<br>' +
				'Start Time: ' +
				formatted_time +
				'<br>' +
				'Start Date: ' +
				formatted_date +
				'</div>' +
				'</td>')
			if(counter % 3 == 0)
				$("#product-list").append('<tr>')
			$("#product-list").append(element_string)
			if(counter % 3 == 0)
				$("#product-list").append('</tr>')
		}
		counter++
	})
}

function getCSRFToken()
{
	let cookies = document.cookie.split(";")
	for(let i = 0; i < cookies.length; i++)
	{
		let c = cookies[i].trim()
		if (c.startsWith("csrftoken="))
		{
			return c.substring("csrftoken=".length, c.length)
		}
	}
	return "unknown";
}
