
const getDateStr = (ts) => {
    var date = new Date(ts * 1000);
    var year = date.getFullYear()
    var month = date.getMonth()
    var day = date.getDate()
    var hours = date.getHours();
    var minutes = "0" + date.getMinutes();
    var seconds = "0" + date.getSeconds();
    var formattedTime = year + "-" + month + "-" + day + " " + hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
    return formattedTime
}

export default getDateStr;