
# Mapeamento de Componentes Cromáticos em Sinais Sonoros Audíveis

Este repositório reúne o **Trabalho de Graduação** e **quatro versões funcionais de um sistema de sonificação de cores**, desenvolvidos por **Beatriz Grassi Pereira** e **Caio Henrique Falcheti Nunes**, no **Bacharelado de Engenharia de Informação da Universidade Federal do ABC (UFABC)**.

O projeto propõe um método de **conversão de cores em sons audíveis**, estabelecendo uma correspondência consistente entre atributos cromáticos e parâmetros sonoros, com aplicações em **acessibilidade**, **comunicação multimodal**, **educação** e **arte sonora**.

---

## Trabalho de Graduação

[Trabalho de Graduação](Trabalho de Graduação/TGIII_EngInfo_BeatrizGrassi_CaioNunes_Abril2026_v4.pdf)
  **Mapeamento de componentes cromáticos em sinais sonoros audíveis**  
  Universidade Federal do ABC – UFABC  
  Santo André – SP – Abril/2026  
  **Orientador:** Prof. Dr. Kenji Nose Filho

### Resumo
O trabalho apresenta uma aplicação capaz de capturar informações cromáticas (a partir de imagens ou webcam), converter essas cores para o modelo HSL e mapear seus atributos em sinais sonoros audíveis.  
A proposta estabelece as seguintes correspondências principais:

- **Matiz (Hue)** → frequência / nota musical  
- **Saturação (S)** → timbre (presença de harmônicos)  
- **Luminosidade (L)** → intensidade sonora (volume)

---

## Estrutura do Repositório

O repositório contém **quatro versões do código**, organizadas a partir de duas dimensões:

- **Tipo de entrada**
  - Imagem estática
  - Captura por webcam
- **Resolução do mapeamento sonoro**
  - 12 notas (1 oitava)
  - 36 notas (3 oitavas)

---

## Versões do Código

### Versões com **12 Notas Musicais (1 Oitava)**

Essas versões utilizam **12 frequências**, correspondentes às notas da **4ª oitava musical**.  
São mais simples do ponto de vista perceptual e adequadas para testes iniciais ou uso introdutório.

#### [inspeciona_cores_imagem_som_12notas.py](Codigos_FINAL/inspeciona_cores_imagem_som_12notas.py)


**Entrada:** imagem estática  

**Características:**
- Leitura de arquivos de imagem
- Captura da cor do pixel sob o cursor
- Conversão BGR → HSL e HEX
- Exibição:
  - Valores cromáticos
  - Código hexadecimal
  - Nome aproximado da cor
- Reproduz o som ao clique do mouse
- Gera gráficos das formas de onda

**Uso recomendado:**  
Testes controlados, escalas cromáticas e validação conceitual.

---

#### [inspeciona_cores_camera_som_12notas.py](Codigos_FINAL/inspeciona_cores_camera_som_12notas.py)
**Entrada:** captura em tempo real via webcam  

**Características:**
- Captura contínua de vídeo
- Inspeção de cor sob o cursor
- Sonificação em tempo real
- Sensível a variações de iluminação
- Mapeamento simples (12 notas)

**Uso recomendado:**  
Demonstrações rápidas e experimentos em ambientes reais.

---

### Versões com **36 Notas Musicais (3 Oitavas)**

Essas versões utilizam **36 frequências**, distribuídas pelas **3ª, 4ª e 5ª oitavas**, oferecendo **maior resolução cromática-sonora**.

#### [inspeciona_cores_imagem_som_36notas.py](Codigos_FINAL/inspeciona_cores_imagem_som_36notas.py)
**Entrada:** imagem estática  

**Características:**
- Leitura de imagens a partir de arquivo
- Conversão detalhada de cor
- Mapeamento cromático com maior discriminação sonora
- Reprodução de som + visualização das componentes da onda
- Interface gráfica com informações completas

**Uso recomendado:**  
Análises comparativas, testes perceptuais e experimentos acadêmicos.

---

#### [inspeciona_cores_camera_som_36notas.py](Codigos_FINAL/inspeciona_cores_camera_som_36notas.py)
**Entrada:** captura em tempo real via webcam  

**Características:**
- Conversão dinâmica de cores em som
- Maior sensibilidade a pequenas variações cromáticas
- Sons distribuídos em múltiplas oitavas
- Permite distinguir tons cromáticos próximos

**Uso recomendado:**  
Exploração interativa, aplicações artísticas e estudos avançados de sonificação.

---

## Estratégia de Mapeamento Cromático-Sonoro

| Atributo Visual | Parâmetro Sonoro |
|-----------------|------------------|
| Matiz (Hue) | Frequência / Nota musical |
| Saturação (S) | Timbre (harmônicos) |
| Luminosidade (L) | Volume (amplitude) |

- Cores mais saturadas → sons com maior complexidade harmônica  
- Cores mais claras → sons mais intensos  
- Tons próximos ao preto → sons de baixa amplitude  

---

## Programa e Bibliotecas Utilizadas

- **Python 3**
- **OpenCV (cv2)** – processamento e captura de imagens
- **NumPy** – manipulação numérica
- **Matplotlib** – visualização das formas de onda
- **SoundDevice** – síntese e reprodução sonora

---

## Vídeo de Demonstração

Abaixo está um vídeo curto demonstrando o funcionamento do sistema desenvolvido neste projeto.

No vídeo é possível observar:
- A interface gráfica do programa em execução
- A inspeção de cores a partir do cursor
- A conversão dos parâmetros cromáticos (HSL)
- A reprodução do som correspondente à cor selecionada
- A visualização das formas de onda geradas

[![Demonstração do sistema de mapeamento cromático-sonoro](https://img.youtube.com/vi/bMO6mAAcVAg/0.jpg)](https://www.youtube.com/watch?v=bMO6mAAcVAg)

Clique na imagem acima para assistir ao vídeo no YouTube.

Este vídeo complementa a documentação do projeto e ilustra, de forma visual e auditiva, os conceitos apresentados no Trabalho de Graduação e nas implementações em Python.

---

## Como Executar

1. Instale as dependências:
   ```bash
   pip install opencv-python numpy matplotlib sounddevice
2. Execute uma das versões:
    ```bash
   python inspeciona_cores_camera_som_12notas.py
   python inspeciona_cores_imagem_som_12notas.py
   python inspeciona_cores_camera_som_36notas.py
   python inspeciona_cores_imagem_som_36notas.py
4. Posicione o cursor sobre a cor desejada e clique com o botão esquerdo do mouse
5. Pressione ESC para encerrar o programa

---
## Observações Importantes

- O comportamento sonoro depende do equipamento de áudio
- Versões com webcam são sensíveis à iluminação ambiente
- O código é modular, permitindo:
-- Alterar número de notas
-- Modificar faixas de frequência
-- Adaptar os mapeamentos cromático-sonoros

---
## Autores

Beatriz Grassi Pereira
Caio Henrique Falcheti Nunes

Universidade Federal do ABC – UFABC
Bacharelado em Engenharia de Informação
