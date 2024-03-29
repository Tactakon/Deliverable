# **1. Introduction**

## **1.1 Purpose**

The purpose of this document is to describe the implementation details and objectives of our upcoming collaborative DJing web app - Verge.

## **1.2 Intended Audiemce**

The audience of this document is our team members, including Kirstyn Fagnani, Kinjal Rele, Derrick Hood, and John Bergin, as well as our instructor for CSC 4351 - Professor John Martin. 

## **1.3 Intended Use**

This document will allow our team to align with the work that needs to be completed with this project. With this document, we intend to refer back to it and ensure we are on task and have completed the original scope. This includes items like the design, brainstorming of features, planning durations, and measuring what can be accomplished in the amount of time we have. We will use this document to guide the future of our product while staying aligned with our initial ideas. 

## **1.4 Scope**

Verge is a seamless collaborative DJ experience that lets listeners control the music. DJs can instantly accept and relinquish control of the mix without missing a beat. As a listener, you can request your favorite song, and the DJ will see it. Whether you are a professional DJ, a weekend hobbyist, or just someone who enjoys good tunes, Verge lets everyone play a part in the mix.
<br><br>
Some features that define our product:
- Create, browse, share, and listen to playlists. 
- Your playlist can be locked or unlocked. Totally up to you what playlist you want to make public.
- If you give access to another user, they can add songs to your playlists. This requires a passcode.
- If a DJ plays live (in-person or virtually), you can quickly scan their QR code to request songs.
- As a DJ, you can set a genre before you start mixing. Songs requested that do not match the vibe will be automatically denied.
<br><br>

Many web apps on the market allow DJs to mix electronically, but we have found none that incorporate the experience we intend to. We intend to create a space where listeners can connect with their favorite DJs easily and where DJs can share their premade playlist or their music in real time. Think of a mix between Spotify, Twitch, and Social Media. We hope that Verge will allow DJs and Listeners to have a meaningful experience on both ends. 

## **1.5 Definitions and Acronyms**

The remainder of the document will use the following conventions:
- QR Code
  : Quick Response Code
- VST
  : Virtual Studio Technology
- MFA
  : Multi-Factor Authentication
<br>

In addition:
- "Listeners" will refer to a user that listens to the DJs. This is the standard user in our application. 
- "DJs" will refer to a user that is offering their music services to the listeners.

# **2. Overall Description**

## **2.1 User Needs**

Verge attempts to solve four core user problems:
1. Listeners cannot follow and connect with their favorite DJs on a single platform that will also let them know when the DJ has dropped a new mix or are live at an in-person event. 

2. Simultaneously, it is difficult for new and upcoming DJs to expand their marketability and increase their listening audience. While having the ability to grow - DJs will still be able to be in control of their mix choices. 

3. Currently, it is difficult for listeners to request songs at live events - you have to yell over loud crowds, be turned down with requesting music, make your way to the DJ in a sea of people, and so many more unfortunate situations.

4. While Spotify allows you to share playlists with others, if the playlist is locked - the person it is shared with will not be able to add any music. There is no way around this other than making the said friend a contributor on the main user's end. We have worked around this with a passcode option. With the passcode shared with friends in a private playlist, they can add music and contribute to it. 

Our targeted users need a web app that is more than watching a DJ live stream and more than listening to famous DJ's pre-recorded songs on a playlist. There are other ways to hear DJs mixes (Spotify, Twitch), but they do not offer a connection between DJs and their Listeners seamlessly. 

## **2.2 Assumptions and Dependencies**

This web app makes 3 major assumptions:
1. As covid restrictions are easing up, demand for DJs at live events is increasing. 
2. Back-to-back DJing is becoming increasingly popular as more DJs enter the industry.  To avoid overcrowding in festivals, organizers would pair DJs together.
3. Many users wish the DJ would play their favorite song, but they either don't have the opportunity to speak with the DJ or are too shy to request a song in person.

Other major dependencies:

1. Spotify’s API is a key component of our project. If Spotify is not working, our web app will not function properly.
2. There are countless tools at the disposal of a modern DJ. There are so many plugins and VST’s available that our web app must offer unique functionality to make it desirable to our user base.

# **3. System Features and Requirements**

## **3.1 Functional Requirements**

### **3.1.1 Functional Requirement 1: Login and Signup**
Description: A listener or DJ should be able to log in and sign up for Verge using their existing phone number, social media, or their email.  

Acceptance criteria:
- If visiting the web app for the first time, a modal should appear asking the listener or DJ to sign up.
- The modal should contain options to sign up via phone number, social media, or email.
- In the signup process, we will ask the user if they want to set up MFA. If not, the signup process continues as normal. If yes, we take the user through the proper MFA screens to complete the setup (text or email is their choice).
- Confirmation text/email should be sent to the listener or DJ, depending on their designated sign-in option.
- A modal to log in should appear if the listener or DJ has already signed up. 
- Listeners should be able to log in with their phone number, social media, or email when they sign in.
- MFA via email or phone is required to complete the login process.

### **3.1.2 Functional Requirement 2: Connect with DJ**
Description: Listeners should be able to follow and connect with their favorite DJs to be notified when the DJ’s new mixes are dropped. 

