#include <iostream>
#include <vector>
#include <cmath>

// You run a moving truck business, and you can pack the most in your truck when you have stacks of equal size - no slack space. So, you're an enterprising person, and you want to write some code to help you along.
// You'll be given two numbers per line. The first number is the number of stacks of boxes to yield. The second is a list of boxes, one integer per size, to pack.

using namespace std;

tuple<bool, vector<vector<int>>*> make_stack(vector<int> *boxes, vector<vector<int>> *stacks, int height) {
    for (int i=0; i<pow(2,boxes->size()); i++) {
        int stack_height = 0; 
        vector<int> new_stack;
        vector<int> remaining_boxes;
        for (int j=0; j<boxes->size(); j++) {
            if(i & (1<<j)) {
                new_stack.push_back(boxes->at(j));
                stack_height += boxes->at(j);
            }
            else
                remaining_boxes.push_back(boxes->at(j));
        }
        if (stack_height == height) {
            stacks->push_back(new_stack);
            if (remaining_boxes.size() == 0)
                return make_tuple(true, stacks);
            if (get<0>(make_stack(&remaining_boxes, stacks, height)))
                return make_tuple(true, stacks);
            stacks->pop_back();
        }
    }
    return make_tuple(false, stacks);
}

int main(int argn, char** args) {

    int n_stacks = stoi(args[1]);

    vector<int> heights;
    int sum_height = 0;
    for (int i=0; i<string(args[2]).length(); i++) {
        heights.push_back(args[2][i] - '0');
        sum_height += (args[2][i] - '0');
    }

    if (sum_height % n_stacks != 0) {
        cout << "Not possible" << endl;
        return(0);
    }
    
    int stack_height = sum_height / n_stacks;

    // just fucking brute force it
    vector<vector<int>> stacks;
    auto results = make_stack(&heights, &stacks, stack_height);
    if (get<0>(results)) {
        for (auto stack : *get<1>(results)) {
            for (int height : stack)
                cout << height << " ";
            cout << endl;
        }
    }
    else
        cout << "Not possible" << endl;

    return(0);
}
