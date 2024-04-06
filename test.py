import tweepy

# Replace with your API credentials
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Keywords for incident detection
incident_keywords = ["fire", "water leak", "road collapse", "trash pile"]

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
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        process_tweet(status)

# Create stream listener and start streaming
myListener = MyStreamListener()
stream = tweepy.Stream(auth, myListener)
stream.filter(track=incident_keywords)