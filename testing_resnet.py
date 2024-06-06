import numpy as np
import cv2
import tensorflow as tf


try:
    from livechess2fen.lc2fen.predict_board import (
        predict_board_keras,
        predict_board_onnx,
    )
    from utilities import delete
except ModuleNotFoundError:  
    import sys
    sys.path.append("..")
    try:
        from livechess2fen.lc2fen.predict_board import (
            predict_board_keras,
            predict_board_onnx,
        )
        from utilities import delete
    except ModuleNotFoundError:
        print("Please make sure to set your terminal's directory to the project's root.")
        sys.exit()

ACTIVATE_KERAS = True  # Assuming your ResNet model is in Keras format
MODEL_PATH_KERAS = "F:/final/resnet50_custom_model.h5"
#MODEL_PATH_KERAS = "livechess2fen/selected_models/SqueezeNet1p1_all_last.h5"
IMG_SIZE_KERAS = 224
#PRE_INPUT_KERAS = prein_resnet
PRE_INPUT_KERAS = tf.keras.applications.resnet50.preprocess_input

ACTIVATE_ONNX = False
MODEL_PATH_ONNX = "path_to_your_resnet_model.onnx"
IMG_SIZE_ONNX = 224
#PRE_INPUT_ONNX = prein_resnet

def predict_fen_and_move(
    img: np.ndarray,
    a1_pos: str = "BL",
    board_corners: (list[list[int]] | None) = None,
    previous_fen: (str | None) = None,
    must_detect_move: bool = False,
) -> tuple[str, str | None]:
  
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

if __name__ == "__main__":
    import time

    img = cv2.imread("F:/final/Brandon_v_appanna/9.jpg")
    a1_pos = "BL"
    board_corners = None
    previous_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    must_detect_move = True

    start_time = time.time()
    fen, detected_move = predict_fen_and_move(
        img, a1_pos, board_corners, previous_fen, must_detect_move
    )
    finish_time = time.time()
    print(f"\tPredicted FEN: {fen}")
    print(f"detected_move: {detected_move}")
    print(f"\tThis prediction took {finish_time - start_time} s")

    from visualize_fen import generate_fen_image
    # fen_image = generate_fen_image(fen)
    # cv2.imshow("Predicted FEN", cv2.cvtColor(fen_image, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
