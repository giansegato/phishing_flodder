# Phishing Flodder

After a friend of mine had been targeted by a phishing attack, I decided to make this Python script: It floods the phishing endpoint with thousands of seemingly valid usernames and passwords, just to annoy the dams phishers. 

Best case scenario, it makes invalid the whole dataset they  collected. Worst case scenario, they can still split the data I artificially generated from the genuine one (using complex regex, cross-checking the IP sending the requests, or analysing the traffic peak time) but still – I made it so that it can be quite a pain in the ass to recover the data.

## Room for improvement

- using a parallelized queue in combination with proxies can overcome the IP cross-check countermeasure
- sending a different number of requests in different times can help overcome the traffic-time analysis

## How I generated the usernames

I googled `email list inurl:"pastebin"`. Among the first results, there was a list of emails scraped somewhere. The usernames are that list of emails, just without the domain. So, basically `gian@example.com` becomes just `gian`.

The purpose is to have a list that can be as close to a real username as possible, in order to make quite difficult any kind of post processing that could tamper our effort of making the phished data utterly unusable.

(I renamed the file to a generic `users.txt` so that this repo won't be found because of that specific file)

## How I generated the passwords

I downloaded a list of the top 10,000 most used passwords. The final list is generated as follows:

- the whole top 10K list
- the whole top 10K list, plus a random string between 0 and 3 characters that has 100% probability to contain at least a number, and 20% probability to contain at least a symbol
- 10K synthetically generated passwords (between 4 and 14 characters long, 50% probability to contain at least a number, 20% probability to contain at least a symbol

The final list is then shuffled, and for each username there's a randomly associated password. Even knowing the aforementioned algorithm, it's still impossible to make a regex / an educated guess at what password is artificially coming from this script, and what password is actually a legit one coming from a victim.

## How you can edit the script in order to target your own phisher
Take the phishing endpoint, switch Chrome's inspector, and go to the `Network` tab. Make sure you have the flag `Preserve log` checked, because it's quite possible that the form will redirect to the legit website after capturing the credentials.

Put into the phishing form some __random__ data, and record the request. Right-click on it, and then `Copy > Copy as cURL`. Paste the copied text into [this awesome tool](https://curl.trillworks.com/), and adjust the method `make_the_call` accordingly.

Please, make sure you don't override the setting of the headers' field "User-Agent": it could be quite easy to recover the legit data if the whole flodding has been made by a single user agent.

## License

GNU GPL v3.