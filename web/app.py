# imageghost v3.0 - web dashboard
# flask-based web interface running on localhost

import os
import sys
import json
import threading
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, session
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

# add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scrubber import ImageScrubber
from core.crypto import ImageCrypto
from core.secure_delete import SecureDelete
from core.formats import check_format
from core.logger import get_logger
from core.config import get_config

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()
app.config['UPLOAD_FOLDER'] = '/tmp/imageghost_uploads'
app.config['OUTPUT_FOLDER'] = '/tmp/imageghost_outputs'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max

socketio = SocketIO(app, cors_allowed_origins="*")

# ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

logger = get_logger('web', verbose=True)
config = get_config()

# active jobs tracker
active_jobs = {}
job_counter = 0
job_lock = threading.Lock()


class WebLogger:
    """logger that emits to websocket"""
    def __init__(self, job_id):
        self.job_id = job_id

    def info(self, msg):
        socketio.emit('log', {'job_id': self.job_id, 'level': 'info', 'message': msg})

    def success(self, msg):
        socketio.emit('log', {'job_id': self.job_id, 'level': 'success', 'message': msg})

    def error(self, msg):
        socketio.emit('log', {'job_id': self.job_id, 'level': 'error', 'message': msg})

    def warning(self, msg):
        socketio.emit('log', {'job_id': self.job_id, 'level': 'warning', 'message': msg})


def create_job(job_type, params):
    """create new job and return job id"""
    global job_counter
    with job_lock:
        job_counter += 1
        job_id = f"job_{job_counter}"
        active_jobs[job_id] = {
            'id': job_id,
            'type': job_type,
            'status': 'pending',
            'progress': 0,
            'total': 0,
            'params': params,
            'results': {}
        }
        return job_id


def update_job_status(job_id, status=None, progress=None, total=None, results=None):
    """update job status and emit to websocket"""
    if job_id not in active_jobs:
        return

    if status:
        active_jobs[job_id]['status'] = status
    if progress is not None:
        active_jobs[job_id]['progress'] = progress
    if total is not None:
        active_jobs[job_id]['total'] = total
    if results:
        active_jobs[job_id]['results'] = results

    socketio.emit('job_update', active_jobs[job_id])


def run_scrub_job(job_id, input_files, output_dir, options):
    """run scrubbing job in background"""
    try:
        update_job_status(job_id, status='running', total=len(input_files))

        scrubber = ImageScrubber(verbose=False)
        results = {'success': [], 'failed': []}

        for idx, file_path in enumerate(input_files):
            try:
                filename = os.path.basename(file_path)
                output_path = os.path.join(output_dir, f"clean_{filename}")

                success, msg = scrubber.scrub_image(file_path, output_path)

                if success:
                    results['success'].append(filename)
                    socketio.emit('log', {
                        'job_id': job_id,
                        'level': 'success',
                        'message': f"cleaned: {filename}"
                    })
                else:
                    results['failed'].append(filename)
                    socketio.emit('log', {
                        'job_id': job_id,
                        'level': 'error',
                        'message': f"failed: {filename}"
                    })

                update_job_status(job_id, progress=idx + 1)

            except Exception as e:
                results['failed'].append(os.path.basename(file_path))
                socketio.emit('log', {
                    'job_id': job_id,
                    'level': 'error',
                    'message': f"error processing {os.path.basename(file_path)}: {str(e)}"
                })

        update_job_status(job_id, status='completed', results=results)
        socketio.emit('log', {
            'job_id': job_id,
            'level': 'success',
            'message': f"completed: {len(results['success'])} success, {len(results['failed'])} failed"
        })

    except Exception as e:
        update_job_status(job_id, status='failed', results={'error': str(e)})
        socketio.emit('log', {
            'job_id': job_id,
            'level': 'error',
            'message': f"job failed: {str(e)}"
        })


def run_encrypt_job(job_id, input_files, output_dir, password):
    """run encryption job in background"""
    try:
        update_job_status(job_id, status='running', total=len(input_files))

        crypto = ImageCrypto(verbose=False)
        results = {'success': [], 'failed': []}

        for idx, file_path in enumerate(input_files):
            try:
                filename = os.path.basename(file_path)
                output_path = os.path.join(output_dir, f"{filename}.enc")

                if crypto.encrypt_file(file_path, output_path, password):
                    results['success'].append(filename)
                    socketio.emit('log', {
                        'job_id': job_id,
                        'level': 'success',
                        'message': f"encrypted: {filename}"
                    })
                else:
                    results['failed'].append(filename)
                    socketio.emit('log', {
                        'job_id': job_id,
                        'level': 'error',
                        'message': f"failed to encrypt: {filename}"
                    })

                update_job_status(job_id, progress=idx + 1)

            except Exception as e:
                results['failed'].append(os.path.basename(file_path))
                socketio.emit('log', {
                    'job_id': job_id,
                    'level': 'error',
                    'message': f"error: {str(e)}"
                })

        update_job_status(job_id, status='completed', results=results)

    except Exception as e:
        update_job_status(job_id, status='failed', results={'error': str(e)})


