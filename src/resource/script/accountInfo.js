document.querySelector("#ai_p_logout").onclick = function (e) {
    fetch('/logout')
        .then(response => response.json())
        .then(location.href = "/")
        .catch(error => console.error('Error:', error));
}

flatpickr("#input-udt-date", { minDate: "2020-01-01", maxDate: "today" });

document.querySelector("#ai_b_udt_save").onclick = function (e) {
    let bthis = this
    bthis.innerHTML = '<span class="spinner-border spinner-border-sm" aria-hidden="true"> </span><span role="status"> Loading...</span>'
    document.querySelector("#ai_udt_boolert").parentNode.classList.add("g")


    let nick = document.querySelector("#input-udt-nick").value
    let date = document.querySelector("#input-udt-date").value

    let formData = new FormData();
    formData.append("nick", nick);
    formData.append("date", date);


    fetch("/updateAccount", {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            dealHttpHint("#ai_udt_boolert", data)
            bthis.innerHTML = "Save"
            if (data.status == "200") {
                location.reload()
            }
        })
        .catch(error => {
            dealHttpHint("#ai_udt_boolert", { "status": "usr", "desc": "System Error." })
            bthis.innerHTML = "Save"
            console.error("Error:", error)
        });

}

function updateAvatar(file){
    if (file) {
        const por = document.querySelector("#ai_d_img img")
        let reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = function (e) {
            const img = new Image();
            img.src = e.target.result;
            img.onload = function () {
                const targetSize = 100;
                const canvas = document.createElement("canvas");
                canvas.width = targetSize;
                canvas.height = targetSize;
                const ctx = canvas.getContext("2d");

                const imgWidth = img.width;
                const imgHeight = img.height;

                // crop the center area
                let cropSize, sx, sy;
                if (imgWidth > imgHeight) {
                    cropSize = imgHeight;
                    sx = (imgWidth - cropSize) / 2;
                    sy = 0;
                } else {
                    cropSize = imgWidth;
                    sx = 0;
                    sy = (imgHeight - cropSize) / 2;
                }

                ctx.drawImage(img, sx, sy, cropSize, cropSize, 0, 0, targetSize, targetSize);
                const compressedBase64 = canvas.toDataURL("image/jpeg", 1);
                por.src = compressedBase64;

                fetch("/uploadImage", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ image: compressedBase64 })
                })
                    .then(res => {
                        // refresh avatar in nav bar
                        refreshAvatar(compressedBase64)
                    })
                    .then(data => console.log("success", data.desc))

            };
        }

    }
}

const ai_d_img = document.querySelector("#ai_d_img")
ai_d_img.onclick = function (e) {
    dthis = this
    const hfs = this.querySelector("input")
    hfs.click()
    hfs.addEventListener("change", function (event) {
        if (hfs.files.length > 0) {
            const file = hfs.files[0]
            updateAvatar(file)
        }
    })
}

// const dropArea = document.getElementById("dropArea");
// const preview = document.getElementById("preview");

ai_d_img.addEventListener("dragover", (event) => {
    event.preventDefault(); // allow dragging, obligatory
    ai_d_img.style.borderColor = "red"; 
});

ai_d_img.addEventListener("dragleave", () => {
    ai_d_img.style.borderColor = "#d9dde1";
});

//when drop of file
ai_d_img.addEventListener("drop", (event) => {
    event.preventDefault();
    ai_d_img.style.borderColor = "#d9dde1";

    const file = event.dataTransfer.files[0]; 
    if (file && file.type.startsWith("image/")) {
        updateAvatar(file)
    }
});