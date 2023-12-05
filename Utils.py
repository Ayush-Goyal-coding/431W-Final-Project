import psycopg2
from psycopg2 import sql
from common import User
import datetime
# Establish a database connection
def connect_to_db():
    conn = psycopg2.connect(
        database="moview_review_apl",
        user="postgres",
        # password="",
        host="localhost",
        port=5433
    )
    return conn

# Close the database connection
def close_connection(conn):
    conn.close()

# Signup function
def signup(username, password, email, name):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password, email, name) VALUES (%s, %s, %s, %s)",
                       (username, password, email, name))
        conn.commit()
        print("Signup successful!")
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Error: User already exists.")

    close_connection(conn)

# Login function
def login(username, password):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    user = None if user is None else User(user[0], user[1], user[2], user[3])
    close_connection(conn)
    return user

# Add movie function
def validate_movie_data(title, release_date, runtime, genre, adder_id):
    # Validate title
    if not title or len(title) > 255:
        print("Title is required and must be at most 255 characters.")

    # Validate release date
    try:
        datetime.datetime.strptime(release_date, "%d-%m-%Y")
    except ValueError:
        release_date = None
        print("Invalid release date format. Use DD-MM-YYYY.")

    # Validate runtime
    if not isinstance(runtime, int) or runtime <= 0:
        print("Runtime must be a positive integer.")

    # Validate genre
    if not genre or len(genre) > 30 or len(genre) < 3:
        print("Genre is must be at most 30 characters.")

    # Validate adder_id (assuming it's a string)
    if not adder_id or len(adder_id) > 50:
        print.append("Adder ID is required and must be at most 50 characters.")

    return

# Add movie function with automatic movie ID generation

