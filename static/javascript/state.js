//Action Types
const rootUrl = "https://smbclassic.com.ng";
const LOADED = "LOADED";
const LOADING = "LOADING";
const ADD_ERROR = "ADD_ERROR";
const ADD_USER_ID = "ADD_USER_ID";


const addUserId = () => {
    const date = Date.now().toString().slice(5)
    const random = Math.floor(Math.random() * 100)
    const userId = `AS${random}${date}`
    return {
        type: ADD_USER_ID,
        data: userId
    }
}

const load = (type) => {
    return {
        type: type
    }
}

const getState = () => {
    const localdata = localStorage.getItem("datastate");
    let finaldata = ""
    if (localdata) {
        const jsonify = JSON.parse(localdata)
        finaldata = {
            user: "",
            loading: false,
            // success: false,
            ...jsonify,
            // message: "",
            // status: "",
            // messages: "",
            // check: "",
        }
    } else {
        finaldata = {
            user: "",
            loading: false,
            // success: false,
            // message: "",
            // status: "",
            // messages: "",
            // check: "",
        }
    }
    return finaldata
}

//Reducer
const storeReducer = (action) => {
    let state = getState()
    switch (action.type) {


        case ADD_USER_ID:
            return {
                ...state,
                user: action.data,
                loading: false,
            }

        case LOADING:
            return {
                ...state,
                loading: true
            }
        case LOADED:
            return {
                ...state,
                loading: false,
            }

        default:
            return {
                ...state
            }
    }
}

const setState = (datastate) => {
    localStorage.setItem("datastate", JSON.stringify(datastate))
}

// const ProcessOrder = async(data, token, url = '/sales/process') => {
//     setState(storeReducer(load(LOADING)))
//     let response = await fetch(url, {
//         method: 'POST', // or 'PUT'
//         credentials: 'same-origin',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': token
//         },
//         body: JSON.stringify(data),
//     })

//     if (!response.ok) {
//         throw new Error(response.statusText)
//     }
//     return await response.json()
// }


// const GetCustomer = async(data, token) => {
//     setState(storeReducer(load(LOADING)))
//     let response = await fetch(`${rootUrl}/user/customer/0/get`, {
//         method: 'POST', // or 'PUT'
//         credentials: 'same-origin',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': token
//         },
//         body: JSON.stringify(data),
//     })

//     if (!response.ok) {
//         throw new Error(response.statusText)
//     }
//     return await response.json()
// }