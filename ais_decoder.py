def sincronizar_ais_com_visao(t_frame, ais_log):
    # encontre a mensagem AIS mais próxima no tempo
    melhor = None
    menor_diferenca = float("inf")
    for t_ais, dados in ais_log:
        dif = abs(t_frame - t_ais)
        if dif < menor_diferenca:
            menor_diferenca = dif
            melhor = (t_ais, dados)
    return melhor  # retorna o par AIS mais próximo