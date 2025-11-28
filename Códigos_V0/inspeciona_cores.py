import cv2
import numpy as np

WINDOW_NAME = "Leitor de cores - camera (ESC para sair)"

# Variáveis globais
frame_atual = None
mouse_x = 0
mouse_y = 0
mouse_inside = False  # indica se o mouse está dentro da área do vídeo


def bgr_to_hex(bgr):
    # OpenCV usa BGR, HEX usa RGB
    b, g, r = int(bgr[0]), int(bgr[1]), int(bgr[2])
    return f"#{r:02X}{g:02X}{b:02X}"


def on_mouse(event, x, y, flags, userdata):
    """
    Callback do mouse: só guarda a posição.
    O processamento é feito no loop principal.
    """
    global mouse_x, mouse_y, mouse_inside, frame_atual

    if frame_atual is None:
        return

    if event == cv2.EVENT_MOUSEMOVE:
        h, w, _ = frame_atual.shape
        if 0 <= x < w and 0 <= y < h:
            mouse_x = x
            mouse_y = y
            mouse_inside = True
        else:
            mouse_inside = False
    elif event == cv2.EVENT_LBUTTONDOWN:
        # Se quiser fazer algo no clique depois, dá pra usar aqui
        pass


def main():
    global frame_atual

    # Abre a camera (0 = webcam padrão)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro ao abrir a câmera.")
        return

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback(WINDOW_NAME, on_mouse)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Não consegui ler frame da câmera.")
            break

        # Opcional: redimensionar para ficar mais leve
        frame = cv2.resize(frame, (400, 400))

        frame_atual = frame  # atualiza o frame global para o callback usar

        # Cria placeholder preta para o painel de informações
        h, w, _ = frame.shape
        placeholder = np.zeros((h, 400, 3), dtype=np.uint8)

        if mouse_inside:
            # Garante que ainda está dentro dos limites
            x = int(mouse_x)
            y = int(mouse_y)
            if 0 <= x < w and 0 <= y < h:
                bgr_pixel = frame[y, x]
                bgr_1x1 = np.uint8([[bgr_pixel]])

                hsv = cv2.cvtColor(bgr_1x1, cv2.COLOR_BGR2HSV)[0, 0]
                ycb = cv2.cvtColor(bgr_1x1, cv2.COLOR_BGR2YCrCb)[0, 0]
                lab = cv2.cvtColor(bgr_1x1, cv2.COLOR_BGR2Lab)[0, 0]
                hex_code = bgr_to_hex(bgr_pixel)

                # Desenha um pequeno círculo na posição do mouse
                cv2.circle(frame, (x, y), 5, (0, 255, 0), 1)

                # Escreve textos no painel
                cv2.putText(
                    placeholder,
                    f"Posicao: x={x}, y={y}",
                    (20, 40),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.8,
                    (255, 255, 255),
                    1,
                )

                cv2.putText(
                    placeholder,
                    f"BGR [{bgr_pixel[0]}, {bgr_pixel[1]}, {bgr_pixel[2]}]",
                    (20, 90),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.8,
                    (255, 255, 255),
                    1,
                )

                cv2.putText(
                    placeholder,
                    f"HSV [{hsv[0]}, {hsv[1]}, {hsv[2]}]",
                    (20, 140),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.8,
                    (255, 255, 255),
                    1,
                )

                cv2.putText(
                    placeholder,
                    f"YCrCb [{ycb[0]}, {ycb[1]}, {ycb[2]}]",
                    (20, 190),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.8,
                    (255, 255, 255),
                    1,
                )

                cv2.putText(
                    placeholder,
                    f"Lab [{lab[0]}, {lab[1]}, {lab[2]}]",
                    (20, 240),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.8,
                    (255, 255, 255),
                    1,
                )

                cv2.putText(
                    placeholder,
                    f"HEX {hex_code}",
                    (20, 290),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.8,
                    (0, 255, 0),
                    1,
                )

        # Junta o vídeo com o painel lateral
        combined = np.hstack((frame, placeholder))

        cv2.imshow(WINDOW_NAME, combined)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC para sair
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
