from datetime import datetime

import Utils


def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    user = Utils.login(username,password)
    if user is None:
        print("Login Unsucessful. Please Try again. \n")
        return None
    return user

def signup():
    username = input("Enter a new username: ")
    password = input("Enter a new password: ")
    email = input("Enter your email: ")
    name = input("Enter your name: ")
    # Check if the username already exists
    Utils.signup(username, password, email, name)

def view_list(title, user_list):
    pass

def view_someones_movie_list(users):
    username_to_view = input("Enter the username of the person whose movie list you want to view: ")
    pass

def add_movie(user: Utils.User):
    title = input("Enter the title of the movie: ")
    genre = input("Enter the genre of the movie: ")
    release_date = input("Enter the release Date of the movie: ")
    runtime = input("Enter the runtime of the movie (in minutes): ")
    Utils.validate_movie_data(title, release_date, runtime, genre, user.username)
    Utils.add_movie(title, release_date, runtime, genre, user.username)


def delete_movie(user):
    movie_name = input("Enter the name of the movie you want to delete: ")
    movie_id = Utils.search_movie_id_by_name(movie_name)
    Utils.delete_movie(user, movie_id)

def movie_submenu(user: Utils.User):
    while True:
        print("\nMovie Menu:")
        print("1. Add Movie")
        print("2. Delete Movie")
        print("3. List Movies added by you")
        print("4. Back to Main Menu")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            add_movie(user)
        elif choice == '2':
            delete_movie(user)
        elif choice == '3':
            Utils.list_movies_added_by_user(user.username)

        elif choice == '4':
            print("Returning to the main menu.")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")

def view_movie_id_by_name(user):
    movie_name = input("Enter the name of the movie you want to view: ")
    movie_ids = Utils.search_movies_by_name_substring(movie_name)

def add_review(user):
    movie_id = int(input("Enter the ID of the movie you want to review: "))
    stars = int(input("Enter the number of stars (1-5): "))
    description = input("Enter your review: ")

    Utils.add_review(movie_id, user.username,stars, description)

def edit_review(user):
    movie_id = int(input("Enter the ID of the movie whose review you want to edit: "))
    stars = int(input("Enter the new number of stars (1-5): "))
    description = input("Enter your new review: ")
    Utils.update_review(user.username,movie_id, stars, description)

def delete_review(user):
    movie_id = input("Enter the ID of the movie whose review you want to delete: ")
    Utils.delete_review(user.username,movie_id)


def review_submenu(user):
    while True:
        print("\nReview Menu:")
        print("1. Add Review")
        print("2. Edit Review")
        print("3. Delete Review")
        print("4. Find Movie by Name")
        print("5. View all your reviews")
        print("6. Back to Main Menu")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            add_review(user)
        elif choice == '2':
            edit_review(user)
        elif choice == '3':
            delete_review(user)
        elif choice == '4':
            view_movie_id_by_name(user)
        elif choice == '5':
            Utils.view_user_reviews(user.username)
        elif choice == '6':
            print("Returning to the main menu.")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")

def add_to_favorite(user):
    movie_id = int(input("Enter the ID of the movie you want to add to your favorites: "))
    list_id = input("Enter the id of the list you want to add this movie to: ")
    Utils.add_movie_to_favorite_list(user.username, list_id, movie_id)

def delete_from_favorite(user):
    movie_id = input("Enter the ID of the movie you want to remove from your favorites: ")
    list_title = input("Enter the ID of the list you want to add this movie to: ")
    Utils.delete_movie_from_favorite_list(user.username,list_title, movie_id)
    print("Movie removed from your favorite list.")

def view_favorite_lists(user):
    Utils.view_user_favorite_lists(user.username)

def view_movies_in_favorite_list():
    list_id = input("Enter the listID you want to view: ")
    Utils.view_movies_in_favorite_list(list_id)

def create_favorite_list(user):
    list_title = input("Enter the title for the new favorite list: ")

    # Call the function to add a new favorite list to the database
    Utils.add_favorite_list(user.username, list_title)

def delete_favorite_list(user):
    list_id = input("Enter the ID of the favorite list you want to delete: ")

    # Call the function to delete a favorite list from the database
    Utils.delete_favorite_list_by_id(user.username, list_id)


def favorite_submenu(user):
    while True:
        print("\nFavorite Menu:")
        print("1. Create a new Favorite List")
        print("2. Delete a Favorite List")
        print("3. View Favorite lists")
        print("4. View Movies in a Favorite List")
        print("5. Add a movie to a Favorite (by ID)")
        print("6. Delete a movie from a Favorite (by ID)")
        print("7. Back to Main Menu")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            create_favorite_list(user)
        elif choice == '2':
            delete_favorite_list(user)
        elif choice == '3':
            view_favorite_lists(user)
        elif choice == '4':
            view_movies_in_favorite_list()
        elif choice == '5':
            add_to_favorite(user)
        elif choice == '6':
            delete_from_favorite(user)
        elif choice == '7':
            print("Returning to the main menu.")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 3.")

def add_to_watch_list(user):
    movie_id = int(input("Enter the ID of the movie you want to add to your watch list: "))
    Utils.add_movie_to_watched(user.username, movie_id)
    print("Movie added to your watch list.")

def watch_list_submenu(user):
    while True:
        print("\nWatch List Menu:")
        print("1. Add to Watch List")
        print("2. View Watch List")
        print("3. Back to Main Menu")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            add_to_watch_list(user)
        elif choice == '2':
            Utils.view_watched_list(user.username)
        elif choice == '3':
            print("Returning to the main menu.")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 3.")

def main_menu(current_user, users):
    while True:
        print(f"\nWelcome, {current_user.username}!")
        print("1. Movies")
        print("2. Reviews")
        print("3. Favorite List")
        print("4. Watch List")
        print("5. Log Out")
        print("6. View Someone's Movie List")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            movie_submenu(current_user)

        elif choice == '2':
            review_submenu(current_user)

        elif choice == '3':
            favorite_submenu(current_user)

        elif choice == '4':
            watch_list_submenu(current_user)

        elif choice == '5':
            print("Logging out. Goodbye!")
            return

        elif choice == '6':
            view_someones_movie_list(users)

        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    users = []
    current_user = None

    while True:
        print("\nWelcome to the User Interface!")
        print("1. Log In")
        print("2. Sign Up")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            current_user = login()
            print(current_user)
            if current_user is not None:
                print(f"\nLogged in as {current_user.username}.\n")
                main_menu(current_user, users)
            else:
                print("\nInvalid username or password.")

        elif choice == '2':
            signup()
            continue

        elif choice == '3':
            print("Exiting the User Interface. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter a number between 1 and 3.")