import tweepy # Downgraded to v3.10.0

consumer_key = "mwVc9zQGm4RVYXe2aqHVZ6iyT"
consumer_secret = "gpDGqMZvPfO9u6qnlqgTDtHXVXv6qntvGNdSsS8ZqQmNEjm7gZ"
access_token = "1324319741998104576-07IGlcSaDaWMIfqRhrSQzJMkU9ci9G"
access_token_secret = "k6B5zc1MHAg60rHQbhx4yqF30IA0j5cGUOuMmDSkaIDN1"

# Connect Bot to Twitter API - With this tweepy is now fully set up
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Keywords for incident detection
incident_keywords_map = {
    "fire": [
        "fire breaks out",
        "fire tender",
        "control fire",
        "gutted in fire",
        "fire broke out",
        "fire call",
        "fire incident",
        "engulfed in a fire",
        "engulfed in fire",
        "forest fire"
    ],
    "water leak": [
        "water leakage",
        "water pipeline leakage",
        "water pipe leakage",
        "leakage in water pipe"
    ],
    "road damaged": [
        "road damaged",
        "roads damaged",
        "damaged road",
        "damaged roads",
        "pothole"
    ],
    "building collapse": [
        "building collapse"
    ],
    "trash pile": [
        "trash is piling up",
        "trash piling up",
        "garbage is piling up",
        "garbage piling up",
        "waste is piling up",
        "waste piling up"
    ],
    "tree collapse": [
        "tree collapse",
        "cause trees to fall",
        "tree fall",
        "uprooting of trees"
    ]
}

# All possible reporting locations in Delhi
location_keywords = [
    "new delhi",
    "central delhi",
    "east delhi",
    "north delhi",
    "north east delhi",
    "north west delhi",
    "south delhi",
    "south east delhi",
    "south west delhi",
    "west delhi",
    "rajouri garden",
    "punjabi bagh",
    "janakpuri",
    "tilak nagar",
    "patel nagar",
    "dwarka",
    "palam",
    "mandi house",
    "moolchand",
    "central secretariat",
    "vasant vihar",
    "najafgarh",
    "dabri",
    "lajpat nagar",
    "defence colony",
    "sarita vihar",
    "kalkaji",
    "govindpuri",
    "hauz khas",
    "saket",
    "greater kailash",
    "vasant kunj",
    "defence colony",
    "rohini",
    "pitampura",
    "lok kalyan marg",
    "shalimar bagh",
    "ashok vihar",
    "wazirpur",
    "yamuna vihar",
    "bikaji kama place",
    "nehru place",
    "netaji subash place",
    "jhilmil",
    "karkarduma",
    "dilshad garden",
    "shahdara",
    "nand nagri",
    "seelampur",
    "civil lines",
    "kashmere gate",
    "okhla",
    "model town",
    "tis hazari",
    "pitampura",
    "mangolpuri",
    "kanjhawala",
    "india gate",
    "red fort",
    "qutub minar",
    "lotus temple",
    "pragati maidan",
    "narela",
    "race course",
    "malviya nagar",
    "sarojni nagar",
    "vinobapuri",
    "samaypur badli",
    "shalimar bagh",
    "wazirabad",
    "india gate",
    "rashtrapati bhavan",
    "parliament house",
    "diplomatic enclave",
    "khan market",
    "preet vihar",
    "mayur vihar",
    "shahdara",
    "gandhi nagar",
    "krishna nagar",
    "connaught place",
    "chandni chowk",
    "daryaganj",
    "paharganj",
    "karol bagh",
    "ring road",
    "mahatma gandhi road",
    "outer ring road",
    "inner ring road",
    "nh44",
    "nh48",
    "nh9",
    "delhi-gurgaon expressway",
    "delhi-noida direct flyway",
    "barapullah elevated road",
    "akshardham flyover",
    "mehrauli-gurgaon road",
    "delhi-meerut expressway",
    "noida-greater noida expressway",
    "chhatarpur road",
    "mathura road",
    "aurobindo marg",
    "bhairon marg",
    "dr. zakir hussain marg",
    "nelson mandela marg",
    "bahadur shah zafar marg",
    "gt karnal road"
]

# Mapping of incidents to agencies
agency_map = {
    "fire": "@DelFireService",
    "water leak": "@DelhiJalBoard",
    "road damaged": "@DelhiPwd @MCD_Delhi",
    "trash pile": "@MCD_Delhi",
    "building collapse": "@DelFireService",
    "tree collapse": "@MCD_Delhi"
}

# Function to process tweets from stream
def process_tweet(tweet):
    # Extract location and incident type from tweet (replace with your NER implementation)
    location = "UNKNOWN"  # Implement location extraction
    for keyword in location_keywords:
        if keyword in tweet.text.lower():
            location = keyword
            break
    incident_types = []
    for keyword in incident_keywords:
        if keyword in tweet.text.lower():
            keys = find_keys(incident_keywords_map, keyword)
            incident_types.extend(keys)
            break

    # Check if location and incident types are valid
    if location != "UNKNOWN" and incident_types:
        # Get agency handle from mapping
        agency_handles = [agency_map.get(incident_type) for incident_type in incident_types]
        agency_handles = [handle for handle in agency_handles if handle]  # Remove None values

        if agency_handles:
            # Construct alert messages
            messages = [f"Alert! {incident_type} incident reported in {location}. {handle} please investigate."
                        for incident_type, handle in zip(incident_types, agency_handles)]

            # Send tweets tagging the agencies (within Twitter character limit)
            for message in messages:
                api.update_status(status=message[:280])  # Adjust for character limit

#Find key from dictionary from value inside it
def find_keys(dictionary, target_value):
    keys = []
    for key, value_list in dictionary.items():
        if target_value in value_list:
            keys.append(key)
    return keys

# Stream listener class
class MyStreamListener(tweepy.Stream):

    def on_status(self, status):
        process_tweet(status)

# Create stream listener and start streaming
myListener = MyStreamListener(auth, process_tweet)
myListener.filter(track=incident_keywords_map)
