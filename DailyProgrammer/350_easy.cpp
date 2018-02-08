#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <boost/algorithm/string.hpp>

using namespace std;

// You have an enormous book collection and want to buy some shelves. You go to a bookshelfstore and they sell all kinds of shelves. The wierd part is, some shelves are different in length but they all cost the same.
// You now want to puzzle your collection so that you can fit as many books on the least number of shelves.
// The first line are the available bookshelves in the store, seperated by a space.
// From the second line on you get the book collections with the width followed by a title.
// Output the number of bookshelves you have to buy. If you can't fit them, even just one, you respond with impossible.
// NOTE: Damn problem is NP-hard, so it's brute force.

int main() {

    ifstream inFile;
    string fileName = "350_easy.txt";
    inFile.open(fileName);

    if (!inFile) {
        cout << "File not found" << endl;
        return(0);
    }

    // first line - parse available shelves
    string line;
    getline(inFile, line);
    vector<string> shelf_words;
    boost::split(shelf_words, line, [](char c){return c == ' ';});
    vector<int> shelves;
    transform(shelf_words.begin(), shelf_words.end(), back_inserter(shelves), [](string &word){return stoi(word);});

    // other lines
    vector<int> books;
    while (getline(inFile, line)) {
        vector<string> words;
        boost::split(words, line, [](char c){return c == ' ';});
        books.push_back(stoi(words[0]));
    }

    // sort shelves in decreasing order
    sort(shelves.begin(), shelves.end(), [](int i, int j){return i>j;});

    // run through all permutations of books
    int least_shelves = -1;
    sort(books.begin(), books.end());
    do {
        int current_shelf_index = 0;
        int current_shelf_used = 0;
        bool skip = false;
        for (int book : books) {
            current_shelf_used += book;
            if (shelves[current_shelf_index] < current_shelf_used) {
                current_shelf_index++;
                if (current_shelf_index + 1 > shelves.size())
                    skip = true;
                current_shelf_used = book;
                if (shelves[current_shelf_index] < current_shelf_used)
                    skip = true;
            }
        }
        if (skip)
            continue;
        if (least_shelves > current_shelf_index + 1 || least_shelves == -1)
            least_shelves = current_shelf_index + 1;
    } while (next_permutation(books.begin(), books.end()));

    // print results
    if (least_shelves == -1)
        cout << "Impossible" << endl;
    else
        cout << "Least possible number of shelves is " << least_shelves << endl;
}
