// Class Page - One singe instance of it represents the active part of the page.
function Page() {
    this.updateCounter = 0;
    this.websocket = null;
}
Page.prototype = {

    constructor: Page,

    init:function() {
        websocket_uri = "ws://" + window.location.hostname + ":" + window.location.port + "/websocket"
        this.websocket = new WebSocket(websocket_uri);
        this.websocket.onmessage = function(event) {
            context = this
            data = JSON.parse(event.data)
            this.updateCounter = data['update_counter'];
            scoreboardDictionary = data['scoreboard'];
            for (entryKey in scoreboardDictionary)
            {
                entryValue = scoreboardDictionary[entryKey];
                entryId = 'span#' + entryKey;
                formattedValue = entryValue
                switch (entryKey)
                {
                    case "game_phase":
                        formattedValue = entryValue.substring(0,1)
                    break;
                    case "game_ball_on":
                    case "game_clock_seconds":
                    case "game_clock_minutes":
                    case "game_yards_to_go":
                    case "home_score":
                    case "guest_score":
                        if (entryValue < 10)
                        {
                            formattedValue = "0" + entryValue
                        }
                        else {
                            formattedValue = "" + entryValue
                        }
                    break;
                    case "game_offencive_team":
                        if (entryValue != "Home") {
                            $("img#game_offencive_team_home").addClass("HiddenObject");
                        }
                        else {
                            $("img#game_offencive_team_home").removeClass("HiddenObject");
                        }
                        if (entryValue != "Guest") {
                            $("img#game_offencive_team_guest").addClass("HiddenObject");
                        }
                        else {
                            $("img#game_offencive_team_guest").removeClass("HiddenObject");
                        }
                }
                $(entryId).html(formattedValue);
            }
        }
    }
}


$(document).ready(function()
{
    page = new Page();
    page.init();
});
