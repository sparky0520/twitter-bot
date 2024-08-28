import tweepy

# Replace with your API credentials
from keys import consumer_key 
from keys import consumer_secret 
from keys import access_token
from keys import access_token_secret 
from keys import bearer_token

# Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Keywords for incident detection
incident_keywords = ["fire", "water leak", "road collapse", "trash pile"]

# Keywords for location detection
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
    "fire": "@DelhiFireDept",
    "water leak": "@DelhiJalBoard",
    # Add more mappings for other incidents
}

# Function to process tweets from stream
def process_tweet(tweet):
    # Extract location and incident type from tweet (replace with your NER implementation)
    location = "UNKNOWN"  # Implement location extraction
    incident_type = ""
    for keyword in incident_keywords:
        if keyword in tweet.text.lower():
            incident_type = keyword
            break

    # Check if location and incident type are valid
    if location != "UNKNOWN" and incident_type:
        # Get agency handle from mapping
        agency_handle = agency_map.get(incident_type)
        if agency_handle:
            # Construct alert message
            message = f"Alert! {incident_type} incident reported in {location}. @{agency_handle} please investigate."

            # Send tweet tagging the agency (within Twitter character limit)
            api.update_status(status=message[:280])  # Adjust for character limit

# Stream listener class
class MyStreamListener(tweepy.streaming):
    def on_status(self, status):
        process_tweet(status)

# Create stream listener and start streaming
myListener = MyStreamListener()
stream = tweepy.streaming(auth, myListener)
stream.filter(track=incident_keywords)