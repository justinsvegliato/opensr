// Loads the input file into the variable "startIAT"
function initialize(iatSource) {
    $.getJSON(iatSource, startIAT);
}

// Initialize variables, build page & data object, display instructions
function startIAT(data) {
    currentState = "instruction";
    session = 0;
    roundnum = 0;
    input = data;

    // default to show results to participant
    if (!('showResult' in input)) {
        input.showResult = true;
    }

    // make the target or association words green
    if (Math.random() < 0.5) {
        openA = "<font color=green>";
        closeA = "</font>";
        open1 = "";
        close1 = "";
    } else {
        open1 = "<font color=green>";
        close1 = "</font>";
        openA = "";
        closeA = "";
    }
    buildPage();
    roundArray = initRounds();
    instructionPage();
}

// Adds all images to page (initially hidden) so they are pre-loaded for IAT
function buildPage() {
    if (input.catA.itemtype == "img") {
        for (i in input.catA.items) {
            var itemstr = '<img id="' + input.catA.datalabel + i +
                    '" class="IATitem" src="' + input.catA.items[i] + '">';
            $("#exp_instruct").after(itemstr);
        }
    }
    if (input.catB.itemtype == "img") {
        for (i in input.catB.items) {
            var itemstr = '<img id="' + input.catB.datalabel + i +
                    '" class="IATitem" src="' + input.catB.items[i] + '">';
            $("#exp_instruct").after(itemstr);
        }
    }
    if (input.cat1.itemtype == "img") {
        for (i in input.cat1.items) {
            var itemstr = '<img id="' + input.cat1.datalabel + i +
                    '" class="IATitem" src="' + input.cat1.items[i] + '">';
            $("#exp_instruct").after(itemstr);
        }
    }
    if (input.cat2.itemtype == "img") {
        for (i in input.cat2.items) {
            var itemstr = '<img id="' + input.cat2.datalabel + i +
                    '" class="IATitem" src="' + input.cat2.items[i] + '">';
            $("#exp_instruct").after(itemstr);
        }
    }
}

// Round object
function IATround() {
    this.starttime = 0;
    this.endtime = 0;
    this.itemtype = "none";
    this.category = "none";
    this.catIndex = 0;
    this.correct = 0;
    this.errors = 0;
}

// Create array for each session & round, with pre-randomized ordering of images
function initRounds() {
    var roundArray = [];
    // for each session
    for (var i = 0; i < 7; i++) {
        roundArray[i] = [];
        switch (i) {
            case 0:
            case 4:
                stype = "target";
                numrounds = 20;
                break;
            case 1:
                stype = "association";
                numrounds = 20;
                break;
            case 2:
            case 3:
            case 5:
            case 6:
                stype = "both";
                numrounds = 40;
                break;

        }
        prevIndexA = -1;
        prevIndex1 = -1;
        for (var j = 0; j < numrounds; j++) {
            var round = new IATround();

            if (stype == "target") {
                round.category = (Math.random() < 0.5 ? input.catA.datalabel :
                        input.catB.datalabel);
            } else if (stype == "association") {
                round.category = (Math.random() < 0.5 ? input.cat1.datalabel :
                        input.cat2.datalabel);
            } else if (stype == "both") {
                if (j % 2 == 0) {
                    round.category = (Math.random() < 0.5 ? input.catA.datalabel :
                            input.catB.datalabel);
                } else {
                    round.category = (Math.random() < 0.5 ? input.cat1.datalabel :
                            input.cat2.datalabel);
                }
            }
            // pick a category
            if (round.category == input.catA.datalabel) {
                round.itemtype = input.catA.itemtype;
                if (i < 4) {
                    round.correct = 1;
                } else {
                    round.correct = 2;
                }

                // pick an item different from the last
                while (prevIndexA == round.catIndex) {
                    round.catIndex = Math.floor(Math.random() * input.catA.items
                            .length);
                }
                prevIndexA = round.catIndex;

            } else if (round.category == input.catB.datalabel) {
                round.itemtype = input.catB.itemtype;
                if (i < 4) {
                    round.correct = 2;
                } else {
                    round.correct = 1;
                }
                // pick an item different from the last
                while (prevIndexA == round.catIndex) {
                    round.catIndex = Math.floor(Math.random() * input.catB.items
                            .length);
                }
                prevIndexA = round.catIndex;
            } else if (round.category == input.cat1.datalabel) {
                round.itemtype = input.cat1.itemtype;
                round.correct = 1;
                // pick an item different from the last
                while (prevIndex1 == round.catIndex) {
                    round.catIndex = Math.floor(Math.random() * input.cat1.items
                            .length);
                }
                prevIndex1 = round.catIndex;
            } else if (round.category == input.cat2.datalabel) {
                round.itemtype = input.cat2.itemtype;
                round.correct = 2;
                // pick an item different from the last
                while (prevIndex1 == round.catIndex) {
                    round.catIndex = Math.floor(Math.random() * input.cat2.items
                            .length);
                }
                prevIndex1 = round.catIndex;
            }

            roundArray[i].push(round);
        }
    }

    return roundArray;
}

