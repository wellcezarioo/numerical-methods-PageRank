# Roteiro de fala — Método das Potências e o PageRank

Equipe: Wellington Cezario, Antonio Rodrigo e Másio César.

Divisão: Wellington apresenta o método numérico (slides 1–8), Antonio a aplicação real, o PageRank (slides 9–11), e Másio a implementação e a solução em Python (slides 12–19).

Duração estimada da fala: cerca de 18 minutos, dentro do limite de 20 minutos.

Slides: deck “Método das Potências e o PageRank” (exportável em PDF/PowerPoint). Os gráficos dos slides são gerados por `apresentacao/graficos_slides.py`.

## Slide 1 — Método das Potências

*Wellington Cezario · cerca de 30 s*

Boa tarde. Nosso tema é o cálculo de autovalores e autovetores pelo Método das Potências.

A apresentação tem três partes. Eu começo com o método numérico: a ideia, o algoritmo, um exemplo e quando ele funciona. O Antonio mostra um problema real em que ele é a peça central: o PageRank, o algoritmo que o Google usou para ordenar páginas. E o Másio mostra nossa implementação em Python, aplicada a um grafo real com 281 mil páginas.

## Slide 2 — Uma busca encontra milhares de páginas. Qual delas mostrar primeiro?

*Wellington Cezario · cerca de 45 s*

Quando digitamos uma busca, existem milhares de páginas que contêm aquelas palavras. O problema é decidir a ordem. Contar quantas vezes a palavra aparece é fácil de manipular. A ideia de Brin e Page, em 1998, foi usar a estrutura de links: uma página é importante se páginas importantes apontam para ela.

Essa definição é circular, e é justamente por isso que ela vira um problema de autovetor. Para resolvê-lo numa matriz com milhões ou bilhões de linhas, a ferramenta é o Método das Potências. Então vamos começar pelo método.

## Slide 3 — Autovetor: a direção que a matriz apenas estica

*Wellington Cezario · cerca de 50 s*

Relembrando: um autovetor v de uma matriz A é uma direção que a matriz não gira. Ao multiplicar A por v, o resultado é o próprio v multiplicado por um número, λ, o autovalor.

Uma matriz n por n tem n autovalores. Chamamos de dominante aquele de maior módulo, λ₁, com |λ₁| estritamente maior que |λ₂|. O Método das Potências encontra exatamente esse par: o autovalor dominante e seu autovetor.

Pelo caminho tradicional, resolveríamos o polinômio característico, que é inviável para matrizes grandes. O método das potências evita isso e usa só multiplicações de matriz por vetor.

## Slide 4 — Multiplicar muitas vezes por A destaca o autovetor dominante

*Wellington Cezario · cerca de 1 min 20 s (3 cliques revelam as linhas)*

Esta é a ideia central. Supondo que os autovetores formam uma base, qualquer vetor inicial x₀ pode ser escrito como combinação deles, com coeficientes c₁ até cₙ.

[clique] Quando multiplicamos por A, cada autovetor é multiplicado pelo seu autovalor. Depois de k multiplicações, cada termo carrega λᵢ elevado a k.

[clique] Colocando c₁λ₁ᵏ em evidência, sobra v₁ mais uma soma em que cada termo tem a razão λᵢ/λ₁ elevada a k.

[clique] Como λ₁ é o dominante, todas essas razões têm módulo menor que 1. Elevadas a k, vão a zero. Depois de muitas multiplicações, o vetor aponta na direção de v₁.

A rapidez depende do termo que demora mais a sumir, o de λ₂. O erro diminui como |λ₂/λ₁| elevado a k. Guardem essa razão, porque ela volta no PageRank.

## Slide 5 — Multiplicar, estimar λ, normalizar e repetir

*Wellington Cezario · cerca de 1 min 15 s*

Na prática, o algoritmo é curto. Partimos de um vetor x, por exemplo só de uns. A cada iteração, multiplicamos por A. A componente de maior módulo do resultado é a estimativa do autovalor. Dividimos o vetor por ela, o que mantém a maior componente igual a 1.

Essa normalização é necessária: sem ela, o vetor cresce como λ₁ elevado a k e estoura a representação em ponto flutuante, ou vai a zero se |λ₁| for menor que 1.

