import time
from flask import Flask, jsonify, render_template, request, redirect
import urllib.parse
import base64
import numpy as np
import cv2
from predict_fen import predict_fen_and_move


app = Flask(__name__)

fen_list = [
    'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR']

real_fen=[]

def remove_duplicates_from_fen_list(fen_list): 
    seen = set()
    unique_fen_list = []
    
    for fen in fen_list:
        if fen not in seen:
            seen.add(fen)
            unique_fen_list.append(fen)
    
    return unique_fen_list


def fen_to_data(fen):
    if not fen:
        return None
    try:
        fields = fen.split(' ')
        while len(fields) < 6:
            fields.append('-')  # Fill in missing fields with '-'
        return {
            'place': [row.replace('1', ' ' * 1).replace('2', ' ' * 2).replace('3', ' ' * 3)
                      .replace('4', ' ' * 4).replace('5', ' ' * 5).replace('6', ' ' * 6)
                      .replace('7', ' ' * 7).replace('8', ' ' * 8) for row in fields[0].split('/')],
            'color': fields[1],
            'fullMoveNumber': int(fields[5]) if fields[5].isdigit() else float('nan')  # Convert to int if possible, otherwise NaN
        }
    except Exception as err:
        raise ValueError('Wrong fen: {}\nError: {}'.format(fen, err))



def fen_to_pgn(fens):
    if not isinstance(fens, list):
        raise ValueError('fens is not a list')
    if len(fens) < 2:
        return ''
    pgn = '' if fens[0] == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1' else f''
    previous = fen_to_data(fens.pop(0))
    pgn += str(previous['fullMoveNumber']) + '.' + ('..' if previous['color'] == 'b' else '')
    while fens:
        current = fen_to_data(fens.pop(0))
        removes, adds = {}, {}
        for r in range(8):
            for f in range(8):
                if previous['place'][r][f] == current['place'][r][f]:
                    continue
                if previous['place'][r][f] != ' ':
                    removes[previous['place'][r][f]] = {'r': r, 'f': f}
                if current['place'][r][f] != ' ':
                    adds[current['place'][r][f]] = {'r': r, 'f': f}
        pieces = list(adds.keys())
        piece_name = pieces[0].upper()
        capture = len(removes) == 2
        if len(pieces) == 2:
            if adds.get('k') and adds['k']['f'] == 6 or adds.get('K') and adds['K']['f'] == 6:
                pgn += 'O-O'
            elif adds.get('k') and adds['k']['f'] == 2 or adds.get('K') and adds['K']['f'] == 2:
                pgn += 'O-O-O'
        else:
            to = ''
            if piece_name == 'P' or not removes.get(pieces[0]):
                to = 'abcdefgh'[removes.get(pieces[0], removes.get('P' if previous['color'] == 'w' else 'p')).get('f', 0)] if capture else ''
            else:
                to = piece_name + 'abcdefgh'[removes[pieces[0]]['f']] + '87654321'[removes[pieces[0]]['r']]
            pgn += to + ('x' if capture else '') + 'abcdefgh'[adds[pieces[0]]['f']] + '87654321'[adds[pieces[0]]['r']] + ('' if removes.get(pieces[0]) else '=' + piece_name)
        pgn += ' ' if previous['fullMoveNumber'] == current['fullMoveNumber'] else '\n' + (str(current['fullMoveNumber']) + '.' if fens else '')
        previous = current
    return pgn.strip()



@app.route('/get_fen_list', methods=['GET'])
def get_fen_list():
    real_fen=remove_duplicates_from_fen_list(fen_list)
    print("real fen",real_fen)
    return jsonify({'fen_list': real_fen})

        
def generate_lichess_analysis_url(fen):
    if not fen:
        return None
    base_url = "https://lichess.org/analysis"
    params = {"fen": fen}
    url_params = urllib.parse.urlencode(params)
    full_url = f"{base_url}?{url_params}"
    return full_url

def generate_lichess_analysis_link(pgn_moves):
    if not pgn_moves:
        return None
    formatted_moves = urllib.parse.quote(pgn_moves)
    lichess_analysis_url = f"https://lichess.org/analysis/pgn/{formatted_moves}"
    return lichess_analysis_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/adjustcamera', methods=['POST'])
def adjust_camera():
    return render_template('camera.html')

@app.route('/digitize', methods=['POST'])
def start_match():
    return render_template('digitize.html')

@app.route('/analyze_fen', methods=['POST'])
def analyze_fen():
    try:
        fen_input = request.form['fenInput'].strip()
        if not fen_input:
            return "No FEN input provided. Please enter a valid FEN."
        
        lichess_url = generate_lichess_analysis_url(fen_input)
        if lichess_url:
            return redirect(lichess_url)
        else:
            return "Error generating Lichess URL. Please try again."
    except Exception as e:
        print(f"Error analyzing FEN: {e}")
        return "Incorrect FEN format. Please provide valid FEN."

@app.route('/analyze_pgn', methods=['POST'])
def analyze_pgn():
    try:  
        pgn_moves = request.form['pgnInput'].strip()
        if not pgn_moves:
            return "No PGN input provided."
        lichess_url = generate_lichess_analysis_link(pgn_moves)
        if lichess_url:
            return redirect(lichess_url)
        else:
            return "Incorrect PGN format. Please provide valid PGN."
    except Exception as e:
        print(f"Error analyzing PGN: {e}")
        return "Incorrect PGN format. Please provide valid PGN."
    
@app.route('/livedigitization', methods=['POST'])
def livedigitization():
    return render_template('livedigitization.html')

@app.route('/process_image', methods=['POST'])
def process_image():
   
    data = request.get_json()
    image_data_url = data.get('image', '')
    a1_pos = data.get('a1_pos', 'BR')  # Default to 'BR' if not provided

    encoded_data = image_data_url.split(',')[1]  
    decoded_data = base64.b64decode(encoded_data)  # Decode Base64-encoded data
    image_array = np.frombuffer(decoded_data, np.uint8)  # Convert to numpy array
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)  

    
    
    #board_corners = [ [ 76 ,266], [734 ,271], [752, 915],  [ 89 ,945]]
    board_corners = None
    print(fen_list)
    
    
    
    previous_fen = fen_list[-1]
    
    must_detect_move = True
    #must_detect_move = False

    start_time = time.time()
    fen, detected_move = predict_fen_and_move(
        img, a1_pos, board_corners, previous_fen, must_detect_move
    )
    finish_time = time.time()
    
    
    
    if detected_move !="None":
        fen_list.append(fen)
        
   
    
    return jsonify({'fen': fen, 'move': detected_move})


@app.route('/convert_fen_to_pgn', methods=['POST'])
def convert_fen_to_pgn():
    try:
        data = request.get_json()
        fen_list = data.get('fen_list', [])

        if not isinstance(fen_list, list):
            return jsonify({'error': 'Invalid FEN list provided'})

        if len(fen_list) < 2:
            return jsonify({'error': 'At least two FEN positions are required'})

        pgn_result = fen_to_pgn(fen_list).replace("nan.", "")
        return jsonify({'pgn': pgn_result})

    except Exception as e:
        return jsonify({'error': f'Error converting FEN to PGN: {str(e)}'})


if __name__ == '__main__':
    app.run(debug=True)
