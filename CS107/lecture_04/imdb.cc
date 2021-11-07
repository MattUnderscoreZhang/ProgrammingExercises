#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include "imdb.h"
#include <stdlib.h>

const char *const imdb::kActorFileName = "actordata";
const char *const imdb::kMovieFileName = "moviedata";

imdb::imdb(const string& directory)
{
  const string actorFileName = directory + "/" + kActorFileName;
  const string movieFileName = directory + "/" + kMovieFileName;
  
  actorFile = acquireFileMap(actorFileName, actorInfo);
  movieFile = acquireFileMap(movieFileName, movieInfo);
}

bool imdb::good() const
{
  return !( (actorInfo.fd == -1) || 
            (movieInfo.fd == -1) ); 
}

struct actor_and_file {
    string actor;
    const void* actorFile;

    actor_and_file(const string& a, const void* aF) {
        actor = a;
        actorFile = aF;
    }
};

static int cmp_actor(const void* searched_actor_and_file, const void* actor_index) {
    string actor = ((actor_and_file*)searched_actor_and_file)->actor;
    const void* actorFile = ((actor_and_file*)searched_actor_and_file)->actorFile;
    return strcmp(actor.c_str(), (char*)actorFile + *(int*)actor_index);
}

struct movie_and_cast {
    film movie;
    vector<int> cast_pointers;
};

static movie_and_cast get_movie_info(char* movie_info_pointer) {
    char* movie_name = movie_info_pointer;
    int movie_name_bytes = 0;
    while (*(movie_info_pointer + movie_name_bytes) != '\0') {
        movie_name_bytes++;
    }
    movie_name_bytes++;

    char year_offset = *(movie_info_pointer + movie_name_bytes);
    int year = 1900 + year_offset;
    int padding_offset = 0;
    if ((movie_name_bytes + 1) % 2 != 0)
        padding_offset = 1;

    short n_actors = *(short*)(movie_info_pointer + movie_name_bytes + 1 + padding_offset);
    if ((movie_name_bytes + 3 + padding_offset) % 4 != 0)
        padding_offset += 2;

    vector<int> return_cast_pointers;
    for (int i=0; i<n_actors; i++) {
        int actor_pointer = *((int*)(movie_info_pointer + movie_name_bytes + 3 + padding_offset) + i);
        return_cast_pointers.push_back(actor_pointer);
    }

    film return_movie;
    return_movie.title = string(movie_name);
    return_movie.year = year;
    movie_and_cast return_movie_and_cast;
    return_movie_and_cast.movie = return_movie;
    return_movie_and_cast.cast_pointers = return_cast_pointers;
    return return_movie_and_cast;
}

// you should be implementing these two methods right here... 
bool imdb::getCredits(const string& actor, vector<film>& films) const {
    int n_actors = ((int*)actorFile)[0];
    int* actor_indices = (int*)actorFile + 1;
    struct actor_and_file searched_actor_and_file = actor_and_file(actor, this->actorFile);
    int* actor_pointer_offset = (int*)bsearch(&searched_actor_and_file, actor_indices, n_actors, sizeof(int), cmp_actor);
    if (actor_pointer_offset == NULL)
        return false;
    else {
        char* actor_pointer = (char*)(this->actorFile) + *actor_pointer_offset; 
        int actor_name_bytes = ((actor.length() / 2) + 1) * 2; // integer division truncation and padding \0
        short n_movies = *(short*)(actor_pointer + actor_name_bytes);
        // append movies to films vector
        int* movie_pointer_offset = (int*)(actor_pointer + actor_name_bytes + 2);
        if ((actor_name_bytes + 2) % 4 != 0)
            movie_pointer_offset = (int*)((char*)movie_pointer_offset + 2);
        for (int i=0; i<n_movies; i++) {
            char* movie_info_pointer = (char*)(this->movieFile) + movie_pointer_offset[i];
            film new_movie = get_movie_info(movie_info_pointer).movie;
            films.push_back(new_movie);
        }
        return true;
    }
}

struct movie_and_file {
    film movie;
    const void* movieFile;

    movie_and_file(const film& m, const void* mF) {
        movie = m;
        movieFile = mF;
    }
};

static int cmp_movie(const void* searched_movie_and_file, const void* movie_index) {
    film movie = ((movie_and_file*)searched_movie_and_file)->movie;
    const void* movieFile = ((movie_and_file*)searched_movie_and_file)->movieFile;
    char* movie_info_pointer = (char*)(movieFile) + *(int*)movie_index;
    film compare_movie = get_movie_info(movie_info_pointer).movie;
    if (movie < compare_movie)
        return -1;
    else if (movie == compare_movie)
        return 0;
    else
        return 1;
}

bool imdb::getCast(const film& movie, vector<string>& actors) const {
    int n_movies = ((int*)movieFile)[0];
    int* movie_indices = (int*)movieFile + 1;
    struct movie_and_file searched_movie_and_file = movie_and_file(movie, this->movieFile);
    int* movie_pointer_offset = (int*)bsearch(&searched_movie_and_file, movie_indices, n_movies, sizeof(int), cmp_movie);
    if (movie_pointer_offset == NULL)
        return false;
    else {
        char* movie_info_pointer = (char*)(this->movieFile) + *movie_pointer_offset; 
        vector<int> cast_pointers = get_movie_info(movie_info_pointer).cast_pointers;
        for (int i=0; i<(int)cast_pointers.size(); i++) {
            char* actor_name = (char*)(this->actorFile) + cast_pointers[i]; 
            actors.push_back(actor_name);
        }
        return true;
    }
}

imdb::~imdb()
{
  releaseFileMap(actorInfo);
  releaseFileMap(movieInfo);
}

// ignore everything below... it's all UNIXy stuff in place to make a file look like
// an array of bytes in RAM.. 
const void *imdb::acquireFileMap(const string& fileName, struct fileInfo& info)
{
  struct stat stats;
  stat(fileName.c_str(), &stats);
  info.fileSize = stats.st_size;
  info.fd = open(fileName.c_str(), O_RDONLY);
  return info.fileMap = mmap(0, info.fileSize, PROT_READ, MAP_SHARED, info.fd, 0);
}

void imdb::releaseFileMap(struct fileInfo& info)
{
  if (info.fileMap != NULL) munmap((char *) info.fileMap, info.fileSize);
  if (info.fd != -1) close(info.fd);
}