def add_movie(title, release_date, runtime, genre, adder_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Get the largest existing movie ID
        cursor.execute("SELECT MAX(id) FROM movies")
        max_movie_id = cursor.fetchone()[0]

        # If there are no movies in the database, set the movie ID to 1, else increment the largest movie ID by 1
        new_movie_id = 1 if max_movie_id is None else max_movie_id + 1

        # Insert the new movie with the generated movie ID
        cursor.execute("INSERT INTO movies (id, title, release_date, runtime, genre, adder_id) VALUES (%s, %s, %s, %s, %s, %s)",
                       (new_movie_id, title, release_date, runtime, genre, adder_id))
        conn.commit()
        print("Movie added successfully!")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error while adding a movie: {e}")
        print("Movie addition failed.")
        print("Please check your input and try again.")

    close_connection(conn)

# Delete movie review function
def delete_review(review_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM review WHERE id = %s", (review_id,))
        conn.commit()
        print("Review deleted successfully!")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error: {e}")

    close_connection(conn)

# Delete movie function
# Delete movie function with user adder check
def search_movie_id_by_name(movie_name):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Search for the movie ID by name
        cursor.execute("SELECT id FROM movies WHERE title = %s", (movie_name,))
        movie_id = cursor.fetchone()

        if movie_id:
            print(f"Movie ID for '{movie_name}': {movie_id[0]}")
            return movie_id[0]
        else:
            print(f"No movie found with the name '{movie_name}'.")

    except psycopg2.Error as e:
        print(f"Error while searching for a movie: {e}")

    close_connection(conn)

# Example usage:
def delete_movie(user, movie_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Check if the user is the adder of the movie
        cursor.execute("SELECT adder_id FROM movies WHERE id = %s", (movie_id,))
        adder_id = cursor.fetchone()

        if adder_id and adder_id[0] == user.username:
            # User is the adder, proceed with deletion
            cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
            conn.commit()
            print("Movie deleted successfully!")
        else:
            print("Unauthorized. You are not the adder of this movie.")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error while deleting a movie: {e}")

    close_connection(conn)

def list_movies_added_by_user(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Retrieve movies added by the user
        cursor.execute("SELECT id, title, release_date, runtime, genre FROM movies WHERE adder_id = %s", (user_id,))
        movies = cursor.fetchall()

        if movies:
            print(f"Movies added by user {user_id}:")
            for movie in movies:
                print(f"ID: {movie[0]}, Title: {movie[1]}, Release Date: {movie[2]}, Runtime: {movie[3]}, Genre: {movie[4]}")
        else:
            print(f"No movies found for user {user_id}.")

    except psycopg2.Error as e:
        print(f"Error while retrieving movies: {e}")

    close_connection(conn)



def search_movies_by_name_substring(substring):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Retrieve movie IDs and names where the title contains the provided substring
        cursor.execute("SELECT id, title FROM movies WHERE LOWER(title) LIKE LOWER(%s)", ('%' + substring + '%',))
        movies = cursor.fetchall()

        if movies:
            print(f"Movies with '{substring}' in the name:")
            for movie in movies:
                print(f"ID: {movie[0]}, Title: {movie[1]}")
        else:
            print(f"No movies found with '{substring}' in the name.")

    except psycopg2.Error as e:
        print(f"Error while searching for movies: {e}")

    close_connection(conn)

# Add review function
# Add review function with getting new review ID
def add_review(movie_id, reviewer_id, stars, description):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        if not (1 <= stars <= 5):
            print("Invalid stars. Stars must be an integer between 1 and 5.")
            return

        # Get the latest review ID
        cursor.execute("SELECT MAX(id) FROM review")
        latest_review_id = cursor.fetchone()[0]

        # Calculate the new review ID
        new_review_id = 1 if latest_review_id is None else latest_review_id + 1

        # Insert the new review with the calculated review ID
        cursor.execute("INSERT INTO review (id, movie_id, reviewer_id, stars, description) VALUES (%s, %s, %s, %s, %s)",
                       (new_review_id, movie_id, reviewer_id, stars, description))
        conn.commit()
        print("Review added successfully!")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error while adding a review: {e}")

    close_connection(conn)

# Update review function
# Update review by user ID and movie ID function
def update_review(user_id, movie_id, stars, description):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        if stars is not None and not (1 <= stars <= 5):
            print("Invalid stars. Stars must be an integer between 1 and 5.")
            return

        # Check if the review exists for the specified user and movie
        cursor.execute("SELECT id FROM review WHERE reviewer_id = %s AND movie_id = %s", (user_id, movie_id))
        review_id = cursor.fetchone()

        if review_id:
            # Update the review
            cursor.execute("UPDATE review SET stars = %s, description = %s WHERE id = %s",
                           (stars, description, review_id[0]))
            conn.commit()
            print("Review updated successfully!")
        else:
            print("Review not found for the specified user and movie.")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error while updating a review: {e}")

    close_connection(conn)

# Example usage:
# update_review_by_user_movie("user1", 1, 4, "This is an excellent movie.")


# Delete review function
## Transaction with ROLL BACK
def delete_review(user_id, movie_id):
    # Delete review by user ID and movie ID function
    conn = connect_to_db()
    try:
        with conn, conn.cursor() as cursor:
            # Check if the review exists for the specified user and movie
            cursor.execute("SELECT id FROM review WHERE reviewer_id = %s AND movie_id = %s", (user_id, movie_id))
            review_id = cursor.fetchone()

            if review_id:
                # Delete the review
                cursor.execute("DELETE FROM review WHERE id = %s", (review_id[0],))
                print("Review deleted successfully!")
            else:
                print("Review not found for the specified user and movie.")

    except psycopg2.Error as e:
        print(f"Error while deleting a review: {e}")

    close_connection(conn)

    # Example usage:
    # delete_review_by_user_movie("user1", 1)


# View all reviews by a user function
def view_user_reviews(reviewer_id):
    conn = connect_to_db()
    try:
        with conn, conn.cursor() as cursor:
            # Retrieve all reviews submitted by the user
            cursor.execute("SELECT id, movie_id, stars, description FROM review WHERE reviewer_id = %s", (reviewer_id,))
            reviews = cursor.fetchall()

            if reviews:
                print(f"Reviews submitted by user {reviewer_id}:")
                for review in reviews:
                    print(f"Review ID: {review[0]}, Movie ID: {review[1]}, Stars: {review[2]}, Description: {review[3]}")
            else:
                print(f"No reviews found for user {reviewer_id}.")

    except psycopg2.Error as e:
        print(f"Error while retrieving reviews: {e}")

    close_connection(conn)

# Add movie to favorite list function
## TRANSACTION WITH ROLL BACK
# Function to add a movie to a favorite list
def add_movie_to_favorite_list(user_id, list_id, movie_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Check if the list belongs to the specified user
        cursor.execute("SELECT user_id FROM fav WHERE id = %s", (list_id,))
        list_user_id = cursor.fetchone()

        if list_user_id and list_user_id[0] == user_id:
            # Add the movie to the favorite list
            cursor.execute("INSERT INTO user_fav (list_id, movie_id) VALUES (%s, %s)", (list_id, movie_id))
            conn.commit()

            print(f"Movie with ID {movie_id} added to favorite list with ID {list_id} successfully!")

        else:
            print(f"Favorite list with ID {list_id} does not belong to the specified user {user_id}.")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error while adding a movie to the favorite list: {e}")

    finally:
        close_connection(conn)

# View all favorite lists by the user function
def view_user_favorite_lists(user_id):
    conn = connect_to_db()
    try:
        with conn, conn.cursor() as cursor:
            # Retrieve all favorite lists created by the user
            cursor.execute("SELECT id, title FROM fav WHERE user_id = %s", (user_id,))
            favorite_lists = cursor.fetchall()

            if favorite_lists:
                print(f"Favorite lists created by user {user_id}:")
                for fav_list in favorite_lists:
                    print(f"List ID: {fav_list[0]}, Title: {fav_list[1]}")
            else:
                print(f"No favorite lists found for user {user_id}.")

    except psycopg2.Error as e:
        print(f"Error while retrieving favorite lists: {e}")

    close_connection(conn)

# Example usage:
# view_user_favorite_lists("user1")





# View movies in a favorite list function
def view_movies_in_favorite_list(list_id):
    conn = connect_to_db()

    try:
        with conn, conn.cursor() as cursor:
            # Retrieve all movies in the specified favorite list
            cursor.execute("""
                SELECT m.id, m.title, m.release_date, m.runtime, m.genre
                FROM movies m
                JOIN user_fav uf ON m.id = uf.movie_id
                WHERE uf.list_id = %s
            """, (list_id,))
            movies = cursor.fetchall()

            if movies:
                print(f"Movies in favorite list with ID {list_id}:")
                for movie in movies:
                    print(f"Movie ID: {movie[0]}, Title: {movie[1]}, Release Date: {movie[2]}, Runtime: {movie[3]}, Genre: {movie[4]}")
            else:
                print(f"No movies found in favorite list with ID {list_id}.")

    except psycopg2.Error as e:
        print(f"Error while retrieving movies from the favorite list: {e}")

    close_connection(conn)


# Function to get the latest favorite list ID for a user
def get_latest_list_id():
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Retrieve the maximum list ID for the user
        cursor.execute("SELECT MAX(id) FROM fav")
        latest_list_id = cursor.fetchone()[0]

        return latest_list_id if latest_list_id is not None else 0

    except psycopg2.Error as e:
        print(f"Error while retrieving the latest list ID: {e}")
        return None

    finally:
        close_connection(conn)

# Function to add a new favorite list
def add_favorite_list(user_id, list_title):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Get the latest list ID and increment it by 1
        latest_list_id = get_latest_list_id()
        new_list_id = latest_list_id + 1

        # Insert the new favorite list
        cursor.execute("INSERT INTO fav (id, title, user_id) VALUES (%s, %s, %s)", (new_list_id, list_title, user_id))
        conn.commit()

        print(f"Favorite list '{list_title}' with ID {new_list_id} created successfully!")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error while adding a favorite list: {e}")

    finally:
        close_connection(conn)


# Function to delete a favorite list by ID
def delete_favorite_list_by_id(user_id, list_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Delete the favorite list
        cursor.execute("DELETE FROM fav WHERE id = %s AND user_id = %s", (list_id, user_id))
        conn.commit()

        print(f"Favorite list with ID {list_id} deleted successfully!")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error while deleting a favorite list: {e}")

    close_connection(conn)



# Delete movie from favorite list function
def delete_movie_from_fav(user_id, list_title, movie_id):
    conn = connect_to_db()

    try:
        with conn, conn.cursor() as cursor:
            # Check if the favorite list exists for the user
            cursor.execute("SELECT id FROM fav WHERE title = %s AND user_id = %s", (list_title, user_id))
            fav_list_id = cursor.fetchone()

            if fav_list_id:
                # Delete the movie from the favorite list
                cursor.execute("DELETE FROM user_fav WHERE movie_id = %s AND list_id = %s",
                               (movie_id, fav_list_id[0]))
                print("Movie deleted from favorite list successfully!")
            else:
                print(f"Favorite list '{list_title}' not found for user {user_id}.")

    except psycopg2.Error as e:
        print(f"Error while deleting a movie from the favorite list: {e}")

    close_connection(conn)

# Add movie to watched list function
def add_movie_to_watched(user_id, movie_id):
    conn = connect_to_db()

    # Check if the user is logged in
    if not is_user_logged_in(user_id):
        print("Unauthorized. Please log in to add movies to your watched list.")
        close_connection(conn)
        return

    try:
        with conn, conn.cursor() as cursor:
            # Check if the movie is already in the watched list
            cursor.execute("SELECT * FROM watched WHERE user_id = %s AND movie_id = %s",
                           (user_id, movie_id))
            existing_entry = cursor.fetchone()

            if not existing_entry:
                # Add the movie to the watched list
                cursor.execute("INSERT INTO watched (user_id, movie_id) VALUES (%s, %s)",
                               (user_id, movie_id))
                print("Movie added to watched list successfully!")
            else:
                print("Movie is already in the watched list.")

    except psycopg2.Error as e:
        print(f"Error while adding a movie to the watched list: {e}")

    close_connection(conn)

# View all movies in the watched list function
def view_watched_list(user_id):
    conn = connect_to_db()
    try:
        with conn, conn.cursor() as cursor:
            # Retrieve all movies in the watched list for the user
            cursor.execute("""
                SELECT m.id, m.title, m.release_date, m.runtime, m.genre
                FROM movies m
                JOIN watched w ON m.id = w.movie_id
                WHERE w.user_id = %s
            """, (user_id,))
            movies = cursor.fetchall()

            if movies:
                print(f"Movies in watched list for user {user_id}:")
                for movie in movies:
                    print(f"Movie ID: {movie[0]}, Title: {movie[1]}, Release Date: {movie[2]}, Runtime: {movie[3]}, Genre: {movie[4]}")
            else:
                print(f"No movies found in the watched list for user {user_id}.")

    except psycopg2.Error as e:
        print(f"Error while retrieving movies from the watched list: {e}")

    close_connection(conn)

