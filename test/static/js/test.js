$(document).ready(function() {
    Test.initializeInstructionPhase();
    $(document).keypress(function(event) {
        if (Test.phase !== Test.Phase.TERMINATION) {
            var keyPressed = event.keyCode ? event.keyCode : event.which;
            if (keyPressed === Test.START_KEY_BIND && Test.phase === Test.Phase.INSTRUCTION) {
                Test.initializeTestingPhase();
            } else if ($.inArray(keyPressed, Test.LEFT_KEY_BINDS.concat(Test.RIGHT_KEY_BINDS)) >= 0 && Test.phase === Test.Phase.TESTING) {
                var isNextPhaseTriggeredByParticipant = !Test.block.fields.trial_interval || Test.block.fields.trial_interval === 0;
                var correctRightCategory = $.inArray(keyPressed, Test.RIGHT_KEY_BINDS) >= 0 && $.inArray(Test.stimulus.fields.category, Test.getIds(Test.rightCategories)) >= 0;
                var correctLeftCategory = $.inArray(keyPressed, Test.LEFT_KEY_BINDS) >= 0 && $.inArray(Test.stimulus.fields.category, Test.getIds(Test.leftCategories)) >= 0;
                var isCorrectCategoryChosen = correctRightCategory || correctLeftCategory;
                if (isCorrectCategoryChosen) {
                    if (isNextPhaseTriggeredByParticipant) {
                        Test.handleNextEvent();
                        Test.recordTrial();
                    } else {
                        Test.phase = Test.Phase.WAITING;
                        $("#wrongStatus").css("display", "none").css("visibility", "hidden");
                        $("#rightStatus").css("display", "block").css("visibility", "visible");
                        Test.recordTrial();
                    }
                } else {
                    if (!isNextPhaseTriggeredByParticipant) {
                        Test.phase = Test.Phase.WAITING;
                    }
                    Test.correct = false;
                    $("#wrongStatus").css("display", "block").css("visibility", "visible");
                    $("#rightStatus").css("display", "none").css("visibility", "hidden");
                    Test.recordTrial();
                }
            }
        }
    });
});

function Test() {}

Test.Phase = {
    INSTRUCTION: 0,
    TESTING: 1,
    TERMINATION: 2,
    WAITING: 3
};

Test.phase = Test.Phase.INSTRUCTION;
Test.test = test;
Test.blocks = blocks;
Test.categories = categories;
Test.stimuli = stimuli;
Test.stimuli_orders = stimuli_orders;
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
    for (var order = 0; order < 10; order++) {
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
};

Test.handleStimulus = function(leftCategories, rightCategories) {
    var categoryIds = Test.getIds(leftCategories).concat(Test.getIds(rightCategories));
    var filteredStimuli = $.grep(Test.stimuli, function(n) {
        return $.inArray(n.fields.category, categoryIds) >= 0;
    });
    var stimuli_order = $.grep(Test.stimuli_orders, function(n) {
       return n.fields.block === Test.block.pk
    })[0];
    var stimuli_id = stimuli_order.fields.stimuli[Test.stimulusCount];
    var stimulus = $.grep(filteredStimuli, function(n) {
        return stimuli_id === n.pk;
    })[0];
    
    if (stimuli_order.fields.random_order || (Test.stimulusCount >= filteredStimuli.length) ) {
        stimulus = filteredStimuli[Math.floor(Math.random() * filteredStimuli.length)];
    } 
    var html = !stimulus.fields.word 
            ? '<img class="image-stimulus" src="' + Test.media_url + stimulus.fields.image + '" alt="picture" />'
            : '<span class="text-stimulus">' + stimulus.fields.word + "</span>";          
    $("#stimulus").html(html);
    return stimulus;
};

