// Class Page - One singe instance of it represents the active part of the page.
function Page() {
    this.updateCounter = 0;
    this.websocket = null;
}
Page.prototype = {

    constructor: Page,

    _formatNumber:function(value) {
        if (value < 10) {
            formattedValue = "0" + value;
        }
        else {
            formattedValue = "" + value;
        }
        return formattedValue;
    },

    init:function() {
        websocket_uri = "ws://" + window.location.hostname + ":" + window.location.port + "/websocket"
        this.websocket = new WebSocket(websocket_uri);
        context = this;
        this.websocket.onmessage = function(event) {
            console.log(event.data);
            data = JSON.parse(event.data);
            context.receiveData(data);
        }
    },

    receiveScoreboardUpdate:function(payload) {
        console.log(payload);
        updateCount = payload["update_counter"];
        scoreboardData = payload["scoreboard"];
        for (entryKey in scoreboardData)
        {
            entryValue = scoreboardData[entryKey];
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
                    formattedValue = this._formatNumber(entryValue)
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
    },

    receiveClockUpdate:function(payload) {
        seconds = payload["seconds"];
        minutes = payload["minutes"];
        $("#game_clock_minutes").html(this._formatNumber(minutes));
        $("#game_clock_seconds").html(this._formatNumber(seconds));
    },

    receiveTimeUpdate:function(payload) {
        seconds = payload["seconds"];
        minutes = payload["minutes"];
        $("#game_clock_minutes").html(this._formatNumber(minutes));
        $("#game_clock_seconds").html(this._formatNumber(seconds));
    },

    receiveData:function(data) {
        switch (data["event"]) {
            case "clock_update":
                this.receiveClockUpdate(data["data"]);
            break;
            case "time_update":
                this.receiveTimeUpdate(data["data"]);
            break;
            case "scoreboard_update":
                this.receiveScoreboardUpdate(data["data"]);
            break;
            default:
                console.log("Unknown event", data);
            break;
        }
    }
}


$(document).ready(function()
{
    page = new Page();
    page.init();
});
