import mechanicalsoup
from util import parser
from datetime import datetime as dt

from util.util import lprint


class AO3Session:
    # urls
    _ARCHIVE_URL = "https://archiveofourown.org"
    _LOGIN_URL = f"{_ARCHIVE_URL}/users/login"
    DASHBOARD_URL = ""

    # properties
    username = ""
    password = ""
    session = ""

    # states
    logged_in = False

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.DASHBOARD_URL = f"{self._ARCHIVE_URL}/users/{self.username}"

    def new_session(self):
        lprint("Heading to AO3...")

        # login information:
        user_info = {
            "user[login]": self.username,
            "user[password]": self.password,
        }
        self.session = mechanicalsoup.StatefulBrowser()
        self.session.open(self._LOGIN_URL)
        form = self.session.select_form('form')
        form.set_input(user_info)
        self.session.submit_selected()

        # Confirm logged in: browser should be at User Dashboard
        if self.session.url == self.DASHBOARD_URL: self.logged_in = True
        else: raise Exception('Failed to log in.')

    def _fetch_new_work_url(self):
        if not self.logged_in: raise Exception('Please login first.')

        try:
            # go to Dashboard to retrieve latest work
            self.session.open(self.DASHBOARD_URL)
        except:
            raise Exception('Failed to go to Dashboard.')

        soup = self.session.page()
        work_url = ""

        for line in soup:
            header = line.find_all('div', {'class': 'header module'})
            if header is not None:
                for h in header:
                    element = h.find_all('h4', {'class': 'heading'})
                    for e in element:
                        work_url += e.find('a')['href']
                    break
            break
        return work_url

    def _new_chapter(self, link, story, chapter_num):
        new_ch_url = f'{link}/chapters/new'
        chapter = story.get_chapter(chapter_num)
        try: self.session.open(new_ch_url)
        except: raise Exception(f'Failed to add a new chapter [Chapter {chapter_num}].')

        form = self.session.select_form('form', 1)
        form.set('chapter[title]', chapter.title)
        form.set('chapter[content]', chapter.content)
        form.choose_submit("post_without_preview_button")
        self.session.submit_selected()
        lprint(f"\tChapter {chapter_num} posted.")

        return 0

    def new_story(self, work):
        if not work.f_cached: raise Exception('No story found.')

        # new work
        url = f"{self._ARCHIVE_URL}/works/new"
        try:
            # create new work
            self.session.open(url)
            form = self.session.select_form('form', 1)
        except:
            raise Exception('Failed to create new work.')
        lprint('Creating new work.')

        form.set('work[rating_string]', work.work_meta['rating'])
        # default to no archive warnings, since ffnet's rating is rather vague
        default_warning = "No Archive Warnings Apply"
        form.set('work[archive_warning_strings][]', default_warning)

        # might have multiple fandoms (crossover)
        fandoms = parser.parse_multi_tags(work.work_meta['fandoms'])
        form.set('work[fandom_string]', fandoms)

        # default category is Gen (if your work is not gen, you should change it manually)
        form.set('work[category_strings][]', "Gen")

        # AO3 tags  (all other metadata not covered in other parts of the form go here)
        tags = parser.parse_multi_tags(work.work_meta['tags'])
        form.set('work[freeform_string]', tags)

        form.set('work[title]', work.work_meta['title'])
        form.set('work[summary]', work.work_meta['summary'])
        form.set('work[language_id]', work.work_meta['language'])

        # set original published date
        date, month, year = dt.utcfromtimestamp(int(work.work_meta['publish_date'])).strftime('%d %B %Y').split(" ")
        form.set('work[backdate]', 1)
        form.set('work[chapter_attributes][published_at(3i)]', int(date))
        form.set('work[chapter_attributes][published_at(2i)]', str(month))
        form.set('work[chapter_attributes][published_at(1i)]', int(year))

        # post chapter 1 first, so we can retrieve new work url
        ch1 = work.get_chapter(1)
        form.set('work[chapter_attributes][content]', ch1.content)

        # check if the work has multiple chapters: if yes, set chapter title and total chapters
        if work.work_meta['chapters'] > 1:
            form.set('chapters-options-show', 1)
            form.set('work[wip_length]', int(work.work_meta['chapters']))
            form.set('work[chapter_attributes][title]', str(ch1.title))

        form.choose_submit("post_button")
        self.session.submit_selected()
        lprint("\tChapter 1 posted.")

        # retrieve new work url from browser confirmation
        new_work_url = '/'.join(map(str, self.session.url.split("/")[:-2]))

        # post additional chapters, if exist
        if work.work_meta['chapters'] > 1:
            for i in range(2, int(work.work_meta['chapters']) + 1):
                self._new_chapter(new_work_url, work, i)

        # TODO: mark work as complete/incomplete based on metadata extracted

        # return new work's url
        return new_work_url
