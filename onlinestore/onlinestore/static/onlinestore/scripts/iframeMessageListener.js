(function () {
    "use strict";
    /* global $ */

    var EVENT_MESSAGE = "message";
    var TYPE_LOAD = "LOAD";
    var TYPE_LOAD_REQUEST = "LOAD_REQUEST";
    var TYPE_SAVE = "SAVE";
    var TYPE_SCORE = "SCORE";
    var TYPE_MESSAGE = "MESSAGE";

    var csrftoken = $.cookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    window.addEventListener(EVENT_MESSAGE, messageListener, false);

    function messageListener(event) {
        var messageType = event.data.messageType;
        if (messageType === TYPE_LOAD_REQUEST) {
            initiateLoad(event);
        }
        else if (messageType === TYPE_SAVE) {
            saveGame(event);
        }
        else if (messageType === TYPE_SCORE) {
            postScore(event);
        }
    }

    function initiateLoad(event) {
        $.getJSON('../load/', event.data, loadSuccess).error(loadFailure);
    }

    function saveGame(event) {
        var save = {
            gameState: JSON.stringify(event.data.gameState)
        };
        $.post('../save/', save, saveSuccess).error(genericError);
    }

    function saveSuccess(data) {
        sendMessage('Save successful.');
    }

    function postScore(event) {
        $.post('../score/', event.data, scoreSuccess).error(genericError);
    }

    function scoreSuccess() {
        sendMessage('Score saved.');
    }

    function loadSuccess(response) {
        //post message to iframe
        var message = {
            messageType: TYPE_LOAD,
            gameState: response
        };
        window.frames[0].postMessage(message, '*');
        sendMessage('Load successful.');
    }

    function loadFailure(response) {
        if(response.status === 404) {
            sendMessage('No save file found.');
        }
        else {
            sendMessage('An error occured: ' + response.status + ' ' + response.statusText +'. Load failed.');
        }
    }

    function genericError(response) {
        sendMessage('An error occured: ' + response.status + ' ' + response.statusText + '.');
    }


    function sendMessage(messageString) {
        var message = {
            messageType: TYPE_MESSAGE,
            message: messageString
        };
        window.frames[0].postMessage(message, '*');
    }
})();