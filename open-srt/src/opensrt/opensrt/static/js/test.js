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
            var keyPressed = event.keyCode ? event.keyCode : event.which;
            var START_KEY_BIND = 32;
            var LEFT_KEY_BINDS = [
                test[0].fields.left_key_bind.toLowerCase().charCodeAt(0),
                test[0].fields.left_key_bind.toUpperCase().charCodeAt(0)
            ]
            var RIGHT_KEY_BINDS = [
                test[0].fields.right_key_bind.toLowerCase().charCodeAt(0), 
                test[0].fields.right_key_bind.toUpperCase().charCodeAt(0)
            ]
            if (keyPressed === START_KEY_BIND && phase === Phase.INSTRUCTION) {
                phase = Phase.TESTING;
                $("#instruction-phase-container").hide();
                $("#testing-phase-container").show();
                leftLabels = handleLabel(block, "left");
                rightLabels = handleLabel(block, "right");
                anchor = handleAnchor(leftLabels, rightLabels);
                anchorCount = 1;
                startTime = new Date().getTime();
                correct = true;
            } else if ($.inArray(keyPressed, LEFT_KEY_BINDS.concat(RIGHT_KEY_BINDS)) >= 0 && phase === Phase.TESTING) {
                if (anchorCount < block.fields.length + 1) {
                    var anchorLabelId = anchor.fields.label;
                    if (($.inArray(keyPressed, RIGHT_KEY_BINDS) >= 0 && $.inArray(anchorLabelId, getIds(rightLabels)) >= 0)
                            || ($.inArray(keyPressed, LEFT_KEY_BINDS) >= 0 && $.inArray(anchorLabelId, getIds(leftLabels)) >= 0)) {
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

function handleLabel(block, labelType) {
    // TODO Replace with inArray
    var filteredLabels = $.grep(labels, function(n) {
        return n.pk === block.fields["primary_" + labelType + "_label"] || n.pk === block.fields["secondary_" + labelType + "_label"];
    });
    $("#primary-" + labelType + "-label").html(filteredLabels[0].fields.name).css("color", "#" + filteredLabels[0].fields.color);
    if (filteredLabels.length > 1) {
        $("#secondary-" + labelType + "-label").html(filteredLabels[1].fields.name).css("color", "#" + filteredLabels[1].fields.color);
        $("#" + labelType + "-separator").show();
    } else {
        $("#" + labelType + "-separator").hide();
    }
    return filteredLabels;
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