import cv2
import numpy as np
import math
import time
import unicodedata

# =========================
# SELETOR DE MODO DE SOM
# =========================
# 2 = notas musicais com winsound.Beep (mais simples)
# 3 = notas musicais com sounddevice (onda senoidal, som mais suave)
SOUND_MODE = 3

# =========================
# IMPORTS DE SOM
# =========================
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False
    print("winsound não disponível (som modo 2 pode não funcionar).")

try:
    import sounddevice as sd
    HAS_SD = True
except ImportError:
    HAS_SD = False
    print("sounddevice não disponível (som modo 3 pode não funcionar).")

WINDOW_NAME = "Leitor de cores - camera (ESC para sair)"

# -------------------------------
# TABELA DE CORES CSS3 (147 cores)
# -------------------------------
CSS3_COLORS = {
    '#F0F8FF': 'aliceblue', '#FAEBD7': 'antiquewhite', '#00FFFF': 'aqua', '#7FFFD4': 'aquamarine',
    '#F0FFFF': 'azure', '#F5F5DC': 'beige', '#FFE4C4': 'bisque', '#000000': 'black',
    '#FFEBCD': 'blanchedalmond', '#0000FF': 'blue', '#8A2BE2': 'blueviolet', '#A52A2A': 'brown',
    '#DEB887': 'burlywood', '#5F9EA0': 'cadetblue', '#7FFF00': 'chartreuse', '#D2691E': 'chocolate',
    '#FF7F50': 'coral', '#6495ED': 'cornflowerblue', '#FFF8DC': 'cornsilk', '#DC143C': 'crimson',
    '#00FFFF': 'cyan', '#00008B': 'darkblue', '#008B8B': 'darkcyan', '#B8860B': 'darkgoldenrod',
    '#A9A9A9': 'darkgray', '#006400': 'darkgreen', '#BDB76B': 'darkkhaki', '#8B008B': 'darkmagenta',
    '#556B2F': 'darkolivegreen', '#FF8C00': 'darkorange', '#9932CC': 'darkorchid', '#8B0000': 'darkred',
    '#E9967A': 'darksalmon', '#8FBC8F': 'darkseagreen', '#483D8B': 'darkslateblue', '#2F4F4F': 'darkslategray',
    '#00CED1': 'darkturquoise', '#9400D3': 'darkviolet', '#FF1493': 'deeppink', '#00BFFF': 'deepskyblue',
    '#1E90FF': 'dodgerblue', '#B22222': 'firebrick', '#FFFAF0': 'floralwhite', '#228B22': 'forestgreen',
    '#FF00FF': 'fuchsia', '#DCDCDC': 'gainsboro', '#F8F8FF': 'ghostwhite', '#FFD700': 'gold',
    '#DAA520': 'goldenrod', '#808080': 'gray', '#008000': 'green', '#ADFF2F': 'greenyellow',
    '#F0FFF0': 'honeydew', '#FF69B4': 'hotpink', '#CD5C5C': 'indianred', '#4B0082': 'indigo',
    '#FFFFF0': 'ivory', '#F0E68C': 'khaki', '#E6E6FA': 'lavender', '#FFF0F5': 'lavenderblush',
    '#7CFC00': 'lawngreen', '#FFFACD': 'lemonchiffon', '#ADD8E6': 'lightblue', '#F08080': 'lightcoral',
    '#E0FFFF': 'lightcyan', '#FAFAD2': 'lightgoldenrodyellow', '#D3D3D3': 'lightgray', '#90EE90': 'lightgreen',
    '#FFB6C1': 'lightpink', '#FFA07A': 'lightsalmon', '#20B2AA': 'lightseagreen', '#87CEFA': 'lightskyblue',
    '#778899': 'lightslategray', '#B0C4DE': 'lightsteelblue', '#FFFFE0': 'lightyellow', '#00FF00': 'lime',
    '#32CD32': 'limegreen', '#FAF0E6': 'linen', '#FF00FF': 'magenta', '#800000': 'maroon',
    '#66CDAA': 'mediumaquamarine', '#0000CD': 'mediumblue', '#BA55D3': 'mediumorchid',
    '#9370DB': 'mediumpurple', '#3CB371': 'mediumseagreen', '#7B68EE': 'mediumslateblue',
    '#00FA9A': 'mediumspringgreen', '#48D1CC': 'mediumturquoise', '#C71585': 'mediumvioletred',
    '#191970': 'midnightblue', '#F5FFFA': 'mintcream', '#FFE4E1': 'mistyrose', '#FFE4B5': 'moccasin',
    '#FFDEAD': 'navajowhite', '#000080': 'navy', '#FDF5E6': 'oldlace', '#808000': 'olive',
    '#6B8E23': 'olivedrab', '#FFA500': 'orange', '#FF4500': 'orangered', '#DA70D6': 'orchid',
    '#EEE8AA': 'palegoldenrod', '#98FB98': 'palegreen', '#AFEEEE': 'paleturquoise',
    '#DB7093': 'palevioletred', '#FFEFD5': 'papayawhip', '#FFDAB9': 'peachpuff', '#CD853F': 'peru',
    '#FFC0CB': 'pink', '#DDA0DD': 'plum', '#B0E0E6': 'powderblue', '#800080': 'purple',
    '#FF0000': 'red', '#BC8F8F': 'rosybrown', '#4169E1': 'royalblue', '#8B4513': 'saddlebrown',
    '#FA8072': 'salmon', '#F4A460': 'sandybrown', '#2E8B57': 'seagreen', '#FFF5EE': 'seashell',
    '#A0522D': 'sienna', '#C0C0C0': 'silver', '#87CEEB': 'skyblue', '#6A5ACD': 'slateblue',
    '#708090': 'slategray', '#FFFAFA': 'snow', '#00FF7F': 'springgreen', '#4682B4': 'steelblue',
    '#D2B48C': 'tan', '#008080': 'teal', '#D8BFD8': 'thistle', '#FF6347': 'tomato',
    '#40E0D0': 'turquoise', '#EE82EE': 'violet', '#F5DEB3': 'wheat', '#FFFFFF': 'white',
    '#F5F5F5': 'whitesmoke', '#FFFF00': 'yellow', '#9ACD32': 'yellowgreen'
}

