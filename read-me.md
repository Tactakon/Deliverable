# How to run the application
Go to https://developer.spotify.com/dashboard/ and login with Spotify account. From here, click create an app and fill out the required fields. Once your app is created, make a .env file with variables named SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET corresponding to your client ID and client secret on the app dashboard.
# Spotify API
## Basics
+ There are two separate services that we will need to achieve our goals in Verge
	+ Spotify Web API
	+ Spotify Web Playback SDK
+ Both require authentication which is tied to the developers Spotify account. The Web Playback SDK in particular requires a premium account to be utilized properly.
+ The Web API will return JSON when called upon and we can interact with it similarly to our homework assignments that dealt with API calls. The documentation includes:
	+ A guide for creating a search function (less work for us)
	+ Syntax for every type of endpoint that we would be seeking whether it is song, album, or artist
	+ A guide for pulling album covers
	+ A specific set of rules for what we can do with API data. They are very particular about the use                                                 of their logo and color scheme. We also must display album covers and song data in a specific way as well (no cropping or modulation of any kind allowed)
+ The Web Playback SDK is where things become less familiar.
	+ It allows song playback of a song inside of our 3rd party application
	+ We can use data from our API calls to play the specific song we want
	+ It can be displayed inside a square window
+ We are not permitted to crop album covers, so the circular design from the mockups may have to be adjusted 
+ Spotify already has sample code for importing the play button as well as buttons for previous track/next track
	+ You can not fast forward or rewind a track outside of the Spotify App
	+ Volume must be adjusted programmatically as a parameter in the SDK call
+ There is a method for interacting with Spotify playlists. This includes the ability to like, share, follow or make a playlist private (while granting access to contributors of your choosing). While this perfectly fits the description of our goal for verge, every Verge user would also need to have a Spotify account and be signed in. This also means playlist data would be stored on 
+ The Web Playback SDK acts as a “device” on the associated Spotify account of the developer similarly to how a Playstation, computer, or phone will show up on your account if you are signed in on those devices. We will need to do some testing to determine if this will prevent multiple users from listening simultaneously. It may also mean that we will require every user to sign in to Spotify regardless of whether or not we want them to do that.
## Resources
+ [Reference for API endpoints](https://developer.spotify.com/documentation/web-api/reference/#/)
+ [Syntax for Web Playback SDK](https://developer.spotify.com/documentation/web-playback-sdk/reference/)
+ [Example projects with open source code](https://developer.spotify.com/community/showcase/open-source/)

**Python Libraries**
+ [spotipy](https://github.com/spotipy-dev/spotipy)
+ [tekore](https://pypi.org/project/tekore/)


