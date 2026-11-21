# Roteiro de fala — Método das Potências e o PageRank

Equipe: Másio César, Antonio Rodrigo e Wellington Cezario.

Duração estimada da fala: cerca de 17 minutos (130 palavras por minuto), dentro do limite de 20 minutos.

## Slide 1 — Método das Potências

*Másio César · cerca de 30 s*

Boa tarde. Nosso trabalho é sobre o Método das Potências, um método numérico para calcular autovalores e autovetores.

Vamos fazer em três partes. Eu explico como o método funciona e mostro uma conta passo a passo. O Antonio mostra quando ele converge rápido ou devagar e onde ele é usado de verdade: no PageRank, o sistema que o Google usou para ordenar páginas. E o Wellington mostra o nosso programa em Python resolvendo um caso real, com 281 mil páginas.

## Slide 2 — Uma busca encontra milhares de páginas. Qual delas mostrar primeiro?

*Másio César · cerca de 30 s*

Quando você pesquisa algo no Google, milhares de páginas têm aquelas palavras. Qual mostrar primeiro?

A ideia do Google foi: uma página é importante se outras páginas importantes apontam para ela. Isso vira uma conta com uma matriz enorme, e a resposta é um autovetor dessa matriz. O jeito de calcular esse autovetor é o Método das Potências. Então vamos entender o método.

> **Para entender:** aqui não precisa explicar o PageRank, o Antonio faz isso. Este slide só mostra por que o assunto importa.

## Slide 3 — Autovetor: a direção que a matriz apenas estica

*Másio César · cerca de 40 s*

Primeiro, o que é um autovetor. Quando multiplicamos uma matriz A por um vetor, normalmente o vetor muda de direção. Mas existem direções especiais em que isso não acontece: o vetor só fica maior ou menor. Essas direções são os autovetores. O número que diz quanto o vetor esticou é o autovalor, o λ. Por isso escrevemos A v = λ v.

Uma matriz tem vários autovalores. O maior deles, em valor absoluto, chamamos de autovalor dominante, λ₁. É ele que o Método das Potências encontra, junto com o seu autovetor.

> **Para entender:** pense na matriz A como uma máquina que transforma vetores. Quase todo vetor sai da máquina apontando para outro lado. O autovetor é o vetor que sai apontando para o mesmo lado, só que maior ou menor. Se A·v = 3·v, então v é autovetor e λ = 3.
>
> **Se perguntarem por que não calcular direto:** o jeito dos livros é resolver det(A − λI) = 0, que vira um polinômio de grau n. Para matrizes grandes isso é impraticável. O Método das Potências só faz multiplicações.

## Slide 4 — Multiplicar muitas vezes por A destaca o autovetor dominante

*Másio César · cerca de 1 min 20 s*

Agora, a ideia do método. Pegamos um vetor inicial qualquer, x₀. Ele pode ser escrito como uma combinação linear dos autovetores: c₁v₁ + c₂v₂ + … + cₙvₙ.

Quando multiplicamos por A, cada termo é multiplicado pelo seu autovalor. Se multiplicarmos k vezes, cada termo fica multiplicado pelo seu autovalor elevado a k.

Como λ₁ é o maior, o termo de v₁ cresce mais rápido que todos os outros. Na fórmula, colocamos λ₁ᵏ em evidência, e os outros termos ficam com a fração λᵢ/λ₁ elevada a k. Essas frações são menores que 1, então, elevadas a k, vão para zero. No fim, sobra só a direção de v₁.

A velocidade depende da fração λ₂/λ₁: quanto menor ela, mais rápido os outros termos somem. O erro cai como |λ₂/λ₁| elevado a k.

Isso vale com duas condições: os autovetores precisam formar uma base, para dar para escrever x₀ como essa combinação linear, e o coeficiente c₁ não pode ser zero.

> **Para entender, com números:** se λ₁ = 10 e λ₂ = 5, a fração é 0,5. Depois de 10 multiplicações, o termo de v₂ ficou com 0,5¹⁰ ≈ 0,001 do tamanho do termo de v₁: praticamente sumiu. É como uma corrida em que um corredor é duas vezes mais rápido: depois de muitas voltas, só ele aparece na frente.
>
> **Se perguntarem "e se c₁ = 0?":** na teoria o método falha. Na prática, o arredondamento do computador cria uma pequena componente na direção de v₁, e ele acaba aparecendo.

