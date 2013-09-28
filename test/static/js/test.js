$(document).ready(function() {
    Phase = {
        INSTRUCTION: 0,
        TESTING: 1,
        TERMINATION: 2
    };

    initializeInstructionPhase();
    
    $(document).keypress(function(event) {
        if (phase !== Phase.TERMINATION) {
            var keyPressed = event.keyCode ? event.keyCode : event.which;
            var START_KEY_BIND = 32;
            var LEFT_KEY_BINDS = [
                test[0].fields.left_key_bind.toLowerCase().charCodeAt(0),
                test[0].fields.left_key_bind.toUpperCase().charCodeAt(0)
            ];
            var RIGHT_KEY_BINDS = [
                test[0].fields.right_key_bind.toLowerCase().charCodeAt(0),
                test[0].fields.right_key_bind.toUpperCase().charCodeAt(0)
            ];
            if (keyPressed === START_KEY_BIND && phase === Phase.INSTRUCTION) {
                initializeTestingPhase();
            } else if ($.inArray(keyPressed, LEFT_KEY_BINDS.concat(RIGHT_KEY_BINDS)) >= 0 && phase === Phase.TESTING) {
                var correctRightCategory = $.inArray(keyPressed, RIGHT_KEY_BINDS) >= 0 && $.inArray(stimulus.fields.category, getIds(rightCategories)) >= 0;
                var correctLeftCategory = $.inArray(keyPressed, LEFT_KEY_BINDS) >= 0 && $.inArray(stimulus.fields.category, getIds(leftCategories)) >= 0;
                if (correctRightCategory || correctLeftCategory) {
                    handleCorrectAnswer();
                    if (stimulusCount > block.fields.number_of_stimuli) {
                        if (blocks.length > 0) {
                            initializeInstructionPhase();
                        } else {
                            initializeTerminationPhase();
                        }
                    }
                } else {
                    handleIncorrectAnswer();
                }
            }
        }
    });
});

function handleBlock() {
    for (var order = 1; order < 10; order++) {
        var blockGroup = $.grep(blocks, function(n) {
            return n.fields.order === order;
        });
        if (blockGroup !== null && blockGroup.length !== 0) {
            var block = blockGroup[Math.floor(Math.random() * blockGroup.length)];
            blocks = blocks.filter(function(item) {
                return item.pk !== block.pk;
            });
            return block;
        }
    }
}

function handleStimulus(leftCategories, rightCategories) {
    var categoryIds = getIds(leftCategories).concat(getIds(rightCategories));
    var filteredStimuli = $.grep(stimuli, function(n) {
        return $.inArray(n.fields.category, categoryIds) >= 0;
    });
    var stimulus = filteredStimuli[Math.floor(Math.random() * filteredStimuli.length)];
    var html = (stimulus.model === "portal.imagestimulus") 
          ? '<img class="image-stimulus" src="' + media_url + stimulus.fields.value + '" alt="picture" />'
          : '<span class="text-stimulus">' + stimulus.fields.value + "</span>";
    $("#stimulus").html(html);
    return stimulus;
}

function handleCategory(block, categoryType) {
    var filteredCategories = $.grep(categories, function(n) {
        return n.pk === block.fields["primary_" + categoryType + "_category"] || n.pk === block.fields["secondary_" + categoryType + "_category"];
    });
    $("#primary-" + categoryType + "-category").html(filteredCategories[0].fields.category_name).css("color", filteredCategories[0].fields.color);
    if (filteredCategories.length > 1) {
        $("#secondary-" + categoryType + "-category").html(filteredCategories[1].fields.category_name).css("color", filteredCategories[1].fields.color);
        $("#" + categoryType + "-separator").show();
    } else {
        $("#" + categoryType + "-separator").hide();
    }
    return filteredCategories;
}

function initializeTerminationPhase() {
    phase = Phase.TERMINATION;
    $("#testing-phase-container").hide();
    $("#termination-phase-container").show();
    data = {'test_status': true};
    $.get("../record/test-status/", data);
}

function initializeInstructionPhase() {
    phase = Phase.INSTRUCTION;
    block = handleBlock();
    stimulusCount = 0;
    $("#instructions").html(block.fields.instructions);
    $("#testing-phase-container").hide();
    $("#instruction-phase-container").show();
    $("#status").css("visibility", "hidden");
}

function initializeTestingPhase() {
    phase = Phase.TESTING;
    leftCategories = handleCategory(block, "left");
    rightCategories = handleCategory(block, "right");
    stimulus = handleStimulus(leftCategories, rightCategories);
    previousStimulus = stimulus;
    stimulusCount = 1;
    startTime = new Date().getTime();
    correct = true;
    $("#instruction-phase-container").hide();
    $("#testing-phase-container").show();
}

function handleCorrectAnswer() {
    function record_trial(block, leftCategories, rightCategories, stimulus, latency, correct) {
        data = {
            "block": block.fields.block_name,
            "practice": block.fields.practice,
            "primary_left_category": leftCategories[0].fields.category_name,
            "secondary_left_category": leftCategories.length > 1 ? leftCategories[1].fields.category_name : null,
            "primary_right_category": rightCategories[0].fields.category_name,
            "secondary_right_category": rightCategories.length > 1 ? rightCategories[1].fields.category_name : null,
            "stimulus": stimulus.fields.value,
            "latency": latency,
            "correct": correct
        };
        $.get("../record/trial/", data);
    }

    record_trial(block, leftCategories, rightCategories, stimulus, new Date().getTime() - startTime, correct);
    startTime = new Date().getTime();
    while (stimulus === previousStimulus) {
         stimulus = handleStimulus(leftCategories, rightCategories);
    }
    previousStimulus = stimulus;
    stimulusCount++;
    $("#status").css("visibility", "hidden");
}

function handleIncorrectAnswer() {
    correct = false;
    $("#status").css("visibility", "visible");
}

function getIds(list) {
    var ids = [];
    $.each(list, function(index, value) {
        ids.push(value.pk);
    });
    return ids;
}