const loginClick = document.querySelector("#co_d_navr_f>.co_a_lnr:first-of-type")
const topAd = document.querySelector(".co_div_top_ad")

const theme_fes = "/css/common_fes.css"
const theme_norm = "/css/common_norm.css"

function loadTheme() {
    let isFes = localStorage.getItem("fesTheme") === "true";
    let themeFile = isFes ? theme_fes : theme_norm;
    document.getElementById("theme-css").href = themeFile;
    if(isFes){
        topAd.classList.add("g")
    }else{
        topAd.classList.remove("g")
    }
}

function toggleTheme() {
    let isFes = localStorage.getItem("fesTheme") === "true"; 
    localStorage.setItem("fesTheme", !isFes); 
    loadTheme(); 
}

topAd.querySelector("button").onclick = (e)=>{
    topAd.classList.add("g")
}

loadTheme()

//change of title style
document.getElementById("shift").onclick = function (e) {
    e.preventDefault()
    toggleTheme()
    // let dts = document.documentElement.style
    // if (dts.getPropertyValue('--fes-bgi') == "url('')") {
    //     dts.setProperty('--fes-bgi', "url('../pic/hometop.avif')");
    //     dts.setProperty('--fes-fc', 'white')
    //     dts.setProperty('--fes-fhc', '#f5cf9a')
    //     dts.setProperty('--fes-sc', 'rgba(0, 0, 0, 0.40)')
    //     dts.setProperty('--fes-sbc', 'transparent')
    //     document.querySelector('.co_div_top_ad').style.display = 'block'
    // } else {
    //     dts.setProperty('--fes-bgi', "url('')");
    //     dts.setProperty('--fes-fc', '#545C63')
    //     dts.setProperty('--fes-fhc', 'black')
    //     dts.setProperty('--fes-sc', '#F01414')
    //     dts.setProperty('--fes-sbc', '#F01414')
    //     document.querySelector('.co_div_top_ad').style.display = 'none'
    // }

}

//tab discovery popup window
let popup = document.querySelector(".co_popwin_discovery")
let dcr = document.querySelector(".co_i_discovery").parentNode.parentNode

dcr.onmouseover = function (e) {

    const rect = this.getBoundingClientRect();
    popup.style.width = `${rect.right - rect.left}px`

    popup.style.top = `${rect.bottom + window.scrollY}px`;
    popup.style.left = `${rect.left + window.scrollX}px`;
    popup.classList.add("show")
}
let out = function (e) {
    if (!popup.contains(e.relatedTarget) && !dcr.contains(e.relatedTarget)) {
        popup.classList.remove("show")
    }
}
dcr.onmouseout = out
popup.onmouseout = out

//r4 hover effects
let r4ds = document.querySelectorAll(".co_div_r4_icon")
for (let i = 0; i < r4ds.length; i++) {
    r4ds[i].onmouseover = function (e) {
        let pp = this.firstElementChild;
        pp.innerHTML = pp.dataset.txt
        pp.style.color = "black"
        pp.style.fontSize = "12px"
        // pp.style.lineHeight = "30px"
    }

    r4ds[i].onmouseout = function (e) {
        let pp = this.firstElementChild;
        pp.innerHTML = pp.dataset.icon
        pp.style = ""
    }

}

