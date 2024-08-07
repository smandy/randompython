import base64
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error

#These are the secrets etc from Fitbit developer
OAuthTwoClientID = "23B7K7"
ClientOrConsumerSecret = "2e52f4e0ec078a03d28097a18692b765"

#This is the Fitbit URL
TokenURL = "https://api.fitbit.com/oauth2/token"

#I got this from the first verifier part when authorising my application
AuthorisationCode = "ddec633e6c46c0704b0ff7513eaa0b9ffc5ffb87"

#Form the data payload
BodyText = {'code' : AuthorisationCode,
            'redirect_uri' : 'http://www,giigke,cin/',
            'client_id' : OAuthTwoClientID,
            'grant_type' : 'authorization_code'}

BodyURLEncoded = urllib.parse.urlencode(BodyText)
print(BodyURLEncoded)

#Start the request
req = urllib.request.Request(TokenURL,BodyURLEncoded)

#Add the headers, first we base64 encode the client id and client secret with a : inbetween and create the authorisation header
req.add_header('Authorization', bytes('Basic ' + base64.b64encode(OAuthTwoClientID + ":" + ClientOrConsumerSecret), 'utf-8'))

req.add_header('Content-Type', 'application/x-www-form-urlencoded')

#Fire off the request
try:
  response = urllib.request.urlopen(req)
  FullResponse = response.read()
  print(("Output >>> " + FullResponse))
except urllib.error.URLError as e:
  print((e.code))
  print((e.read()))
