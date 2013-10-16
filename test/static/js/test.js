$(document).ready(function() {
    Test.initializeInstructionPhase();
    $(document).keypress(function(event) {
        if (Test.phase !== Test.Phase.TERMINATION) {
            var keyPressed = event.keyCode ? event.keyCode : event.which;
            if (keyPressed === Test.START_KEY_BIND && Test.phase === Test.Phase.INSTRUCTION) {
                Test.initializeTestingPhase();
            } else if ($.inArray(keyPressed, Test.LEFT_KEY_BINDS.concat(Test.RIGHT_KEY_BINDS)) >= 0 && Test.phase === Test.Phase.TESTING) {
                var correctRightCategory = $.inArray(keyPressed, Test.RIGHT_KEY_BINDS) >= 0 && $.inArray(Test.stimulus.fields.category, Test.getIds(Test.rightCategories)) >= 0;
                var correctLeftCategory = $.inArray(keyPressed, Test.LEFT_KEY_BINDS) >= 0 && $.inArray(Test.stimulus.fields.category, Test.getIds(Test.leftCategories)) >= 0;
                if (correctRightCategory || correctLeftCategory) {
                    Test.handleCorrectAnswer();
                    if (Test.stimulusCount > Test.block.fields.number_of_stimuli) {
                        if (Test.blocks.length > 0) {
                            Test.initializeInstructionPhase();
                        } else {
                            Test.initializeTerminationPhase();
                        }
                    }
                } else {
                    Test.handleIncorrectAnswer();
                }
            }
        }
    });
});

function Test() {};

Test.Phase = {
    INSTRUCTION: 0,
    TESTING: 1,
    TERMINATION: 2
};

Test.phase = Test.Phase.INSTRUCTION;
Test.test = test;
Test.blocks = blocks;
Test.categories = categories;
Test.stimuli = stimuli;
Test.media_url = media_url;

Test.leftCategories = null;
Test.rightCategories = null;
Test.block = null;
Test.stimulus = null;
Test.previousStimulus = null;
Test.stimulusCount = null;
Test.startTime = null;
Test.correct = null;

Test.START_KEY_BIND = 32;
Test.LEFT_KEY_BINDS = [
    Test.test[0].fields.left_key_bind.toLowerCase().charCodeAt(0),
    Test.test[0].fields.left_key_bind.toUpperCase().charCodeAt(0)
];
Test.RIGHT_KEY_BINDS = [
    Test.test[0].fields.right_key_bind.toLowerCase().charCodeAt(0),
    Test.test[0].fields.right_key_bind.toUpperCase().charCodeAt(0)
];

Test.handleBlock = function() {
    for (var order = 1; order < 10; order++) {
        var blockGroup = $.grep(Test.blocks, function(n) {
            return n.fields.order === order;
        });
        if (blockGroup !== null && blockGroup.length !== 0) {
            var block = blockGroup[Math.floor(Math.random() * blockGroup.length)];
            Test.blocks = Test.blocks.filter(function(item) {
                return item.pk !== block.pk;
            });
            return block;
        }
    }
}

Test.handleStimulus = function(leftCategories, rightCategories) {
    var categoryIds = Test.getIds(leftCategories).concat(Test.getIds(rightCategories));
    var filteredStimuli = $.grep(Test.stimuli, function(n) {
        return $.inArray(n.fields.category, categoryIds) >= 0;
    });
    var stimulus = filteredStimuli[Math.floor(Math.random() * filteredStimuli.length)];
    var html = (stimulus.model === "portal.imagestimulus") 
          ? '<img class="image-stimulus" src="' + Test.media_url + stimulus.fields.value + '" alt="picture" />'
          : '<span class="text-stimulus">' + stimulus.fields.value + "</span>";
    $("#stimulus").html(html);
    return stimulus;
}

Test.handleCategory = function(block, categoryType) {
    var filteredCategories = $.grep(Test.categories, function(n) {
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

Test.initializeTerminationPhase = function() {
    Test.phase = Test.Phase.TERMINATION;
    $("#testing-phase-container").hide();
    $("#termination-phase-container").show();
    var data = {'test_status': true};
    $.get("../record/test-status/", data);
}

Test.initializeInstructionPhase = function() {
    Test.phase = Test.Phase.INSTRUCTION;
    Test.block = Test.handleBlock();
    Test.stimulusCount = 0;
    $("#instructions").html(Test.block.fields.instructions);
    $("#testing-phase-container").hide();
    $("#instruction-phase-container").show();
    $("#status").css("visibility", "hidden");
}

Test.initializeTestingPhase = function() {
    Test.phase = Test.Phase.TESTING;
    Test.leftCategories = Test.handleCategory(Test.block, "left");
    Test.rightCategories = Test.handleCategory(Test.block, "right");
    Test.stimulus = Test.handleStimulus(Test.leftCategories, Test.rightCategories);
    Test.previousStimulus = Test.stimulus;
    Test.stimulusCount = 1;
    Test.startTime = new Date().getTime();
    Test.correct = true;
    $("#instruction-phase-container").hide();
    $("#testing-phase-container").show();
}

Test.handleCorrectAnswer = function() {
    function record_trial(block, leftCategories, rightCategories, stimulus, latency, correct) {
        var data = {
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

    record_trial(Test.block, Test.leftCategories, Test.rightCategories, Test.stimulus, new Date().getTime() - Test.startTime, Test.correct);
    Test.startTime = new Date().getTime();
    while (Test.stimulus === Test.previousStimulus) {
         Test.stimulus = Test.handleStimulus(Test.leftCategories, Test.rightCategories);
    }
    Test.previousStimulus = Test.stimulus;
    Test.stimulusCount++;
    Test.correct = true;
    $("#status").css("visibility", "hidden");
}

Test.handleIncorrectAnswer = function() {
    Test.correct = false;
    $("#status").css("visibility", "visible");
}

Test.getIds = function(list) {
    var ids = [];
    $.each(list, function(index, value) {
        ids.push(value.pk);
    });
    return ids;
}