Paramos quando duas coisas estabilizam: a estimativa de λ e o próprio vetor. Daqui a pouco mostramos por que olhar só para λ não basta.

O ponto mais importante: cada iteração é um único produto de matriz por vetor. Não fatoramos nem invertemos A. Para uma matriz esparsa, isso é muito barato.

## Slide 6 — Exemplo 3×3: 38 iterações e 11 casas decimais corretas

*Wellington Cezario · cerca de 1 min 15 s*

Um exemplo pequeno, para conferir. Esta matriz simétrica 3 por 3, partindo do vetor de uns.

Na primeira iteração, A vezes (1, 1, 1) dá (6, 6, 8). A maior componente é 8, então λ ≈ 8 e o vetor normalizado é (0,75; 0,75; 1). Na segunda, a estimativa cai para 7,25, depois 7,03, e vai se aproximando.

Com tolerância 10⁻¹², o método para na iteração 38, com λ = 6,895106515929. O numpy.linalg.eig dá 6,895106515928: a diferença está na décima segunda casa. O autovetor também coincide, e o resíduo Av − λv é da ordem de 10⁻¹².

Aqui a razão |λ₂/λ₁| é cerca de 0,49, então cada iteração reduz o erro mais ou menos pela metade. No próximo slide, o que acontece quando essa razão muda.

## Slide 7 — |λ₂/λ₁| decide quantas iterações são necessárias

*Wellington Cezario · cerca de 1 min*

Para ver o efeito dessa razão, montamos matrizes 5 por 5 com autovalores conhecidos: λ₁ sempre 10 e só λ₂ mudando. O gráfico mostra o erro em escala logarítmica.

Cada curva é praticamente uma reta, e a inclinação é o logaritmo da razão |λ₂/λ₁|. Com razão 0,2, convergimos em 22 iterações. Com 0,5, em 48. Com 0,8, em 141. Com 0,95, são 581.

Conclusão: o método é ótimo quando o autovalor dominante se destaca e fica lento quando o segundo está próximo dele.

## Slide 8 — Limites do método e como contorná-los

*Wellington Cezario · cerca de 1 min 15 s*

O método tem limites. Se houver dois autovalores com o mesmo módulo, como λ e −λ, a sequência não converge. Se a razão estiver perto de 1, fica lento, como acabamos de ver. Em teoria, se o vetor inicial não tiver componente na direção de v₁, o método não o encontra, mas na prática o arredondamento quase sempre introduz essa componente. E ele encontra só o dominante.

Para outros autovalores existe a variação inversa: aplicar o mesmo método à inversa de A − σI. Os autovalores dela são 1/(λᵢ − σ), então o dominante corresponde ao λ mais próximo de σ. Na implementação, fatoramos LU uma vez e resolvemos um sistema por iteração. Na nossa matriz, com σ = 3, obtemos 3,397295; com σ = 0, o menor autovalor, 1,707598.

Um aprendizado da implementação: a primeira versão parava só quando λ deixava de mudar. Com σ = 3, duas estimativas consecutivas coincidiram por acaso e o método parou em 3,4, errado. Por isso o critério final exige que o vetor também estabilize.

Passo agora para o Antonio, que mostra onde isso é usado de verdade.

## Slide 9 — O navegador aleatório

*Antonio Rodrigo · cerca de 1 min 15 s*

Obrigado, Wellington. Agora, o problema real. O PageRank modela um navegador aleatório. Ele está numa página e, com probabilidade α, normalmente 0,85, clica num dos links dela, escolhido ao acaso. Com probabilidade 0,15, ele se cansa e pula para uma página qualquer.

A importância de cada página é a fração do tempo que esse navegador passa nela depois de muito tempo navegando.

Para explicar, usamos esta mini-web de seis páginas. As setas são links. Dois casos especiais: Contato, em laranja, não tem link de saída; nesse caso o navegador pula para qualquer página. E ninguém aponta para Arquivo: ela só recebe visitas pelo salto aleatório.

Esse passeio é uma cadeia de Markov, e a distribuição de longo prazo é justamente um autovetor.

## Slide 10 — O PageRank é o autovetor dominante da matriz de Google

