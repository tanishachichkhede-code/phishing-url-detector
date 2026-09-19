async function scanURL() {

    const input = document.getElementById("urlInput");
    const button = document.getElementById("scanButton");
    const buttonText = document.getElementById("buttonText");
    const loader = document.getElementById("buttonLoader");

    const resultContainer =
        document.getElementById("resultContainer");

    const errorContainer =
        document.getElementById("errorContainer");

    const errorMessage =
        document.getElementById("errorMessage");

    const url = input.value.trim();

    if (!url) {
        showError("Please enter a URL.");
        return;
    }

    resultContainer.classList.add("hidden");
    errorContainer.classList.add("hidden");

    button.disabled = true;
    buttonText.textContent = "Scanning...";
    loader.classList.remove("hidden");

    try {

        const response = await fetch("/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                url: url
            })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Unable to scan URL."
            );
        }

        showResult(data);

    } catch (error) {

        showError(error.message);

    } finally {

        button.disabled = false;
        buttonText.textContent = "Scan URL";
        loader.classList.add("hidden");

    }
}


function showResult(data) {

    const resultContainer =
        document.getElementById("resultContainer");

    const resultTitle =
        document.getElementById("resultTitle");

    const resultIcon =
        document.getElementById("resultIcon");

    const scannedUrl =
        document.getElementById("scannedUrl");

    const legitimateProbability =
        document.getElementById(
            "legitimateProbability"
        );

    const phishingProbability =
        document.getElementById(
            "phishingProbability"
        );

    const legitimateBar =
        document.getElementById(
            "legitimateBar"
        );

    const phishingBar =
        document.getElementById(
            "phishingBar"
        );


    scannedUrl.textContent = data.url;

    resultTitle.textContent =
        data.prediction;


    legitimateProbability.textContent =
        `${data.legitimate_probability}%`;

    phishingProbability.textContent =
        `${data.phishing_probability}%`;


    legitimateBar.style.width =
        `${data.legitimate_probability}%`;

    phishingBar.style.width =
        `${data.phishing_probability}%`;


    if (data.prediction === "Phishing") {

        resultIcon.textContent = "⚠";

        resultTitle.style.color = "#ff6174";

        resultContainer.style.borderColor =
            "#69313c";

    } else {

        resultIcon.textContent = "✓";

        resultTitle.style.color = "#55e6b5";

        resultContainer.style.borderColor =
            "#1b4a42";

    }


    resultContainer.classList.remove(
        "hidden"
    );

    resultContainer.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}


function showError(message) {

    const errorContainer =
        document.getElementById("errorContainer");

    const errorMessage =
        document.getElementById("errorMessage");

    errorMessage.textContent = message;

    errorContainer.classList.remove(
        "hidden"
    );
}


document
    .getElementById("urlInput")
    .addEventListener(
        "keydown",
        function(event) {

            if (event.key === "Enter") {
                scanURL();
            }

        }
    );