$(function() {

    // define speech recognition
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 5; 
    var resultObtained = false;
    function setupRecognitionSession(onresult_cb) {
        recognition.onresult = function(event) {
            console.log('registered result');
            onresult_cb(event);
        };
        recognition.onend = function(event) {
            if (!resultObtained) {
                console.log('recognition session timeout. restarting.');
                recognition.start();
            } else {
                resultObtained = false;
            }
        };
    }

    // get all audio files
    var steps = $('[id^="step_"]');
    var ings = $('[id^="ing_"]');

    var num_ing = ings.length;
    var num_steps = steps.length;
    console.log("num_ing: " + num_ing);
    console.log("num_step: " + num_steps);

    var state = 'start';
    var idx = 0;

    function play_next_clip() {
        $("#" + state + '_' + idx)[0].play();
    }

    // define the onAudioEnd handler
    function onAudioEnd() {
        console.log(state + idx);
        // idx is next index to be played
        if (state === 'ing' || state === 'step') {
            idx++;
        }

        if (state === 'start') {
            // if start, switch to ing
            state = 'ing';
            idx = 0;
            play_next_clip();
        } else if (state === 'ing') {
            // if last ing has finished continue to steps
            if (idx >= num_ing) {
                // ask if you would like to repeat the ing
                // or not
                state = 'prompt_repeat_ingredients';
                idx = 0;
                $("#misc_ing_end")[0].play();
            } else {
                play_next_clip();
            }
        }  else if (state === 'prompt_repeat_ingredients') {
            // listen to the user, if they say, yes then
            // redo ing, else go on to step
            idx = 0;
            //recognition.start();
            //recognition.onresult = function(event) {
            //    console.log(event.results);
            //    if (event.results[0][0].transcript.toLowerCase() === "yes") {
            //        state = 'ing';
            //        play_next_clip();
            //    } else {
            //        state = 'step';
            //        $("#misc_step_start")[0].play();
            //    }
            //};
            console.log('listening for user...');
            setupRecognitionSession(function(event) {
                console.log(event.results);
                var input = event.results[0][0].transcript.toLowerCase();
                if (input === "yes") {
                    state = 'ing';
                    play_next_clip();
                    resultObtained = true;
                } else if (input === "no") {
                    state = 'step';
                    $("#misc_step_start")[0].play();
                    resultObtained = true;
                }
            });
            recognition.start();
        } else if (state === 'step') {
            state = 'repeat_last_step';
            $("#misc_prompt_next")[0].play();
        } else if (state === 'repeat_last_step') {
            // listen to user input for yes or no
            console.log('listening for user...');
            state = 'step';
            // recognition.start();
            // recognition.onresult = function(event) {
            //     console.log(event.results);
            //     if (event.results[0][0].transcript.toLowerCase() === "yes") {
            //         idx--;
            //     }
            //     if (idx >= num_steps) {
            //         // you have finished the recipe
            //         state = 'finished';
            //         $("#misc_finish")[0].play();
            //     } else {
            //         play_next_clip();
            //     }
            // };
            setupRecognitionSession(function(event) {
                console.log(event.results);
                var input = event.results[0][0].transcript.toLowerCase();
                if (input === "yes") {
                    console.log('rewinding one step');
                    idx--;
                    resultObtained = true;
                    if (idx >= num_steps) {
                        console.log('finished the recipe, verbalize it');
                        // you have finished the recipe
                        state = 'finished';
                        $("#misc_finish")[0].play();
                    } else {
                        play_next_clip();
                    }
                } else if (input === "no") {
                    resultObtained = true;
                    if (idx >= num_steps) {
                        console.log('finished the recipe, verbalize it');
                        // you have finished the recipe
                        state = 'finished';
                        $("#misc_finish")[0].play();
                    } else {
                        play_next_clip();
                    }
                } else {}});
            recognition.start();
        }

        // scroll view to upcoming idx
        if (state == 'step') {
            $('html, body').animate({
                scrollTop: $("#s_" + (idx + 1)).offset().top
            }, 1000);
        } else if (state == 'ing') {
            $('html, body').animate({
                scrollTop: $(".ingCard").offset().top
            }, 1000);
        }
    }

    function addOnAudioEndListener() {
        $("#misc_ing_start").bind('ended', onAudioEnd);
        $("#misc_ing_end").bind('ended', onAudioEnd);
        $("#misc_step_start").bind('ended', play_next_clip);
        $("#misc_prompt_next").bind('ended', onAudioEnd);
        // all ing
        for (var i = 0; i < num_ing; i++) {
            $("#ing_" + i).bind('ended', onAudioEnd);
        }
        // all step
        for (var i = 0; i < num_ing; i++) {
            $("#step_" + i).bind('ended', onAudioEnd);
        }
    }

    // start the state machine
    addOnAudioEndListener();
    $("#misc_ing_start")[0].play();
});