# YouTubeTranscriptAPI Imports
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, VideoUnavailable, TooManyRequests, \
    TranscriptsDisabled, NoTranscriptAvailable
from youtube_transcript_api.formatters import TextFormatter

# Flask Imports
from flask import Flask, jsonify, request, send_from_directory, render_template, redirect

# NLTK Imports
import nltk

# Other Imports
import os

# Summarizer Import (Our Another File: summarizer.py)
from summarizer import gensim_summarize, spacy_summarize, nltk_summarize, sumy_lsa_summarize, sumy_luhn_summarize, \
    sumy_text_rank_summarize

# Waitress Import for Serving at Heroku
from waitress import serve


def create_app():
    # Creating Flask Object and returning it.
    app = Flask(__name__)

    # "Punkt" download before nltk tokenization
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print('Downloading punkt')
        nltk.download('punkt', quiet=True)

    # "Wordnet" download before nltk tokenization
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        print('Downloading wordnet')
        nltk.download('wordnet')

    # "Stopwords" download before nltk tokenization
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        print('Downloading Stopwords')
        nltk.download("stopwords", quiet=True)

    # Processing Function for below route.
    @app.route('/summarize/', methods=['GET'])
    def transcript_fetched_query():
        # Getting argument from the request
        video_id = request.args.get('id')  # video_id of the YouTube Video
        percent = request.args.get('percent')  # percentage of the summary
        choice = request.args.get('choice')  # summarization choice

        # Checking whether all parameters exist or not
        if video_id is not None and percent is not None and choice is not None:
            # every parameter exists here: checking validity of choice
            choice_list = ["gensim-sum", "spacy-sum", "nltk-sum", "sumy-lsa-sum", "sumy-luhn-sum", "sumy-text-rank-sum"]
            if choice in choice_list:
                # Choice Correct Proceeding with Transcript Fetch and its Summarization
                try:
                    # Using Formatter to store subtitles properly.
                    formatter = TextFormatter()
                    transcript = YouTubeTranscriptApi.get_transcript(video_id)
                    formatted_text = formatter.format_transcript(transcript).replace("\n", " ")

                    # Summarizing Formatted Text based upon the request's choice
                    if choice == "gensim-sum":
                        summary = gensim_summarize(formatted_text,
                                                   percent)  # Gensim Library for TextRank Based Summary.
                    elif choice == "spacy-sum":
                        summary = spacy_summarize(formatted_text,
                                                  percent)  # Spacy Library for frequency-based summary.
                    elif choice == "nltk-sum":
                        summary = nltk_summarize(formatted_text,
                                                 percent)  # NLTK Library used for frequency-based summary.
                    elif choice == "sumy-lsa-sum":
                        summary = sumy_lsa_summarize(formatted_text,
                                                     percent)  # Sumy for extractive summary using LSA.
                    elif choice == "sumy-luhn-sum":
                        summary = sumy_luhn_summarize(formatted_text,
                                                      percent)  # Sumy Library for TF-IDF Based Summary.
                    elif choice == "sumy-text-rank-sum":
                        summary = sumy_text_rank_summarize(formatted_text,
                                                           percent)  # Sumy for Text Rank Based Summary.
                    else:
                        summary = None

                    # Returning Result
                    response_list = [
                        {'fetched_transcript': formatted_text,
                         'processed_summary': summary,
                         'length_original': len(formatted_text),
                         'length_summary': len(summary)}
                    ]
                    return jsonify(success=True,
                                   message="Subtitles for this video was fetched and summarized successfully.",
                                   response=response_list), 200

                # Catching Exceptions
                except VideoUnavailable:
                    return jsonify(success=False, message="VideoUnavailable: The video is no longer available.",
                                   response=None), 400
                except TooManyRequests:
                    return jsonify(success=False,
                                   message="TooManyRequests: YouTube is receiving too many requests from this IP."
                                           " Wait until the ban on server has been lifted.",
                                   response=None), 500
                except TranscriptsDisabled:
                    return jsonify(success=False, message="TranscriptsDisabled: Subtitles are disabled for this video.",
                                   response=None), 400
                except NoTranscriptAvailable:
                    return jsonify(success=False,
                                   message="NoTranscriptAvailable: No transcripts are available for this video.",
                                   response=None), 400
                except NoTranscriptFound:
                    return jsonify(success=False, message="NoTranscriptAvailable: No transcripts were found.",
                                   response=None), 400
                except:
                    return jsonify(success=False,
                                   message="Some error occurred."
                                           " Contact the administrator if it is happening too frequently.",
                                   response=None), 500
            else:
                return jsonify(success=False,
                               message="Invalid Choice: Please create your request with correct choice.",
                               response=None), 400

        elif video_id is None:
            # video_id parameter doesn't exist in the request.
            return jsonify(success=False,
                           message="No Video ID Passed. "
                                   "Please check that you have added id in your request correctly.",
                           response=None), 400
        elif percent is None:
            # percent parameter doesn't exist.
            return jsonify(success=False,
                           message="No Percentage Value given in request. "
                                   "Please check whether your request is correct.",
                           response=None), 400
        else:
            # choice parameter for the summary type doesn't exist here.
            return jsonify(success=False,
                           message="No Choice given in request. " "Please request along with your choice correctly.",
                           response=None), 400

    @app.route('/favicon.ico')
    # Favicon is stored in static folder, browsers request it to display along with tab title.
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                                   mimetype='image/vnd.microsoft.icon')

    @app.route('/')
    def root_function():
        # Since we have two end points inside root, we are closing root endpoint.
        # Displaying root.html to the end user
        return render_template('root.html')

    @app.route('/web/')
    def summarizer_web():
        # We are at web.html, online input boxes are there to summarize the given video URL.
        # Displaying web.html to the end user
        return render_template('web.html')

    @app.route('/api/')
    def summarizer_api_info_route():
        # Since we have two end points inside root, we are closing root endpoint.
        # Displaying root.html to the end user
        return render_template('api.html')

    @app.before_request
    def enforce_https_in_heroku():
        if 'DYNO' in os.environ:
            if request.headers.get('X-Forwarded-Proto') == 'http':
                url = request.url.replace('http://', 'https://', 1)
                code = 301
                return redirect(url, code=code)

    return app


if __name__ == '__main__':
    # Running Flask Application
    # app.run()
    flask_app = create_app()
    serve(flask_app, host='0.0.0.0', port=80, debug=False, url_scheme='https')