def run_decrypt_job(job_id, input_files, output_dir, password):
    """run decryption job in background"""
    try:
        update_job_status(job_id, status='running', total=len(input_files))

        crypto = ImageCrypto(verbose=False)
        results = {'success': [], 'failed': []}

        for idx, file_path in enumerate(input_files):
            try:
                filename = os.path.basename(file_path)
                output_name = filename.replace('.enc', '')
                output_path = os.path.join(output_dir, output_name)

                if crypto.decrypt_file(file_path, output_path, password):
                    results['success'].append(filename)
                    socketio.emit('log', {
                        'job_id': job_id,
                        'level': 'success',
                        'message': f"decrypted: {filename}"
                    })
                else:
                    results['failed'].append(filename)
                    socketio.emit('log', {
                        'job_id': job_id,
                        'level': 'error',
                        'message': f"failed to decrypt: {filename}"
                    })

                update_job_status(job_id, progress=idx + 1)

            except Exception as e:
                results['failed'].append(os.path.basename(file_path))
                socketio.emit('log', {
                    'job_id': job_id,
                    'level': 'error',
                    'message': f"error: {str(e)}"
                })

        update_job_status(job_id, status='completed', results=results)

    except Exception as e:
        update_job_status(job_id, status='failed', results={'error': str(e)})


def run_pipeline_job(job_id, input_files, output_dir, password, shred_method):
    """run full pipeline job in background"""
    try:
        update_job_status(job_id, status='running', total=len(input_files) * 3)

        scrubber = ImageScrubber(verbose=False)
        crypto = ImageCrypto(verbose=False)
        shredder = SecureDelete(verbose=False)

        results = {'success': [], 'failed': []}
        progress = 0

        for file_path in input_files:
            try:
                filename = os.path.basename(file_path)

                # step 1: scrub
                temp_clean = os.path.join(output_dir, f"temp_clean_{filename}")
                success, msg = scrubber.scrub_image(file_path, temp_clean)
                progress += 1
                update_job_status(job_id, progress=progress)

                if not success:
                    results['failed'].append(filename)
                    continue

                # step 2: encrypt
                output_path = os.path.join(output_dir, f"{filename}.enc")
                if not crypto.encrypt_file(temp_clean, output_path, password):
                    results['failed'].append(filename)
                    os.remove(temp_clean)
                    progress += 2
                    update_job_status(job_id, progress=progress)
                    continue

                progress += 1
                update_job_status(job_id, progress=progress)

                # step 3: secure delete originals
                shredder.shred_file(file_path, method=shred_method)
                shredder.shred_file(temp_clean, method=shred_method)
                progress += 1
                update_job_status(job_id, progress=progress)

                results['success'].append(filename)
                socketio.emit('log', {
                    'job_id': job_id,
                    'level': 'success',
                    'message': f"pipeline completed: {filename}"
                })

            except Exception as e:
                results['failed'].append(os.path.basename(file_path))
                socketio.emit('log', {
                    'job_id': job_id,
                    'level': 'error',
                    'message': f"error: {str(e)}"
                })

        update_job_status(job_id, status='completed', results=results)

    except Exception as e:
        update_job_status(job_id, status='failed', results={'error': str(e)})


@app.route('/')
def index():
    """main dashboard"""
    return render_template('dashboard.html', themes=get_themes())


