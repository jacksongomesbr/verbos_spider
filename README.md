# verbos_spider
Um crawler/spider para obtenção de dados do site https://www.conjugacao.com.br/

Este projeto utiliza o [scrapy](https://scrapy.org/) para fazer o crawler do site e gerar um conteúdo em JSON.

A página inicial é https://www.conjugacao.com.br/verbos-populares/. A partir dela são obtidos os links para as páginas 
dos verbos e para outras páginas (já que a lista é paginada; há até 100 verbos por página; há 50 páginas).

A saída é um `Array`  com a seguinte estrutura:

* `id`: o identificador do verbo (é o verbo no infinitivo, em letras minúsculas)
* `verbo`: o nome do verbo (é o verbo no infinitivo, com a inicial maiúscula)
* `intro`: a descrição verbo
* `gerundio`: o gerúndio do verbo
* `participio_passado`: o particípio passado do verbo
* `infinitivo`: o infinitivo do verbo
* `tipos`: um array de `String` representando os tipos do verbo
* `transitividade`: um array de `String` representando as indicações de transitividade do verbo
* `separacao`: a informação da separação silábica
* `conjugacoes`: um objeto cujos atributos indicam o modo da conjugação

Cada objeto em `conjugacoes` contém objetos cujos atributos indicam o tempo verbal da conjugação.
Esses objetos são `Array` de objetos com a estrutura:

* `preposicao`: a preposição da conjugação (opcional)
* `pessoa`: a pessoa da conjugação
* `flexao`: a flexão do verbo no tempo e modo de conjugação

## Exemplo

O trecho de código a seguir ilustra uma parte das informações para o verbo **caber**.

```json
{
   "id":"caber",
   "verbo":"Caber",
   "intro":"O verbo caber é um verbo irregular que apresenta alterações no seu radical.",
   "gerundio":"cabendo",
   "participio_passado":"cabido",
   "infinitivo":"caber",
   "tipos":[
      "irregular"
   ],
   "transitividade":[
      "transitivo indireto",
      "intransitivo"
   ],
   "separacao":"ca-ber",
   "conjugacoes":{
      "Indicativo":{
         "Presente":[
            {
               "pessoa":"eu",
               "flexao":"caibo"
            },
            {
               "pessoa":"tu",
               "flexao":"cabes"
            },
            {
               "pessoa":"ele",
               "flexao":"cabe"
            },
            {
               "pessoa":"nós",
               "flexao":"cabemos"
            },
            {
               "pessoa":"vós",
               "flexao":"cabeis"
            },
            {
               "pessoa":"eles",
               "flexao":"cabem"
            }
         ]
      }
   }
}
```

## Executando

Para executar o crawler, depois de configurar o ambiente Python, execute:

```
scrapy crawl verbos -o verbos.json
```

Na última vez que executei os resultados do scrapy foram:

```json
{
  "downloader/exception_count": 33,
  "downloader/exception_type_count/twisted.internet.error.TimeoutError": 33,
  "downloader/request_bytes": 1519239,
  "downloader/request_count": 5085,
  "downloader/request_method_count/GET": 5085,
  "downloader/response_bytes": 31962933,
  "downloader/response_count": 5052,
  "downloader/response_status_count/200": 5052,
  "dupefilter/filtered": 653,
  "finish_reason": "finished",
  "finish_time": datetime.datetime(2019,  11,  21,  6,  1,  7,  899672),
  "item_scraped_count": 4998,
  "log_count/DEBUG": 10084,
  "log_count/ERROR": 2,
  "log_count/INFO": 36,
  "request_depth_max": 11,
  "response_received_count": 5052,
  "retry/count": 33,
  "retry/reason_count/twisted.internet.error.TimeoutError": 33,
  "robotstxt/request_count": 1,
  "robotstxt/response_count": 1,
  "robotstxt/response_status_count/200": 1,
  "scheduler/dequeued": 5084,
  "scheduler/dequeued/memory": 5084,
  "scheduler/enqueued": 5084,
  "scheduler/enqueued/memory": 5084,
  "spider_exceptions/IndexError": 2,
  "start_time": datetime.datetime(2019,  11,  21,  5,  34,  28,  46339)
}
```

:v: :raised_hands:
