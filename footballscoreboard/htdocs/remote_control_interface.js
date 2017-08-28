

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

    init:function() {
        websocket_uri = "ws://" + window.location.hostname + ":" + window.location.port + "/websocket"
        this.websocket = new WebSocket(websocket_uri);
        context = this;
        this.websocket.onmessage = function(event) {
            console.log(event.data)
            data = JSON.parse(event.data);
            context.receiveData(data);
        };
        this.websocket.onopen = function () {
            context.sendGetClock();
        };
        this.websocket.onerror = function (error) {
            console.log('WebSocket Error ' + error);
        };

        $("#ScoreboardFormAreaBackButton").on( "click", function() {
            window.location.href = "index.html";
        });
        $("#ScoreboardFormAreaSubmitButton").on( "click", function() {
            context.submitScoreboardForm();
        });
        $("#ShowClockButton").on( "click", function() {
            context.showClockOperationArea();
        });

        $("#ClockOperationAreaBackButton").on( "click", function() {
            context.hideClockOperationArea();
        });
        $("#ClockOperationAreaSettingsButton").on( "click", function() {
            context.showClockSettingsArea();
        });
        $("#StartButton").on( "click", function() {
            context.sendStartClock();
        });
        $("#StopButton").on( "click", function() {
            context.sendStopClock();
        });

        $("#ClockSettingAreaBackButton").on( "click", function() {
            context.hideClockSettingsArea();
        });
        $("#ClockSettingAreaSubmitButton").on( "click", function() {
            context.submitClockSettingsForm();
            context.hideClockSettingsArea();
        });

    },

    receiveScoreboardUpdate:function(payload) {
        console.log(payload);
        updateCount = payload["update_counter"];
        scoreboardData = payload["scoreboard"];
        for (name in scoreboardData) {
            value = scoreboardData[name];
            console.log(name, value);
            switch (name) {
                case "game_phase":
                    $("#game_phase option").filter(function() {
                        return $(this).text() == value;
                    }).prop('selected', true);
                break;
                case "game_offencive_team":
                    if (value == "Home") {
                        $( "#game_offencive_team_home" ).prop( "checked", true );
                    }
                    else {
                        $( "#game_offencive_team_guest" ).prop( "checked", true );
                    }
                break;
                default:
                    $("#" + name).val(value);
                break;
            }
        }
    },

    receiveClockUpdate:function(payload) {
        seconds = payload["seconds"]
        minutes = payload["minutes"]
        mode = payload["mode"]
        is_ticking = payload["is_ticking"]

        $("#minutes").html(minutes);
        $("#seconds").html(seconds);
        $("#clock_minutes").val(minutes);
        $("#clock_seconds").val(seconds);

        $("#clock_mode option").filter(function() {
            return $(this).text() == mode;
        }).prop('selected', true);

        if (is_ticking == true) {
            $("#ClockOperationTime").removeClass("Stopped")
            $("#ClockOperationTime").addClass("Ticking")
        }
        else {
            $("#ClockOperationTime").removeClass("Ticking")
            $("#ClockOperationTime").addClass("Stopped")
        }
    },

    receiveTimeUpdate:function(payload) {
        seconds = payload["seconds"]
        minutes = payload["minutes"]
        $("#minutes").html(minutes);
        $("#seconds").html(seconds);
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
    },

    showClockOperationArea:function() {
        $("#ClockOperationArea").removeClass("HiddenScreen")
    },

    hideClockOperationArea:function() {
        $("#ClockOperationArea").addClass("HiddenScreen")
    },

    showClockSettingsArea:function() {
        $("#clock_minutes").val($("#minutes").html());
        $("#clock_seconds").val($("#minutes").html());
        $("#ClockSettingsArea").removeClass("HiddenScreen");
    },

    hideClockSettingsArea:function() {
        $("#ClockSettingsArea").addClass("HiddenScreen");
    },

    submitScoreboardForm:function() {
        parameters = this._readParametersOfForm("form#ScoreboardForm");
        this.sendUpdateScoreboard(parameters);
    },

    submitClockSettingsForm:function() {
        parameters = this._readParametersOfForm("form#ClockSettingsForm");
        this.sendUpdateClockSettings(parameters);
    },

    sendGetScoreboard:function() {
        command = new Command('get_scoreboard', {});
        this.websocket.send(command.jsonString());
    },

    sendUpdateScoreboard:function(parameters) {
        command = new Command('update_scoreboard', parameters);
        this.websocket.send(command.jsonString());
    },

    sendGetClock:function() {
        command = new Command('get_clock', {});
        this.websocket.send(command.jsonString());
    },

    sendUpdateClockSettings:function(parameters) {
        command = new Command('update_clock_settings', parameters);
        this.websocket.send(command.jsonString());
    },

    sendStartClock:function() {
        command = new Command('start_clock', {});
        this.websocket.send(command.jsonString());
    },

    sendStopClock:function() {
        command = new Command('stop_clock', {});
        this.websocket.send(command.jsonString());
    },

    _readParametersOfForm:function(formId) {
        parameters = {}
        form_data = $(formId).serializeArray()
        for (index in form_data) {
            object = form_data[index];
            parameters[object.name] = object.value;
        }
        return parameters
    },
};


$(document).ready(function()
{
    page = new Page();
    page.init();
});