// insert instruction text based on stage in IAT
function instructionPage() {
    switch (session) {
        case 0:
            $('#left_cat').ready(function() {
                $('#left_cat').html(openA + input.catA.label + closeA);
            });
            $('#right_cat').ready(function() {
                $('#right_cat').html(openA + input.catB.label + closeA);
            });
            break;
        case 1:
            $("#left_cat").html(open1 + input.cat1.label + close1);
            $("#right_cat").html(open1 + input.cat2.label + close1);
            break;
        case 2:
        case 3:
            $("#left_cat").html(openA + input.catA.label + closeA +
                    '<br>or<br>' + open1 + input.cat1.label + close1);
            $("#right_cat").html(openA + input.catB.label + closeA +
                    '<br>or<br>' + open1 + input.cat2.label + close1);
            break;
        case 4:
            $("#left_cat").html(openA + input.catB.label + closeA);
            $("#right_cat").html(openA + input.catA.label + closeA);
            break;
        case 5:
        case 6:
            $("#left_cat").html(openA + input.catB.label + closeA +
                    '<br>or<br>' + open1 + input.cat1.label + close1);
            $("#right_cat").html(openA + input.catA.label + closeA +
                    '<br>or<br>' + open1 + input.cat2.label + close1);
            break;
    }
    if (session == 7) {
        $("#left_cat").html("");
        $("#right_cat").html("");
        $("#exp_instruct").html("<img src='spinner.gif'>");
        WriteFile();
        if (input.showResult)
        {
            calculateIAT();
        }
        else
        {
            resulttext = "<div style='text-align:center;padding:20px'>Thanks for participating! Please click the button below to proceed to a short survey. <br/><a href='http://localhost:8080/survey/' class='btn btn-primary' type='button'>Next &rarr;</a></div>";
            $("#picture_frame").html(resulttext);
        }
    } else {
        $.get("../static/iat/html/instructions" + (session + 1) + ".html", function(
                data) {
            $('#exp_instruct').html(data);
        });
    }
}

// Calculates estimate of effect size to present results to participant
function calculateIAT() {
    // calculate mean log(RT) for first key trial
    compatible = 0;
    for (i = 1; i < roundArray[3].length; i++) {
        score = roundArray[3][i].endtime - roundArray[3][i].starttime;
        if (score < 300) {
            score = 300;
        }
        if (score > 3000) {
            score = 3000;
        }
        compatible += Math.log(score);
    }
    compatible /= (roundArray[3].length - 1);

    // calculate mean log(RT) for second key trial
    incompatible = 0;
    for (i = 1; i < roundArray[6].length; i++) {
        score = roundArray[6][i].endtime - roundArray[6][i].starttime;
        if (score < 300) {
            score = 300;
        }
        if (score > 3000) {
            score = 3000;
        }
        incompatible += Math.log(score);
    }
    incompatible /= (roundArray[6].length - 1);

    // calculate variance log(RT) for first key trial
    cvar = 0;
    for (i = 1; i < roundArray[3].length; i++) {
        score = roundArray[3][i].endtime - roundArray[3][i].starttime;
        if (score < 300) {
            score = 300;
        }
        if (score > 3000) {
            score = 3000;
        }
        cvar += Math.pow((Math.log(score) - compatible), 2);
    }

    // calculate variance log(RT) for second key trial
    ivar = 0;
    for (i = 1; i < roundArray[6].length; i++) {
        score = roundArray[6][i].endtime - roundArray[6][i].starttime;
        if (score < 300) {
            score = 300;
        }
        if (score > 3000) {
            score = 3000;
        }
        ivar += Math.pow((Math.log(score) - incompatible), 2);
    }

    // calculate t-value
    tvalue = (incompatible - compatible) / Math.sqrt(((cvar / 39) + (ivar / 39)) /
            40);

    // determine effect size from t-value and create corresponding text
    if (Math.abs(tvalue) > 2.89) {
        severity = " <b>much more</b> than ";
    } else if (Math.abs(tvalue) > 2.64) {
        severity = " <b>more</b> than ";
    } else if (Math.abs(tvalue) > 1.99) {
        severity = " <b>a little more</b> than ";
    } else if (Math.abs(tvalue) > 1.66) {
        severity = " <b>just slightly more</b> than ";
    } else {
        severity = "";
    }

    // put together feedback based on direction & magnitude
    if (tvalue < 0 && severity != "") {
        resulttext =
                "<div style='text-align:center;padding:20px'>You associate " +
                openA + input.catB.label + closeA + " with " + open1 + input.cat1.label +
                close1;
        resulttext += " and " + openA + input.catA.label + closeA + " with " +
                open1 + input.cat2.label + close1 + severity;
        resulttext += "you associate " + openA + input.catA.label + closeA +
                " with " + open1 + input.cat1.label + close1;
        resulttext += " and " + openA + input.catB.label + closeA + " with " +
                open1 + input.cat2.label + close1 + ".</div>";
        // resulttext += "<div>incompatible: "+incompatible+" ("+(ivar/39)+"); compatible: "+compatible+" ("+(cvar/39)+"); tvalue: "+tvalue+"</div>";
    } else if (tvalue > 0 && severity != "") {
        resulttext =
                "<div style='text-align:center;padding:20px'>You associate " +
                openA + input.catA.label + closeA + " with " + open1 + input.cat1.label +
                close1;
        resulttext += " and " + openA + input.catB.label + closeA + " with " +
                open1 + input.cat2.label + close1 + severity;
        resulttext += "you associate " + openA + input.catB.label + closeA +
                " with " + open1 + input.cat1.label + close1;
        resulttext += " and " + openA + input.catA.label + closeA + " with " +
                open1 + input.cat2.label + close1 + ".</div>";
        // resulttext += "<div>incompatible: "+incompatible+" ("+(ivar/39)+"); compatible: "+compatible+" ("+(cvar/39)+"); tvalue: "+tvalue+"</div>";
    } else {
        resulttext =
                "<div style='text-align:center;padding:20px'>You do not associate " +
                openA + input.catA.label + closeA;
        resulttext += " with " + open1 + input.cat1.label + close1 +
                " any more or less than you associate ";
        resulttext += openA + input.catB.label + closeA + " with " + open1 +
                input.cat1.label + close1 + ".</div>";
        // resulttext += "<div>incompatible: "+incompatible+" ("+(ivar/39)+"); compatible: "+compatible+" ("+(cvar/39)+"); tvalue: "+tvalue+"</div>";
    }
    $("#picture_frame").html(resulttext);
}