# -------------------------------
# Utilitários de texto
# -------------------------------
def sem_acentos(s: str) -> str:
    if s is None:
        return ""
    nf = unicodedata.normalize("NFD", s)
    return "".join(c for c in nf if unicodedata.category(c) != "Mn")


def closest_color_name(hex_code):
    r = int(hex_code[1:3], 16)
    g = int(hex_code[3:5], 16)
    b = int(hex_code[5:7], 16)

    min_diff = float("inf")
    closest = None

    for hex_val, name in CSS3_COLORS.items():
        r2 = int(hex_val[1:3], 16)
        g2 = int(hex_val[3:5], 16)
        b2 = int(hex_val[5:7], 16)

        diff = (r - r2)**2 + (g - g2)**2 + (b - b2)**2
        if diff < min_diff:
            min_diff = diff
            closest = name

    return closest


def translate_color_name(en_name: str) -> str:
    if en_name is None:
        return "desconhecida"

    name = en_name.lower()

    especiais = {
        "darkolivegreen": "verde oliva escuro",
        "darkslateblue": "azul ardósia escuro",
        "darkslategray": "cinza ardósia escuro",
        "darkseagreen": "verde mar escuro",
        "darkturquoise": "turquesa escuro",
        "darkviolet": "violeta escuro",
        "darkgoldenrod": "dourado escuro",
        "deepskyblue": "azul céu profundo",
        "dodgerblue": "azul dodger",
        "firebrick": "vermelho tijolo",
        "forestgreen": "verde floresta",
        "gainsboro": "gainsboro (cinza claro)",
        "ghostwhite": "branco fantasma",
        "honeydew": "honeydew (verde muito claro)",
        "indianred": "vermelho indiano",
        "lavenderblush": "lavanda rosada",
        "lavender": "lavanda",
        "lawngreen": "verde grama",
        "lemonchiffon": "amarelo chiffon",
        "lightsteelblue": "azul aço claro",
        "lightslategray": "cinza ardósia claro",
        "mediumseagreen": "verde mar médio",
        "mediumslateblue": "azul ardósia médio",
        "midnightblue": "azul meia-noite",
        "mistyrose": "rosa enevoado",
        "oldlace": "renda antiga",
        "olivedrab": "verde oliva pardo",
        "palegoldenrod": "dourado pálido",
        "paleturquoise": "turquesa pálido",
        "palevioletred": "vermelho violeta pálido",
        "peachpuff": "pêssego suave",
        "powderblue": "azul talco",
        "rosybrown": "marrom rosado",
        "royalblue": "azul royal",
        "saddlebrown": "marrom sela",
        "seagreen": "verde mar",
        "sandybrown": "marrom areia",
        "slateblue": "azul ardósia",
        "slategray": "cinza ardósia",
        "springgreen": "verde primavera",
        "steelblue": "azul aço",
        "whitesmoke": "fumaça branca",
        "yellowgreen": "amarelo esverdeado",
        "wheat": "trigo",
        "salmon": "salmão",
        "tomato": "vermelho tomate",
        "hotpink": "rosa choque",
        "lightgray": "cinza claro",
        "darkgray": "cinza escuro",
        "lightskyblue": "azul céu claro",
        "skyblue": "azul céu",
        "navy": "azul marinho",
        "olive": "verde oliva",
        "gold": "dourado",
    }
    if name in especiais:
        return especiais[name]

    COMPONENT_PT = {
        "red": "vermelho",
        "green": "verde",
        "blue": "azul",
        "yellow": "amarelo",
        "purple": "roxo",
        "violet": "violeta",
        "pink": "rosa",
        "orange": "laranja",
        "brown": "marrom",
        "black": "preto",
        "white": "branco",
        "gray": "cinza",
        "grey": "cinza",
        "gold": "dourado",
        "silver": "prata",
        "navy": "azul marinho",
        "olive": "verde oliva",
        "teal": "verde azulado",
        "aqua": "ciano",
        "cyan": "ciano",
        "magenta": "magenta",
        "coral": "coral",
    }

    MODIFIER_PT = {
        "light": "claro",
        "dark": "escuro",
        "medium": "médio",
        "deep": "profundo",
        "pale": "pálido",
        "royal": "royal",
        "hot": "vivo",
        "soft": "suave",
    }

    tokens = []
    i = 0
    all_keys = list(MODIFIER_PT.keys()) + list(COMPONENT_PT.keys())
    all_keys.sort(key=len, reverse=True)

    while i < len(name):
        matched = False
        for k in all_keys:
            if name.startswith(k, i):
                tokens.append(k)
                i += len(k)
                matched = True
                break
        if not matched:
            i += 1

    if not tokens:
        return en_name

    partes_pt = []
    vistos = set()
    for t in tokens:
        if t in MODIFIER_PT:
            pt = MODIFIER_PT[t]
        elif t in COMPONENT_PT:
            pt = COMPONENT_PT[t]
        else:
            pt = t
        if pt not in vistos:
            partes_pt.append(pt)
            vistos.add(pt)

    return " ".join(partes_pt)


