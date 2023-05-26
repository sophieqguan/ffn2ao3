## FFN to AO3 Transferrer CLI (Version 2)

---

Bare bone setup (for now):

1. Download this repo (git clone, download as zip, etc)


2. install all requirements

```
pip -r requirements.txt
```

3. Go to repo directory and run main

```
cd ffn2ao3
python3 main.py
```

4. Follow on-screen instructions to transfer work. Sample execution as below:

```
[25 May 2023, 18:09:23] Username: (Enter username)
[25 May 2023, 18:09:25] Password: (Enter password)
[25 May 2023, 18:09:28] Heading to AO3...
[25 May 2023, 18:09:30] Logged into AO3
[25 May 2023, 18:09:30] Fanfiction.net URL: (Enter ffn url)
[25 May 2023, 18:09:35] Story retrieved
[25 May 2023, 18:09:36] Creating new work.
[25 May 2023, 18:09:36] Chapter 1 retrieved
[25 May 2023, 18:09:37] 	Chapter 1 posted.
[25 May 2023, 18:09:38] Chapter 2 retrieved
[25 May 2023, 18:09:39] 	Chapter 2 posted.
[25 May 2023, 18:09:39] Chapter 3 retrieved
[25 May 2023, 18:09:40] 	Chapter 3 posted.
[25 May 2023, 18:09:40] Chapter 4 retrieved
[25 May 2023, 18:09:42] 	Chapter 4 posted.
[25 May 2023, 18:09:42] New work URL: https://archiveofourown.org/works/47429380
```

---

### Plans

- Front-End or better CLI implementation
- Add Character/Relationship tags
- Automatic tagging
