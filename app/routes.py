from flask import Blueprint, request, jsonify, render_template
from app.services.ai_service import generate_content, summarize_content
from app.services.data_service import save_generation_record, get_history

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/generate-content', methods=['POST'])
def api_generate_content():
    data = request.json
    if not data or not data.get('topic'):
        return jsonify({'status': 'error', 'message': 'Topic is required'}), 400
        
    topic = data.get('topic')
    tone = data.get('tone', 'professional')
    word_count = data.get('word_count', 300)
    keywords = data.get('keywords', [])
    
    try:
        content = generate_content(topic, tone, word_count, keywords)
        record = save_generation_record(
            prompt_type='generation',
            inputs={'topic': topic, 'tone': tone, 'word_count': word_count, 'keywords': keywords},
            output=content
        )
        return jsonify({'status': 'success', 'data': record})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@main_blueprint.route('/summarize-content', methods=['POST'])
def api_summarize_content():
    data = request.json
    if not data or not data.get('text'):
        return jsonify({'status': 'error', 'message': 'Text is required'}), 400
        
    text = data.get('text')
    max_length = data.get('max_length', 100)
    
    try:
        summary = summarize_content(text, max_length)
        record = save_generation_record(
            prompt_type='summarization',
            inputs={'text_length': len(text), 'max_length': max_length},
            output=summary
        )
        return jsonify({'status': 'success', 'data': record})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@main_blueprint.route('/keyword-content', methods=['POST'])
def api_keyword_content():
    data = request.json
    if not data or not data.get('topic') or not data.get('keywords'):
        return jsonify({'status': 'error', 'message': 'Topic and keywords are required'}), 400
        
    topic = data.get('topic')
    keywords = data.get('keywords', [])
    
    try:
        # A variant of generation that strictly focuses on keywords
        content = generate_content(topic, tone="SEO-optimized", word_count=400, keywords=keywords)
        record = save_generation_record(
            prompt_type='keyword-focused',
            inputs={'topic': topic, 'keywords': keywords},
            output=content
        )
        return jsonify({'status': 'success', 'data': record})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@main_blueprint.route('/history', methods=['GET'])
def api_history():
    try:
        limit = request.args.get('limit', default=10, type=int)
        format_type = request.args.get('format', 'json')
        
        history_data = get_history(limit=limit)
        
        if format_type.lower() == 'csv':
            # Could stream a CSV directly using Pandas, but for now returning a simulated path/message
            return jsonify({'status': 'success', 'message': 'CSV download implemented via file.', 'data': history_data})
            
        return jsonify({'status': 'success', 'data': history_data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