Test.handleCategory = function(block, categoryType) {
    var filteredCategories = $.grep(Test.categories, function(n) {
        return n.pk === block.fields["primary_" + categoryType + "_category"] || n.pk === block.fields["secondary_" + categoryType + "_category"];
    });
    $("#primary-" + categoryType + "-category").html(filteredCategories[0].fields.category_name).css("color", filteredCategories[0].fields.color);
    if (filteredCategories.length > 1) {
        $("#secondary-" + categoryType + "-category").show().html(filteredCategories[1].fields.category_name).css("color", filteredCategories[1].fields.color);
        $("#" + categoryType + "-separator").show();
    } else {
        $("#secondary-" + categoryType + "-category").hide();
        $("#" + categoryType + "-separator").hide();
    }
    return filteredCategories;
};

Test.initializeTerminationPhase = function() {
    Test.phase = Test.Phase.TERMINATION;
    $("#testing-phase-container").hide();
    $("#termination-phase-container").show();
    var data = {'test_status': true};
    $.get("../record/test-status/", data);
};

Test.initializeInstructionPhase = function() {
    Test.phase = Test.Phase.INSTRUCTION;
    Test.block = Test.handleBlock();
    Test.stimulusCount = 0;
    $("#instructions").html(Test.block.fields.instructions);
    $("#testing-phase-container").hide();
    $("#instruction-phase-container").show();
    $("#wrongStatus").css("visibility", "hidden");
    $("#rightStatus").css("visibility", "hidden");
};

Test.initializeTestingPhase = function() {
    Test.phase = Test.Phase.TESTING;
    Test.leftCategories = Test.handleCategory(Test.block, "left");
    Test.rightCategories = Test.handleCategory(Test.block, "right");
    Test.displayNextStimulus(false);
    Test.stimulusCount = 0;
    $("#instruction-phase-container").hide();
    $("#testing-phase-container").show();
};

Test.displayNextStimulus = function(shouldWait) {
    var showStimulus = function() {
        Test.phase = Test.Phase.TESTING;
        Test.startTime = new Date().getTime();
        while (Test.stimulus === Test.previousStimulus) {
            Test.stimulus = Test.handleStimulus(Test.leftCategories, Test.rightCategories);
        }
        Test.previousStimulus = Test.stimulus;
        Test.correct = true;
        
        if (Test.block.fields.trial_interval > 0) {
            setTimeout(Test.handleNextEvent, Test.block.fields.trial_interval);
        }
    };
    
    if (Test.block.fields.intertrial_interval > 0 && shouldWait) {
        $("#status").css("visibility", "hidden");
        $("#stimulus").html('<img src="/static/img/loading-spinner.gif" alt="picture" />');
        Test.phase = Test.Phase.WAITING;
        setTimeout(showStimulus, Test.block.fields.intertrial_interval);
    } else {
        showStimulus();
    }
};

Test.handleNextEvent = function() {
    $("#wrongStatus").css("visibility", "hidden");
    $("#rightStatus").css("visibility", "hidden");
    
    if (Test.stimulusCount >= Test.block.fields.number_of_stimuli) {
        if (Test.blocks.length > 0) {
            Test.initializeInstructionPhase();
        } else {
            Test.initializeTerminationPhase();
        }
    } else {
        Test.stimulusCount++;
        Test.displayNextStimulus(true);
    }
};

Test.getIds = function(list) {
    var ids = [];
    $.each(list, function(index, value) {
        ids.push(value.pk);
    });
    return ids;
};

Test.recordTrial = function() {
    var data = {
        "block": Test.block.fields.block_name,
        "practice": Test.block.fields.practice,
        "primary_left_category": Test.leftCategories[0].fields.category_name,
        "secondary_left_category": Test.leftCategories.length > 1 ? Test.leftCategories[1].fields.category_name : null,
        "primary_right_category": Test.rightCategories[0].fields.category_name,
        "secondary_right_category": Test.rightCategories.length > 1 ? Test.rightCategories[1].fields.category_name : null,
        "stimulus": !Test.stimulus.fields.word ? Test.stimulus.fields.image : Test.stimulus.fields.word,
        "latency": new Date().getTime() - Test.startTime,
        "correct": Test.correct
    };
    $.get("../record/trial/", data);
};