"""This module is responsible for generating the FEN string."""


import numpy as np
import cv2
from keras.applications.imagenet_utils import (
    preprocess_input as prein_squeezenet1p1,
)

try:
    from livechess2fen.lc2fen.predict_board import (
        predict_board_keras,
        predict_board_onnx,
    )
    from utilities import delete
except (
    ModuleNotFoundError
):  
    import sys

    sys.path.append("..")
    try:
        from livechess2fen.lc2fen.predict_board import (
            predict_board_keras,
            predict_board_onnx,
        )
        from utilities import delete
    except ModuleNotFoundError:
        print(
            "Please make sure to set your terminal's directory to "
            
        )
        sys.exit()


ACTIVATE_KERAS = False
MODEL_PATH_KERAS = "livechess2fen/selected_models/SqueezeNet1p1_all_last.h5"
IMG_SIZE_KERAS = 227
PRE_INPUT_KERAS = prein_squeezenet1p1

ACTIVATE_ONNX = True
MODEL_PATH_ONNX = "livechess2fen/selected_models/SqueezeNet1p1_all_last.onnx"
IMG_SIZE_ONNX = 227
PRE_INPUT_ONNX = prein_squeezenet1p1


def predict_fen_and_move(
    img: np.ndarray,
    a1_pos: str = "BL",
    board_corners: (list[list[int]] | None) = None,
    previous_fen: (str | None) = None,
    must_detect_move: bool = False,
) -> tuple[str, str | None]:
    """Predict FEN of current position and move in previous position.

    Note that the input image `img` must be a BGR image.

    :param img: Input BGR image.

    :param a1_pos: Position of the a1 square of the chessboard image. (`"BL"`, `"BR"`, `"TL"or `"TR"`)

    :param board_corners: Length-4 list of coordinates of four corners.

        The 4 board corners are in the order of top left, top right,
        bottom right, and bottom left.

        If it is not `None` and the corner coordinates are accurate
        enough, the neural-network-based board-detection step is skipped
        (which means the total processing time is reduced).

    :param previous_fen: FEN string of the previous board position.

        If it is not `None`, it could significantly improve the accuracy
        of FEN prediction.

    :param must_detect_move: Whether a valid move must be detected.

        This parameter controls whether a valid move must be detected in
        order to return an FEN that is different from the previous FEN.

        This parameter only makes a difference if `previous_fen` is
        not `None`.

    :return: Predicted current FEN and detected previous move.
    """
    assert ACTIVATE_KERAS != ACTIVATE_ONNX
    path = "_.png"
    cv2.imwrite(path, img)
    if ACTIVATE_KERAS:
        fen, _, detected_move = predict_board_keras(
            MODEL_PATH_KERAS,
            IMG_SIZE_KERAS,
            PRE_INPUT_KERAS,
            path,
            a1_pos,
            board_corners,
            previous_fen,
            must_detect_move,
        )
    else:  # elif ACTIVATE_ONNX:
        fen, _, detected_move = predict_board_onnx(
            MODEL_PATH_ONNX,
            IMG_SIZE_ONNX,
            PRE_INPUT_ONNX,
            path,
            a1_pos,
            board_corners,
            previous_fen,
            must_detect_move,
        )

    delete(path)

    return str(fen), detected_move


if (
    __name__ == "__main__"
):  
    
    MODEL_PATH_KERAS =  MODEL_PATH_KERAS
    MODEL_PATH_ONNX = MODEL_PATH_ONNX
    import time

    img = cv2.imread("ddd.jpg")
    
        
    a1_pos = "BL"
    
    #board_corners = [[588,378], [1183  ,388], [1265, 1018], [ 527 ,1003]]
    board_corners = None
    
    previous_fen = "r1bqkbnr/ppp1pppp/2n5/3p4/3P1B2/5N2/PPP1PPPP/RN1QKB1R"
    #previous_fen = None
    
    must_detect_move = True
    #must_detect_move = False

    start_time = time.time()
    fen, detected_move = predict_fen_and_move(
        img, a1_pos, board_corners, previous_fen, must_detect_move
    )
    finish_time = time.time()
    print(f"\tPredicted FEN: {fen}")
    #print(f"\tDetected move: {detected_move}")
    print(f"\tThis prediction took {finish_time - start_time} s")

    
    from visualize_fen import generate_fen_image
    
    #fen_image = generate_fen_image(fen)
    #cv2.imshow("Predicted FEN", cv2.cvtColor(fen_image, cv2.COLOR_RGB2BGR))
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
