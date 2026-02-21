import pygame
import random

pygame.init()

# Dimensões da tela
LARGURA = 600
ALTURA = 400

# Configuração da tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Ping Pong")

# Dimensões das raquetes e bola
RAQUETE_LARGURA = 15
RAQUETE_ALTURA = 90
BOLA_TAM = 15

# Criação das raquetes e bola
r1 = pygame.Rect(40, ALTURA // 2 - RAQUETE_ALTURA // 2, RAQUETE_LARGURA, RAQUETE_ALTURA)
r2 = pygame.Rect(LARGURA - 40 - RAQUETE_LARGURA, ALTURA // 2 - RAQUETE_ALTURA // 2, RAQUETE_LARGURA, RAQUETE_ALTURA)
bola = pygame.Rect(LARGURA // 2 - BOLA_TAM // 2, ALTURA // 2 - BOLA_TAM // 2, BOLA_TAM, BOLA_TAM)

# Constantes de cor
VERDE_MESA = (34, 139, 34)
BRANCO = (255, 255, 255)
AZUL = (30, 114, 225)
VERMELHO = (220, 20, 60)
PRETO = (0, 0, 0)

# Velocidade da bola e raquetes
veloc_bola = [4, 6]
VELOC_RAQUETE = 5

# Fontes
fonte = pygame.font.SysFont("Arial", 40, bold=True)
fonte_grande = pygame.font.SysFont("Arial", 50, bold=True)

# Estados do jogo
tela_inicial = True
jogo_ativo = False
vencedor_final = None

# Placar
placar1, placar2 = 0, 0

# Função para desenhar a mesa
def desenhar_mesa():
    tela.fill(VERDE_MESA)
    pygame.draw.line(tela, BRANCO, (20, 20), (LARGURA - 20, 20), 5)  # Linha superior
    pygame.draw.line(tela, BRANCO, (20, ALTURA - 20), (LARGURA - 20, ALTURA - 20), 5)  # Linha inferior
    pygame.draw.line(tela, BRANCO, (20, 20), (20, ALTURA - 20), 5)  # Linha esquerda
    pygame.draw.line(tela, BRANCO, (LARGURA - 20, 20), (LARGURA - 20, ALTURA - 20), 5)  # Linha direita
    pygame.draw.line(tela, BRANCO, (LARGURA // 2, 20), (LARGURA // 2, ALTURA - 20), 3)  # Linha central

# Função para desenhar o jogo
def desenhar_jogo():
    desenhar_mesa()
    pygame.draw.rect(tela, AZUL, r1)
    pygame.draw.rect(tela, VERMELHO, r2)
    pygame.draw.ellipse(tela, PRETO, bola)
    texto1 = fonte.render(str(placar1), True, BRANCO)
    texto2 = fonte.render(str(placar2), True, BRANCO)
    tela.blit(texto1, (LARGURA // 4 - texto1.get_width() // 2, 20))
    tela.blit(texto2, (3 * LARGURA // 4 - texto2.get_width() // 2, 20))

# Função para desenhar a tela inicial
def desenhar_tela_inicial():
    tela.fill(PRETO)
    titulo = fonte_grande.render("Ping Pong", True, BRANCO)
    cor_botao = AZUL
    botao_texto = fonte.render("Play", True, BRANCO)
    botao_rect = pygame.Rect(
        LARGURA // 2 - botao_texto.get_width() // 2 - 20,
        200 - 10,
        botao_texto.get_width() + 40,
        botao_texto.get_height() + 20
    )
    pygame.draw.rect(tela, cor_botao, botao_rect, border_radius=10)
    tela.blit(botao_texto, (LARGURA // 2 - botao_texto.get_width() // 2, 200))
    tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 100))
    return botao_rect

# Função para desenhar a tela de vencedor
def desenhar_vencedor():
    tela.fill(PRETO)
    titulo = fonte_grande.render(f"Jogador {vencedor_final} venceu!", True, BRANCO)
    tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 100))
    cor_botao = AZUL
    botao_texto = fonte.render("Reiniciar", True, BRANCO)
    botao_rect = pygame.Rect(
        LARGURA // 2 - botao_texto.get_width() // 2 - 20,
        250 - 10,
        botao_texto.get_width() + 40,
        botao_texto.get_height() + 20
    )
    pygame.draw.rect(tela, cor_botao, botao_rect, border_radius=10)
    tela.blit(botao_texto, (LARGURA // 2 - botao_texto.get_width() // 2, 250))
    return botao_rect

# Função para mover as raquetes
def mover_raquete():
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w] and r1.top > 20:
        r1.y -= VELOC_RAQUETE
    if teclas[pygame.K_s] and r1.bottom < ALTURA - 20:
        r1.y += VELOC_RAQUETE
    if teclas[pygame.K_UP] and r2.top > 20:
        r2.y -= VELOC_RAQUETE
    if teclas[pygame.K_DOWN] and r2.bottom < ALTURA - 20:
        r2.y += VELOC_RAQUETE

# Função para mover a bola
def mover_bola():
    global placar1, placar2
    bola.x += veloc_bola[0]
    bola.y += veloc_bola[1]
    if bola.colliderect(r1):
        veloc_bola[0] = abs(veloc_bola[0])
    if bola.colliderect(r2):
        veloc_bola[0] = -abs(veloc_bola[0])
    if bola.top <= 20 or bola.bottom >= ALTURA - 20:
        veloc_bola[1] = -veloc_bola[1]
    if bola.left <= 20:
        placar2 += 1
        resetar_bola(1)
    if bola.right >= LARGURA - 20:
        placar1 += 1
        resetar_bola(-1)

# Função para resetar a bola
def resetar_bola(direcao):
    bola.center = (LARGURA // 2, ALTURA // 2)
    veloc_bola[0] = 4 * direcao
    veloc_bola[1] = random.choice([-6, 6])

# Função para reiniciar o jogo
def reiniciar_jogo():
    global placar1, placar2, vencedor_final, tela_inicial, jogo_ativo
    r1.y = ALTURA // 2 - RAQUETE_ALTURA // 2
    r2.y = ALTURA // 2 - RAQUETE_ALTURA // 2
    resetar_bola(1)
    placar1, placar2 = 0, 0
    vencedor_final = None
    jogo_ativo = True

# Relógio para controlar o FPS
relogio = pygame.time.Clock()

# Inicializar o botão fora do loop
botao_rect = pygame.Rect(0, 0, 0, 0)

# Loop principal do jogo
rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if tela_inicial and botao_rect.collidepoint(event.pos):
                tela_inicial = False
                jogo_ativo = True
                reiniciar_jogo()
            elif not jogo_ativo and vencedor_final and botao_rect.collidepoint(event.pos):
                reiniciar_jogo()

    if tela_inicial:
        botao_rect = desenhar_tela_inicial()
    elif jogo_ativo:
        mover_raquete()
        mover_bola()
        desenhar_jogo()
        if placar1 >= 10:
            vencedor_final = "Azul"
            jogo_ativo = False
        elif placar2 >= 10:
            vencedor_final = "Vermelho"
            jogo_ativo = False
    elif not jogo_ativo and vencedor_final:
        botao_rect = desenhar_vencedor()

    pygame.display.update()
    relogio.tick(60)