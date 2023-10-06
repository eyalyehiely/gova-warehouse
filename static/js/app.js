const form_btn = document.getElementById('form-btn');
const category = document.getElementById('category');
const categoryItem = document.getElementById('item_name');
const form = document.getElementById('request-form');
const submit_btn = document.getElementById('submit_btn');
items = [];


categoryItem.addEventListener('change', async function () {
    // const data = await fetch(`/item/quantity/${categoryItem.value}`);
    const data = await fetch(`/item/quantity/`);
    const item = await data.json();
    const amount = document.getElementById('quantity');
    if (item.quantity === 0){
        amount.max = 0;
    }
    else {
        amount.max = item.quantity;
        amount.min = 1;
    }
    console.log(item);

});


form_btn.addEventListener('click',  function () {
    event.preventDefault();
    const categoryValue = category.value;
    const itemValue = categoryItem.value;
    const quantity = document.getElementById('quantity').value;
    const returning_date = document.getElementById('returning_date').value;
    const taking_date = document.getElementById('taking_date').value;


    const request = {
        category: categoryValue,
        name : itemValue,
        quantity : quantity,
        returning_date : returning_date,
        taking_date : taking_date,
    }
    console.log(request);
    items.push(request);
    displayItems();
    form.reset();
    category.focus();




});

submit_btn.addEventListener('click', async function (event) {
    event.preventDefault();  // Prevent the default form submission behavior

    // Send items to server
    try {
        const response = await fetch('/get_data_requests', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',

            },
            body: JSON.stringify({ items: items })
        });

        // Check if the request was successful
        if (!response.ok) {
            throw new Error(`Network response was not ok ${response.statusText}`);
        }

        const responseData = await response.json();  // Parse and return the JSON from the response
        console.log(responseData);

        window.alert("Your request has been sent successfully");
        window.location.href = '/';  // Redirect to home page

    } catch (error) {
        console.error('There was a problem with the fetch:', error);
        window.alert("Failed to send request, please try again.");
    }
});



function deleteItem(id){
    items.splice(id, 1);
    displayItems();
}
function displayItems(){
    const itemsContainer = document.getElementById("itemsContainer");

    let html = "";
    for(let i = 0; i < items.length; i++){
        const formattedTakingDate = new Date(items[i].taking_date).toLocaleDateString();
        const formattedReturningDate = new Date(items[i].returning_date).toLocaleDateString();

        html += `
        <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">📦 ${items[i].category}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">${items[i].name}</h6>
                    <p class="card-text">
                        <strong>🔢 Quantity:</strong> ${items[i].quantity}<br>
                        <strong>📅 Taking Date:</strong> ${formattedTakingDate}<br>
                        <strong>🔄 Returning Date:</strong> ${formattedReturningDate}
                    </p>
                </div>
                <div class="card-footer">
                    <button class="btn btn-danger" onclick="deleteItem(${i})">Delete</button>
                </div>
            </div>
        </div>
        `;
    }
    itemsContainer.innerHTML = html;
}




category.addEventListener("change", async function () {
        let categoryValue = category.value;
        const data = await fetch(`/select_category?category=${categoryValue}`);
        const items = await data.json();

        categoryItem.innerHTML = '';
        items.forEach(item => {
            const option = document.createElement('option');
            option.value = item.item_name;
            option.innerText = item.item_name;
            categoryItem.appendChild(option);
        });
    });

function validateInput(input) {
    const min = parseInt(input.min);
    const max = parseInt(input.max);
    if (input.value < min) {
        input.setCustomValidity(`Minimum value is ${min}`);
    } else if (input.value > max) {
        input.setCustomValidity(`Maximum value is ${max}`);
    } else {
        // Reset custom validity if the value is now valid
        input.setCustomValidity('');
    }
}


