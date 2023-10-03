document.addEventListener("DOMContentLoaded", () => {
    const searchButton = document.getElementById("searchButton");
    const searchInput = document.getElementById("searchInput");
    const resultsDiv = document.getElementById("results");

    searchButton.addEventListener("click", () => {
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
                            const restaurantDiv = document.createElement("div");
                            restaurantDiv.textContent = restaurant.name;
                            resultsDiv.appendChild(restaurantDiv);
                        });
                    }
                })
                .catch(error => {
                    console.error("Error fetching data:", error);
                });
        }
    });
});
