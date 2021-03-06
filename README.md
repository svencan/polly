# polly

**polly** is a minimal remote voting system.

Meet namesake Polly: http://www.nichtlustig.de/toondb/020302.html

## Persistence

Data is persisted in JSON files.

### Folder hierarchy

This hierarchy description comes with examples. If a list item has a trailing slash, it is a folder, otherwise it is a file.

Files are always appended by the timestamp of creation, e.g. `emma_1470245559`. The timestamps are also included in the files themselves.

  - event/
    - lk16-2/
      - description_1470247500
      - question/ 
        - säa1/
          - vote/
            - emma_1470247700
            - emma_1470247100
            - mary_1470247150
          - opening_1470247500
          - closure_1470247800
        - säa2/
      - accreditation/
        - in/
          - emma_1470247600
          - emma_1470247000
          - mary_1470247000
        - out/
          - emma_1470247300
    - lk17-1/
    - lk17-2/
  - member/
    - emma_1470245559
    - emma_1470246882
    - mary_1470245559

## Endpoints

`baseurl` is a placeholder for the actual base URL. Each endpoint corresponds to a folder or a file.

`GET`ting something from an endpoint corresponding to a folder will return its description, and a list of references to folders or files.

`GET`ing something from an endpoint corresponding to a file will return the most recent version of that file.

`POST`ing something to an endpoint corresponding to a folder will create a new file in that folder.

If you try anything else you'll have to walk the plank. Or at least deal with ``405 Method Not Allowed``.

### Overview: `baseurl`

`GET` returns general information of the system and references to events.

Example:
```json
{
    "version": "1.33.7",
    "event": [
        "baseurl/event/lk16-2",
        "baseurl/event/lk17-1",
        "baseurl/event/lk17-2",
    ]
}
```

### Event: `baseurl/event/event-id`

`GET` returns the latest description of an event, references to the questions within that event, and references to accredited members.

Example:
`GET baseurl/event/lk16-2`
```json
{
    "id": "lk16-2",
    "url": "baseurl/event/lk16-2",
    "timestamp": "1470247500",
    "title": {
        "short": "LK16-2",
        "long": "Uerdentlechen Landeskongress 2016-2"
    },
    "question": [
        "baseurl/event/lk16-2/question/säa1",
        "baseurl/event/lk16-2/question/säa2"
    ],
    "accreditation": [
        "baseurl/event/lk16-2/accreditation/emma",
        "baseurl/event/lk16-2/accreditation/mary"
    ]
}
```

`POST` creates a new folder (if inexistent) and timestamped description file in that folder.

Example:
`POST baseurl/event/lk16-2`
```json
{
    "id": "lk16-2",
    "title": {
        "short": "LK16-2",
        "long": "Uerdentlechen Landeskongress 2016-2"
    }
}
```

### Question: `baseurl/event/event-id/question/question-id`

`GET` returns the description of question, its opening times (if any), whether it is open (calculated), and its votes (if any) and an additional votecount (calculated).

TBD: Only aye/nay/abstention as options?

Example:
```json
{
    "id": "lk16-2/question/säa1",
    "url": "baseurl/event/lk16-2/question/säa1",
    "timestamp": "1470247500",
    "title": {
        "short": "SÄA1 Prokuratiounen",
        "long": "SÄA1: Prokuratioune sinn doof"
    },
    "open": true,
    "opening": [
        "baseurl/event/lk16-2/question/säa1/opening",
        "baseurl/event/lk16-2/question/säa1/closure",
    ],
    "vote": [
        "baseurl/event/lk16-2/question/säa1/vote/emma",
        "baseurl/event/lk16-2/question/säa1/vote/mary"
    ],
    "votecount": {
        "votes": 2,
        "aye": 1,
        "nay": 1,
        "abstention": 0
    }
}
```

### Opening: `baseurl/event/event-id/question/question-id/opening-type`

`POST` creates a new timestamped opening or closure (depending on opening-type) in the question.

Example 1:
```json
{
    "type": "opening",
}
```

Example 2:
```json
{
    "type": "opening",
}
```

### Members: `baseurl/member`

`GET` returns members.

Example:
```json
{
    "count": "2",
    "member": [
        "baseurl/member/emma",
        "baseurl/member/mary"
    ]
}
```

### Member: `baseurl/member/member-id`

`GET` returns the latest member file

Example:
```json
{
    "id": "emma",
    "title": {
        "short": "emma",
        "long": "Emma Schmit"
    }
}
```

`POST` creates a new timestamped member file in that folder.

Example:
`POST baseurl/member/emma`
```json
{
    "id": "emma",
    "title": {
        "short": "emma",
        "long": "Emma Müller"
    }
}
```