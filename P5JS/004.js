var money_in_bank = 0;
var quarters = 0;
var dimes = 0;
var nickels = 0;
var pennies = 0;

function setup() {
    createCanvas(400, 400).parent("#canvas");
    select("#put_money").mouseClicked(function() {
        var money_text = select("#input_money").value();
        new_money = parseFloat(money_text.slice(1)); // remove $
        money_in_bank += new_money;
        money_in_bank = round(money_in_bank*100)/100;
        select("#money_in_bank").html("Money in bank: $" + money_in_bank);
        quarters += floor(new_money / 0.25);
        new_money = new_money % 0.25;
        dimes += floor(new_money / 0.1);
        new_money = new_money % 0.1;
        nickels += floor(new_money / 0.05);
        new_money = new_money % 0.05;
        pennies += floor(new_money / 0.01);
        new_money = new_money % 0.01;
    });
}

function draw() {
    background('lightBlue');
    fill(220);
    ellipse(80, 210, 60);
    ellipse(160, 210, 40);
    ellipse(240, 210, 50);
    fill(184, 115, 51);
    ellipse(320, 210, 40);
    fill('black');
    text('quarter', 60, 160);
    text(quarters, 77, 214);
    text('dime', 147, 160);
    text(dimes, 157, 214);
    text('nickel', 224, 160);
    text(nickels, 237, 214);
    text('penny', 305, 160);
    text(pennies, 317, 214);
}
