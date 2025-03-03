function goToMajor() {
    let major = document.getElementById("major").value;
    if (major) {
        window.location.href = "/" + major;
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const year = document.getElementById("year");
    const term = document.getElementById("term");
    const major = document.getElementById("major");
    const goButton = document.getElementById("goButton");

    function validateFields() {
        if (year.value !== "Select Year" && term.value !== "Select Term" && major.value !== "Select Major") {
            goButton.disabled = false;
        } else {
            goButton.disabled = true;
        }
    }
    year.addEventListener("change", validateFields);
    term.addEventListener("change", validateFields);
    major.addEventListener("change", validateFields);
    goButton.disabled = true;
});
