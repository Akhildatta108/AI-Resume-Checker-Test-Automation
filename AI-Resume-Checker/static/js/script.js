// script.js
// Small helper for the upload page: shows the chosen file name
// and lets the user drag-and-drop a file onto the drop area.

document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("resume");
    const fileLabel = document.getElementById("fileLabel");
    const dropArea = document.getElementById("dropArea");

    if (!fileInput) return; // not on the upload page, do nothing

    // Update the label text whenever a file is chosen via the file picker.
    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            fileLabel.textContent = "Selected file: " + fileInput.files[0].name;
        }
    });

    // Highlight the drop area while a file is being dragged over it.
    dropArea.addEventListener("dragover", function (event) {
        event.preventDefault();
        dropArea.style.backgroundColor = "#dbeafe";
    });

    dropArea.addEventListener("dragleave", function () {
        dropArea.style.backgroundColor = "";
    });

    // Handle the actual file drop.
    dropArea.addEventListener("drop", function (event) {
        event.preventDefault();
        dropArea.style.backgroundColor = "";
        const droppedFiles = event.dataTransfer.files;
        if (droppedFiles.length > 0) {
            fileInput.files = droppedFiles;
            fileLabel.textContent = "Selected file: " + droppedFiles[0].name;
        }
    });
});
