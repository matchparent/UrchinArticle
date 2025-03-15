
const requestPrompt = document.getElementById('request_prompt')
const prompt_content = document.getElementById('prompt_content')
const prompt_use = prompt_content.querySelector("use")
const prompt_span = document.querySelector("#request_prompt span")

requestPrompt.addEventListener('shown.bs.modal', event => {
    const backdrops = document.querySelectorAll('.modal-backdrop');
    const lastBackdrop = backdrops[backdrops.length - 1];
    lastBackdrop.style.zIndex = 1999
})

const promptor = new bootstrap.Modal(requestPrompt);
const promptSpan = document.querySelector("#request_prompt span")
const promptLoad = document.querySelector("#request_prompt .spinner-border-sm")

function showPrompt(d) {
    promptor.show()
    prompt_span.innerHTML = d.desc
    prompt_content.classList.remove("alert-primary")
    prompt_content.classList.remove("alert-danger")
    prompt_content.classList.remove("alert-info")
    if (d.status == "load") {
        prompt_content.classList.add("alert-info")
        prompt_use.parentNode.classList.add("g")
        promptLoad.classList.remove("g")
    } else {
        promptLoad.classList.add("g")
        prompt_use.parentNode.classList.remove("g")
        if (d.status == "200") {
            prompt_content.classList.add("alert-primary")
            prompt_use.setAttribute("xlink:href", "#check-circle-fill")
        } else {
            prompt_content.classList.add("alert-danger")
            prompt_use.setAttribute("xlink:href", "#exclamation-triangle-fill")
        }
    }

}

function hidePrompt() {
    promptor.hide()
}

// showPrompt({ "status": "load", "desc": "Loading..." })
// showPrompt({ "status": "err", "desc": "Success!" })
// hidePrompt()
