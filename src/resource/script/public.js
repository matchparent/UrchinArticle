function dealHttpHint(id, data) {
    let boolert = document.querySelector(id);
    boolert.parentNode.classList.remove("g")
    boolert.classList.remove("alert-primary")
    boolert.classList.remove("alert-danger")
    let boolert_d = boolert.querySelector("div")
    let use = boolert.querySelector("use")

    if (data.status == "200") {
        boolert.classList.add("alert-primary")
        use.setAttribute("xlink:href", "#check-circle-fill")
    } else {
        boolert.classList.add("alert-danger")
        use.setAttribute("xlink:href", "#exclamation-triangle-fill")
    }
    boolert_d.innerHTML = data.desc

}


function initDropdown(outerId) {
    const ddItems = document.querySelectorAll(outerId + " .dropdown-item")
    const ddSpan = document.querySelector(outerId + " span")
    
    function ddItemsClick(e) {
        e.preventDefault()
        const preAct = document.querySelector(outerId + " .dropdown-item.active")
        if (preAct) {
            preAct.classList.remove("active")
        }
        this.classList.add("active")

        ddSpan.innerHTML = this.innerHTML
        ddSpan.dataset.ddId = this.dataset.ddId
    }
    ddItems.forEach(item => {
        item.onclick = ddItemsClick
    });
}