# ---------------------------
# SOM: mapeamento Hue → nota
# ---------------------------
NOTAS = [
    261,  # C4
    277,  # C#4
    293,  # D4
    311,  # D#4
    329,  # E4
    349,  # F4
    369,  # F#4
    392,  # G4
    415,  # G#4
    440,  # A4
    466,  # A#4
    494,  # B4
]


def bgr_to_hex(bgr):
    b, g, r = int(bgr[0]), int(bgr[1]), int(bgr[2])
    return f"#{r:02X}{g:02X}{b:02X}"


def hue_from_bgr(bgr):
    bgr_1x1 = np.uint8([[bgr]])
    hsv = cv2.cvtColor(bgr_1x1, cv2.COLOR_BGR2HSV)[0, 0]
    return int(hsv[0]), hsv  # devolvo hue e o próprio hsv


def hue_to_note_freq(hue):
    idx = int((hue / 180.0) * len(NOTAS))
    if idx >= len(NOTAS):
        idx = len(NOTAS) - 1
    return NOTAS[idx]


def play_note_winsound(freq, dur_ms=600):
    if HAS_WINSOUND:
        winsound.Beep(freq, dur_ms)
    else:
        print(f"(winsound indisponível) Nota ~{freq} Hz")


def play_note_sounddevice(freq, dur=0.6):
    if not HAS_SD:
        print(f"(sounddevice indisponível) Nota ~{freq} Hz")
        return
    sr = 44100
    t = np.linspace(0, dur, int(sr * dur), False)
    wave = 0.3 * np.sin(2 * np.pi * freq * t)
    sd.play(wave, sr)
    sd.wait()