## Slide 5 — O algoritmo: multiplicar e normalizar

*Másio César · cerca de 1 min*

Na prática, o algoritmo tem quatro passos, repetidos:

Um: multiplicar o vetor pela matriz, y = A·x.

Dois: pegar a maior componente de y. Ela é a estimativa do autovalor.

Três: dividir o vetor por esse número. Assim a maior componente fica igual a 1.

Quatro: parar quando o autovalor e o vetor praticamente param de mudar.

O passo três, a normalização, é necessário porque, sem ele, os números crescem como λ₁ᵏ e estouram a capacidade do computador, ou vão para zero.

E o mais importante: cada repetição custa só uma multiplicação de matriz por vetor. Não precisamos inverter nem fatorar a matriz. Por isso o método funciona até com matrizes gigantes.

> **Para entender o critério de parada:** comparamos o λ de agora com o da repetição anterior. Se a diferença for menor que uma tolerância, como 10⁻¹², e o vetor também quase não mudou, paramos.

## Slide 6 — Exemplo 3×3: 38 iterações e 11 casas decimais corretas

*Másio César · cerca de 1 min 30 s*

Vamos ver a conta funcionando nesta matriz 3 por 3, começando com o vetor (1, 1, 1).

Primeira repetição: A vezes (1, 1, 1) é a soma de cada linha da matriz. 4 + 1 + 1 = 6, 1 + 3 + 2 = 6 e 1 + 2 + 5 = 8. Dá (6, 6, 8). A maior componente é 8, então a primeira estimativa é λ ≈ 8. Dividindo por 8, o vetor fica (0,75; 0,75; 1).

Repetindo, a estimativa cai para 7,25, depois 7,03, e vai se aproximando.

Com tolerância de 10⁻¹², o método para na repetição 38, com λ = 6,895106515929. A função pronta do numpy dá 6,895106515928. Só muda a última casa: são 11 casas decimais corretas.

E dá para prever esse número de repetições. Nesta matriz, a fração |λ₂/λ₁| é 0,49, então o erro cai mais ou menos pela metade a cada repetição. Para o erro ir de 1 até 10⁻¹², precisamos de umas 39 repetições. O método parou em 38. Ou seja, a fórmula do slide anterior funcionou na prática.

Agora o Antonio mostra o que acontece quando essa fração muda.

> **Se pedirem a segunda repetição:** A·(0,75; 0,75; 1) = (4·0,75 + 0,75 + 1; 0,75 + 3·0,75 + 2; 0,75 + 2·0,75 + 5) = (4,75; 5; 7,25). A maior é 7,25, então λ ≈ 7,25.
>
> **De onde vem o 39:** queremos 0,49ᵏ = 10⁻¹². Tirando o logaritmo dos dois lados: k = log(10⁻¹²) / log(0,49) ≈ 39.

## Slide 7 — A razão |λ₂/λ₁| decide quantas iterações são necessárias

*Antonio Rodrigo · cerca de 1 min*

Obrigado, Másio. Para ver o efeito dessa razão, montamos matrizes 5 por 5 com autovalores conhecidos: λ₁ sempre 10 e só λ₂ mudando. O gráfico mostra o erro em escala logarítmica.

Cada curva é praticamente uma reta, e a inclinação é o logaritmo da razão |λ₂/λ₁|. Com razão 0,2, convergimos em 22 iterações. Com 0,5, em 48. Com 0,8, em 141. Com 0,95, são 581 iterações.

A conclusão: o método é ótimo quando o autovalor dominante se destaca bem e fica lento quando o segundo autovalor está próximo dele.

## Slide 8 — Limites do método e como contorná-los

*Antonio Rodrigo · cerca de 1 min 15 s*

O método tem limites. Se houver dois autovalores com o mesmo módulo, como λ e −λ, a soma não converge. Se a razão estiver perto de 1, ele fica lento, como acabamos de ver. Em teoria, se o vetor inicial não tiver componente na direção de v₁, o método não o encontra, mas na prática o erro de arredondamento quase sempre introduz essa componente. Por fim, ele encontra só o dominante.

Para outros autovalores, existe a variação inversa: aplicar o mesmo método à inversa de A menos σI. Os autovalores dela são 1 sobre λᵢ menos σ, então o dominante corresponde ao λ mais próximo de σ. Na implementação, fatoramos LU uma vez e resolvemos um sistema por iteração. Na nossa matriz, com σ = 3, obtemos 3,397295. Com σ = 0, o menor autovalor, 1,707598.

