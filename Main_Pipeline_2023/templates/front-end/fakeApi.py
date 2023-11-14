from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api/v1/submit')
def submit_img():
    try:
        print("send")
        # Get query parameters from the URL
        item = request.args.get('item')
        frame = request.args.get('frame')
        session = request.args.get('session')
        print(item)
        print(frame)
        print(session)

        # Process the parameters and prepare a response
        response_data = {
            'item': item,
            'frame': frame,
            'session': session,
            'message': 'Received your request and processed it.'
        }

        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Change the port to 8080
