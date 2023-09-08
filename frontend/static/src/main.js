const captureButton = document.getElementById("captureButton");
const spinner = document.getElementById("spinnerToggle");
captureButton.addEventListener("click", function () {
    spinner.click()
    fetch("/_check_face")
        .then(function (response) {
            // The API call was successful!
            return response.json();
        })
        .then(function (data) {
            console.log(data);
            spinner.click();

            const modalToggle = document.getElementById("modalToggle");
            const modalText = document.getElementById("modalText");
            modalText.innerHTML = `${data["name"]} has successfully checked in!`;
            modalToggle.click();
        })
        .catch(function (err) {
            // There was an error
            console.warn("Something went wrong.", err);
        });
});