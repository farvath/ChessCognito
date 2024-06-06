import re

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
    pgn = '' if fens[0] == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1' else f'[SetUp "1"]\n[FEN "{fens[0]}"]\n'
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
    return pgn



# Test cases
fens = [

"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
"rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR",
"rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR",
"rnbqkbnr/pppp1ppp/8/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR",
"r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR",
"r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR",
"r1bqkbnr/ppp2ppp/2np4/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR",
"r1bqkbnr/ppp2Qpp/2np4/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR",

]

print(fen_to_pgn(fens))


