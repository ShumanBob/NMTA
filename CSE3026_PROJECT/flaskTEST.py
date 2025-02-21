from flask import Flask, render_template_string, redirect, url_for, request
import flaskPAGETEST  # Import the second file (flaskPAGETEST.py)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the checked boxes from the form
        checked_boxes = request.form.getlist('checkbox')
        return redirect(url_for('another.another_page', checked_boxes=','.join(checked_boxes)))
    
    return render_template_string('''
        <center><h1>NMT CSE/IT CLASSES</h1></center>
        <form method="POST" action="/">

        <!---------------------------------------------------------------------------------------------------------------------------------------------------------------->
            <div class="container">
                <center><h3 style="background-color: #ADD8E6;">CS FRESHMEN</h3></center>
                <div class="top-row">
                    <table class="top-class">
                        <tr>
                            <td style="background-color: #FF7F7F;">CSE 101</td>
                            <td style="background-color: white;"><input type="checkbox" name="checkbox" value="CSE 101"></td>
                        </tr>
                    </table>
                    <table class="top-class">
                        <tr>
                            <td>CSE 113</td>
                            <td style="background-color: white;"><input type="checkbox" name="checkbox" value="CSE 113"></td>
                        </tr>
                    </table>
                </div>
                                  
                <div class="bottom2-row">
                    <table>
                        <tr>
                            <td>CSE 122</td>
                            <td style="background-color: white;"><input type="checkbox" name="checkbox" value="CSE 122"></td>
                        </tr>
                    </table>
                </div>
                                  
        <!---------------------------------------------------------------------------------------------------------------------------------------------------------------->
            <center><h3 style="background-color: #ADD8E6;">CS SOPHOMORE</h3></center>
            <div class="bottom3-row">
                <table>
                    <tr>
                        <td style="background-color: #FF7F7F;">CSE 221</td>
                        <td style="background-color: white;"><input type="checkbox" name="checkbox" value="CSE 221"></td>
                    </tr>
                </table>
                <table>
                    <tr>
                        <td style="background-color: #39FF14;">CSE 222</td>
                        <td style="background-color: white;"><input type="checkbox" name="checkbox" value="CSE 222"></td>
                    </tr>
                </table>
                <table>
                    <tr>
                        <td style="background-color: #39FF14;">CSE 213</td>
                        <td style="background-color: white;"><input type="checkbox" name="checkbox" value="CSE 213"></td>
                    </tr>
                </table>
                <table>
                    <tr>
                        <td style="background-color: #FF7F7F;">CSE 241</td>
                        <td style="background-color: white;"><input type="checkbox" name="checkbox" value="CSE 241"></td>
                    </tr>
                </table>
            </div>
                                  
        <!---------------------------------------------------------------------------------------------------------------------------------------------------------------->
            <center><h3 style="background-color: #ADD8E6;">CS JUNIOR</h3></center>
            <div class="bottom4-row">
                <table>
                    <tr>
                        <td style="background-color: #39FF14;">CSE 331</td>
                        <td style="background-color: white;"><input type="checkbox" name="checkbox" value="CSE 331"></td>
                    </tr>
                </table>
                <table>
                    <tr>
                        <td style="background-color: #FF7F7F;">CSE 325</td>
                        <td style="background-color: white;"><input type="checkbox" name="checkbox" value="CSE 325"></td>
                    </tr>
                </table>
                <table>
                    <tr>
                        <td style="background-color: #FF7F7F;">CSE 353</td>
                        <td style="background-color: white;"><input type="checkbox" name="checkbox" value="CSE 353"></td>
                    </tr>
                </table>
                <table>
                    <tr>
                        <td style="background-color: #39FF14;">CSE 326</td>
                        <td style="background-color: white;"><input type="checkbox" name="checkbox" value="CSE 326"></td>
                    </tr>
                </table>
                <table>
                    <tr>
                        <td style="background-color: #39FF14;">CSE 324</td>
                        <td style="background-color: white;"><input type="checkbox" name="checkbox" value="CSE 324"></td>
                    </tr>
                </table>
                <table>
                    <tr>
                        <td style="background-color: #39FF14;">CSE 342</td>
                        <td style="background-color: white;"><input type="checkbox" name="checkbox" value="CSE 342"></td>
                    </tr>
                </table>
                <table>
                    <tr>
                        <td style="background-color: #FF7F7F;">CSE 344</td>
                        <td style="background-color: white;"><input type="checkbox" name="checkbox" value="CSE 344"></td>
                    </tr>
                </table>
            </div>

        <!---------------------------------------------------------------------------------------------------------------------------------------------------------------->
            <div class="bottom5-row">
                <table>
                    <tr>
                        <td style="background-color: #39FF14;">CSE 363</td>
                        <td style="background-color: white;"><input type="checkbox" name="checkbox" value="CSE 363"></td>
                    </tr>
                </table>
                <table>
                    <tr>
                        <td style="background-color: #39FF14;">CSE 382</td>
                        <td style="background-color: white;"><input type="checkbox" name="checkbox" value="CSE 382"></td>
                    </tr>
                </table>
            </div>

        <!---------------------------------------------------------------------------------------------------------------------------------------------------------------->
            <center><h3 style="background-color: #ADD8E6;">CS SENIOR</h3></center>
            <div class="bottom6-row">
                <table>
                    <tr>
                        <td style="background-color: #39FF14;">CSE 423</td>
                        <td style="background-color: white;"><input type="checkbox" name="checkbox" value="CSE 423"></td>
                    </tr>
                </table>                           
            </div>    
                                                      
        <!---------------------------------------------------------------------------------------------------------------------------------------------------------------->
        </div>

        <!---------------------------------------------------------------------------------------------------------------------------------------------------------------->
        <div class="line"></div>

        <br>
        <button type="submit">Submit</button>
        </form>

        <style>
            /* Basic container styles */
            .container {
                width: 80%;
                margin: 20px auto;
                text-align: center;
            }

            /* Row styles for the top and bottom sections */
            .top-row, .bottom2-row, .bottom3-row, .bottom4-row, .bottom5-row, .bottom6-row {
                display: flex;
                justify-content: center;
                align-items: center;
            }

            /* Style for the individual class tables */
            table {
                margin: 0 10px;
                border: none;  /* Remove the border from the table */
                border-collapse: collapse;
            }

            td {
                padding: 8px 15px;
                text-align: center;
                border-radius: 25px;  /* This makes the boxes oval */
                background-color: #f0f0f0; /* A light gray background for better visibility of the oval shape */
            }

            /* Styling for the checkbox cell */
            .checkbox-cell {
                display: flex;
                justify-content: center;
            }

            /* Line connecting the top and bottom classes */
            .line {
                width: 100%;
                height: 2px;
                background-color: black;
                margin: 10px 0;
            }

            /* Styling for the top classes */
            .top-class {
                margin-bottom: 30px;  /* Increased space between rows */
            }

            .bottom2-row, .bottom3-row, .bottom4-row, .bottom5-row, .bottom6-row {
                margin-bottom: 30px;  /* Increased space between rows */
            }
        </style>

    ''')

# Register the blueprint from flaskPAGETEST.py
app.register_blueprint(flaskPAGETEST.bp)

if __name__ == '__main__':
    app.run(debug=True)
