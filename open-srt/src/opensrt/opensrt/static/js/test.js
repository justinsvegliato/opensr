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
                var correctRightLabel = $.inArray(keyPressed, RIGHT_KEY_BINDS) >= 0 && $.inArray(anchor.fields.label, getIds(rightLabels)) >= 0;
                var correctLeftLabel = $.inArray(keyPressed, LEFT_KEY_BINDS) >= 0 && $.inArray(anchor.fields.label, getIds(leftLabels)) >= 0;
                if (correctRightLabel || correctLeftLabel) {
                    handleCorrectAnswer();
                    if (anchorCount > block.fields.length) {
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
    for (var rank = 1; rank < 10; rank++) {
        var blockGroup = $.grep(blocks, function(n) {
            return n.fields.rank === rank;
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

function handleAnchor(leftLabels, rightLabels) {
    var labelIds = getIds(leftLabels).concat(getIds(rightLabels));
    var filteredAnchors = $.grep(anchors, function(n) {
        return $.inArray(n.fields.label, labelIds) >= 0;
    });
    var anchor = filteredAnchors[Math.floor(Math.random() * filteredAnchors.length)];
    $("#anchor").html(anchor.fields.value);
    return anchor;
}

function handleLabel(block, labelType) {
    var filteredLabels = $.grep(labels, function(n) {
        return n.pk === block.fields["primary_" + labelType + "_label"] || n.pk === block.fields["secondary_" + labelType + "_label"];
    });
    $("#primary-" + labelType + "-label").html(filteredLabels[0].fields.name).css("color", filteredLabels[0].fields.color);
    if (filteredLabels.length > 1) {
        $("#secondary-" + labelType + "-label").html(filteredLabels[1].fields.name).css("color", filteredLabels[1].fields.color);
        $("#" + labelType + "-separator").show();
    } else {
        $("#" + labelType + "-separator").hide();
    }
    return filteredLabels;
}

function initializeTerminationPhase() {
    phase = Phase.TERMINATION;
    $("#testing-phase-container").hide();
    $("#termination-phase-container").show();
}

function initializeInstructionPhase() {
    phase = Phase.INSTRUCTION;
    block = handleBlock();
    anchorCount = 0;
    $("#instructions").html(block.fields.instructions);
    $("#testing-phase-container").hide();
    $("#instruction-phase-container").show();
}

function initializeTestingPhase() {
    phase = Phase.TESTING;
    leftLabels = handleLabel(block, "left");
    rightLabels = handleLabel(block, "right");
    anchor = handleAnchor(leftLabels, rightLabels);
    previousAnchor = anchor;
    anchorCount = 1;
    startTime = new Date().getTime();
    correct = true;
    $("#instruction-phase-container").hide();
    $("#testing-phase-container").show();
}

function handleCorrectAnswer() {
    function record(leftLabels, rightLabels, anchor, reactionTime, correct) {
        data = {
            "primary_left_label": leftLabels[0].fields.name,
            "secondary_left_label": leftLabels > 1 ? leftLabels[1].fields.name : null,
            "primary_right_label": rightLabels[0].fields.name,
            "secondary_right_label": rightLabels > 1 ? rightLabels[1].fields.name : null,
            "anchor": anchor.fields.value,
            "reaction_time": reactionTime,
            "correct": correct
        };
        $.get("../record/", data);
    }

    record(leftLabels, rightLabels, anchor, new Date().getTime() - startTime, correct);
    startTime = new Date().getTime();
    while (anchor === previousAnchor) {
         anchor = handleAnchor(leftLabels, rightLabels);
    }
    previousAnchor = anchor;
    anchorCount++;
    correct = true;
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