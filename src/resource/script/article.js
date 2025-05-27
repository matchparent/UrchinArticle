const ac_a_subscribe = document.querySelector("#ac_a_subscribe")
const focus_txt = document.querySelector(".ac_d_atrnums table tr:last-child td:nth-child(2)");

function loadFocus() {
    if (ac_a_subscribe != null) {
        ac_a_subscribe.classList = ""
        ac_a_subscribe.classList.add(focused ? "ac_a_subscribe_gray" : "ac_a_subscribe_blue")
        ac_a_subscribe.innerHTML = focused ? "Focused" : "Focus and Subscribe"
    }
}

loadFocus()

if (ac_a_subscribe != null)
    ac_a_subscribe.onclick = (e) => {
        e.preventDefault()
        if (uid) {
            focused = !focused
            focus_txt.innerHTML = parseInt(focus_txt.innerHTML) + (focused ? (1) : (-1))
            loadFocus()
            reqFocus()
        } else {
            loginClick.click()
        }
    }

// expand collpased content
document.getElementById("ac_click_more").onclick = function (e) {
    this.style.display = "none"
    document.querySelector('.ac_div_click_more').style.display = "none"
    document.querySelector(".ac_art_html").style.maxHeight = "none"
    document.querySelector(".ac_d_support").style.display = "none"
    document.querySelector(".ac_d_artom").style.display = "none"
}

// show remark writing dialog
document.querySelector(".ac_d_rewr span:last-child").onclick = function (e) {
    e.preventDefault()
    if ("" == uid)
        new bootstrap.Modal(document.getElementById("loginModal")).show()
    else
        new bootstrap.Modal(document.getElementById("remarkWriting")).show()
}

// Remark region
var curRpLayout = null;
let comments = document.querySelectorAll(".ac_d_ritm_b>span:nth-of-type(1)");
let wrrms = document.querySelectorAll(".ac_d_wrrp")
for (let i = 0; i < comments.length; i++) {
    let report = comments[i].nextElementSibling;

    // hover on remark and report
    let omor = function (e) {
        this.style.color = "#545c63"
        report.style.display = "inline"
    }

    let omot = function (e) {
        this.style.color = "#9199a1"

        if (!this.contains(e.relatedTarget) && !report.contains(e.relatedTarget)) {
            report.style.display = "none"
        }
    }

    comments[i].onmouseover = omor
    comments[i].onmouseout = omot
    report.onmouseover = omor
    report.onmouseout = omot

    // click to show sub-remakr writing layout
    comments[i].onclick = function (e) {
        if (uid == ""){
            loginClick.click()
            return
        }

        const cthis = this;
        const rbid = this.dataset.rbid

        wrrms.forEach(each => {
            if (each.dataset.rbid === rbid) {

                if (curRpLayout != null && curRpLayout != each) {
                    curRpLayout.classList.add("g")
                }

                each.classList.remove("g")
                curRpLayout = each
                const l2reply = each.querySelector("textarea")
                l2reply.value = ""
                if (comments[i].dataset.rtuname != undefined && comments[i].dataset.rtuname != null) {
                    l2reply.placeholder = "Reply to " + comments[i].dataset.rtuname + ":"
                } else {
                    l2reply.placeholder = "Write your comment ..."
                }
                l2reply.dataset.rbid = cthis.dataset.rbid
                l2reply.dataset.rtuid = cthis.dataset.rtuid

                each.querySelector('.fr div:first-child').onclick = function (e) {
                    each.classList.add("g")
                }

                each.querySelector('.fr div:last-child').onclick = function (e) {
                    submitComment(l2reply.value,l2reply.dataset.rbid,l2reply.dataset.rtuid)
                }
            }
        });
    }
}

function reqFocus() {
    const params = new URLSearchParams({ tuid: auid, status: focused ? "+" : "-" });

    fetch(`/focusAuthor?${params.toString()}`)
        .then(response => response.json())
        .catch(error => console.error('Error:', error));
}

function reqLike(sta) {
    const params = new URLSearchParams({ aid: aid, status: sta ? "+" : "-" });

    fetch(`/like?${params.toString()}`)
        .then(response => response.json())
        .catch(error => console.error('Error:', error));
}

// left fixed layout - like hover
let is = document.querySelector(".ac_div_options_l i")
const like_txt = document.querySelector(".ac_div_options_l span:first-of-type")
const laf_txt = document.querySelector(".ac_d_atrnums table tr:last-child td:nth-child(3)");

// let liked = false
is.innerHTML = liked ? "&#xe83b;" : "&#xe83c;"
is.onmouseover = function (e) {
    this.innerHTML = liked ? "&#xe83c;" : "&#xe83b;"
}
is.onmouseout = function (e) {
    this.innerHTML = liked ? "&#xe83b;" : "&#xe83c;"
}
is.onclick = function (e) {
    if (uid) {
        liked = !liked
        is.innerHTML = liked ? "&#xe83b;" : "&#xe83c;"
        like_txt.innerHTML = parseInt(like_txt.innerHTML) + (liked ? (1) : (-1))
        laf_txt.innerHTML = parseInt(laf_txt.innerHTML) + (liked ? (1) : (-1))
        reqLike(liked)
    } else {
        loginClick.click()
    }
}

// scroll certain distance to hide left fixed layout
window.addEventListener("scroll", function () {
    let scrollTop = window.scrollY || document.documentElement.scrollTop;
    document.querySelector(".ac_div_options_l").style.display = scrollTop > 1000 ? "none" : "block"
});

// config of u-editor
const uePlaceHolder = "Whatever that is in your mind ..."
const ue = UE.getEditor('editor', {
    shortcutMenu: false,
    elementPathEnabled: false,
    wordCount: false,
    autoHeightEnabled: false,
    initialContent: uePlaceHolder,
    toolbars: [["insertcode", "bold", "italic", "redo", "undo", "emotion"]]
});

ue.addListener("focus", function () {
    if (ue.getContentTxt().trim() === uePlaceHolder) {
        ue.setContent("");
    }
});
ue.addListener("blur", function () {
    if (ue.getContentTxt().trim() === "") {
        ue.setContent(uePlaceHolder);
    }
});

if (document.getElementById('ac_art_safecontent').offsetHeight < 480) {
    document.querySelector('.ac_div_click_more').style.display = "none"
    document.querySelector('#ac_click_more').style.display = "none"
    document.querySelector(".ac_d_support").style.display = "none"
    document.querySelector(".ac_d_artom").style.display = "none"
}

function submitComment(content,rbid,rtuid) {
    fetch('/submitComment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "aid": aid, "content": content,"rbid":rbid,"rtuid":rtuid })
    })
        .then(response => response.json())
        .then(data => {
            showPrompt(data)
            if (data.status == "200") {
                window.setTimeout(function () {
                    location.reload()
                },1000)
            }
        })
        .catch(error => {
            console.error("error:", error);
            showPrompt({ "status": "err", "desc": "Publish failed:" + error })
        });
}

document.getElementById("ac_reply_publish").onclick = (e) => {
    if (ue.getContent().trim() === '' || ue.getContent().trim() === uePlaceHolder) {
        showPrompt({ "status": "err", "desc": "Content can't be empty." })
        return
    } else {
        submitComment(ue.getContent().trim(),null,null)
    }
}