function WriteFile() {
    var str = "";
    for (i = 0; i < roundArray.length; i++) {
        for (j = 0; j < roundArray[i].length; j++) {
            str += i + "," + j + ",";
            str += roundArray[i][j].category + ",";
            str += roundArray[i][j].catIndex + ",";
            str += roundArray[i][j].errors + ",";
            str += (roundArray[i][j].endtime - roundArray[i][j].starttime) + "\n";
        }
    }

    $.get("../record/", {
        data: str
    });
}

// This monitors for keyboard events
function keyHandler(kEvent) {
    // move from instructions to session on spacebar press
    var unicode = kEvent.keyCode ? kEvent.keyCode : kEvent.charCode;
    if (currentState == "instruction" && unicode == 32) {
        currentState = "play";
        $('#exp_instruct').html('');
        displayItem();
    }
    // in session
    if (currentState == "play") {
        runSession(kEvent);
    }
}

// Get the stimulus for this session & round and display it
function displayItem() {
    var tRound = roundArray[session][roundnum];
    tRound.starttime = new Date().getTime(); // the time the item was displayed
    if (tRound.itemtype == "img") {
        if (tRound.category == input.catA.datalabel) {
            $("#" + input.catA.datalabel + tRound.catIndex).css("display",
                    "block");
        } else if (tRound.category == input.catB.datalabel) {
            $("#" + input.catB.datalabel + tRound.catIndex).css("display",
                    "block");
        } else if (tRound.category == input.cat1.datalabel) {
            $("#" + input.cat1.datalabel + tRound.catIndex).css("display",
                    "block");
        } else if (tRound.category == input.cat2.datalabel) {
            $("#" + input.cat2.datalabel + tRound.catIndex).css("display",
                    "block");
        }
    } else if (tRound.itemtype == "txt") {
        if (tRound.category == input.catA.datalabel) {
            $("#word").html(openA + input.catA.items[tRound.catIndex] + closeA)
            $("#word").css("display", "block");
        } else if (tRound.category == input.catB.datalabel) {
            $("#word").html(openA + input.catB.items[tRound.catIndex] + closeA)
            $("#word").css("display", "block");
        } else if (tRound.category == input.cat1.datalabel) {
            $("#word").html(open1 + input.cat1.items[tRound.catIndex] + close1)
            $("#word").css("display", "block");
        } else if (tRound.category == input.cat2.datalabel) {
            $("#word").html(open1 + input.cat2.items[tRound.catIndex] + close1)
            $("#word").css("display", "block");
        }
    }
}

function runSession(kEvent) {
    var rCorrect = roundArray[session][roundnum].correct;
    var unicode = kEvent.keyCode ? kEvent.keyCode : kEvent.charCode;
    keyE = (unicode == 69 || unicode == 101);
    keyI = (unicode == 73 || unicode == 105);

    // if correct key (1 & E) or (2 & I)
    if ((rCorrect == 1 && keyE) || (rCorrect == 2 && keyI)) {
        $("#wrong").css("display", "none"); // remove X if it exists
        roundArray[session][roundnum].endtime = new Date().getTime(); // end time
        // if more rounds
        if (roundnum < roundArray[session].length - 1) {
            roundnum++;
            $(".IATitem").css("display", "none"); // hide all items
            displayItem(); // display chosen item
        } else {
            $(".IATitem").css("display", "none"); // hide all items
            currentState = "instruction"; // change state to instruction
            session++; // move to next session
            roundnum = 0; // reset rounds to 0
            instructionPage(); // show instruction page
        }
    }
    // incorrect key
    else if ((rCorrect == 1 && keyI) || (rCorrect == 2 && keyE)) {
        $("#wrong").css("display", "block"); // show X
        roundArray[session][roundnum].errors++; // note error
    }
}