let eastclockElement = document.getElementById('east_clock');
let chinaClockElement = document.getElementById("china_clock")
let westClockElement = document.getElementById("west_clock")

function clock() {
    eastclockElement.textContent = new Date().toLocaleString('en-US', {timeZone: 'America/New_York'});
    chinaClockElement.textContent = new Date().toLocaleString('en-US', {timeZone: 'Asia/Shanghai'});
    westClockElement.textContent = new Date().toLocaleString('en-US', {timeZone: 'America/Los_Angeles'});
}


setInterval(clock, 1000);