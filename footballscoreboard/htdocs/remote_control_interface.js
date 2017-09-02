

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
        $("#ShowDisplaySelectionButton").on( "click", function() {
            context.openDisplaySelectionArea();
        });

        $("#DisplaySelectionAreaBackButton").on( "click", function() {
            context.hideDisplaySelectionArea();
        });
        $("#AppearanceSelectionAreaBackButton").on( "click", function() {
            context.hideAppearanceSelectionArea();
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
        seconds = payload["seconds"];
        minutes = payload["minutes"];
        mode = payload["mode"];
        is_ticking = payload["is_ticking"];

        $("#minutes").html(this._formatNumber(minutes));
        $("#seconds").html(this._formatNumber(seconds));
        $("#clock_minutes").val(this._formatNumber(minutes));
        $("#clock_seconds").val(this._formatNumber(seconds));

        $("#clock_mode option").filter(function() {
            return $(this).text() == mode;
        }).prop('selected', true);

        if (is_ticking == true) {
            $("#ClockOperationTime").removeClass("Stopped");
            $("#ClockOperationTime").addClass("Ticking");
        }
        else {
            $("#ClockOperationTime").removeClass("Ticking");
            $("#ClockOperationTime").addClass("Stopped");
        }
    },

    receiveTimeUpdate:function(payload) {
        seconds = payload["seconds"];
        minutes = payload["minutes"];
        $("#minutes").html(this._formatNumber(minutes));
        $("#seconds").html(this._formatNumber(seconds));
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
        $("#ClockOperationArea").removeClass("HiddenScreen");
    },

    hideClockOperationArea:function() {
        $("#ClockOperationArea").addClass("HiddenScreen");
    },

    showClockSettingsArea:function() {
        $("#clock_minutes").val($("#minutes").html());
        $("#clock_seconds").val($("#seconds").html());
        $("#ClockSettingsArea").removeClass("HiddenScreen");
    },

    hideClockSettingsArea:function() {
        $("#ClockSettingsArea").addClass("HiddenScreen");
    },

    openDisplaySelectionArea:function() {
        context = this;
        $.get("/display-list.json", function(data, status) {
            if (status == 'success') {
                $("#DisplayList").html("");
                for (displayId in data["display_list"]) {
                    html = '<div class="DisplayTile">' + displayId +'</div>\n';
                    $("#DisplayList").append(html);
                }
                $("#AppearanceList").html("");
                for (appearanceKey in data["appearance_dict"]) {
                    appearanceName = data["appearance_dict"][appearanceKey];
                    html = '<div class="AppearanceTile" name="'+ appearanceKey +
                           '" style="background-image: url(/img/' + appearanceKey + '.png);">' +
                           '<div class="AppearanceTileTitle">' +
                           appearanceName +
                           '</div></div>\n';
                    $("#AppearanceList").append(html);
                }
                setTimeout(function() {
                    $(".DisplayTile").on( "click", function() {
                        context.openAppearanceSelectionAreaFor(this);
                    });
                    $(".AppearanceTile").on( "click", function() {
                        context.changeDisplayAppearance(this);
                    });
                }, 100);
                context.showDisplaySelectionArea();
                context.sendIdentifyAllDisplays();
            }
            else {
                console.log("Error (Status:"  + status + ")\n Data: " + data + "\n");
            }
        });
    },

    showDisplaySelectionArea:function() {
        $("#DisplaySelectionArea").removeClass("HiddenScreen");
    },

    hideDisplaySelectionArea:function() {
        $("#DisplaySelectionArea").addClass("HiddenScreen");
    },

    openAppearanceSelectionAreaFor:function(tile) {
        displayNumber = $(tile).html();
        $("#DisplayNumber").html(displayNumber);
        $("#AppearanceSelectionArea").removeClass("HiddenScreen");
    },

    showAppearanceSelectionArea:function() {
        $("#AppearanceSelectionArea").removeClass("HiddenScreen");
    },

    hideAppearanceSelectionArea:function() {
        $("#AppearanceSelectionArea").addClass("HiddenScreen");
    },

    changeDisplayAppearance:function(tile) {
        displayNumber = $("#DisplayNumber").html();
        appearanceKey = $(tile).attr("name");
        this.sendChangeDisplayAppearance(displayNumber, appearanceKey);
        this.hideAppearanceSelectionArea();
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

    sendIdentifyAllDisplays:function() {
        command = new Command('identify_all_displays', {});
        this.websocket.send(command.jsonString());
    },

    sendChangeDisplayAppearance:function(displayNumber, appearanceKey) {
        command = new Command('change_display_appearance', {"appearance_id": appearanceKey,
                                                            "display_id": displayNumber});
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

    _formatNumber:function(value) {
        if (value < 10) {
            formattedValue = "0" + value;
        }
        else {
            formattedValue = "" + value;
        }
        return formattedValue;
    },

    _readParametersOfForm:function(formId) {
        parameters = {};
        form_data = $(formId).serializeArray();
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
