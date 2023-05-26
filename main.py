from account.ao3session import AO3Session
from util.util import lprint, validate_url
from work.work import Work


if __name__ == '__main__':
    # login
    lprint("Username: ", end="")
    USERNAME = str(input())
    lprint("Password: ", end="")
    PASSWORD = str(input())

    session = AO3Session(USERNAME, PASSWORD)
    session.new_session()
    lprint("Logged into AO3")

    # retrieve story from FFNet via API
    lprint("Fanfiction.net URL: ", end="")
    URL = input()

    while URL != 'exit':
        URL = validate_url(URL)
        while URL is None:
            lprint(f"Invalid URL. Try again: ", end="")
            URL = validate_url(input())
            continue

        work = Work(URL)
        work.retrieve_content()
        lprint("Story retrieved")

        # Run entire thing
        work_url = session.new_story(work)
        lprint(f'New work URL: {work_url}')

        print("\n")

        lprint("Fanfiction.net URL: ", end="")
        URL = input()






