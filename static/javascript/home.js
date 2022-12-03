copyRightDate(2022)

function copyRightDate(x) {
    var d = new Date;
    var year = d.getFullYear();
    var footerDate = document.getElementById("footerdate");
    if (year == x) {
        footerDate.innerHTML = year;
    } else {
        footerDate.innerHTML = x + "-" +
            year;
    }
}


const backToTop = () => {
    let y_axis_offset = window.pageYOffset ||
        document.documentElement.scrollTop ||
        document.body.scrollTop;
    x = "300";
    let backToTopButton = document.getElementById("backToTop");
    if (y_axis_offset >= x) {
        backToTopButton.style.display = "block";
    } else {
        backToTopButton.style.display = "none";
    }
}

let state = getState()
if (state.user == "") {
    setState(storeReducer(addUserId()))
    state = getState()
}

const createDataId = () => {
    const date = Date.now().toString().slice(5)
    const random = Math.floor(Math.random() * 100)
    const dataId = `data${random}${date}`
    return dataId
}

try {
    let dataset = document.querySelector("#id_dataset")
    let dataset_id = document.querySelector("#id_dataset_id")
    let user_id = document.querySelector("#id_user_id")
    let user_id2 = document.querySelector("#id_user_id2")

    dataset.accept = ".csv,.xlsx"
    dataset_id.value = createDataId()
    dataset_id.style.display = "none"

    user_id.value = state.user
    user_id.style.display = "none"

    user_id2.value = state.user

} catch (error) {
    console.log(error)
}