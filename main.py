import cv2
from matplotlib import pyplot as plt
import numpy as np


cap = cv2.VideoCapture('pedra-papel-tesoura.mp4')

result = 0
placar_1 = 0
placar_2 = 0

pedra_template_esquerda = cv2.imread('pedra_esquerda.png', 0)
papel_template_esquerda = cv2.imread('papel_esquerda.png', 0)
tesoura_template_esquerda = cv2.imread('tesoura_esquerda.png', 0)

pedra_template_direita = cv2.imread('pedra_direita.png', 0)
papel_template_direita = cv2.imread('papel_direita.png', 0)
tesoura_template_direita = cv2.imread('tesoura_direita.png', 0)

jogada_1_anterior = None
jogada_2_anterior = None

# Função para realizar correspondência de modelo do template na mão esquerda.


def detect_jogada(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    res_pedra = cv2.matchTemplate(
        gray, pedra_template_esquerda, cv2.TM_CCOEFF_NORMED)
    res_papel = cv2.matchTemplate(
        gray, papel_template_esquerda, cv2.TM_CCOEFF_NORMED)
    res_tesoura = cv2.matchTemplate(
        gray, tesoura_template_esquerda, cv2.TM_CCOEFF_NORMED)

    max_pedra = cv2.minMaxLoc(res_pedra)[1]
    max_papel = cv2.minMaxLoc(res_papel)[1]
    max_tesoura = cv2.minMaxLoc(res_tesoura)[1]

    vars_dict = {'pedra': max_pedra,
                 'papel': max_papel, 'tesoura': max_tesoura}
    max_var = max(vars_dict, key=vars_dict.get)
    return max_var

# Função para realizar correspondência de modelo do template na mão direita.


def detect_jogada_2(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    res_pedra = cv2.matchTemplate(
        gray, pedra_template_direita, cv2.TM_CCOEFF_NORMED)
    res_papel = cv2.matchTemplate(
        gray, papel_template_direita, cv2.TM_CCOEFF_NORMED)
    res_tesoura = cv2.matchTemplate(
        gray, tesoura_template_direita, cv2.TM_CCOEFF_NORMED)

    max_pedra = cv2.minMaxLoc(res_pedra)[1]
    max_papel = cv2.minMaxLoc(res_papel)[1]
    max_tesoura = cv2.minMaxLoc(res_tesoura)[1]

    vars_dict = {'pedra': max_pedra,
                 'papel': max_papel, 'tesoura': max_tesoura}
    max_var = max(vars_dict, key=vars_dict.get)
    return max_var


# Uma função responsável por comparar a jogada 1 e jogada 2 e determinar qual jogador é o vencedor.
def comparar_jogadas(jogada_1, jogada_2, placar_1, placar_2):
    result = None
    if jogada_1 == jogada_2:
        result = 0

    elif (
        (jogada_1 == 'pedra' and jogada_2 == 'tesoura') or
        (jogada_1 == 'tesoura' and jogada_2 == 'papel') or
        (jogada_1 == 'papel' and jogada_2 == 'pedra')
    ):
        placar_1 += 1
        result = -1

    else:
        placar_2 += 1
        result = 1

    return placar_1, placar_2, result


# Loop principal
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (700, 500))

    jogada_1 = detect_jogada(frame)
    jogada_2 = detect_jogada_2(frame)

    if jogada_1 is not None:
        cv2.putText(frame, jogada_1, (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    if jogada_2 is not None:
        cv2.putText(frame, jogada_2, (500, 49),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    if jogada_1_anterior != jogada_1 or jogada_2_anterior != jogada_2:
        placar_1, placar_2, result = comparar_jogadas(
            jogada_1, jogada_2, placar_1, placar_2)

        jogada_1_anterior = jogada_1
        jogada_2_anterior = jogada_2

    meio_tela = int(frame.shape[1] * 0.25)

# Uma função que exibe na tela o vencedor da rodada.
    if result == 0:
        cv2.putText(frame, "Empate!", (meio_tela, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
    elif result == -1:
        cv2.putText(frame, "Jogador Esquerda ganhou!", (meio_tela,
                    150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
    elif result == 1:
        cv2.putText(frame, "Jogador Direita ganhou!", (meio_tela, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    cv2.putText(frame, f"Placar: (Jogador da Esquerda) {placar_1} - {placar_2} (Jogador da Direita)", (
        50, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    cv2.imshow('frame', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
