# YouTube Transcript Summarizer: Flask Back-End Repository
### This back-end also hosts the web version of the online summarizer [here](https://ytsum.herokuapp.com/web/).
**YouTube Video Transcript Summarization over Flask:** This back-end uses Flask framework to receive API calls from the client and then respond with the summarized text response. This API can work only on those YouTube videos which have well-formatted closed captions in it. The same backend also hosts a web version of the Summarizer to make those API calls in simple way and show the output within the webpage.

![](/readme_images/image_cover_f.png)

*Pre-requisite Knowledge:* YouTube is an American free to use online video sharing and social media platform launched in February 2005. It is currently one of the biggest video platforms where its users watch more than 1 billion hours of videos every day.\
Closed captions are the text derived from the video which are intended for adding more details (such as dialogues, speech translation, non-speech elements) for the viewer. They are widely used to understand video without understanding its audio.

*Use case Scenario:* YouTube has very large number of videos which has transcripts. Summarization would be especially helpful in the cases where videos are longer in length and different parts might have varying importance. In this sense, Summarization of the video might be useful in saving the viewer’s time. It will help in improving user productivity since they will focus only on the important text spoken in video. 

![](/readme_images/demonstration.gif)

## Aim
By our project, we would be building functionality for summarizing those YouTube videos in which captions are added by their owner, to generate a summarized text response through various summarization techniques. The Summarizer should be accessible to the end user in an easy way, and that is why we would be generating summary in many accessible ways.\
We will be hosting a Flask back-end server which will receive a **`GET Request`** along with the `YouTube Video Id`, selected `Algorithm Choice`, and required `ratio` of the summarized response. This server will ensure *avoiding the summarization processing at user end*.\
This approach also has scope of improving algorithm directly later, users have no need to update at their ends, thus saving users’ resources as well.
The client could be accessing this API from anywhere (say a Chrome extension) which will request our server. We would be also creating a web version of this summarizer as well as a GUI Program based on Tkinter with Command Line Integration that asks for required data and process on it directly.
In this way, we would make summarizer accessible in many ways, and reducing user’s time and effort to get the text summary on the basis of their request.

### More information about the backend
There are four endpoints:
* `/` (Root Endpoint): It displays a general purpose introductory webpage and also provides links to web summarizer and API information. You can go to this point [here](https://ytsum.herokuapp.com/).
* `/web/` (Web Summarizer Endpoint): It displays the web version of the summarizer tool. The webpage has input elements and a summarize button. After clicking summarize, the `API` is called and the response is displayed to the user. You can go to this endpoint by directly clicking [here](https://ytsum.herokuapp.com/web/).
* `/api/` (API Description Endpoint): The webpage at this endpoint describes basic API information in case you would like to use it. Feel free to learn and use our API in your projects.
You can go to this endpoint by directly clicking [here](https://ytsum.herokuapp.com/api/).
* `/summarize/` (API Endpoint): This endpoint is for **API purposes only**. That is why, the response type of the **`GET Request`** at this endpoint is in JSON format.\
More details about using our API is written below:
  
  #### Sending request to our API
  The query (or API request) to our backend can be made using following three variables only. They are:
  * **`id`** : Video ID of the YouTube Video. Each video has its own unique ID in its URL.\
  For example, *9No-FiEInLA* is the Video ID in *https​://www​.youtube​.com/watch?v=9No-FiEInLA.*
  * **`choice`** : Algorithm Choice for the summarizing the Transcript. There are only six accepted values in this variable.\
  These choices are written along with algorithm names as follows:
    * `gensim-sum` : Text Rank Algorithm Based using Gensim
    * `spacy-sum` : Frequency Based Approach using Spacy.
    * `nltk-sum` : Frequency Based Summarization using NLTK.
    * `sumy-lsa-sum` : Latent Semantic Analysis Based using Sumy.
    * `sumy-luhn-sum` : Luhn Algorithm Based using Sumy.
    * `sumy-text-rank-sum` : Text Rank Algorithm Based using Sumy.
  * **`percent`** : The percentage is used to present the summary in approx. `X% lines` of the available transcript.
  
  These values in the query to our server can be used in following manner:
  ```
  https://ytsum.herokuapp.com/summarize/?id=your-video-id&percent=your-percent&choice=your-summary-choice
  ```
  
  More similar details about sending API request can also be found [here](https://ytsum.herokuapp.com/api/).
 
  #### Receiving request from our API
  Once you send a successful API request, our server will take that request and process it. After successful processing, the server will send back the relevant response to the made request. The response sent is always in the **`JSON Format`** and very much similar to below snippet:
  ```json
  {
    "message": "Subtitles for this video was fetched and summarized successfully.",
    "response": {
        "length_original": 32792,
        "length_summary": 6087,
        "processed_summary": "Your summary will be here :)",
        "sentence_original": 438,
        "sentence_summary": 43
    },
    "success": true
  }
  ```
  There might be cases, where summarization couldn't be performed (Say subtitles are not available, or subtitles are badly formatted). In this case, the JSON response would be simiiar like this:
  ```json
  {
    "message": "TranscriptsDisabled: Subtitles are disabled for this video.",
    "response": null,
    "success": false
  }
  ```

### More information about the front-end
The image below shows the front-end of the web version of the summarizer.

![](/readme_images/sample_browser_ui.jpg)

As before mentioned, this back-end repository also hosts the web summmarizer. This basic HTML+CSS+JS webpage takes input which is required for making API requests. The webpage is self explanatory. Once you click on summarize button, the JS script makes an API request to the back-end. Once the request is completed, the received response is displayed to the user in the formatted mannner.

#### Feel free to improve this back-end, add comments and ask any queries if you have any.

##### The back-end uses an undocumented part of the YouTube API, which is called by the YouTube web-client. So there is no guarantee that it would stop working tomorrow, if they change how things work. In case that happens, I will do my best to make things work again as soon as possible if that happens. So if it stops working, let me know!
##### This is not an official tool from YouTube. I have built this package for my final year project. 
