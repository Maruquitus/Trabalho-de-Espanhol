# Trabalho de Espanhol 
Desenvolvido para um trabalho em grupo, onde cada equipe deveria fazer um jogo com o tema determinado, no caso, verbos terminados em AR do espanhol.
Front-end feito por <a href="https://www.github.com/GuilhermePain">@GuilhermePain</a>.
Back-end utilizando Flask e JSON.

## Códigos
### conjugador.py
Conjuga os verbos terminados em AR na pessoa (começando do zero) e número (singular ou plural) especificados. Também é capaz de gerar uma lista com as conjugações possíveis de um verbo.
![image](https://github.com/Maruquitus/Trabalho-de-Espanhol/assets/58173530/77a45304-ef40-4f30-90e3-b94a1bd712c3)
![image](https://github.com/Maruquitus/Trabalho-de-Espanhol/assets/58173530/cf302231-c267-4053-bd7e-3ebec9f0f202)

### app.py
Inicia o servidor do Flask para rodar o jogo.

<h3>Tela de introdução</h3>
<p>Apenas apresenta o tema e dá boas vindas ao jogador, voltar a esta tela também reseta o jogo.</p>

![image](https://github.com/Maruquitus/Trabalho-de-Espanhol/assets/58173530/77f8759b-9c5c-42fe-9f79-4ec85d1ff0b5)

<h3>Explicação</h3>
<p>Contém uma tabela com os pronomes pessoais e suas respectivas conjugações no Espanhol.</p>

![image](https://github.com/Maruquitus/Trabalho-de-Espanhol/assets/58173530/5e4ab640-3691-4e35-bee0-18b6ef033a12)

<h3>Questão</h3>
<p>Tela que exibe questões aleatoriamente para responder, existem dois tipos: as de completar com a conjugação adequada e as de verdadeiro ou falso. A tela também contém botões para navegar entre as questões já vistas e um contador de acertos no canto superior direito.</p>

![image](https://github.com/Maruquitus/Trabalho-de-Espanhol/assets/58173530/73880c82-763d-42a2-9d4c-5a3eea67582e)
![image](https://github.com/Maruquitus/Trabalho-de-Espanhol/assets/58173530/a2b01974-9336-484b-b986-2d2aca3f41c5)

<h3>Resultados</h3>
<p>Depois de responder a 15ª questão, os resultados de seus acertos são exibidos nessa tela.</p>

![image](https://github.com/Maruquitus/Trabalho-de-Espanhol/assets/58173530/a6ab4b0b-4ec9-43fe-a6d9-68bf1b2c0dc6)


