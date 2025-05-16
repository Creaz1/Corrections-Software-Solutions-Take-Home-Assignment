import argparse
import csv
import sys
import json

def validInt(value):
    try:
        return int(value)
    except ValueError:
        print("Input Error: " + value + " is not a valid integer")
        sys.exit()

def validFloat(value):
    try:
        return float(value)
    except ValueError:
        print("Input Error: " + value + " is not a valid float")
        sys.exit()

parser = argparse.ArgumentParser(description="Process movie queries")

parser.add_argument("--input", type=str, help="Name of input file")
parser.add_argument("--year-after", dest="year_after", type=validInt, help="Movie made after a given year")
parser.add_argument("--year-before", dest="year_before", type=validInt, help="Movie made before a given year")
parser.add_argument("--genre", type=str, help="Genre of movie")
parser.add_argument("--rating-above", dest="rating_above", type=validFloat, help="Movie with IMDb rating above a given value")
parser.add_argument("--rating-below", dest="rating_below", type=validFloat, help="Movie with IMDb rating below a given value")
parser.add_argument("--director", type=str, help="Director of movie")
parser.add_argument("--actor", type=str, help="Actor in movie")
parser.add_argument("--runtime-more-than", dest="runtime_more_than", type=validInt, help="Movie longer in duration than a given value")
parser.add_argument("--runtime-less-than", dest="runtime_less_than", type=validInt, help="Movie shorter in duration than a given value")
parser.add_argument("--gross-min", dest="gross_min", type=validInt, help="Minimum gross revenue a movie should have")
parser.add_argument("--gross-max", dest="gross_max", type=validInt, help="Maximum gross revenue a movie should have")
parser.add_argument("--output-format", choices=["json", "csv", "text"], default="text", help="Output format: json, csv, or text")
parser.add_argument("--output-file", type=str, default="filtered_movies", help="Name of output file")
parser.add_argument("--top-10", type=str, choices=["highest-rated", "most-popular", "highest-grossing"], help="Generate Top 10 list by highest-rated, most-popular, or highest-grossing")
parser.add_argument("--genre-insights", action="store_true", help="Display average rating, gross, and runtime by genre")
parser.add_argument("--find-hidden-gems", action="store_true", help="List highly rated but low vote count movies")
parser.add_argument("--export-log", type=str, help="Export summary report to a text file")

args = parser.parse_args()

inputFile = args.input

filters = {"year_after": args.year_after, "year_before": args.year_before, "genre": args.genre, "rating_above": args.rating_above, "rating_below": args.rating_below, "director": args.director, "actor": args.actor, "runtime_more_than": args.runtime_more_than, "runtime_less_than": args.runtime_less_than, "gross_min": args.gross_min, "gross_max": args.gross_max}

def isValidMovie(movie, filters):
    try:
        yearMade = int(movie["released_year"])
    except:
        if filters["year_after"] != None or filters["year_before"] != None:
            return False
    else:
        if filters["year_after"] != None and yearMade <= filters["year_after"]:
            return False
        if filters["year_before"] != None and yearMade >= filters["year_before"]:
            return False

    if filters["genre"] != None:
        genreList = movie["genre"].split(", ")
        if filters["genre"] not in genreList:
            return False

    try:
        imdbRating = float(movie["imdb_rating"])
    except:
        if filters["rating_above"] != None or filters["rating_below"] != None:
            return False
    else:
        if filters["rating_above"] != None and imdbRating <= filters["rating_above"]:
            return False
        if filters["rating_below"] != None and imdbRating >= filters["rating_below"]:
            return False

    if filters["director"] != None:
        if movie["director"] == "" or movie["director"] != filters["director"]:
            return False

    if filters["actor"] != None:
        actorList = [movie["star_1"], movie["star_2"], movie["star_3"], movie["star_4"]]
        if filters["actor"] not in actorList:
            return False

    try:
        runtime = int(''.join(filter(str.isdigit, movie["runtime"])))
    except:
        if filters["runtime_more_than"] != None or filters["runtime_less_than"] != None:
            return False
    else:
        if filters["runtime_more_than"] != None and runtime <= filters["runtime_more_than"]:
            return False
        if filters["runtime_less_than"] != None and runtime >= filters["runtime_less_than"]:
            return False

    try:
        grossRevenue = int(''.join(filter(str.isdigit, movie["gross"])))
    except:
        if filters["gross_min"] != None or filters["gross_max"] != None:
            return False
    else:
        if filters["gross_min"] != None and grossRevenue < filters["gross_min"]:
            return False
        if filters["gross_max"] != None and grossRevenue > filters["gross_max"]:
            return False

    return True

filteredMovieList = []

