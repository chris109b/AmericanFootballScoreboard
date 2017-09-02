// Class Page - One singe instance of it represents the active part of the page.


function Command(name, parameters) {
    this.command = name;
    this.parameters = parameters;
}

Command.prototype = {

    constructor: Command,

    jsonString:function() {
        return JSON.stringify(this);
    }
};


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
        };
        display_id = this.getUrlParameter("id");
        this.websocket.onopen = function () {
            context.sendRegisterDisplay(display_id);
        };
        this.websocket.onerror = function (error) {
            console.log('WebSocket Error ' + error);
        };
    },

    getUrlParameter:function(search_parameter_name) {
        url_parameter_part = decodeURIComponent(window.location.search.substring(1));
        url_variables = url_parameter_part.split('&');
        for (i=0; i < url_variables.length; i++) {
            key_value_pair = url_variables[i];
            parameter_name = key_value_pair.split('=');
            if (parameter_name[0] === search_parameter_name) {
                return parameter_name[1];
            }
        }
        return undefined;
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

    receiveShowIdentification:function(payload) {
        display_id = payload["id_string"]
        $(".DisplayIdentity").html(display_id);
        $(".DisplayIdentity").removeClass("HiddenObject");
        setTimeout(function() {
            $(".DisplayIdentity").addClass("HiddenObject");
        }, 5000);
    },

    receiveShowIdentification:function(payload) {
        display_id = payload["id_string"]
        $(".DisplayIdentity").html(display_id);
        $(".DisplayIdentity").removeClass("HiddenObject");
        setTimeout(function() {
            $(".DisplayIdentity").addClass("HiddenObject");
        }, 5000);
    },

    receiveChangeAppearance:function(payload) {
        display_id = payload["display_id"]
        appearance_id = payload["appearance_id"]
        page_url = "/" + appearance_id + ".html?id=" + display_id;
        setTimeout(function() {
            document.location.href = page_url;
        }, 100);
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
            case "show_identification":
                this.receiveShowIdentification(data["data"]);
            break;
            case "change_appearance":
                this.receiveChangeAppearance(data["data"]);
            break;
            default:
                console.log("Unknown event", data);
            break;
        }
    },

    sendRegisterDisplay:function(display_id) {
        command = new Command('register_display', { "display_id": display_id });
        this.websocket.send(command.jsonString());
    }
}


$(document).ready(function()
{
    page = new Page();
    page.init();
});
