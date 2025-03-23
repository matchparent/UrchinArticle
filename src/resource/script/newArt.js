const tags = document.querySelectorAll("#new_pub_d_tags .new_pub_tag")
const selectedtags_d = document.querySelector("#new_pub_d_selectedtags")
const selecttagCount = document.querySelector("#new_d_pub_tag>span")
const tagSearch = document.querySelector("#new_pub_d_intag>input")
const pubTitle = document.querySelector(".new_div_editor input")
const new_pub_img_input = document.getElementById("new_pub_img_input")
const new_d_cam = document.getElementById("new_d_cam")
const new_d_drafts = document.getElementById("new_d_drafts")
const modal_pub = new bootstrap.Modal(document.getElementById('publish'))

function decodeHTML(html) {
    const doc = new DOMParser().parseFromString(html, "text/html");
    return doc.documentElement.textContent;
}

// config of u-editor
const uePlaceHolder = "Whatever that is in your mind ..."
const ue = UE.getEditor('editor', {
    shortcutMenu: false,
    elementPathEnabled: false,
    wordCount: false,
    autoHeightEnabled: false,
    initialContent: drtent ? drtent : uePlaceHolder,
    // initialContent: uePlaceHolder,

    allowImageUpload: true,
    imageAllowFiles: ['.png', '.jpg', '.jpeg'],
    serverUrl: "/ueditor/controller",
    imageConfig: {
        // 禁止本地上传
        disableUpload: false,
        // 禁止在线管理
        disableOnline: false,
        // 自定义选择按钮
        selectCallback: null,
    },
    toolbars: [["bold", "italic", "simpleupload", "link", "redo", "undo", "emotion"]]
});

// mimic of placeholder
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

initDropdown("#new_pub_category")
initDropdown("#new_pub_type")

function setPublishImg(img) {
    new_d_cam.innerHTML = ""
    new_d_cam.style.backgroundColor = "transparent"
    new_d_cam.style.backgroundImage = "url(" + img + ")"
}

// click toggle u-editor/markdown
let new_header_mid_txt = document.querySelectorAll(".new_header_mid_txt")
for (i = 0; i < new_header_mid_txt.length; i++) {
    new_header_mid_txt[i].onclick = function (e) {
        document.querySelector(".new_header_mid_txt.new_header_mid_txt_selected").className = "new_header_mid_txt"
        this.classList.toggle("new_header_mid_txt_selected")
    }
}

document.querySelector(".new_header_publish").onclick = () => {
    if (pubTitle.value.trim() === '') {
        showPrompt({ "status": "err", "desc": "Title can't be empty." })
        return
    }

    if (ue.getContent().trim() === '' || ue.getContent().trim() === uePlaceHolder) {
        showPrompt({ "status": "err", "desc": "Content can't be empty." })
        return
    } else {
        modal_pub.show()
    }
}


const selectedTagClick = function (e) {
    if (selectedtags_d.childElementCount == 3) {
        tagSearch.classList.remove("g")
    }
    const target = document.querySelector('#new_pub_d_tags .new_pub_tag[data-tags-id="' + (this.dataset.tagsId) + '"]')
    target.classList.remove("g")
    this.parentNode.removeChild(this)
    selecttagCount.innerHTML = selectedtags_d.childElementCount + "/3"

}

const tagClick = function (e) {
    if (selectedtags_d.childElementCount < 3) {
        if (selectedtags_d.childElementCount == 2) {
            tagSearch.classList.add("g")
        }
        tagSearch.value = ""
        tagSearch.dispatchEvent(new Event('input'));
        const clonedTag = this.cloneNode(true)
        clonedTag.onclick = selectedTagClick
        selectedtags_d.appendChild(clonedTag)
        selecttagCount.innerHTML = selectedtags_d.childElementCount + "/3"
        this.classList.add("g")
    }
}
tags.forEach(tag => {
    tag.onclick = tagClick
})

document.getElementById("new_pl_upload").onclick = (e) => {
    new_pub_img_input.click()
}

