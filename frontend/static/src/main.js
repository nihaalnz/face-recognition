const captureButton = document.getElementById("captureButton");
const registerButton = document.getElementById("registerButton");
const registerForm = document.getElementById("registerForm");
const spinner = document.getElementById("spinnerToggle");
const capacity = document.getElementById("capacity");

function reloadCapacity() {
    fetch("/_capacity")
    .then(function (response) {
        // The API call was successful!
        return response.json();
    })
    .then(function (data) {
        console.log(data);
        capacity.innerHTML = `Capacity: ${data["capacity"]}`;
    })
    .catch(function (err) {
        // There was an error
        console.warn("Something went wrong.", err);
    }); 
}

window.onload = function () {
    console.log("loaded")
    reloadCapacity();
}

captureButton?.addEventListener("click", function () {
    spinner.click()
    fetch("/_check_face")
        .then(function (response) {
            // The API call was successful!
            return response.json();
        })
        .then(function (data) {
            console.log(data);
            const modalToggle = document.getElementById("modalToggle");
            const modalText = document.getElementById("modalText");
            const modalHeader = document.getElementById("modalHeader");

            if (data.detail) {
                console.log('error')
                modalHeader.innerHTML = "Error!";
                modalHeader.classList.add("text-red-500");
                modalText.innerHTML = `${data["detail"]}`;
                spinner.click()
                modalToggle.click();
                return;
            }

            spinner.click();
            modalHeader.innerHTML = "Success!";
            modalText.innerHTML = `<strong>${data["name"]}</strong> has successfully <strong>${data["status"]}</strong>!`;
            modalToggle.click();
            reloadCapacity();
        })
        .catch(function (err) {
            // There was an error            
            modalHeader.innerHTML = "Error!";
            modalText.innerHTML = "A client side error has occurred. Please check logs and try again later.";
            spinner.click(); // Hide spinner
            modalToggle.click();
            console.warn("Client side error.", err);
        });
});

registerForm?.addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent default form submission
    const name = document.getElementById("name").value;
    spinner.click(); // Show spinner
    fetch("/_register", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({name: name}),
    })
        .then(function (response) {
            // The API call was successful!
            return response.json();
        })
        .then(function (data) {
            console.log(data);
            const modalToggle = document.getElementById("modalToggle");
            const modalText = document.getElementById("modalText");
            const modalHeader = document.getElementById("modalHeader");

            if (data.detail) {
                console.log('error')
                modalHeader.innerHTML = "Error!";
                modalHeader.classList.add("text-red-500");
                modalHeader.classList.add("font-bold");
                modalHeader.classList.add("text-lg");
                modalText.innerHTML = `${data["detail"]}`;
                spinner.click(); // Hide spinner
                modalToggle.click();
                return;
            }
            
            spinner.click(); // Hide spinner
            modalHeader.innerHTML = "Success!";
            modalText.innerHTML = `${data["name"]} has <strong>successfully registered</strong>!`;
            modalToggle.click();
        })
        .catch(function (err) {
            // There was an error
            modalHeader.innerHTML = "Error!";
            modalText.innerHTML = "A client side error has occurred. Please check logs and try again later.";
            spinner.click(); // Hide spinner
            modalToggle.click();
            console.warn("Client side error.", err);
        });
});