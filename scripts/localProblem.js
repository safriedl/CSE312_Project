const d = new Date();
let earliestCorrectTime = 0;
function userSubmit(id){
    const value = document.getElementsByName("user"+id)[0].value
    let response = document.getElementById("response");
    if (value === answer){
        if (earliestCorrectTime != 0){
            earliestCorrectTime = d.getTime()
            response.innerHTML = "Player " + id + "got it first!"
        }
        else{
            response.innerHTML = "Sorry, the other player got it right first!"
        }
    }
    else{
        response.innerHTML = "Player " + id +"'s answer was wrong!" + "Their answer was " + value
    }
}