document.querySelector(".co_b_reg_send").onclick = function (e) {
    let send = this;
    this.disabled = "disabled"
    let secs = 3000
    let iid = 0
    var tick = () => {
        secs -= 1000;
        this.innerHTML = (secs / 1000) + "s"

        if (secs <= 0) {
            clearInterval(iid)
            send.innerHTML = "Send"
            send.disabled = false
        }
    }
    iid = setInterval(tick, 1000);

    let formData = new FormData();
    formData.append("email", document.querySelector("#input-reg-mail").value);

    fetch("/emailVerify", {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(data => {
        })
        .catch(error => {

        });
}

let passes = document.querySelectorAll("#input-reg-pass, #input-reg-psag, input-login-pass")
let pass_over = function () {
    this.type = "text"
}

let pass_out = function () {
    this.type = "password"
}
passes.forEach(each => {
    each.onmouseover = pass_over
    each.onmouseout = pass_out
});

function deal_reg_hint(d) {
    let co_reg_boolert = document.querySelector("#co_reg_boolert");
    co_reg_boolert.parentNode.classList.remove("g")
    co_reg_boolert.classList.remove("alert-primary")
    co_reg_boolert.classList.remove("alert-danger")
    let co_reg_boolert_d = co_reg_boolert.querySelector("div")
    let use = co_reg_boolert.querySelector("use")

    if (d.status == "200") {
        co_reg_boolert.classList.add("alert-primary")
        use.setAttribute("xlink:href", "#check-circle-fill")
    } else {
        co_reg_boolert.classList.add("alert-danger")
        use.setAttribute("xlink:href", "#exclamation-triangle-fill")
    }
    co_reg_boolert_d.innerHTML = d.desc

}

function deal_login_hint(d) {
    let co_login_boolert = document.querySelector("#co_login_boolert");
    co_login_boolert.parentNode.classList.remove("g")
    co_login_boolert.classList.remove("alert-primary")
    co_login_boolert.classList.remove("alert-danger")
    let co_login_boolert_d = co_login_boolert.querySelector("div")
    let use = co_login_boolert.querySelector("use")

    if (d.status == "200") {
        co_login_boolert.classList.add("alert-primary")
        use.setAttribute("xlink:href", "#check-circle-fill")
    } else {
        co_login_boolert.classList.add("alert-danger")
        use.setAttribute("xlink:href", "#exclamation-triangle-fill")
    }
    co_login_boolert_d.innerHTML = d.desc
}

document.querySelector(".co_b_reg_submit").onclick = function (e) {
    e.preventDefault()

    let bthis = this
    bthis.innerHTML = '<span class="spinner-border spinner-border-sm" aria-hidden="true"> </span><span role="status"> Loading...</span>'
    document.querySelector("#co_reg_boolert").parentNode.classList.add("g")

    let email = bthis.parentNode.querySelector("#input-reg-mail").value
    let pass = bthis.parentNode.querySelector("#input-reg-pass").value
    let psag = bthis.parentNode.querySelector("#input-reg-psag").value
    let veri = bthis.parentNode.querySelector("#input-reg-veri").value

    if (pass === psag) {
        let formData = new FormData();
        formData.append("email", email);
        formData.append("pass", pass);
        formData.append("veri", veri);
        fetch("/register", {
            method: "POST",
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                deal_reg_hint(data)
                bthis.innerHTML = "Register Now"
                if (data.status == "200") {
                    location.reload()
                }
            })
            .catch(error => {
                deal_reg_hint({ "status": "usr", "desc": "System Error." })
                bthis.innerHTML = "Register Now"
                console.error("Error:", error)
            });
    } else {
        deal_reg_hint({ "status": "usr", "desc": "Passwords don't match with each other." })
        bthis.innerHTML = "Register Now"
    }

}

document.querySelector(".co_b_reg_login").onclick = function (e) {
    e.preventDefault()

    let bthis = this
    bthis.innerHTML = '<span class="spinner-border spinner-border-sm" aria-hidden="true"> </span><span role="status"> Loading...</span>'
    document.querySelector("#co_login_boolert").parentNode.classList.add("g")


    let email = bthis.parentNode.querySelector("#input-login-mail").value
    let pass = bthis.parentNode.querySelector("#input-login-pass").value
    let veri = bthis.parentNode.querySelector("#input-login-veri").value


    let formData = new FormData();
    formData.append("email", email);
    formData.append("pass", pass);
    formData.append("veri", veri);
    fetch("/login", {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            deal_login_hint(data)
            bthis.innerHTML = "Login"
            if (data.status == "200") {
                location.reload()
            }
        })
        .catch(error => {
            deal_login_hint({ "status": "usr", "desc": "System Error." })
            bthis.innerHTML = "Login"
            console.error("Error:", error)
        });
}

function refreshAvatar(compressedBase64) {
    document.querySelector("#co_d_navr_t img").src = compressedBase64;
}


const urlParams = new URLSearchParams(window.location.search);
const login = urlParams.get('login');
if (login) {
    loginClick.click()
}