try:
    with open(inputFile, 'r', encoding='utf-8') as file:
        csvreader = csv.DictReader(file)
        for row in csvreader:
            if isValidMovie(row, filters):
                filteredMovieList.append(row)
except FileNotFoundError:
    print("File Error: Input file not found.")
    sys.exit()

print("\nFiltered Movie List:\n")
for movie in filteredMovieList:
    for attribute, value in movie.items():
        print(attribute + ": " + value)
    print("\n")

output_format = args.output_format
output_file = args.output_file

if not output_file.endswith("." + output_format if output_format != "text" else ".txt"):
    print("Warning: Output file extension does not match specified output format.")

try:
    if output_format == "json":
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(filteredMovieList, f, indent=4)
    elif output_format == "csv":
        if filteredMovieList:
            with open(output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=filteredMovieList[0].keys())
                writer.writeheader()
                writer.writerows(filteredMovieList)
    elif output_format == "text":
        with open(output_file, "w", encoding="utf-8") as f:
            for movie in filteredMovieList:
                for attribute, value in movie.items():
                    f.write(attribute + ": " + str(value) + "\n")
                f.write("\n")
    print("\nFiltered movies saved to " + output_file)
except Exception as e:
    print("Error writing output file: " + str(e))

def to_int(value):
    try:
        return int(value.replace(",", ""))
    except:
        return None

def to_float(value):
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        value = value.lower().replace(',', '')
        try:
            return float(value)
        except ValueError:
            return None
    return None

def extract_runtime(value):
    try:
        return int(''.join(filter(str.isdigit, value)))
    except:
        return None

if args.export_log:
    export_lines = []

    if args.top_10:
        key = ""
        if args.top_10 == "highest-rated":
            key = "imdb_rating"
        elif args.top_10 == "most-popular":
            key = "no_of_votes"
        elif args.top_10 == "highest-grossing":
            key = "gross"

        export_lines.append("Top 10 Movies by " + args.top_10.replace("-", " ").title() + ":\n")

        sorted_movies = sorted(filteredMovieList, key=lambda x: to_float(x.get(key, 0)) or 0, reverse=True)
        for i, movie in enumerate(sorted_movies[:10]):
            export_lines.append(str(i+1) + ". " + movie.get("series_title", "N/A") + " (" + movie.get("released_year", "N/A") + ") - " + key + ": " + movie.get(key, "N/A"))
        export_lines.append("\n")

    if args.genre_insights:
        genre_stats = {}
        for movie in filteredMovieList:
            genres = movie["genre"].split(", ")
            rating = to_float(movie.get("imdb_rating", "0"))
            gross = to_int(movie.get("gross", "0"))
            runtime = extract_runtime(movie.get("runtime", "0"))

            for genre in genres:
                if genre not in genre_stats:
                    genre_stats[genre] = {"ratings": [], "gross": [], "runtime": []}
                if rating is not None:
                    genre_stats[genre]["ratings"].append(rating)
                if gross is not None:
                    genre_stats[genre]["gross"].append(gross)
                if runtime is not None:
                    genre_stats[genre]["runtime"].append(runtime)

        export_lines.append("Genre-Based Insights:\n")
        for genre, stats in genre_stats.items():
            avg_rating = sum(stats["ratings"]) / len(stats["ratings"]) if stats["ratings"] else 0
            avg_gross = sum(stats["gross"]) / len(stats["gross"]) if stats["gross"] else 0
            avg_runtime = sum(stats["runtime"]) / len(stats["runtime"]) if stats["runtime"] else 0
            export_lines.append("Genre: " + genre)
            export_lines.append("  Avg Rating: " + str(round(avg_rating, 2)))
            export_lines.append("  Avg Gross: $" + str(round(avg_gross)))
            export_lines.append("  Avg Runtime: " + str(round(avg_runtime)) + " min\n")

    if args.find_hidden_gems:
        export_lines.append("Hidden Gems (IMDb Rating >= 8.0 and Votes <= 50000):\n")
        for movie in filteredMovieList:
            rating = to_float(movie.get("imdb_rating", "0"))
            votes = to_int(movie.get("no_of_votes", "0"))
            if rating is not None and votes is not None and rating >= 8.0 and votes <= 50000:
                export_lines.append("- " + movie.get("series_title", "N/A") + " (" + movie.get("released_year", "N/A") + ") - Rating: " + str(rating) + ", Votes: " + str(votes))
        export_lines.append("\n")

    try:
        with open(args.export_log, "w", encoding="utf-8") as log_file:
            for line in export_lines:
                log_file.write(line + "\n")
        print("Export log saved to " + args.export_log)
    except Exception as e:
        print("Failed to write export log: " + str(e))