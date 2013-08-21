$(document).ready(function() {
    Phase = {
        INSTRUCTION: 0,
        TESTING: 1,
        TERMINATION: 2
    };

    var phase = Phase.INSTRUCTION;
    var block = handleBlock();
    $("#instructions").html(block.fields.instructions);

    $(document).keypress(function(event) {
        if (phase !== phase.TERMINATION) {
            var keyPressed = (event.keyCode ? event.keyCode : event.which);
            var START_KEY_BIND = 32;
            var RIGHT_KEY_BIND = test[0].fields.right_key_bind.charCodeAt(0);
            var LEFT_KEY_BIND = test[0].fields.left_key_bind.charCodeAt(0);
            if (keyPressed === START_KEY_BIND && phase === Phase.INSTRUCTION) {
                phase = Phase.TESTING;
                $("#instruction-phase-container").hide();
                $("#testing-phase-container").show();
                leftLabels = handleLeftLabel(block);
                rightLabels = handleRightLabel(block);
                anchor = handleAnchor(leftLabels, rightLabels);
                anchorCount = 1;
                startTime = new Date().getTime();
                correct = true;
            } else if ((keyPressed === RIGHT_KEY_BIND || keyPressed === LEFT_KEY_BIND) && phase === Phase.TESTING) {
                if (anchorCount < block.fields.length + 1) {
                    var anchorLabelId = anchor.fields.label;
                    if ((keyPressed === RIGHT_KEY_BIND && $.inArray(anchorLabelId, getIds(rightLabels)) >= 0)
                            || (keyPressed === LEFT_KEY_BIND && $.inArray(anchorLabelId, getIds(leftLabels)) >= 0)) {
                        record(leftLabels, rightLabels, anchor, new Date().getTime() - startTime, correct);
                        startTime = new Date().getTime();
                        anchor = handleAnchor(leftLabels, rightLabels);
                        $("#status").css("visibility", "hidden");
                        anchorCount++;
                        correct = true;
                    } else {
                        correct = false;
                        $("#status").css("visibility", "visible");
                    }
                } else if (blocks.length > 0) {
                    phase = Phase.INSTRUCTION;
                    block = handleBlock();
                    $("#instructions").html(block.fields.instructions);
                    $("#testing-phase-container").hide();
                    $("#instruction-phase-container").show();
                    anchorCount = 0;
                    blockLength = 0;
                } else {
                    $("#testing-phase-container").hide();
                    $("#termination-phase-container").show();
                    phase = Phase.TERMINATION;
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

function handleLeftLabel(block) {
    // TODO Replace with inArray
    var leftLabels = $.grep(labels, function(n) {
        return n.pk === block.fields.primary_left_label || n.pk === block.fields.secondary_left_label;
    });
    $("#primary-left-label").html(leftLabels[0].fields.name).css("color", "#" + leftLabels[0].fields.color);
    if (leftLabels.length > 1) {
        $("#secondary-left-label").html(leftLabels[1].fields.name).css("color", "#" + leftLabels[1].fields.color);
        $("#left-separator").show();
    } else {
        $('#left-separator').hide();
    }
    return leftLabels;
}

function handleRightLabel(block) {
    // TODO Replace with inArray
    var rightLabels = $.grep(labels, function(n) {
        return n.pk === block.fields.primary_right_label || n.pk === block.fields.secondary_right_label;
    });
    $("#primary-right-label").html(rightLabels[0].fields.name).css("color", "#" + rightLabels[0].fields.color);
    if (rightLabels.length > 1) {
        $("#secondary-right-label").html(rightLabels[1].fields.name).css("color", "#" + rightLabels[1].fields.color);
        $("#right-separator").show();
    } else {
        $('#right-separator').hide();
    }
    return rightLabels;
}

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

function getIds(list) {
    var ids = [];
    $.each(list, function(index, value) {
        ids.push(value.pk);
    });
    return ids;
}