document.addEventListener("DOMContentLoaded", () => {
    const searchButton = document.getElementById("searchButton");
    const searchInput = document.getElementById("searchInput");
    const resultsDiv = document.getElementById("results");

    function searchRestaurants() {
        const searchTerm = searchInput.value.trim();

        if (searchTerm !== "") {
            // Make an API request to the /search endpoint
            fetch(`/search?query=${searchTerm}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error("Network response was not ok");
                    }
                    return response.json();
                })
                .then(data => {
                    // Clear previous results
                    resultsDiv.innerHTML = "";

                    if (data.length === 0) {
                        resultsDiv.textContent = "No restaurants found.";
                    } else {
                        data.forEach(restaurant => {
                            const restaurantDiv = document.createElement("div");
                            const nameElement = document.createElement("p");
                            nameElement.textContent = "Name: " + restaurant.name + " City: " + restaurant.borough;
                            restaurantDiv.appendChild(nameElement);
                            resultsDiv.appendChild(restaurantDiv);
                        });
                    }
                })
                .catch(error => {
                    console.error("Error fetching data:", error);
                    resultsDiv.textContent = "An error occurred while fetching data.";
                });
        }
    }

    if (searchButton) {
        searchButton.addEventListener("click", searchRestaurants);
    }

    if (searchInput) {
        searchInput.addEventListener("keyup", event => {
            if (event.key === "Enter") {
                searchRestaurants();
            }
        });
    }
});


// Function to save user registration data and redirect to /login
function saveUserDataAndRedirect() {
    const firstNameInput = document.getElementById("first_name");
    const lastNameInput = document.getElementById("last_name");
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

                // Redirect to /login after successful registration
                window.location.href = "/login"; // Redirect to the /login endpoint
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



document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const signUpLink = document.getElementById("signUpLink"); // Add an ID to your "sign up here" link

    loginForm.addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent the default form submission

        const emailInput = document.getElementById("email");
        const passwordInput = document.getElementById("password");

        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

        const loginData = {
            email: email,
            password: password,
        };

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = "/index"; // Redirect to index.html after successful login
            } else {
                // Handle authentication error (display an error message if needed)
                console.error("Authentication failed:", data.message);
            }
        })
        .catch(error => {
            console.error("Error authenticating user:", error);
        });
    });

    // Add an event listener to the "sign up here" link
    if (signUpLink) {
        signUpLink.addEventListener("click", () => {
            // Redirect to the registration page
            window.location.href = "/register";
        });
    }
});

