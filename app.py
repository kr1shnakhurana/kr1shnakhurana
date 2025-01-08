from flask import Flask, request, jsonify
import redis

app = Flask(__name__)

# Connect to Redis
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/record', methods=['POST'])
def record_temperature():
    """Endpoint to record a new temperature reading."""
    data = request.get_json()
    temperature = data.get('temperature')
    if temperature is None:
        return jsonify({'error': 'Temperature is required'}), 400
    redis_client.lpush('engine_temps', temperature)
    return jsonify({'message': 'Temperature recorded'}), 200

@app.route('/collect', methods=['GET'])
def collect_temperature():
    """Endpoint to collect the most recent average temperature."""
    temperatures = redis_client.lrange('engine_temps', 0, -1)
    if not temperatures:
        return jsonify({'error': 'No data available'}), 404
    avg_temp = sum(map(float, temperatures)) / len(temperatures)
    return jsonify({'average_temperature': avg_temp}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
