from flask import Flask, url_for, request, render_template
from PIL import Image
from heapq import nlargest
import ast
import json
import scripts.evaluate_image

application = Flask(__name__, static_folder="static/", template_folder="template/")
emoji_dict = {
    "Angry": ["🤬", "😠", "😾", "😡", "🤬", "😒"],
    "Bank": ["🏢", "🏦", "🏨"],
    "Fitness": ["🚲", "🚴", "🚴"],
    "Book": ["📚", "📘", "📕", "📗", "🖊", "🤓", "✏"],
    "Car": ["🚗", "⛽", "🚐", "🛵", "🚘", "🏎", "🚙"],
    "Electronics": ["💻", "🖥", "💽", "📱", "⌨", "🤓", "💿", "📡", "📺", "🖱"],
    "Happy": ["😄", "😸", "😀", "😁", "🤗", "🤣", "😇", "😊", "☺"],
    "Hotel": ["🏢", "🏦", "🏨"],
    "Money": ["💰", "🏦", "💵", "💳", "💲", "💸", "🤑", "🎰", "🛍"],
    "Nature": ["⛰", "🥾", "🍁", "🗻", "🏞", "🏔", "🌄", "🌋"],
    "Relieved": ["😌", "🤗", "😔", "😇", "😟", "😥"],
    "Sad": ["😢", "😿", "😥", "🥺", "😭"],
    "Sick": ["🤢", "🤮", "🤒", "🤕", "🤧"],
    "Singing": ["🧑", "‍🎤", "🎤", "🎸", "🎶", "🎹", "🎵", "🎼"],
    "Swimming": ["🏊", "🏊", "🏊"],
    "Theatre": ["🎭"],
}
background_color = [
    "AliceBlue",
    "Aqua",
    "Bisque",
    "Beige",
    "LemonChiffon",
    "MediumTurquoise",
]


@application.route("/json_statistics/<my_stats>")
def encoded_dict(my_stats):
    try:
        my_stats = ast.literal_eval(my_stats)
    except ValueError as e:
        my_stats = {
            "You may attempt to create your own json output using valid json formatting": "however please avoid doing this as the system is not designed to be an API yet"
        }
    my_stats = json.dumps(my_stats)
    my_stats = json.loads(my_stats)
    return my_stats


@application.route("/", methods=["GET", "POST"])
def main_entry():
    if request.method == "POST":
        img = request.files["user_img"]
        check = verify_image(img)
        if check == False:
            return render_template(
                "index.html",
                value="Hey, unfortunately that filetype cannot be assessed, try a different one!",
                file_types="most image files are acceptable, for example .png,.jpg,.gif are all fine to use",
                emoji_dict=emoji_dict,
                emoji_keys=[*emoji_dict],
                color=background_color,
            )
        result_dict = scripts.evaluate_image.load_img(img)
        top_three = nlargest(3, result_dict, key=result_dict.get)

        return render_template(
            "model_evaluation.html",
            emoji=top_three,
            all_results=result_dict,
            emoji_dict=emoji_dict,
            emoji_keys=[*emoji_dict],
            color=background_color,
        )
    elif request.method == "GET":
        return render_template(
            "index.html",
            value="Upload an Image and see what the model can tell!",
            file_types="most image files are acceptable, for example .png,.jpg,.gif are all fine to use",
            emoji_dict=emoji_dict,
            emoji_keys=[*emoji_dict],
            color=background_color,
        )
    else:
        return "You've found the hidden exit! No seriously, this isn't a valid path try heading back a few pages"


@application.errorhandler(404)
@application.route("/<path:dummy>")
def handle_unknown_paths(e):
    return render_template(
        "index.html",
        value="Unfortunately, there is no other path except for '\\', sorry!",
        file_types="most image files are acceptable, for example .png,.jpg,.gif are all fine to use",
        emoji_dict=emoji_dict,
        emoji_keys=[*emoji_dict],
        color=background_color,
    )


def verify_image(chosen_file):
    try:
        Image.open(chosen_file)
    except Exception as e:
        return False
    return True


if __name__ == "__main__":
    application.run()
