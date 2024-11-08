#include <vector>
#include <list>
#include <set>
#include <string>
#include <iostream>
#include <iomanip>
#include "imdb.h"
#include "path.h"
using namespace std;

/**
 * Using the specified prompt, requests that the user supply
 * the name of an actor or actress.  The code returns
 * once the user has supplied a name for which some record within
 * the referenced imdb existsif (or if the user just hits return,
 * which is a signal that the empty string should just be returned.)
 *
 * @param prompt the text that should be used for the meaningful
 *               part of the user prompt.
 * @param db a reference to the imdb which can be used to confirm
 *           that a user's response is a legitimate one.
 * @return the name of the user-supplied actor or actress, or the
 *         empty string.
 */

static string promptForActor(const string& prompt, const imdb& db)
{
  string response;
  while (true) {
    cout << prompt << " [or <enter> to quit]: ";
    getline(cin, response);
    if (response == "") return "";
    vector<film> credits;
    if (db.getCredits(response, credits)) return response;
    cout << "We couldn't find \"" << response << "\" in the movie database. "
	 << "Please try again." << endl;
  }
}

/**
 * Serves as the main entry point for the six-degrees executable.
 * There are no parameters to speak of.
 *
 * @param argc the number of tokens passed to the command line to
 *             invoke this executable.  It's completely ignored
 *             here, because we don't expect any arguments.
 * @param argv the C strings making up the full command line.
 *             We expect argv[0] to be logically equivalent to
 *             "six-degrees" (or whatever absolute path was used to
 *             invoke the program), but otherwise these are ignored
 *             as well.
 * @return 0 if the program ends normally, and undefined otherwise.
 */

static path generateShortestPath(const imdb& db, string& actor1, string& actor2) {
    list<path> actor1_paths;
    actor1_paths.push_back(path(actor1));
    list<path> actor2_paths;
    actor2_paths.push_back(path(actor2));

    set<film> seen_films;
    set<string> seen_actors;
    seen_actors.insert(actor1);
    seen_actors.insert(actor2);

    int max_length = 7;
    while (true) {
        path next_path = actor1_paths.front();
        actor1_paths.pop_front();
        if (next_path.getLength() >= max_length)
            break;

        const string& actor = next_path.getLastPlayer();
        vector<film> linked_films;
        db.getCredits(actor, linked_films);
        for (film linked_film : linked_films) {
            if (seen_films.find(linked_film) == seen_films.end()) {
                seen_films.insert(linked_film);
                vector<string> linked_actors;
                db.getCast(linked_film, linked_actors);
                for (string linked_actor : linked_actors) {
                    path new_path = next_path;
                    new_path.addConnection(linked_film, linked_actor);
                    if (seen_actors.find(linked_actor) == seen_actors.end()) {
                        seen_actors.insert(linked_actor);
                        actor1_paths.push_back(new_path);
                    }
                    else if (linked_actor.compare(actor2) == 0) {
                        return new_path;
                    }
                }
            }
        }
    }

    return path(actor1);
}

int main(int argc, const char *argv[])
{
  (void)argc;
  (void)argv;

  imdb db(determinePathToData(argv[1])); // inlined in imdb-utils.h
  if (!db.good()) {
    cout << "Failed to properly initialize the imdb database." << endl;
    cout << "Please check to make sure the source files exist and that you have permission to read them." << endl;
    exit(1);
  }
  
  while (true) {
    string source = promptForActor("Actor or actress", db);
    if (source == "") break;
    string target = promptForActor("Another actor or actress", db);
    if (target == "") break;
    if (source == target) {
      cout << "Good one.  This is only interesting if you specify two different people." << endl;
    } else {
      // replace the following line by a call to your generateShortestPath routine... 
      path shortest_path = generateShortestPath(db, source, target);
      if (shortest_path.getLength() == 0)
          cout << endl << "No path between those two people could be found." << endl << endl;
      else
          cout << shortest_path << endl;
    }
  }
  
  cout << "Thanks for playing!" << endl;
  return 0;
}