def play_color_sound(bgr):
    hue, _ = hue_from_bgr(bgr)
    freq = hue_to_note_freq(hue)

    if SOUND_MODE == 2:
        play_note_winsound(freq, dur_ms=700)  # um pouco mais longo
    elif SOUND_MODE == 3:
        play_note_sounddevice(freq, dur=0.6)
    else:
        print(f"SOUND_MODE inválido, freq ~{freq} Hz")


# --------------------
# Variáveis globais
# --------------------
frame_atual = None
mouse_x = 0
mouse_y = 0
mouse_inside = False
last_click_time = 0.0


def on_mouse(event, x, y, flags, userdata):
    global mouse_x, mouse_y, mouse_inside, frame_atual, last_click_time

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
        h, w, _ = frame_atual.shape
        if 0 <= x < w and 0 <= y < h:
            bgr = frame_atual[y, x]
            agora = time.time()
            if agora - last_click_time > 0.1:
                play_color_sound(bgr)
                last_click_time = agora


def main():
    global frame_atual

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro ao abrir a câmera.")
        return

    cv2.namedWindow(WINDOW_NAME)
    cv2.setMouseCallback(WINDOW_NAME, on_mouse)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (400, 400))
        frame_atual = frame

        h, w, _ = frame.shape
        placeholder = np.zeros((h, 400, 3), dtype=np.uint8)

        if mouse_inside:
            x, y = mouse_x, mouse_y
            bgr = frame[y, x]
            hue, hsv = hue_from_bgr(bgr)
            hex_code = bgr_to_hex(bgr)
            name_en = closest_color_name(hex_code)
            name_pt = translate_color_name(name_en)

            cv2.circle(frame, (x, y), 4, (0, 255, 0), 1)

            cv2.putText(
                placeholder,
                f"Pos: x={x} y={y}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                1,
            )
            cv2.putText(
                placeholder,
                f"BGR: {bgr.tolist()}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                1,
            )
            cv2.putText(
                placeholder,
                f"HSV: {hsv.tolist()}",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                1,
            )
            cv2.putText(
                placeholder,
                f"HEX: {hex_code}",
                (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                1,
            )
            cv2.putText(
                placeholder,
                f"Nome (EN): {sem_acentos(name_en)}",
                (20, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 200, 255),
                1,
            )
            cv2.putText(
                placeholder,
                f"Nome (PT): {sem_acentos(name_pt)}",
                (20, 240),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 200, 255),
                1,
            )
            cv2.putText(
                placeholder,
                f"Modo som: {SOUND_MODE} (clique = nota)",
                (20, 280),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (200, 200, 200),
                1,
            )

            cv2.rectangle(
                placeholder,
                (20, 310),
                (380, 380),
                (int(bgr[0]), int(bgr[1]), int(bgr[2])),
                -1,
            )

        combined = np.hstack((frame, placeholder))
        cv2.imshow(WINDOW_NAME, combined)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
