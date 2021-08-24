let eastclockElement = document.getElementById('east_clock');
let chinaClockElement = document.getElementById("china_clock")
let westClockElement = document.getElementById("west_clock")

function clock() {
    eastclockElement.textContent = new Date().toLocaleString('en-US', {timeZone: 'America/New_York'});
    chinaClockElement.textContent = new Date().toLocaleString('en-US', {timeZone: 'Asia/Shanghai'});
    westClockElement.textContent = new Date().toLocaleString('en-US', {timeZone: 'America/Los_Angeles'});
}


setInterval(clock, 1000);


$(function () {

    $('#advanced-search').on('click', function () {
        let btn = $(this);
        $.ajax({
            type: "GET",
            url: btn.attr('data-url'),
            success: function (data) {
                $('#pgModal').modal("show");
                $('#pgModal .modal-content').html(data);
            },
            error: function (xhr) {
                if (xhr.status === 403) {
                    console.log('invalid');
                    alert(xhr.responseJSON.msg);
                }
            },
        });
    })

})