E um aprendizado da implementação: a primeira versão parava só quando λ deixava de mudar. Com σ = 3, duas estimativas consecutivas coincidiram por acaso, e o método parou em 3,4, que está errado. Por isso o critério final exige que o vetor também estabilize.

## Slide 9 — PageRank: o navegador aleatório

*Antonio Rodrigo · cerca de 1 min 15 s*

Agora, o problema real. O PageRank modela um navegador aleatório. Ele está numa página e, com probabilidade α, normalmente 0,85, clica num dos links dela, escolhido ao acaso. Com probabilidade 0,15, ele se cansa e pula para uma página qualquer da web.

A importância de cada página é a fração do tempo que esse navegador passa nela depois de muito tempo navegando.

Para explicar, vamos usar esta mini-web de seis páginas. As setas são links. Há dois casos especiais. Contato, em laranja, não tem nenhum link de saída. Nesse caso, o navegador pula para qualquer página. E ninguém aponta para Arquivo: ela só recebe visitas pelo salto aleatório.

Esse passeio é uma cadeia de Markov, e a distribuição de longo prazo é justamente um autovetor.

## Slide 10 — O PageRank é o autovetor dominante da matriz de Google

*Antonio Rodrigo · cerca de 1 min 20 s*

Em forma de matriz: S é a matriz de links. A coluna j distribui a probabilidade igualmente entre as páginas para onde j aponta. Para uma página sem links, a coluna é toda 1/n. A matriz de Google é α vezes S mais (1 − α)/n vezes uma matriz só de uns, que representa o salto aleatório.

O vetor de PageRank π satisfaz G π = π. Ou seja, π é um autovetor de G com autovalor 1.

E três propriedades fazem do Método das Potências a escolha natural. Primeiro, cada coluna de G soma 1, então o autovalor dominante é exatamente 1. Segundo, todas as entradas são positivas, e pelo teorema de Perron–Frobenius esse autovetor é único e tem todas as componentes positivas: o ranking está bem definido. Terceiro, Haveliwala e Kamvar mostraram em 2003 que |λ₂| ≤ α. Lembrando que o erro cai como |λ₂/λ₁| elevado a k, com λ₁ = 1 isso garante convergência pelo menos como 0,85 elevado a k, independentemente do tamanho da web.

## Slide 11 — Mini-web: o método reproduz o resultado do eig

*Antonio Rodrigo · cerca de 1 min*

Aplicando o método à mini-web, o autovalor encontrado é 1, como a teoria prevê, e o vetor, normalizado para somar 1, dá o ranking.

Home fica em primeiro, com cerca de um terço da importância. Ela recebe links de Notícias, Esportes e Blog. Arquivo fica em último: ninguém aponta para ela, então ela só recebe visitas pelo salto aleatório.

Comparando com o numpy.linalg.eig, a diferença máxima entre os dois vetores é de 3,5 vezes 10⁻¹⁴, praticamente o limite da precisão de máquina.

Com seis páginas, qualquer método serve. A pergunta é o que acontece com uma web de verdade. Isso é a parte de implementação.

## Slide 12 — Na web real, G nunca é montada: só os links

*Wellington Cezario · cerca de 1 min 20 s*

Obrigado, Antonio. Agora, a implementação. Tudo está em Python, com NumPy e SciPy, no repositório do grupo.

O ponto principal: para a web real não montamos a matriz G, porque ela é densa. O salto aleatório põe um valor em todas as posições. Em vez disso, guardamos só a matriz de links H, que é esparsa, e escrevemos uma função que calcula G vezes x diretamente: α vezes H x, mais um termo constante que soma a contribuição das páginas sem links e do salto aleatório.

O LinearOperator do SciPy faz essa função se comportar como uma matriz. Assim, a mesma função metodo_potencias que usamos no exemplo 3 por 3 funciona aqui sem nenhuma mudança, porque ela só precisa do produto A vezes x.

O custo de cada iteração é proporcional ao número de links, e não ao quadrado do número de páginas.

(Código simplificado no slide; versão completa em pagerank.py.)

## Slide 13 — Por que não usar o numpy.linalg.eig?

*Wellington Cezario · cerca de 1 min*

Uma pergunta natural é: por que não usar a função pronta do numpy? Comparamos as duas em redes aleatórias de tamanhos crescentes.

