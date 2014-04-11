# USA
This is a library that performs basic data gathering of US bills for the
purposes of data analysis.

## Usage

    script/run.sh {start-congress} {end-congress}

For example:

    script/run.sh 78 113

will get all the information from congresses from the 78th to the current
(113th).

Keep in mind that there is a lot of information being downloaded and analyized
so it may take anywhere from a minute to hours depending on how much information
you grab.

**WARNING:** Running `script/run.sh 1 113` will involve about a 100GB download.

## Results

Once you've run script/run.sh, you will have data/{start..stop}.json files for
each congress you've selected.

(You will also have data/{start..stop}/ directories for each congress but these
can be ignored or deleted--they are the source information.)

These JSON files are formatted like this:

    {
        "bills": [
            {"congress": int, "number": int, "year": string, "date": string,
             "sponsor": {
                "vote": "yay|nay|present|not present|null", "name": string,
                "party": "R|D|ID", "state": "XX"
             },
             "votes": {
                "yay": {"D":int?,"R":int?}, "nay": {same}, "present": {same},
                "not_voting": {same}
             }
            }, ...
        ]
    }

There are a couple of gotchas:

 - If no members of a party vote a certain way (yay, nay, present, `not_voting`)
   then the party will not have a field in votes (votes["X"] will be undefined)
 - Some sponsors do not have pary or vote information associated with them (bug
   in our source data)
 - More data may be available in some cases but don't rely on it being there!

## Credit

Original data from govtrack.us. Thanks!
