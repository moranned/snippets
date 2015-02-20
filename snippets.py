import sys
import logging
import argparse
import psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")

def put(name, snippet):
    """
    Store a snippet with an associated name.
    Returns the name and the snippet
    """
    #logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    command = "insert into snippets values (%s, %s)"
    cursor.execute(command,(name,snippet))
    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet

def get(name):
    """Retrieve the snippet with a given name.
    If there is no such snippet gracefully return a message
    Returns the snippet.
    """
    #logging.error("FIXME: Unimplemented - get({!r})".format(name))
    cursor = connection.cursor()
    command = "select message from snippets where keyword = '%s'" %name
    cursor.execute(command)
    connection.commit()
    result = cursor.fetchone()
    logging.debug("Snippet retrieved successfully")
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
  arguments = parser.parse_args(sys.argv[1:])
  arguments = vars(arguments)
  print arguments
  command = arguments.pop("command")
  
  if command == "put":
    name,snippet = put(**arguments)
    print ("Stored {!r} as {!r}".format(snippet,name))
  
  if command == "get":
    snippet = get(**arguments)
    print ("Retrieved snippet: {!r}".format(snippet))
  
if __name__ == '__main__':
  main()