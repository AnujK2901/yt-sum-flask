// Initializing Constants for use
const url_input = document.getElementById("url_input");
const summarize_button = document.getElementById("my_button");
const download_button = document.getElementById("download_button");
const percent_dropdown = document.getElementById('percent-dropdown');
const choice_dropdown = document.getElementById('summary-dropdown');

const youtube_div = document.getElementById("youtube");
const text_out_main_div = document.getElementById("text_out_main");
const re_summarize_element = document.getElementById('re_summarize');

// Button Click Listener for InitializeSummary() Function
summarize_button.addEventListener("click", initializeSummary);
// Button Click Listener for downloadScript() Function
download_button.addEventListener("click", downloadScript);
// Creating a dictionary to store download related info once the summary processing is complete.
const download_info = {script: "", video_id: "", video_percent: "", video_algo: ""}

// Making Summarize button disabled on start
summarize_button.disabled = true;
// Making Re-summarize element hidden at start: till summary is visible
re_summarize_element.style.display = "none";

// Adding EventListeners on both dropdowns to enable button when both dropdowns have selected a valid choice.
percent_dropdown.addEventListener("change", buttonUpdate);
choice_dropdown.addEventListener("change", buttonUpdate);
url_input.addEventListener("input", buttonUpdate);

function buttonUpdate() {
    // Checking Index of the selected element in both dropdowns: if both indexes are <=0, the choice isn't valid.
    // Also Checking if the URL Text Box is empty or not.
    summarize_button.disabled = (percent_dropdown.selectedIndex <= 0 || choice_dropdown.selectedIndex <= 0 || url_input.value.length <= 0);
}

function initializeSummary() {
    // Checking Dropdown and TextBox Validity Again Here
    if (percent_dropdown.selectedIndex > 0 || choice_dropdown.selectedIndex > 0 || url_input.value.length > 0) {

        const text_out_content_element = document.getElementById("text-out");
        const process_element = document.getElementById("current_process");

        // Getting values of both dropdowns
        let percent_value = percent_dropdown.options[percent_dropdown.selectedIndex].text;
        let choice_index = choice_dropdown.selectedIndex;

        // Storing URL of the URL present in the text box
        const url = url_input.value;

        const video_id = parse_youtube_video_id(url);
        const percent = percent_value.split("%")[0];
        const choice = parse_choice(choice_index);

        if (video_id) {
            // Making Selection Div invisible, and text output as visible.
            youtube_div.style.display = "none";
            text_out_main_div.style.display = "block";

            // https://ytsum.herokuapp.com
            // http://127.0.0.1:5000
            // Fetch request to our server. (GET request with arguments received from popup.html
            fetch("https://ytsum.herokuapp.com/summarize/?id=" + video_id +
                "&percent=" + percent + "&choice=" + choice)
                .then(response => response.json()).then(result => {
                // Result now contains the response in JSON
                // Sending result back to popup.html
                process_element.innerHTML = result.message;
                if (result.success) {
                    // If result was successfully received. Then, parse the result_response JSON
                    const response_json = (result.response);

                    // Use the values present in JSON for displaying summary.
                    text_out_content_element.innerHTML = "<b>Processed Summary:</b> " + response_json.processed_summary
                        + "<p>In your video, there are <b>" + response_json.length_original + "</b> characters in <b>" + response_json.sentence_original + "</b> sentences."
                        + "<br>The processed summary has <b>" + response_json.length_summary + "</b> characters in <b>" + response_json.sentence_summary + "</b> sentences."
                        + "</br><br>";

                    // Populating the globally created dictionary
                    download_info.script = response_json.processed_summary
                    download_info.video_id = video_id
                    download_info.video_algo = choice.replaceAll('-', '_')
                    download_info.video_percent = percent
                    // Displaying download button
                    download_button.style.display = "block";
                    // Text Beautification: Aligning Text to be justified
                    text_out_content_element.style.textAlign = "justify";
                    text_out_content_element.style.textJustify = "inter-word";
                    // Enabling re-summarize element
                    re_summarize_element.style.display = "block";
                } else {
                    // We failed: Reason is already pushed to UI in process_element (response.result_message has reason)
                    text_out_content_element.innerHTML = "We failed due to above reason.";
                    text_out_content_element.style.textAlign = "center";
                    // Enabling re-summarize element
                    re_summarize_element.style.display = "block";
                }
            }).catch(error => {
                // Network issue occurred during fetch probably. Logging and sending result backs.
                console.log(error);
                process_element.innerHTML = "A network issue was encountered. Please retry.";
                // We failed to fetch: Reason is already pushed to UI in process_element (response.result_message has reason)
                text_out_content_element.innerHTML = "We failed due to above reason.";
                text_out_content_element.style.textAlign = "center";
                // Enabling re-summarize element
                re_summarize_element.style.display = "block";
            })
        } else {
            // Alerting user that they entered wrong URL
            alert("Your YouTube video URL is invalid. Please retry.");
            url_input.value = "";
        }
    }
}

function parse_youtube_video_id(url) {
    // This function returns video id if it is a valid youtube video. Else it returns false
    const regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
    const match = url.match(regExp);
    return (match && match[7].length === 11) ? match[7] : false;
}

function parse_choice(choice_index) {
    // Return Choice string as per our server
    switch (choice_index) {
        case 1:
            return "gensim-sum";
        case 2:
            return "nltk-sum";
        case 3:
            return "spacy-sum";
        case 4:
            return "sumy-lsa-sum"
        case 5:
            return "sumy-luhn-sum";
        case 6:
            return "sumy-text-rank-sum";
    }
}

function downloadScript() {
    // Creating hyperlink element with tagName "a"
    var element = document.createElement('a');
    // Setting HREF to the script text
    element.setAttribute('href', 'data:application/octet-stream; data:text/plain;charset=utf-8,' +
        encodeURIComponent(download_info.script));
    // Setting download file name in the format "script_videoID_algo_percent.txt"
    element.setAttribute('download', "script_" +
        download_info.video_id + "_" + download_info.video_algo + "_" + download_info.video_percent + ".txt");
    // Making the hyperlink invisible and appending it to the body
    element.style.display = 'none';
    document.body.appendChild(element);

    // Clicking hyperlink to download script into text file and removing the invisible hyperlink.
    element.click();
    document.body.removeChild(element);
}