*Antonio Rodrigo · cerca de 1 min 20 s (3 cliques revelam os cartões)*

Em forma de matriz: S é a matriz de links. A coluna j distribui a probabilidade igualmente entre as páginas para onde j aponta. Para uma página sem links, a coluna é toda 1/n. A matriz de Google é α vezes S mais (1 − α)/n vezes uma matriz só de uns, que representa o salto aleatório.

O vetor de PageRank π satisfaz Gπ = π: π é um autovetor de G com autovalor 1.

Três propriedades fazem do Método das Potências a escolha natural.

[clique] Cada coluna de G soma 1, então o autovalor dominante é exatamente 1.

[clique] Todas as entradas são positivas, e pelo teorema de Perron–Frobenius esse autovetor é único e tem todas as componentes positivas: o ranking está bem definido.

[clique] Haveliwala e Kamvar mostraram em 2003 que |λ₂| ≤ α. Como o erro cai como |λ₂/λ₁|ᵏ e λ₁ = 1, a convergência é pelo menos 0,85ᵏ, independentemente do tamanho da web.

## Slide 11 — Mini-web: o método reproduz o resultado do eig

*Antonio Rodrigo · cerca de 1 min*

Aplicando o método à mini-web, o autovalor encontrado é 1, como a teoria prevê, e o vetor, normalizado para somar 1, dá o ranking.

Home fica em primeiro, com cerca de um terço da importância: ela recebe links de Notícias, Esportes e Blog. Arquivo fica em último: ninguém aponta para ela, então só recebe visitas pelo salto aleatório.

Comparando com o numpy.linalg.eig, a diferença máxima entre os vetores é de 3,5·10⁻¹⁴, praticamente a precisão de máquina.

Com seis páginas, qualquer método serve. A pergunta é o que acontece com uma web de verdade. Para isso, passo para o Másio, com a implementação.

## Slide 12 — O núcleo cabe em 15 linhas de Python

*Másio César · cerca de 1 min*

Obrigado, Antonio. Agora, a implementação. Tudo está em Python, com NumPy e SciPy, no repositório do grupo.

Este é o núcleo da função metodo_potencias, simplificado. Partimos do vetor de uns. Em cada iteração: um produto A @ x, que é o único custo relevante; a componente de maior módulo como estimativa de λ; a normalização; e o critério de parada, que olha tanto a variação de λ quanto a variação do vetor, pelo problema que o Wellington mostrou.

O detalhe importante é que a função só usa A @ x. Por isso ela aceita uma matriz NumPy, uma matriz esparsa ou um LinearOperator, que é o que vamos usar para a web real.

(Versão completa, com a opção de norma 2 e a potência inversa, em metodo_potencias.py.)

## Slide 13 — Na web real, G nunca é montada: só os links

*Másio César · cerca de 1 min 20 s*

O ponto principal: para a web real não montamos a matriz G, porque ela é densa. O salto aleatório põe um valor em todas as posições. Em vez disso, guardamos só a matriz de links H, que é esparsa, e escrevemos uma função que calcula G vezes x diretamente: α vezes H x, mais um termo constante que soma a contribuição das páginas sem links e do salto aleatório.

O LinearOperator do SciPy faz essa função se comportar como uma matriz. Assim, a mesma função metodo_potencias do exemplo 3 por 3 funciona aqui sem nenhuma mudança, porque ela só precisa do produto A vezes x.

O custo de cada iteração é proporcional ao número de links, e não ao quadrado do número de páginas.

## Slide 14 — Por que não usar o numpy.linalg.eig?

*Másio César · cerca de 1 min*

Uma pergunta natural é: por que não usar a função pronta do numpy? Comparamos as duas em redes aleatórias de tamanhos crescentes.

O eig denso calcula todos os autovalores e trabalha com a matriz cheia: o custo cresce com n ao cubo. Dobrando de mil para dois mil páginas, o tempo passou de menos de 1 para cerca de 4 segundos. O Método das Potências ficou na casa do milissegundo em todos os casos, e os dois vetores coincidem até 10⁻¹⁴.

(Os tempos variam com o computador; os da tabela são de uma execução do nosso código.)

