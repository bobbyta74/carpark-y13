parkform.addEventListener("click", async function(event) {
    //Avoid refreshing page
    event.preventDefault();
    //Take input, insert into app.py and wait for it to return
    let reg = reginp.value.trim();
    let response = await window.fetch(`/park?reg=${reg}`);
    //app.py returns object (var response) containing direction of movement (type entry/exit), registration and time/duration of stay
    response = await response.json();
    if (response.type == "entry") {
        message.textContent = `Registration ${reg} entered the car park at ${response.time}`;
    } else if (response.type == "exit") {
        message.textContent = `Registration ${reg} left the car park after ${response.duration} seconds`;
    } else {
        throw new Error();
    }
})