O eig denso calcula todos os autovalores e trabalha com a matriz cheia: o custo cresce com n ao cubo. Dobrando de mil para dois mil páginas, o tempo passou de 0,9 para quase 5 segundos. O Método das Potências ficou na casa do milissegundo em todos os casos, e os dois vetores coincidem até 10⁻¹⁴.

Ressalva justa: o eig resolve um problema maior, porque entrega todos os autovalores. Mas, para o PageRank, só precisamos de um. E com n na casa dos milhões, o eig nem chega a rodar, como vamos ver agora.

## Slide 14 — A web real da Universidade de Stanford, em 2002

*Wellington Cezario · cerca de 1 min*

Para o problema real, usamos um conjunto de dados público do projeto SNAP, de Stanford: o grafo de links do domínio da Universidade de Stanford coletado em 2002. São 281.903 páginas e 2,3 milhões de links.

Se montássemos a matriz G cheia, em precisão dupla, seriam 636 gigabytes. A matriz de links esparsa ocupa 29 megabytes.

Com α = 0,85, o método convergiu em 125 iterações, em cerca de um segundo no nosso computador. Para conferir, calculamos o mesmo autovetor com o ARPACK, pela função eigs do SciPy, que usa outro algoritmo, o de Arnoldi. A diferença máxima entre os dois vetores foi de 5 vezes 10⁻¹³.

## Slide 15 — Na web real, o erro cai como αᵏ

*Wellington Cezario · cerca de 1 min*

Este gráfico conecta a teoria da primeira parte com o problema real. Variamos α e medimos o erro a cada iteração. As linhas tracejadas são α elevado a k.

As curvas medidas são paralelas às tracejadas, ou seja, a taxa de convergência é exatamente α. Isso indica que, nesse grafo, o segundo autovalor tem módulo igual a α, o pior caso permitido pelo resultado de Haveliwala e Kamvar.

Na prática, há um compromisso. Com α = 0,5, bastam 30 iterações, mas o navegador pula aleatoriamente metade do tempo e o ranking reflete pouco a estrutura de links. Com α = 0,99, o ranking segue quase só os links, mas são 2.039 iterações. O valor 0,85, proposto por Brin e Page, fica no meio: 125 iterações.

## Slide 16 — quem-aponta

*Wellington Cezario · cerca de 45 s*

Um resultado do ranking mostra por que o PageRank não é só contar links. A quarta página mais importante de Stanford, segundo o PageRank, é apenas a nonagésima sexta em número de links recebidos: tem 1.802. Várias páginas têm dez ou vinte mil links e ficam abaixo dela.

Isso acontece porque um link vale mais quando vem de uma página importante e com poucos links de saída. É a definição circular do começo, resolvida como um autovetor.

## Slide 17 — O que o Método das Potências entrega

*Másio César · cerca de 1 min*

Obrigado, Wellington. Para fechar, três ideias.

Primeira: o Método das Potências só precisa multiplicar matriz por vetor. Por isso ele funciona em matrizes enormes, onde os métodos tradicionais não cabem na memória.

Segunda: dá para prever a velocidade. O erro cai como |λ₂/λ₁| elevado a k. Vimos isso no exemplo 3×3, com 39 repetições previstas e 38 feitas, e no PageRank, onde o erro cai como 0,85 elevado a k.

Terceira: ele resolveu um problema real. O ranking de 281 mil páginas saiu em cerca de um segundo, e conferimos o resultado com outros dois métodos.

Os limites: ele encontra um autovalor por vez e fica lento quando λ₂ está perto de λ₁. Para esses casos existem outras versões, como a potência inversa, que o Antonio mostrou.

Obrigado.

## Slide 18 — Perguntas?

*Perguntas: responde quem apresentou a parte relacionada*

Perguntas que podem aparecer, com respostas curtas:

Por que α = 0,85? É o valor sugerido por Brin e Page. Equilibra a fidelidade aos links com a velocidade de convergência, que é αᵏ.

E se o grafo tiver páginas sem links? Elas viram colunas 1/n: o navegador pula para qualquer página. No nosso código, isso entra no termo constante do produto G·x.

Por que não o método QR? O QR calcula todos os autovalores e trabalha com a matriz densa, O(n³). Para o PageRank só precisamos de um autovetor.

O vetor inicial importa? Para o PageRank, não: o autovetor é único e positivo, e qualquer vetor positivo converge. Usamos o vetor de uns.