@app.route('/api/scrub', methods=['POST'])
def api_scrub():
    """scrub images endpoint"""
    try:
        files = request.files.getlist('files')
        if not files:
            return jsonify({'error': 'no files provided'}), 400

        # save uploaded files
        input_files = []
        for file in files:
            if file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                input_files.append(filepath)

        # create output directory
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], f'scrub_{job_counter + 1}')
        os.makedirs(output_dir, exist_ok=True)

        # create and start job
        job_id = create_job('scrub', {
            'files': input_files,
            'output_dir': output_dir
        })

        thread = threading.Thread(
            target=run_scrub_job,
            args=(job_id, input_files, output_dir, {})
        )
        thread.daemon = True
        thread.start()

        return jsonify({'job_id': job_id, 'message': 'job started'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/encrypt', methods=['POST'])
def api_encrypt():
    """encrypt files endpoint"""
    try:
        files = request.files.getlist('files')
        password = request.form.get('password')

        if not files or not password:
            return jsonify({'error': 'missing files or password'}), 400

        # save uploaded files
        input_files = []
        for file in files:
            if file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                input_files.append(filepath)

        # create output directory
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], f'encrypt_{job_counter + 1}')
        os.makedirs(output_dir, exist_ok=True)

        # create and start job
        job_id = create_job('encrypt', {
            'files': input_files,
            'output_dir': output_dir
        })

        thread = threading.Thread(
            target=run_encrypt_job,
            args=(job_id, input_files, output_dir, password)
        )
        thread.daemon = True
        thread.start()

        return jsonify({'job_id': job_id, 'message': 'job started'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/decrypt', methods=['POST'])
def api_decrypt():
    """decrypt files endpoint"""
    try:
        files = request.files.getlist('files')
        password = request.form.get('password')

        if not files or not password:
            return jsonify({'error': 'missing files or password'}), 400

        # save uploaded files
        input_files = []
        for file in files:
            if file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                input_files.append(filepath)

        # create output directory
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], f'decrypt_{job_counter + 1}')
        os.makedirs(output_dir, exist_ok=True)

        # create and start job
        job_id = create_job('decrypt', {
            'files': input_files,
            'output_dir': output_dir
        })

        thread = threading.Thread(
            target=run_decrypt_job,
            args=(job_id, input_files, output_dir, password)
        )
        thread.daemon = True
        thread.start()

        return jsonify({'job_id': job_id, 'message': 'job started'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/pipeline', methods=['POST'])
def api_pipeline():
    """full pipeline endpoint"""
    try:
        files = request.files.getlist('files')
        password = request.form.get('password')
        shred_method = request.form.get('shred_method', 'dod')

        if not files or not password:
            return jsonify({'error': 'missing files or password'}), 400

        # save uploaded files
        input_files = []
        for file in files:
            if file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                input_files.append(filepath)

        # create output directory
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], f'pipeline_{job_counter + 1}')
        os.makedirs(output_dir, exist_ok=True)

        # create and start job
        job_id = create_job('pipeline', {
            'files': input_files,
            'output_dir': output_dir,
            'shred_method': shred_method
        })

        thread = threading.Thread(
            target=run_pipeline_job,
            args=(job_id, input_files, output_dir, password, shred_method)
        )
        thread.daemon = True
        thread.start()

        return jsonify({'job_id': job_id, 'message': 'job started'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/jobs')
def api_jobs():
    """get all jobs"""
    return jsonify(list(active_jobs.values()))


@app.route('/api/jobs/<job_id>')
def api_job_status(job_id):
    """get specific job status"""
    if job_id not in active_jobs:
        return jsonify({'error': 'job not found'}), 404
    return jsonify(active_jobs[job_id])


@app.route('/api/download/<job_id>')
def api_download(job_id):
    """download job results as zip"""
    if job_id not in active_jobs:
        return jsonify({'error': 'job not found'}), 404

    job = active_jobs[job_id]
    if job['status'] != 'completed':
        return jsonify({'error': 'job not completed'}), 400

    # create zip of output directory
    import zipfile
    output_dir = job['params']['output_dir']
    zip_path = f"{output_dir}.zip"

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.basename(file_path))

    return send_file(zip_path, as_attachment=True, download_name=f"{job_id}_results.zip")


@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """get or update configuration"""
    if request.method == 'GET':
        return jsonify(config.config)
    else:
        try:
            data = request.json
            for section, values in data.items():
                if isinstance(values, dict):
                    for key, value in values.items():
                        config.set(section, key, value)
            return jsonify({'message': 'config updated'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500


def get_themes():
    """get available themes"""
    return [
        'arch_dark',
        'blackarch',
        'dracula',
        'gruvbox',
        'green_hacker',
        'blue_soc',
        'red_team',
        'purple_team',
        'nord'
    ]


@socketio.on('connect')
def handle_connect():
    """handle websocket connection"""
    emit('connected', {'message': 'connected to imageghost v3.0'})


@socketio.on('disconnect')
def handle_disconnect():
    """handle websocket disconnection"""
    pass


def run_server(host='127.0.0.1', port=5000, debug=False):
    """run the web server"""
    logger.info(f"starting imageghost v3.0 web dashboard on http://{host}:{port}")
    socketio.run(app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)


if __name__ == '__main__':
    run_server()
