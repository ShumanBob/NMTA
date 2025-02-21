from flask import Flask, render_template_string, jsonify, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        checked_boxes = request.form.getlist('checkbox')
        return redirect(url_for('another.another_page', checked_boxes=','.join(checked_boxes)))
    
    return render_template_string('''
        <center><h1>NMT CSE/IT CLASSES</h1></center>
        <form method="POST" action="/">
            <!-- Your existing checkbox and form structure here -->

            <button type="submit">Submit</button>
        </form>

        <!-- Button to load classes dynamically without page refresh -->
        <button id="loadClassesBtn">Load Classes from Database</button>

        <!-- Table to display the classes -->
        <div id="classesContainer"></div>

        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>  <!-- Add jQuery -->
        <script>
            // When the button is clicked, trigger AJAX call to get classes
            $('#loadClassesBtn').on('click', function() {
                $.get('/get_classes', function(data) {
                    const classes = data.classes;
                    let containerHtml = '';
                    
                    // Group classes by their level
                    const groups = {
                        "CS FRESHMEN": [],
                        "CS SOPHOMORE": [],
                        "CS JUNIOR": [],
                        "CS SENIOR": []
                    };

                    // Loop through classes and assign to appropriate group
                    classes.forEach(function(classItem) {
                        if (classItem.level === 'Freshmen') {
                            groups['CS FRESHMEN'].push(classItem);
                        } else if (classItem.level === 'Sophomore') {
                            groups['CS SOPHOMORE'].push(classItem);
                        } else if (classItem.level === 'Junior') {
                            groups['CS JUNIOR'].push(classItem);
                        } else if (classItem.level === 'Senior') {
                            groups['CS SENIOR'].push(classItem);
                        }
                    });

                    // Generate HTML for each group
                    for (const group in groups) {
                        if (groups[group].length > 0) {
                            containerHtml += `
                                <center><h3 style="background-color: #ADD8E6;">${group}</h3></center>
                            `;
                            let rowHtml = '';
                            groups[group].forEach(function(classItem, index) {
                                // Check if it's the start of a new row (every 6 classes in a row)
                                if (index % 6 === 0 && index > 0) {
                                    containerHtml += `<div class="row">${rowHtml}</div>`;
                                    rowHtml = '';  // Reset row for next set of classes
                                }

                                // Append class to the current row
                                rowHtml += `
                                    <div class="column">
                                        <table class="top-class">
                                            <tr>
                                                <td style="background-color: ${classItem.color};">${classItem.class_code}</td>
                                                <td style="background-color: white;"><input type="checkbox" name="checkbox" value="${classItem.class_code}"></td>
                                            </tr>
                                        </table>
                                    </div>
                                `;
                            });

                            // If there are any remaining classes for the last row, add them
                            if (rowHtml) {
                                containerHtml += `<div class="row">${rowHtml}</div>`;
                            }
                        }
                    }

                    // Insert generated HTML into the page
                    $('#classesContainer').html(containerHtml);
                });
            });
        </script>

        <style>
            /* Your CSS styles remain unchanged */

            /* Adjust the layout for rows and columns */
            .row {
                display: flex;
                justify-content: center;
                margin-bottom: 20px;
                flex-wrap: wrap;  /* Allow wrapping if there are more than 6 columns */
            }

            .column {
                margin: 0 10px;
                width: calc(100% / 6 - 20px);  /* Divide the row into 6 equal columns */
            }

            /* Optional: style for the table cells */
            .top-class {
                margin-bottom: 30px;  /* Increased space between rows */
            }

            .bottom2-row, .bottom3-row, .bottom4-row, .bottom5-row, .bottom6-row {
                margin-bottom: 30px;  /* Increased space between rows */
            }
        </style>
    ''')

@app.route('/get_classes', methods=['GET'])
def get_classes():
    classes = [
        {"class_code": "CSE 101", "level": "Freshmen", "color": "#FF7F7F"},
        {"class_code": "CSE 113", "level": "Freshmen", "color": "#FF7F7F"},
        {"class_code": "CSE 122", "level": "Freshmen", "color": "#FF7F7F"},

        {"class_code": "CSE 221", "level": "Sophomore", "color": "#FF7F7F"},
        {"class_code": "CSE 222", "level": "Sophomore", "color": "#39FF14"},
        {"class_code": "CSE 213", "level": "Sophomore", "color": "#39FF14"},
        {"class_code": "CSE 241", "level": "Sophomore", "color": "#FF7F7F"},

        {"class_code": "CSE 331", "level": "Junior", "color": "#39FF14"},
        {"class_code": "CSE 325", "level": "Junior", "color": "#FF7F7F"},
        {"class_code": "CSE 353", "level": "Junior", "color": "#FF7F7F"},
        {"class_code": "CSE 326", "level": "Junior", "color": "#39FF14"},
        {"class_code": "CSE 324", "level": "Junior", "color": "#39FF14"},
        {"class_code": "CSE 342", "level": "Junior", "color": "#39FF14"},
        {"class_code": "CSE 344", "level": "Junior", "color": "#FF7F7F"},
        {"class_code": "CSE 363", "level": "Junior", "color": "#39FF14"},
        {"class_code": "CSE 382", "level": "Junior", "color": "#39FF14"},

        {"class_code": "CSE 423", "level": "Senior", "color": "#39FF14"},
    ]
    return jsonify({"classes": classes})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