Ressalva justa: o eig resolve um problema maior, porque entrega todos os autovalores. Mas para o PageRank só precisamos de um. E com n na casa das centenas de milhares, o eig nem chega a rodar, como vamos ver agora.

## Slide 15 — A web real da Universidade de Stanford

*Másio César · cerca de 1 min*

Para o problema real, usamos um conjunto de dados público do projeto SNAP, de Stanford: o grafo de links do domínio da Universidade de Stanford coletado em 2002. São 281.903 páginas e 2,3 milhões de links.

Se montássemos a matriz G cheia, em precisão dupla, seriam 636 gigabytes. A matriz de links esparsa ocupa 29 megabytes.

Com α = 0,85, o método convergiu em 125 iterações, em cerca de um segundo. Para conferir, calculamos o mesmo autovetor com o ARPACK, pela função eigs do SciPy, que usa outro algoritmo, o de Arnoldi. A diferença máxima entre os dois vetores foi de 5·10⁻¹³.

## Slide 16 — Na web real, o erro cai como αᵏ

*Másio César · cerca de 1 min*

Este gráfico conecta a teoria da primeira parte com o problema real. Variamos α e medimos o erro a cada iteração. As linhas tracejadas são α elevado a k.

As curvas medidas são paralelas às tracejadas: a taxa de convergência é exatamente α. Isso indica que, nesse grafo, o segundo autovalor tem módulo igual a α, o pior caso permitido pelo resultado de Haveliwala e Kamvar.

Na prática há um compromisso. Com α = 0,5 bastam 30 iterações, mas o navegador pula aleatoriamente metade do tempo e o ranking reflete pouco os links. Com α = 0,99 o ranking segue quase só os links, mas são 2.039 iterações. O valor 0,85, proposto por Brin e Page, fica no meio: 125 iterações.

## Slide 17 — Importa quem aponta para você, não só quantos

*Másio César · cerca de 45 s*

Um resultado do ranking mostra por que o PageRank não é só contar links. A quarta página mais importante de Stanford, segundo o PageRank, é apenas a 96ª em número de links recebidos: tem 1.802. Várias páginas têm dez, vinte ou até 38 mil links e ficam acima ou abaixo dela.

Isso acontece porque um link vale mais quando vem de uma página importante e com poucos links de saída. É a definição circular do começo, resolvida como um autovetor.

## Slide 18 — O que o Método das Potências entrega

*Másio César · cerca de 1 min*

Para fechar, três pontos.

Primeiro, o Método das Potências só precisa de produtos de matriz por vetor. Por isso funciona onde métodos diretos não cabem: matrizes enormes e esparsas.

Segundo, a convergência é previsível: o erro cai como |λ₂/λ₁| elevado a k. No PageRank, essa razão é limitada por α, o que dá uma garantia independente do tamanho da web. Vimos isso no gráfico.

Terceiro, ele resolve o problema real: o ranking de 281 mil páginas em cerca de um segundo, conferido com dois métodos independentes.

E os limites: encontra um autovalor por vez e fica lento quando o segundo autovalor está perto do primeiro. Para esses casos existem as variações inversa e com deslocamento, e métodos como QR e Arnoldi.

O código e os dados estão no repositório do grupo. Obrigado.

## Slide 19 — Perguntas?

*Perguntas: responde quem apresentou a parte relacionada.*

Por que α = 0,85? É o valor sugerido por Brin e Page. Equilibra a fidelidade aos links com a velocidade de convergência, que é αᵏ. (Antonio)

E se o grafo tiver páginas sem links? Viram colunas 1/n: o navegador pula para qualquer página. No código, isso entra no termo constante do produto G·x. (Másio)

Por que não o método QR? O QR calcula todos os autovalores e trabalha com a matriz densa, O(n³). Para o PageRank só precisamos de um autovetor. (Wellington)

O vetor inicial importa? Para o PageRank, não: o autovetor é único e positivo, e qualquer vetor positivo converge. Usamos o vetor de uns. (Wellington)

Dados: J. Leskovec, K. Lang, A. Dasgupta, M. Mahoney. Community Structure in Large Networks. Internet Mathematics 6(1), 2009 (SNAP).
