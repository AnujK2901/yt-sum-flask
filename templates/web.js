// Initializing Constants for use
const url_input = document.getElementById("url_input");
const summarize_button = document.getElementById("my_button");
const percent_dropdown = document.getElementById('percent-dropdown');
const choice_dropdown = document.getElementById('summary-dropdown');

const youtube_div = document.getElementById("youtube");
let text_out_main_div = document.getElementById("text_out_main");

// Button Click Listener for InitializeSummary() Function
summarize_button.addEventListener("click", initializeSummary);

// Making Summarize button disabled on start
summarize_button.disabled = true;

// Adding EventListeners on both dropdowns to enable button when both dropdowns have selected a valid choice.
percent_dropdown.addEventListener("click", buttonUpdate);
choice_dropdown.addEventListener("click", buttonUpdate);
percent_dropdown.addEventListener("onmousedown", buttonUpdate);
choice_dropdown.addEventListener("onmousedown", buttonUpdate);
percent_dropdown.addEventListener("keyup", buttonUpdate);
choice_dropdown.addEventListener("keyup", buttonUpdate);
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
        var url = url_input.value;

        var video_id = parse_youtube_video_id(url);
        var percent = percent_value.split("%")[0];
        var choice = parse_choice(choice_index);

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
                    var response_json = (result.response[0]);
                    text_out_content_element.innerHTML = "Processed Summary: " + response_json.processed_summary
                        + "<p>Characters in Original Transcript: " + response_json.length_original
                        + "<br>Characters in Summary: " + response_json.length_summary + "</p><br>";
                    text_out_content_element.style.textAlign = "justify";
                    text_out_content_element.style.textJustify = "inter-word";
                } else {
                    // We failed: Reason is already pushed to UI in process_element (response.result_message has reason)
                    text_out_content_element.innerHTML = "We failed due to above reason.";
                    text_out_content_element.style.textAlign = "center";
                }
            }).catch(error => {
                // Network issue occurred during fetch probably. Logging and sending result backs.
                console.log(error);
                process_element.innerHTML = "A network issue was encountered. Please retry.";
                // We failed to fetch: Reason is already pushed to UI in process_element (response.result_message has reason)
                text_out_content_element.innerHTML = "We failed due to above reason.";
                text_out_content_element.style.textAlign = "center";
            })
        } else {
            alert("Your Video URL is invalid.");
            url_input.value = "";
        }
    }
}

function parse_youtube_video_id(url) {
    // This function returns video id if it is a valid youtube video. Else it returns false
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
    var match = url.match(regExp);
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