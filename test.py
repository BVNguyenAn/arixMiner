from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/api/verify', methods=['GET'])
def verify():
    key = request.args.get('key')
    # Bạn có thể validate key ở đây (ví dụ: kiểm tra trong database)
    # Hoặc luôn trả về thành công cho mọi key
    return jsonify({
        "success": True,
        "status": "active",
        "message": "Xác thực thành công",
        "expires_at": (datetime.utcnow() + timedelta(days=365*10)).isoformat() + "Z",
        "server_time": datetime.utcnow().isoformat() + "Z",
        "type": "vip"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)