// Funtion to update rating
function rating_stars(username,product_id,n) {
    let stars = document.getElementsByClassName("star");
    let output = document.getElementById("output");
    remove();
    for (let i = 0; i < n; i++) {
        if (n == 1) cls = "one";
        else if (n == 2) cls = "two";
        else if (n == 3) cls = "three";
        else if (n == 4) cls = "four";
        else if (n == 5) cls = "five";
        stars[i].className = "star " + cls;
    }
    output.innerText = "Rating is: " + n + "/5";
    post_rating(username,product_id,n)
}
 
// To remove the pre-applied styling
function remove() {
    let stars =  document.getElementsByClassName("star");

    let i = 0;
    while (i < 5) {
        stars[i].className = "star";
        i++;
    }
}

function post_rating(username,product_id,rating){
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value; // Get token from form

    fetch('/rating/', {
        method: 'POST', // Specify the request method
        headers: {
            'Content-Type': 'application/json', // Set content type
            'X-CSRFToken': csrfToken, // Include the CSRF token
        },
        body: JSON.stringify({
            username: username,
            product_id: product_id,
            rating: rating
        }), // The data to send
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json(); // Parse the JSON response
        })
        .then(data => {
            console.log('Success:', data); // Handle the data
        })
        .catch(error => {
            console.error('Error:', error); // Handle any errors
        });
}