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
    return pgn.strip()







# Test cases
fens =['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR',
            "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR",
"rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR",
"rnbqkbnr/pppp1ppp/8/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR",
"rnbqkb1r/pppp1ppp/5n2/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR",
"rnbqkb1r/pppp1ppp/5n2/4p3/2B1P3/3P4/PPP2PPP/RNBQK1NR",
"rnbqk2r/pppp1ppp/5n2/2b1p3/2B1P3/3P4/PPP2PPP/RNBQK1NR",
"rnbqk2r/pppp1ppp/5n2/2b1p3/2B1P3/2NP4/PPP2PPP/R1BQK1NR",
"rnbqk2r/ppp2ppp/3p1n2/2b1p3/2B1P3/2NP4/PPP2PPP/R1BQK1NR",
"rnbqk2r/ppp2ppp/3p1n2/2b1p3/2B1P3/2NP3P/PPP2PP1/R1BQK1NR",
"rnbqk2r/pp3ppp/2pp1n2/2b1p3/2B1P3/2NP3P/PPP2PP1/R1BQK1NR",
"rnbqk2r/pp3ppp/2pp1n2/2b1p3/2B1P3/2NP3P/PPP1NPP1/R1BQK2R",
"rnbqk2r/1p3ppp/2pp1n2/p1b1p3/2B1P3/2NP3P/PPP1NPP1/R1BQK2R",
"rnbqk2r/1p3ppp/2pp1n2/p1b1p3/P1B1P3/2NP3P/1PP1NPP1/R1BQK2R",
"rn1qk2r/1p3ppp/2ppbn2/p1b1p3/P1B1P3/2NP3P/1PP1NPP1/R1BQK2R",
"rn1qk2r/1p3ppp/2ppbn2/p1b1p3/P1B1P3/2NP2NP/1PP2PP1/R1BQK2R",
"r2qk2r/1p1n1ppp/2ppbn2/p1b1p3/P1B1P3/2NP2NP/1PP2PP1/R1BQK2R",
"r2qk2r/1p1n1ppp/2ppbn2/p1b1p3/P1B1P3/2NP2NP/1PP2PP1/R1BQ1RK1",
"r2q1rk1/1p1n1ppp/2ppbn2/p1b1p3/P1B1P3/2NP2NP/1PP2PP1/R1BQ1RK1",
"r2q1rk1/1p1n1ppp/2ppbn2/p1b1p3/P1B1P3/2NP1QNP/1PP2PP1/R1B2RK1",
"r2q1r1k/1p1n1ppp/2ppbn2/p1b1p3/P1B1P3/2NP1QNP/1PP2PP1/R1B2RK1",
"r2q1r1k/1p1n1ppp/2ppbn2/p1b1pN2/P1B1P3/2NP1Q1P/1PP2PP1/R1B2RK1",
"r2q1r1k/1p3ppp/1nppbn2/p1b1pN2/P1B1P3/2NP1Q1P/1PP2PP1/R1B2RK1",
"r2q1r1k/1p3ppp/1nppbn2/p1b1pNB1/P1B1P3/2NP1Q1P/1PP2PP1/R4RK1",
"r2q1r1k/1p1n1ppp/2ppbn2/p1b1pNB1/P1B1P3/2NP1Q1P/1PP2PP1/R4RK1",
"r2q1r1k/1p1n1ppp/2ppbn2/p1b1pNB1/P1B1P3/2NP1Q1P/1PP2PP1/3R1RK1",
"r3qr1k/1p1n1ppp/2ppbn2/p1b1pNB1/P1B1P3/2NP1Q1P/1PP2PP1/3R1RK1",
"r3qr1k/1p1n1ppp/2ppbn2/p1b1pNB1/P1B1P3/1PNP1Q1P/2P2PP1/3R1RK1",
"r3qrnk/1p1n1ppp/2ppb3/p1b1pNB1/P1B1P3/1PNP1Q1P/2P2PP1/3R1RK1",
"r3qrnk/1p1n1ppp/2ppb3/p1b1pNB1/P1B1P3/1P1P1Q1P/2P1NPP1/3R1RK1",
"r3qrnk/1p1n1p1p/2ppb1p1/p1b1pNB1/P1B1P3/1P1P1Q1P/2P1NPP1/3R1RK1",
"r3qrnk/1p1n1p1p/2ppb1pN/p1b1p1B1/P1B1P3/1P1P1Q1P/2P1NPP1/3R1RK1",
"r3qrnk/1p1n3p/2ppbppN/p1b1p1B1/P1B1P3/1P1P1Q1P/2P1NPP1/3R1RK1 w",
"r3qrnk/1p1n3p/2ppbppN/p1b1p3/P1B1P3/1P1PBQ1P/2P1NPP1/3R1RK1 b",
"r3qrnk/1p1n3p/2ppbppN/p3p3/P1B1P3/1P1PbQ1P/2P1NPP1/3R1RK1 w",
"r3qrnk/1p1n3p/2ppbppN/p3p3/P1B1P3/1P1PQ2P/2P1NPP1/3R1RK1 b",
"r3qrnk/1p1n3p/2ppb1pN/p3pp2/P1B1P3/1P1PQ2P/2P1NPP1/3R1RK1",
"r3qrnk/1p1n3p/2ppb1pN/p3pP2/P1B5/1P1PQ2P/2P1NPP1/3R1RK1",
"r3qrnk/1p1n3p/2ppb2N/p3pp2/P1B5/1P1PQ2P/2P1NPP1/3R1RK1",
"r3qrNk/1p1n3p/2ppb3/p3pp2/P1B5/1P1PQ2P/2P1NPP1/3R1RK1",
"r3q1rk/1p1n3p/2ppb3/p3pp2/P1B5/1P1PQ2P/2P1NPP1/3R1RK1",
"r3q1rk/1p1n3p/2ppB3/p3pp2/P7/1P1PQ2P/2P1NPP1/3R1RK1",
"r5rk/1p1n3p/2ppq3/p3pp2/P7/1P1PQ2P/2P1NPP1/3R1RK1",
"r5rk/1p1n3p/2ppq3/p3pp2/P4P2/1P1PQ2P/2P1N1P1/3R1RK1",
"r6k/1p1n3p/2ppq1r1/p3pp2/P4P2/1P1PQ2P/2P1N1P1/3R1RK1",
"r6k/1p1n3p/2ppq1r1/p3pp2/P4P2/1P1PQ2P/2P1NRP1/3R2K1",
"6rk/1p1n3p/2ppq1r1/p3pp2/P4P2/1P1PQ2P/2P1NRP1/3R2K1",
"6rk/1p1n3p/2ppq1r1/p3pp2/P4P2/1P1PQ2P/2P1NRP1/3R3K",
"6rk/1p1n3p/2pp2r1/p2qpp2/P4P2/1P1PQ2P/2P1NRP1/3R3K",
"6rk/1p1n3p/2pp2r1/p2qpp2/P1P2P2/1P1PQ2P/4NRP1/3R3K",
"6rk/1p1n3p/2ppq1r1/p3pp2/P1P2P2/1P1PQ2P/4NRP1/3R3K",
"6rk/1p1n3p/2ppq1r1/p3Pp2/P1P5/1P1PQ2P/4NRP1/3R3K",
"6rk/1p1n3p/2p1q1r1/p3pp2/P1P5/1P1PQ2P/4NRP1/3R3K",
"6rk/1p1n3p/2p1q1r1/p3pp2/P1PP4/1P2Q2P/4NRP1/3R3K",
"6rk/1p1n3p/2p1q1r1/p3p3/P1PP1p2/1P2Q2P/4NRP1/3R3K",
"6rk/1p1n3p/2p1q1r1/p3p3/P1PPQp2/1P5P/4NRP1/3R3K",
"6rk/1p1n3p/2p1q2r/p3p3/P1PPQp2/1P5P/4NRP1/3R3K",
"6rk/1p1n3p/2p1q2r/p3P3/P1P1Qp2/1P5P/4NRP1/3R3K",
"6rk/1p5p/2p1q2r/p1n1P3/P1P1Qp2/1P5P/4NRP1/3R3K",
"6rk/1p5p/2p1q2r/p1n1P3/P1P2p2/1P3Q1P/4NRP1/3R3K",
"6rk/1p5p/2p4r/p1n1q3/P1P2p2/1P3Q1P/4NRP1/3R3K",
"6rk/1p5p/2p4r/p1n1q3/P1P2N2/1P3Q1P/5RP1/3R3K",
"6rk/1p5p/2p4r/p3q3/P1P1nN2/1P3Q1P/5RP1/3R3K",
"6rk/1p5p/2p4r/p3q3/P1P1nN2/1P3Q1P/4R1P1/3R3K",
"4r2k/1p5p/2p4r/p3q3/P1P1nN2/1P3Q1P/4R1P1/3R3K",
"4r2k/1p5p/2p4r/p3q3/P1P1nN2/1P3Q1P/4R1P1/4R2K"]

print(fen_to_pgn(fens).replace("", ""))
