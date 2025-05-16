import argparse
import csv

parser = argparse.ArgumentParser(description="Process movie queries")

parser.add_argument("--input", type=str, help="Name of input file")
parser.add_argument("--year-after", dest="year_after", type=int, help="Movie made after a given year")
parser.add_argument("--year-before", dest="year_before", type=int, help="Movie made before a given year")
parser.add_argument("--genre", type=str, help="Genre of movie")
parser.add_argument("--rating-above", dest="rating_above", type=float, help="Movie with IMDb rating above a given value")
parser.add_argument("--rating-below", dest="rating_below", type=float, help="Movie with IMDb rating below a given value")
parser.add_argument("--director", type=str, help="Director of movie")
parser.add_argument("--actor", type=str, help="Director of movie")
parser.add_argument("--runtime-more-than", dest="runtime_more_than", type=int, help="Movie longer in duration than a given value")
parser.add_argument("--runtime-less-than", dest="runtime_less_than", type=int, help="Movie shorter in duration than a given value")
parser.add_argument("--gross-min", dest="gross_min", type=int, help="Minimum gross revenue a movie should have")
parser.add_argument("--gross-max", dest="gross_max", type=int, help="Maximum gross revenue a movie should have")

args = parser.parse_args()

inputFile = args.input
yearAfter = args.year_after
yearBefore = args.year_before
genre = args.genre
ratingAbove = args.rating_above
ratingBelow = args.rating_below
director = args.director
actor = args.actor
runtimeMoreThan = args.runtime_more_than
runtimeLessThan = args.runtime_less_than
grossMin = args.gross_min
grossMax = args.gross_max

# Header: ['series_title', 'released_year', 'certificate', 'runtime', 'genre', 'imdb_rating', 'overview', 'meta_score', 'director', 'star_1', 'star_2', 'star_3', 'star_4', 'no_of_votes', 'gross']
testMovie = ['The Dark Knight', '2008', 'UA', '152 min', 'Action, Crime, Drama', '9', 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.', '84', 'Christopher Nolan', 'Christian Bale', 'Heath Ledger', 'Aaron Eckhart', 'Michael Caine', '2303232', '534,858,444']
queryFilters = [inputFile, yearAfter, yearBefore, genre, ratingAbove, ratingBelow, director, actor, runtimeMoreThan, runtimeLessThan, grossMin, grossMax]

def isValidMovie(movie, filters):
    yearAfter = filters[1]
    if (not(movie[1].isdigit())):
        if (yearAfter != None):
            return False
    else:
        yearMade = int(movie[1])
        if (yearAfter != None) and (yearMade <= yearAfter):
            return False
    
    yearBefore = filters[2]
    if (not(movie[1].isdigit())):
        if (yearBefore != None):
            return False
    else:
        yearMade = int(movie[1])
        if (yearBefore != None) and (yearMade >= yearBefore):
            return False
    
    genreList = movie[4].split(", ")
    filterGenre = filters[3]
    if (filterGenre != None) and (filterGenre not in genreList):
        return False
    
    ratingAbove = filters[4]
    if (movie[5] == ''):
        if (ratingAbove != None):
            return False
    else:
        imdbRating = float(movie[5])
        if (ratingAbove != None) and (imdbRating <= ratingAbove):
            return False
    
    ratingBelow = filters[5]
    if (movie[5] == ''):
        if (ratingBelow != None):
            return False
    else:
        imdbRating = float(movie[5])
        if (ratingBelow != None) and (imdbRating >= ratingBelow):
            return False
    
    directorFilter = filters[6]
    if (movie[8] == '' and directorFilter != None):
        return False
    director = movie[8]
    if (directorFilter != None) and (director != directorFilter):
        return False
    
    actorFilter = filters[7]
    actorList = [movie[9], movie[10], movie[11], movie[12]]
    if (actorFilter != None) and (actorFilter not in actorList):
        return False
    
    runtimeMoreThan = filters[8]
    if (movie[3] == ''):
        if (runtimeMoreThan != None):
            return False
    else:
        runtime = int(''.join(filter(str.isdigit, movie[3])))
        if (runtimeMoreThan != None) and (runtime <= runtimeMoreThan):
            return False
    
    runtimeLessThan = filters[9]
    if (movie[3] == ''):
        if (runtimeLessThan != None):
            return False
    else:
        runtime = int(''.join(filter(str.isdigit, movie[3])))
        if (runtimeLessThan != None) and (runtime >= runtimeLessThan):
            return False
    
    grossMin = filters[10]
    if (movie[14] == ''):
        if (grossMin != None):
            return False
    else:
        grossRevenue = int(''.join(filter(str.isdigit, movie[14])))
        if (grossMin != None) and (grossRevenue < grossMin):
            return False

    grossMax = filters[11]
    if (movie[14] == ''):
        if (grossMax != None):
            return False
    else:
        grossRevenue = int(''.join(filter(str.isdigit, movie[14])))
        if (grossMax != None) and (grossRevenue > grossMax):
            return False
    
    return True
    
try:
    with open(inputFile, 'r', encoding='utf-8') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        #print("Header:", header)
        for row in csvreader:
            if isValidMovie(row, queryFilters):
                print(row)
except FileNotFoundError:
    print("Error: Input file not found.")