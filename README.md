# TMC exercise

This repo is for codes that match a input csv data to Ohio States' registered voters.
The matched data will be the input file but with one additional columns 'matched_voter_id'.

Simply run
```
python main.py
```
will download, merge, and save data

Pull the data was a challenge, the request library kept getting rejected by Cloudflare error, so I have to find an alternative solution to pull the data, which is cloudscrape

As for how the data is match, I used three columns 'name', 'year', 'zip', which are, in my opinion, enough to distinguish between different registered owners with the same name.

If we want be more accurate, we can also use columns such as 'address', but it will take more time consuming considering that are more significant amount of transformation involved.

Perhaps considering adding 'middle_name' to the match is a potentially good idea, what are the odds of two people having the exact same name, born in the same year, and actually live in the same zip code, right? Still, I think using the three columns mentioned above is enough unless we need to be extremely accurate whatever it takes.

Next step for this repo is probably creating a docker container to specify the versions of the Python libraries, and Python itself so we can make sure to reproduce the same result in the future.