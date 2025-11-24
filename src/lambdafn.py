from flask import Flask, render_template, request, jsonify
import boto3
import re

app = Flask(__name__)

s3 = boto3.client('s3')

# -------------------------
# VALIDATION HELPERS
# -------------------------

def validate_bucket_name(name):
    pattern = r'^[a-z0-9]([a-z0-9-]{1,61}[a-z0-9])?$'
    return bool(re.match(pattern, name))

def bucket_exists(bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
        return True
    except:
        return False


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/transfer', methods=['POST'])
def transfer_file():
    data = request.json
    source_bucket = data.get('source_bucket')
    dest_bucket = data.get('dest_bucket')
    key = data.get('key')

    # Validation
    if not validate_bucket_name(source_bucket):
        return jsonify({"status": "error", "message": "Invalid source bucket name"}), 400

    if not validate_bucket_name(dest_bucket):
        return jsonify({"status": "error", "message": "Invalid destination bucket name"}), 400

    if not bucket_exists(source_bucket):
        return jsonify({"status": "error", "message": "Source bucket does not exist"}), 404

    if not bucket_exists(dest_bucket):
        return jsonify({"status": "error", "message": "Destination bucket does not exist"}), 404

    try:
        copy_source = {'Bucket': source_bucket, 'Key': key}
        s3.copy(copy_source, dest_bucket, key)
        
        return jsonify({"status": "success", "message": "File transferred successfully!"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
