function startTransfer() {
    const sourceBucket = document.getElementById("sourceBucket").value;
    const destBucket = document.getElementById("destBucket").value;
    const key = document.getElementById("fileKey").value;

    const statusBox = document.getElementById("status");
    statusBox.className = "alert alert-info";
    statusBox.textContent = "Transfer in progress...";

    fetch("/transfer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            source_bucket: sourceBucket,
            dest_bucket: destBucket,
            key: key
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            statusBox.className = "alert alert-success";
        } else {
            statusBox.className = "alert alert-danger";
        }
        statusBox.textContent = data.message;
    })
    .catch(err => {
        statusBox.className = "alert alert-danger";
        statusBox.textContent = "Error: " + err;
    });
}