Acceptance criteria:
- A follow button should be next to the DJ’s profile. 
- Once the button is clicked, the DJ’s profile should be added to a list of followed DJs.
- You should have the option to remove DJs from the list.
- The DJs in the list should help the web app learn what type of music you like for recommendations.

### **3.1.3 Functional Requirement 3: Find DJs**
Description: A DJ should be able to expand their audience and find listeners that are supportive of their art to continue to create music that their listeners enjoy. 

Acceptance criteria:
- DJs should be discoverable depending on listeners' preferences and tastes.
- DJs can be browsed based on popularity, location, and genre.
- There will be a new and upcoming section for DJs to be discovered on the playlist page. 
- Similar to how you find new Youtubers on Youtube, we will have an algorithm to suggest DJs based on the listener's preferences. 

### **3.1.4 Functional Requirement 4: Invite to Playlist**
Description: A listener should be able to invite their friends to their playlists to share their favorite DJ’s new mix and connect with the music. 

Acceptance criteria:
- When viewing the playlist, there should be a button for inviting friends.
- Once the button is clicked, users should be able to opt to send the invite by email, phone number, social media, or copy the link.
- After the option is chosen, the user should be able to type the receivers number/email/username in a form.
- The user should see a send button after they have typed an input in the form. 
- Once the send button is sent, there should be a message pop up that says sent when the invite was sent successfully.
- If the invite fails to send, there should be an error message.
- After an invite is successfully sent, the invite form should go away.

### **3.1.5 Functional Requirement 5: Song Request**
Description: A listener should be able to request a song from the DJ to mix so that they can feel that they are part of the experience. 

Acceptance criteria:
- Either in a live or virtual event, the Listener can request a song.
- If the listener is in a live event, we recommend that DJs post QR codes electronically around the venue. On TVs, monitors, and if needed - printed out to be easily scanned. QR codes will be a quick and efficient way to request a song. 
- If the listener is listening virtually in their preferred location - the listener can request songs from the main listening page (mockup shown in Figma to display this functionality). 
- Regardless if Listeners are at a live or remote event, songs can be requested on the main listening page.
- The listener will navigate to Request to Queue, and type the song they want to request (as long as it falls into the DJs genre selected or if the DJ wants to have songs requested), and then the song will be added to the queue once the listener presses the “Queue” button. 
- Once the song is accepted to be queued, the song will be added to the In Queue section.
### **3.1.6 Functional Requirement 6: Live Location**
Description: If they want to, a DJ can share his live location so that his fan following can come and support him.

Acceptance criteria:
- The DJ should have the option to share their location. If the DJ chooses to share their location, the followers can see where they are performing live.
- The DJ’s followers should be alerted when the DJ goes live.
- DJs should also be discoverable based on location if they share their location with the web app.
- Listeners will be alerted when DJs are performing live close to their location as long as the listener is sharing their location with Verge.

### **3.1.7 Functional Requirement 7: Genre Restrictions**
Description: A DJ can set what genre listeners can request and have the option to not accept any requests - keeping the DJ in control of their mix. If open to requests, songs that do not match the genre they have preselected will be automatically denied, and the listener will be notified that their song does not match the genre being played.

Acceptance criteria:
- The DJ will have a toggleable option to decide whether or not the set will be restricted to a specific genre.
- Every set will display the allowed genres for the listener to see.
- In the event that the DJ has a genre restriction in place, a message will alert the user if they choose a song that does not match the allowed genres.
- The listener will be able to filter their song searches to match the DJ’s specified genre(s).
- The listener will be able to filter a list of live DJ sets based on genre.

### **3.1.8 Functional Requirement 8: Notifications**
Description: Listeners should be able to follow and connect with their favorite DJs to be notified when the DJ’s new mixes are dropped. 

Acceptance criteria:
- First-time listeners will have a pop-up box on the screen asking them if they want web app notifications.
- Listeners will be notified when their favorite DJs are live.
- Listeners will be notified when the song they requested starts playing.
- A DJ would be notified of they are invited to collaborate on a playlist.
- Listeners would get a notification if they are invited to a playlist.
- If a listener follows a DJ and the said DJ has a pre-planned mix that is an upcoming event, the listener will see the upcoming event and know when to start listening on Verge. (Think of an upcoming live event on Youtube).

## **3.2 External Interface Requirements**

See our Figma file here: https://www.figma.com/file/WU8gp8hLu8ApWYinHcOOta/Capstone-Project---Verge?node-id=203%3A1142&t=BJPjE1xq3qH9e2ga-1.

## **3.3 System Requirements**

1. Verge requires location services enabled for a DJ to share their location.
2. Every functionality of Verge will require an internet connection, preferably 4G, wifi, or stronger.

## **3.4 Nonfunctional Requirements**

1. The Layout of Verge should feel natural and intuitive for the listener. They should not have to work hard to figure out how to add a song to their DJ’s set.
2. Certain sections of Verge should reflect real-life DJ culture and tools. Someone who has never used the web app should be able to take one look at the homepage and know that Verge is music-centric.
