//let a_left_all = document.querySelectorAll(".h_home_cl .h_a_left")
//for (i = 0; i < a_left_all.length; i++) {
//    a_left_all[i].onclick = function (e) {
//        e.preventDefault();
//        document.querySelector("li.h_li_left.h_li_left_selected").className = "h_li_left"
//        this.parentNode.classList.toggle("h_li_left_selected")
//    }
//}

let artItem = document.querySelectorAll(".h_div_list_item");
artItem.forEach(each => {
    each.onclick = function(e){
        location.href = this.getAttribute("href")
    }
});
