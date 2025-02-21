from flask import Blueprint, render_template_string, request

bp = Blueprint('another', __name__)

@bp.route('/another')
def another_page():
    # Get the checked boxes from the URL query string
    checked_boxes = request.args.get('checked_boxes', '')
    checked_list = checked_boxes.split(',') if checked_boxes else []

    return render_template_string('''
        <h1>TEST CHECK:</h1>
        <ul>
            {% for class in checked_list %}
                <li>{{ class }}</li>
            {% endfor %}
        </ul>
        <a href="/">Back Class Selector</a>
    ''', checked_list=checked_list)
