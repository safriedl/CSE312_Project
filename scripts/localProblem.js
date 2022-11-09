const d = new Date();
let earliestCorrectTime = 0;
let firstUser = 0;
function userSubmit(id){
    const value = Number(document.getElementsByName("user"+id)[0].value)
    let response = document.getElementById("response");
    if (value === answer){
        if (earliestCorrectTime === 0){
            earliestCorrectTime = d.getTime()
            firstUser = id
            response.innerHTML = "Player " + id + " got it first!"
        }
        else{
            response.innerHTML = "Sorry, Player" + firstUser + " got it right first!"
        }
    }
    else{
        response.innerHTML = "Player " + id +"'s answer was wrong! Their answer was " + value + "."
    }
}