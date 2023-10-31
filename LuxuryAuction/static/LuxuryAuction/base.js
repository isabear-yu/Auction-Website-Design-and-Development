"use strict"

function placeBid(item_id){
  var bidTextElement =  document.getElementById("bidprice")

  var bid_value   = bidTextElement.value

  // Clear input box and old error message (if any)
  bidTextElement.value=''
  displayError('')

  var req = new XMLHttpRequest()
  req.onreadystatechange = function() {
      if (req.readyState != 4) return
      if (req.status != 200) return
      var response = JSON.parse(req.responseText);
      if (Array.isArray(response)) {
          updateList(response);
      } else {
          displayError(response.error);
      }
  }

  req.open("POST", "/placeBid", true);
  req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  req.send("bid_value="+bid_value+"&csrfmiddlewaretoken="+getCSRFToken()+"&item_id="+item_id);
}



function getCurrentBid(item_id) {

  let request = new XMLHttpRequest()
  request.onreadystatechange = function() {
      if (request.readyState != 4) return
      updatePage(request)
  }

  request.open("GET", "/get-CurrentBid?item_id="+item_id, true);
  request.send();
}


function updatePage(request) {
  if (request.status != 200) {
      displayError("Received status code = " + request.status)
      return
  }

  let response = JSON.parse(request.responseText)
  if (Array.isArray(response)) {
      updateList(response)
  } else if (response.hasOwnProperty('error')) {
      displayError(response.error)
  } else {
      displayError(response)
  }
}



function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function updateList(items) {
    // Removes the old to-do list items
    let list = document.getElementById("CurrentBid")

    list.innerHTML = "<span>" + "Current bid: $" + items[0].price +"</span>"
}

function getCurrentBid1(item_id) {
  let request = new XMLHttpRequest()
  request.onreadystatechange = function() {
      if (request.readyState != 4) return
      updatePage1(request)
  }

  request.open("GET", "/add-onehund?item_id="+item_id, true);
  request.send();

}


function updatePage1(request) {
  if (request.status != 200) {
      displayError("Received status code = " + request.status)
      return
  }

  let response = JSON.parse(request.responseText)
  if (Array.isArray(response)) {
      updateList1(response)
  } else if (response.hasOwnProperty('error')) {
      displayError(response.error)
  } else {
      displayError(response)
  }
}


function updateList1(items) {
    // Removes the old to-do list items
    let list = document.getElementById("bidprice")
    while (list.hasChildNodes()) {
        list.removeChild(list.firstChild)
    }

    // Adds each new todo-list item to the list
    for (let i = 0; i < items.length; i++) {
        let item = items[i]
        list.value=parseFloat(item.price)+100

    }
}


function getCurrentBid2(item_id) {
  let request = new XMLHttpRequest()
  request.onreadystatechange = function() {
      if (request.readyState != 4) return
      updatePage2(request)
  }

  request.open("GET", "/add-twohund?item_id="+item_id, true);
  request.send();
}


function updatePage2(request) {
  if (request.status != 200) {
      displayError("Received status code = " + request.status)
      return
  }

  let response = JSON.parse(request.responseText)
  if (Array.isArray(response)) {
      updateList2(response)
  } else if (response.hasOwnProperty('error')) {
      displayError(response.error)
  } else {
      displayError(response)
  }
}


function updateList2(items) {
    // Removes the old to-do list items
    let list = document.getElementById("bidprice")
    while (list.hasChildNodes()) {
        list.removeChild(list.firstChild)
    }

    // Adds each new todo-list item to the list
    for (let i = 0; i < items.length; i++) {
        let item = items[i]
        list.value=parseFloat(item.price)+200

    }
}

function getCurrentBid3(item_id) {
  let request = new XMLHttpRequest()
  request.onreadystatechange = function() {
      if (request.readyState != 4) return
      updatePage3(request)
  }

  request.open("GET", "/add-threehund?item_id="+item_id, true);
  request.send();
}


function updatePage3(request) {
  if (request.status != 200) {
      displayError("Received status code = " + request.status)
      return
  }

  let response = JSON.parse(request.responseText)
  if (Array.isArray(response)) {
      updateList3(response)
  } else if (response.hasOwnProperty('error')) {
      displayError(response.error)
  } else {
      displayError(response)
  }
}


function updateList3(items) {
    // Removes the old to-do list items
    let list = document.getElementById("bidprice")
    while (list.hasChildNodes()) {
        list.removeChild(list.firstChild)
    }

    // Adds each new todo-list item to the list
    for (let i = 0; i < items.length; i++) {
        let item = items[i]
        list.value=parseFloat(item.price)+300


    }
}


function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown";
}


function timecountdown(item_id) {
  let request = new XMLHttpRequest()
  request.onreadystatechange = function() {
      if (request.readyState != 4) return
      updateTime(request)
  }

  request.open("GET", "/timecountdown?item_id="+item_id, true);

  request.send();
}

function updateTime(request) {
  if (request.status != 200) {
      displayError("Received status code = " + request.status)
      return
  }

  let response = JSON.parse(request.responseText)
  if (Array.isArray(response)) {
      displayTime(response)
  } else if (response.hasOwnProperty('error')) {
      displayError(response.error)
  } else {
      displayError(response)
  }
}

function displayTime(items) {
  let list = document.getElementById("winner")
  let pay = document.getElementById("payment")
  if ('user' in items[0]){
    if(items[0].loginuser==items[0].user){
      list.innerHTML=' You win the bidding!'
      pay.innerHTML='<button class="btn" style="color:#2F4F4F;" ><strong><a href="payment/'+items[0].id+'" style="color:#2F4F4F;">Pay now!</a></strong></button>'
    }
    else{
      list.innerHTML=items[0].user+' wins the bidding!'
    }
}
}

function biddingbutton(item_id){
  let request = new XMLHttpRequest()
  request.onreadystatechange = function() {
      if (request.readyState != 4) return
      updatebutton(request)

  }
  request.open("GET", "/biddingbutton?item_id="+item_id, true);
  request.send();
}


function updatebutton(request) {
  if (request.status != 200) {
      displayError("Received status code = " + request.status)
      return
  }

  let response = JSON.parse(request.responseText)
  if (Array.isArray(response)) {
      displayButton(response)
  } else if (response.hasOwnProperty('error')) {
      displayError(response.error)
  } else {
      displayError(response)
  }
}

function displayButton(items) {
    // Removes the old to-do list items
    let button = document.getElementById("Bidarea")
    while (button.hasChildNodes()) {
        button.removeChild(button.firstChild)
    }

    // Adds each new todo-list item to the list
    if (items[0].end=='N'){
      button.innerHTML = '<span style="color:#2F4F4F; font-size: 20px;"><strong>Current bid + </strong></span><button class="USD"  onclick="getCurrentBid1('+items[0].id+')" style="background-color:#2F4F4F; color:white;" > <strong>+$100 </strong></button>'
      + ' '+'<button class="USD"  onclick="getCurrentBid2('+items[0].id+')" style="background-color:#2F4F4F; color:white;" > <strong>+$200 </strong></button>'+
      ' '+'<button class="USD"  onclick="getCurrentBid3('+items[0].id+')" style="background-color:#2F4F4F; color:white;" > <strong>+$300 </strong></button>'+ '<br> <br><span id="error" ></span>'
      + '<div id="bidinputbox"><input type="number" id="bidprice" placeholder="bid price" name="item"> <button onclick="placeBid('+items[0].id+')" >Place bid</button></div>'
    }


    }
