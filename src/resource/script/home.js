//let a_left_all = document.querySelectorAll(".h_home_cl .h_a_left")
//for (i = 0; i < a_left_all.length; i++) {
//    a_left_all[i].onclick = function (e) {
//        e.preventDefault();
//        document.querySelector("li.h_li_left.h_li_left_selected").className = "h_li_left"
//        this.parentNode.classList.toggle("h_li_left_selected")
//    }
//}

const opt = document.querySelector(".h_home_cl").dataset.opt

const loading = document.getElementById("h_mainlist_loading")
const no_more = document.getElementById("h_mainlist_end")
const container = document.querySelector(".h_div_list_container");

const artItems = document.querySelectorAll(".h_div_list_item");
artItems.forEach(each => {
    each.onclick = function (e) {
        location.href = this.getAttribute("href")
    }
});


document.addEventListener("DOMContentLoaded", function () {
    let page = 1;
    let isloading = false;

    if(!hasMore){
        no_more.classList.remove("g");
    }

    window.addEventListener("scroll", function () {
        if (!hasMore || isloading) return;

        let scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
        let windowHeight = window.innerHeight;
        let documentHeight = document.documentElement.scrollHeight;

        if (scrollTop + windowHeight >= documentHeight - 300) {
            loadMoreArticles();
        }
    });

    function loadMoreArticles() {
        if (!hasMore) return;
        isloading = true;
        loading.classList.remove("g");

        var thwart = window.setTimeout(()=>{
            fetch(`/load_more_articles?page=${page}&opt=${opt}`)
            .then(response => response.json())
            .then(data => {
                loading.classList.add("g");

                if (data.articles.length === 0) {
                    hasMore = false;
                    no_more.classList.remove("g");
                    return;
                }

                page++; 
                renderArticles(data.articles);
                isloading = false;
            })
            .catch(error => {
                console.error("Error loading articles:", error);
                isloading = false;
                loading.classList.add("g");
            });
        }, 1000)

        
    }

    function renderArticles(articles) {

        articles.forEach(item => {
            let articleDiv = document.createElement("div");
            articleDiv.className = "h_div_list_item";
            articleDiv.href = "/content/{{item.aid}}"
            let tagHtml = '';
            if (opt === "reco") {
                tagHtml = `<a href="/${item.opt}" class="h_a_main_tag">${item.cat_name}</a>`;
            }
            articleDiv.innerHTML = `
                <img src="${item.cover.replace('"', '')}">
                <div>
                    <a class="h_a_main_title">${item.title}</a>
                    <span class="h_span_star" title="Not implemented">Star</span>
                    <div class="h_div_item_bot">
                        ${tagHtml}
                        <span class="iconfont h_txt_main_list_bot">&#xe602;</span>
                        <span class="h_txt_main_list_bot">${item.num_view}</span>
                        <a href="" class="h_txt_main_list_bot">${item.nickname}</a>
                        <a href="" class="h_txt_main_list_bot">${item.tags.replace(",", "﹒")}</a>
                        <div class="h_txt_main_list_bot fr">${item.date}</div>
                    </div>
                </div>
            `;
            // container.appendChild(articleDiv);
            container.insertBefore(articleDiv, loading)
        });
    }
});