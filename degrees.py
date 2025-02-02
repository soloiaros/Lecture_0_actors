import csv, sys
from util import Node, QueueFrontier


names = {}
people = {}
movies = {}


def load_data(directory):
    with open(f"{directory}/people.csv", 'r', encoding='utf-8') as people_db:
        reader = csv.DictReader(people_db)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    with open(f"{directory}/movies.csv", 'r', encoding="utf-8") as movies_db:
        reader = csv.DictReader(movies_db)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    with open(f"{directory}/stars.csv", "r", encoding="utf-8") as stars_db:
        reader = csv.DictReader(stars_db)
        for row in reader:
            if row["person_id"] in people and row["movie_id"] in movies:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("No person found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("No person found.")

    path = shortest_path(source, target)
    actors_list, movies_list = zip(*path)
    actors_list = [source, *list(actors_list), target]

    if path is None:
        print("Not connected.")
    else:
        print(f"{len(path)} degrees of separation.")
        for n in range(len(movies_list)):
            print(f"{n + 1}: {name_from_id(actors_list[n], flag="person")} "
                  f"and {name_from_id(actors_list[n + 1], flag="person")}"
                  f" starred in {name_from_id(movies_list[n], flag="movie")}")


def person_id_for_name(name):
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for i in person_ids:
            print(f'IMDB ID:{people[i]["id"]}, '
                  f'Name:{people[i]["name"]}, '
                  f'Birth: {people[i]["year"]}')
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def name_from_id(id_num, flag="person"):
    if flag == "person":
        return people[id_num]["name"]
    elif flag == "movie":
        return movies[id_num]["title"]
    return None


def shortest_path(source, target):
    frontier = QueueFrontier()
    explored = set()
    cur_node = Node(parent=None, action=None, state=(source, None))
    frontier.add(cur_node)
    while True:
        if frontier.empty():
            raise Exception("No solution.")
        else:
            cur_node = frontier.remove()
            if cur_node.state[0] == target:
                actions = []
                cells = []
                while cur_node.parent is not None:
                    actions.append(cur_node.action)
                    cells.append(cur_node.state)
                    cur_node = cur_node.parent
                return cells
            else:
                explored.add(cur_node.state)
                for new_state in neighbors_for_person(cur_node.state[0]):
                    if (new_state not in explored) and not frontier.contains_state(new_state):
                        child = Node(parent=cur_node, action=None, state=new_state)
                        frontier.add(child)


def neighbors_for_person(person):
    movie_ids = people[person]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            if person_id != person:
                neighbors.add((person_id, movie_id,))
    return neighbors


if __name__ == "__main__":
    main()
