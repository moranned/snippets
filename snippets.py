import sys
import logging
import argparse
import psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")

def put(name, snippet, hidden=False):
    """
    Store a snippet with an associated name.
    Returns the name and the snippet
    """
    with connection, connection.cursor() as cursor:
      try:
        cursor.execute("insert into snippets values (%s, %s, %s)",(name, snippet, hidden))
      except psycopg2.IntegrityError as e:
        connection.rollback()
        cursor.execute("update snippets set message=%s where keyword=%s and hidden=%s",(snippet, name, hidden))
    logging.debug("Snippet stored successfully.")
    return name, snippet, hidden

def get(name):
    """Retrieve the snippet with a given name.
    If there is no such snippet gracefully return a message
    Returns the snippet.
    """
    with connection, connection.cursor() as cursor:
      cursor.execute("select message from snippets where keyword=%s", (name,))
      result = cursor.fetchone()
    logging.debug("Snippet retrieved successfully")
    if not result:
      return 'There is no snippet with the name: %s' %name
    else:
      return result[0]

def show_catalog(hidden=False):
  with connection, connection.cursor() as cursor:
    cursor.execute("select keyword from snippets where hidden=%s",(hidden,))
    result = cursor.fetchall()
    return result

def search_catalog(name,flag):
  name = '%' + name + '%'
  with connection, connection.cursor() as cursor:
    cursor.execute("select keyword from snippets where keyword like %s and hidden=False",(name,))
    result = cursor.fetchall()
    return result
    
def main():
  logging.info("Constructing Parser")
  parser = argparse.ArgumentParser(description="Store and retrieve a snippet of text")
  subparsers = parser.add_subparsers(dest="command", help="Available commands")
  # Subparser for the put command
  logging.debug("Constructing put subparser")
  put_parser = subparsers.add_parser("put", help="Store a snippet")
  put_parser.add_argument("name", help="The name of the snippet")
  put_parser.add_argument("snippet", help="The snippet text")
  get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
  get_parser.add_argument("name", help="The name of the snippet")
  catalog_parser = subparsers.add_parser("catalog", help="Show all keywords")
  search_parser = subparsers.add_parser("search", help="Search for keywords")
  search_parser.add_argument("name", help="Keyword to search for")
  parser.add_argument("--unhide", help="Show hidden keywords", action="store_true")
  parser.add_argument("--hide", help="Store snippets as hidden", action="store_true")
  arguments = parser.parse_args(sys.argv[1:])
  arguments = vars(arguments)
  command = arguments.pop("command")
  unhide = arguments.pop("unhide")
  hide = arguments.pop("hide")
  
  if command == "put":
      name,snippet,hidden = put(arguments['name'],arguments['snippet'],hide)
      print ("Stored {!r} as {!r} with hidden equals {!r}".format(snippet, name, hidden))
  
  if command == "get":
    snippet = get(**arguments)
    print ("Retrieved snippet: {!r}".format(snippet))
  
  if command == "catalog":
    for keyword in show_catalog(unhide):
      print keyword[0]

  if command == "search":
    search_catalog(**arguments)
    for keyword in search_catalog(**arguments):
      print keyword[0]
  
if __name__ == '__main__':
  main()