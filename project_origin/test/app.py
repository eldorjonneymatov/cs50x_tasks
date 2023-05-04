import asyncio
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
loop = asyncio.get_event_loop()
async def long_running_task():
    # Perform long-running task here...
    await asyncio.sleep(10)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # Render the "loading" template
        return render_template('/s.html')

        # Start the long-running task in the background


        # Redirect to a new page once the task is complete
        return redirect(url_for('results'))

    return render_template('/index.html')


@app.route('/s', methods=['POST', 'GET'])
def s():
    if request.method == 'GET':
        # Render the "loading" template

        # Start the long-running task in the background
        loop.run_until_complete(long_running_task())
        # Redirect to a new page once the task is complete
        return render_template('/registered.html')

    return render_template('/s.html')


@app.route('/results')
def results():
    # Render the results template
    return render_template('/results.html')
