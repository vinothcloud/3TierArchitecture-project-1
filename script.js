document.getElementById("loginButton").addEventListener("click", function () {
    // Replace with the actual DNS or IP of your Backend Load Balancer (ALB)
    const backendURL = "http://BackendLB-url.com/login"; // Example: http://api.example.com/login

    // Make a GET request to the backend
    fetch(backendURL, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Network error: ${response.status} ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        const responseElement = document.getElementById("response");

        if (data.username && data.email) {
            responseElement.innerText = `User: ${data.username} - Email: ${data.email}`;
        } else {
            responseElement.innerText = "No user data found!";
        }
    })
    .catch(error => {
        console.error("Fetch error:", error);
        document.getElementById("response").innerText = "Failed to load data!";
    });
});
