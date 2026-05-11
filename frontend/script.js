async function predictImage() {

    const fileInput = document.getElementById("imageInput");

    const resultEmpty = document.getElementById("result-empty");

    const resultContent = document.getElementById("result-content");

    const diseaseName = document.getElementById("disease-name");

    const confidence = document.getElementById("confidence");

    const solutionText = document.getElementById("solution-text");

    const previewContainer = document.getElementById("preview-container");

    const previewImg = document.getElementById("preview-img");

    const file = fileInput.files[0];

    // CHECK IMAGE SELECTED
    if (!file) {

        alert("Please select a cotton leaf image");

        return;
    }

    // VALID IMAGE TYPES
    const allowedTypes = [
        "image/jpeg",
        "image/png",
        "image/webp"
    ];

    if (!allowedTypes.includes(file.type)) {

        alert("Invalid file type");

        return;
    }

    // SHOW PREVIEW
    previewContainer.style.display = "block";

    previewImg.src = URL.createObjectURL(file);

    // LOADING STATE
    resultEmpty.style.display = "block";

    resultContent.style.display = "none";

    resultEmpty.innerHTML = `
        <div class="result-empty-icon">⏳</div>
        <p>Checking cotton leaf image...</p>
    `;

    // SEND IMAGE
    const formData = new FormData();

    formData.append("file", file);

    try {

        const response = await fetch("http://127.0.0.1:5000/predict", {

            method: "POST",

            body: formData

        });

        const data = await response.json();

        // INVALID IMAGE
        if (data.prediction === "Invalid Image") {

            resultEmpty.style.display = "block";

            resultContent.style.display = "none";

            resultEmpty.innerHTML = `
                <div class="result-empty-icon">❌</div>

                <p>
                    Invalid Image <br>
                    Please upload only cotton leaf images
                </p>
            `;

            previewImg.src = "";

            return;
        }

        // SHOW RESULT
        resultEmpty.style.display = "none";

        resultContent.style.display = "block";

        diseaseName.innerText = data.prediction;

        confidence.innerText = data.confidence + "%";

        // SOLUTION
        if (data.prediction === "Bacterial Blight") {

    solutionText.innerText =
        "Apply copper-based bactericide. Remove and destroy infected plant parts. Avoid overhead irrigation.";
}

else if (data.prediction === "Fusarium Wilt") {

    solutionText.innerText =
        "Use resistant varieties. Treat soil with fungicide before planting. Practice crop rotation.";
}

else if (data.prediction === "Alternaria Leaf Spot") {

    solutionText.innerText =
        "Apply mancozeb or iprodione fungicide. Improve air circulation. Avoid prolonged leaf wetness.";
}

else if (data.prediction === "Healthy Leaf") {

    solutionText.innerText =
        "No treatment required. Continue regular monitoring and preventive care.";
}

else if (data.prediction === "Verticillium Wilt") {

    solutionText.innerText =
        "Use resistant cultivars. Implement soil fumigation. Remove infected debris. Practice long crop rotations.";
}

else {

    solutionText.innerText =
        "Maintain field hygiene and monitor crop health.";

    }

}

    catch (error) {

        resultEmpty.style.display = "block";

        resultContent.style.display = "none";

        resultEmpty.innerHTML = `
            <div class="result-empty-icon">⚠️</div>

            <p>
                Server Error <br>
                Please try again
            </p>
        `;

        console.log(error);
    }
}