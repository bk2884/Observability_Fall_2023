document.addEventListener("DOMContentLoaded", () => {
    const searchButton = document.getElementById("searchButton");
    const searchInput = document.getElementById("searchInput");
    const resultsDiv = document.getElementById("results");

    // Function to search for restaurants
    function searchRestaurants() {
        const searchTerm = searchInput.value.trim();
        // Check if the search term is not empty
        if (searchTerm !== "") {
            // Make an API request to /search endpoint (replace with your actual API endpoint)
            // You can use fetch or another library like Axios for this.
            // Example using fetch:
            fetch(`/search?query=${searchTerm}`)
                .then(response => response.json())
                .then(data => {
                    // Clear previous results
                    resultsDiv.innerHTML = "";

                    // Process and display the search results
                    if (data.length === 0) {
                        resultsDiv.innerHTML = "No restaurants found.";
                    } else {
                        data.forEach(restaurant => {
                            // Create a div element for each restaurant
                            const restaurantDiv = document.createElement("div");
                            // Create elements for name and borough
                            const nameElement = document.createElement("p");
                            // Set text content for name and borough
                            nameElement.textContent = "Name: " + restaurant.name + " City: " + restaurant.borough;
                            // Append name and borough elements to the restaurant div
                            restaurantDiv.appendChild(nameElement);
                            // Append the restaurant div to the resultsDiv
                            resultsDiv.appendChild(restaurantDiv);
                        });
                    }
                })
                .catch(error => {
                    console.error("Error fetching data:", error);
                });
        }
    }

    // Attach an event listener to the search button for searching
    if (searchButton) {
        searchButton.addEventListener("click", searchRestaurants);
    }

    // Attach an event listener to the search input field for searching on "Enter" key press
    if (searchInput) {
        searchInput.addEventListener("keyup", event => {
            if (event.key === "Enter") {
                searchRestaurants();
            }
        });
    }
});


// Function to save user registration data and redirect to index.html
function saveUserDataAndRedirect() {
    const firstNameInput = document.getElementById("firstName");
    const lastNameInput = document.getElementById("lastName");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const cuisineInput = document.getElementById("cuisine");

    const userData = {
        firstName: firstNameInput.value.trim(),
        lastName: lastNameInput.value.trim(),
        email: emailInput.value.trim(),
        password: passwordInput.value.trim(),
        cuisine: cuisineInput.value.trim(),
    };

    if (userData.firstName !== "" && userData.lastName !== "" && userData.email !== "" && userData.password !== "" && userData.cuisine !== "") {
        // Make an AJAX POST request to save user registration data
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        })
            .then(response => response.json())
            .then(data => {
                // Handle the response (e.g., show a success message)
                console.log(data.message);

                // Redirect to index.html after successful registration
                window.location.href = "/index";
            })
            .catch(error => {
                console.error("Error saving user data:", error);
            });
    }
}

// Attach an event listener to the registration form submit button for saving user data and redirecting
const registrationForm = document.getElementById("registrationForm");
if (registrationForm) {
    registrationForm.addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent the default form submission
        saveUserDataAndRedirect();
    });
}



