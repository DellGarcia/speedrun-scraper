# Speedrun Scraper ⛏️

Este é um projeto desenvolvido durante o 4º Semestre do curso de Big Data.
A ideia é testar na prática os conceitos de Web Scraping em websites.

Escolhi realizar esse processo de Scraping no site [speedrun.com](https://www.speedrun.com/), esse é um site onde diversos speedrunners submetem suas runs em diversos jogos, dessa forma podem mostrar suas habilidades no jogo e até mesmo quebrar recordes. Speedruns são interessantes, pois crião diversas novas possibilidades de jogo, permitem obter um conhecimento mais profundo sobre o jogo, isso vale para os jogadores, para os desenvolvedores e até para quem assiste. 

## Escopo do projeto ☔

Para esse projeto defini que iria pegar os dados apenas de um jogo (Hollow Knight), a principio pensava em pegar alguns jogos, mas cada jogo além de ter variados tipos de categorias de speedrun, os dados no site também variam para cada jogo, categoria e/ou subcategoria. Então focando em apenas um jogo ficou mais fácil focar no processo de scraping e análise dos dados.


## Como configurar e testar 🔧

Basta criar um ambiente virtual para o projeto:
```
py -m venv <your_env_name> 
```

Ative o ambiente que deseja utilizar:
```
/env/Scripts/activate.ps1
```

E então basta instalar as dependecias
```
pip install -r requirements.txt
```

Com as dependecias instalas primeiro rode o arquivo data_scrapper.py, ele ira coletar os dados do jogo e armazenar os dados em uma estrutura de pastas.

Depois rode o arquivo data_analisys.py onde vai ser agragados os dados e feitas as analises.

Para visuliazar os resultados basta ir na pasta:

```bash
results/<game_name>/summary/
```

Explico com mais detalhes como cada etapa funciona na proxima secao onde explico como foi o desenvolvimentno do projeto.

## Desenvolvimento do projeto 📊

A linguagem de programação utilizada foi a linguagem python, pois é uma das mais utilizadas para esse tipo de trabalho e já possui uma série de funcionalidades e bibliotecas para auxiliar nesse processo.

O objetivo inicial do projeto era usar a biblioteca Beautiful Soup para coletar o conteudo das páginas, mas analisando a estrutura do site foi possivel notar que os dados são carregados de forma dinâmica, sabendo disso optei por usar a biblioteca do Selenium para esse projeto.

Tive de investir um tempo para estudar o Selenium, já que não tinha utilizado ele antes, mas até que foi tranquilo a documentação da bibliteca é boa e tem muitos tutoriais na internet.

Tive que refatorar o código algumas vezes também, a pricipio pensava em criar classes e seguir utilizando o paradimga orientado a objetos, mas o resultado não estava me agradando muito. Resolvi então utilizar uma abordagem de funções tentei quebrar cada tarefa em funções simples e acabou ficando mais simples de resolver o problema.

No código final o fluxo ficou o seguinte utilizando o selenium entro na página do jogo e coleto os links de todas as categorias de speedrun para aquele jogo, fazendo dessa forma consegui simplificar bastante a etapa de coleta dos dados. Os links são salvos juntamente com a hierarquia de pastas de destino na pasta game_links seguido a seguinte estrutura:

```bash
game_links/<game_name>/links.csv
```
Coletado os links agora partimos para a etapa de coleta dos dados, então basta ler o arquivo de links do jogo e coletador os dados da tabela para cada link.
Aqui utilizei alguns conceitos interessantes o primeiro foi pra resolver as paginações da tabela, para isso utilizei a funções recursivas, então basicamente vou pegando os dados de cada página até não ter mais páginas para pegar. O segundo ponto interresante foi que dei uma otimizada no processo separando em threads, no meu PC utilizei 4 threads e dividi os links iguamente entre essas threads isso ajudou a reduzir um pouco o tempo de coletar os dados. A custo de um pouco mais de processamento.
Para configuar o número de threads que vão rodar basta alterar o valor de <strong>NUM_THREADS</strong> no arquivo <strong>.env</strong>.

Feito o processo de coleta os dados serão salvos em uma hierarquia e de pastas seguindo o seguinte padrão:

```bash
games/<game_name>/<categorias>/<subcategorias>/<page>.csv
```
Agora então partimos para a parte final que é agregar todos esse dados em um único arquivo e fazer algumas análises em cima disso.
E é isso que ocorre no arquivo <strong>data_analisys.py</strong> os dados são agregados e são gerados alguns graficos, que ficam armazenados na seguinte pasta:
```bash
results/<game_name>/summary/
```

Sobre o desenvolvimento do projeto é isso, foi um projeto bem legal pude aprender uma série de coisas novas e também aplicar conhecimentos que adquiri em outras disciplinas.


