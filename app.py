import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg before importing pyplot

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, send_file, render_template
import numpy as np
import io
import base64

app = Flask(__name__)

# I am testing the funcitonality of github through this repository one to see simple changes
# Firstly I am cloning the repository
# Next will be to do my first commit after a few changes
# Note all these changes can be seen through Github commit history

# To push on to the main branch simply try this
# NOTe ONE HUGE THING When commiting got a fatal error on first step below why because you have to be in that directory when pushing
# git add .
# git commit -m "TEST"
# git push

# Function to generate the Matplotlib graph
def generate_matplotlib_graph():
    fig = Figure()
    canvas = FigureCanvas(fig)
    
    x = np.random.randn(10000)
    ax = fig.add_subplot(111)
    ax.hist(x, 100)
    ax.set_title('Normal distribution with $\mu=0, \sigma=1$')

    # Save the graph to a BytesIO buffer
    buffer = io.BytesIO()
    canvas.print_figure(buffer, format='png')
    buffer.seek(0)
    
    return buffer

# Route to display the Matplotlib graph and code
@app.route('/')
def display_graph_and_code():
    # Generate the graph
    buffer = generate_matplotlib_graph()
    
    # Get the source code of the generate_matplotlib_graph function
    graph_code = """
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import io

fig = Figure()
canvas = FigureCanvas(fig)

x = np.random.randn(10000)
ax = fig.add_subplot(111)
ax.hist(x, 100)
ax.set_title('Normal distribution with $\\mu=0, \\sigma=1$')

buffer = io.BytesIO()
canvas.print_figure(buffer, format='png')
buffer.seek(0)

return buffer
    """
    
    # Encode the image to base64 for display in HTML
    encoded_image = base64.b64encode(buffer.read()).decode('utf-8')

    return render_template('index.html', graph=encoded_image, graph_code=graph_code)

if __name__ == '__main__':
    app.run(debug=True)
