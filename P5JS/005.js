var R = 0;
var G = 0;
var B = 0;

function setup() {
    createCanvas(200, 200).parent("#canvas");
    select("#R").mouseMoved(updateColor);
    select("#G").mouseMoved(updateColor);
    select("#B").mouseMoved(updateColor);
}

function updateColor() {
    R = int(select("#R").value());
    select("#R_val").html(R);
    G = int(select("#G").value());
    select("#G_val").html(G);
    B = int(select("#B").value());
    select("#B_val").html(B);
}

function draw() {
    background(220);
    noStroke();
    fill(R, G, B);
    ellipse(100, 100, 100);
}
