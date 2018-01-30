#include <iostream>
#include <vector>
#include <string>
#include <boost/algorithm/string.hpp>

using namespace std;

// On the line beginning "Input:" be given a single number that tells you how much change to produce, and then a list of coins you own. The next line, beginning with "Output:", tells you the number of coins to give back to achieve the change you need to give back (bounded by the number of coins you have).
// Your progam should emit the coins you would give back to yield the correct value of change, if possible. Multiple solutions may be possible. If no solution is possible, state that.

vector<int> coins;
string input = "200 50 50 20 20 10";
string output_bound = "n >= 5";
int target_change;
int given_change;

int main() {

    // parse input coins
    vector<string> input_words;
    boost::split(input_words, input, [](char c){return c==' ';});
    for (string word : input_words) {
        coins.push_back(stoi(word));
    }
    target_change = coins[0];
    coins.erase(coins.begin());

    // parse output requirement
    vector<string> output_words;
    boost::split(output_words, output_bound, [](char c){return c==' ';});
    string condition = output_words[1];
    int bound = stoi(output_words[2]);

    // converting >= and <= to pure inequalities
    if (condition == "<=") {
        condition = "<";
        bound++;
    }
    if (condition == ">=") {
        condition = ">";
        bound--;
    }

    // find fewest coins
    if (condition == "<") {
        sort(coins.begin(), coins.end());
        reverse(coins.begin(), coins.end()); // sort biggest to smallest
    }

    // find most coins
    if (condition == ">") {
        sort(coins.begin(), coins.end()); // sort smallest to biggest
    }

    // give change
    given_change = 0;
    int coins_given = 0;
    string change;
    for (int coin : coins) {
        if (given_change + coin <= target_change) {
            given_change += coin;
            coins_given++;
            change += (" " + to_string(coin));
        }
    }
    if ((given_change == target_change) && ((condition == "<" && coins_given < bound) || (condition == ">" && coins_given > bound))) {
        cout << change << endl;
    }
    else {
        cout << "Change not possible";
    }
}