new_pub_img_input.addEventListener("change", async function (event) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("upfile", file);
    try {
        const response = await fetch("/ueditor/controller?action=uploadimage", {
            method: "POST",
            body: formData,
        });
        const result = await response.json();
        if (result.state === "SUCCESS") {
            setPublishImg(result.url)
        } else {
            showPrompt({ "status": "err", "desc": "Upload Failed:" + result.message })
        }
    } catch (error) {
        showPrompt({ "status": "err", "desc": "Upload Failed:" + error })
    }
});

tagSearch.addEventListener("input", function () {
    let inputValue = this.value.toLowerCase();
    let tags = document.querySelectorAll("#new_pub_d_tags .new_pub_tag");

    tags.forEach(tag => {
        if (tag.innerHTML.toLowerCase().includes(inputValue)) {
            tag.classList.remove("g2");
        } else {
            tag.classList.add("g2");
        }
    });
});

document.querySelector("#new_pub_publish").onclick = (e) => {

    if (!new_d_cam.style.backgroundImage) {
        showPrompt({ "status": "err", "desc": "Please upload or select one cover image." })
        return
    }
    const cover = new_d_cam.style.backgroundImage.replace("url(", "").replace(")", "")

    const acid = document.querySelector("#new_pub_category span").dataset.ddId
    if (acid == undefined) {
        showPrompt({ "status": "err", "desc": "Please select category of your article." })
        return
    }

    const ayid = document.querySelector("#new_pub_type span").dataset.ddId
    if (ayid == undefined) {
        showPrompt({ "status": "err", "desc": "Please select type of your article." })
        return
    }

    if (selectedtags_d.childElementCount == 0) {
        showPrompt({ "status": "err", "desc": "Please select at least 1 tag." })
        return
    }

    let atids = ""
    const tags = Array.from(selectedtags_d.children)
    tags.forEach(element => {
        atids += (element.dataset.tagsId + ",")
    });
    atids = atids.slice(0, -1)

    const title = pubTitle.value.trim()
    const content = ue.getContent().trim()

    showPrompt({ "status": "load", "desc": "Loading..." })

    fetch('/publish', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: title, content: content, cover: cover, acid: acid, ayid: ayid, atids: atids })
    })
        .then(response => response.json())
        .then(data => {
            showPrompt(data)
            window.setTimeout(function () {
                if(draid){
                    delDraft(draid)
                }
                location.href = "/"
            }, 1000)
        })
        .catch(error => {
            console.error("error:", error);
            showPrompt({ "status": "err", "desc": "Publish failed:" + error })
        });

}

function hideOnClickOutside(event) {
    if (!new_d_drafts.contains(event.target)) {
        new_d_drafts.classList.add("g");
        document.removeEventListener("click", hideOnClickOutside);
    }
}

function showDiv() {
    new_d_drafts.classList.remove("g")
    setTimeout(() => {
        document.addEventListener("click", hideOnClickOutside);
    }, 0); // postpone binding, avoid immidiate trigger
}

document.getElementById("new_pub_cancel").onclick = (e) => {
    const title = pubTitle.value.trim()
    const content = ue.getContent().trim()

    showPrompt({ "status": "load", "desc": "Loading..." })

    fetch('/draft', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: title, content: content, aid: draid })
    })
        .then(response => response.json())
        .then(data => {
            showPrompt(data)
            window.setTimeout(function () {
                location.reload()
            }, 1000)
        })
        .catch(error => {
            console.error("error:", error);
            showPrompt({ "status": "err", "desc": "Draft save failed:" + error })
        });
    modal_pub.hide()
}

function delDraft(aid){
    fetch('/delDraft', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ aid: aid })
    })
        .then(response => response.json())
        .then(data => {
            showPrompt(data)
            window.setTimeout(function () {
                location.reload()
            }, 1000)
        })
        .catch(error => {
            console.error("error:", error);
            showPrompt({ "status": "err", "desc": "Draft delete failed:" + error })
        });
}