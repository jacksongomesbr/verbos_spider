import scrapy


class VerbosSpider(scrapy.Spider):
    name = "verbos"
    base_url = 'https://www.conjugacao.com.br'
    start_urls = [
        'https://www.conjugacao.com.br/verbos-populares/',
    ]

    def parse(self, response):
        for a in response.css('.wrapper ul li a'):
            next_page = a.attrib['href']
            if next_page is not None:
                yield scrapy.Request(self.base_url + next_page, callback=self.parse_page)
        for a in response.css('.paginacao a'):
            next_page = a.attrib['href']
            if next_page is not None:
                yield scrapy.Request(self.base_url + next_page, callback=self.parse)


    def parse_page(self, response):
        verbo = response.css('.nmt::text').get().replace('Verbo ', '')
        id = verbo.lower()
        intro = response.css('.intro-v p::text').getall()
        intro = ' '.join(intro)
        info = response.css('.info-v')
        primary = info.css('p')[0]
        secondary = info.css('p')[1]
        gerundio = primary.css('.f::text')[0].get()
        participio_passado = primary.css('.f::text')[1].get()
        primary_text_nodes = primary.css('::text').getall()
        infinitivo = primary_text_nodes[len(primary_text_nodes)-1]
        infinitivo = infinitivo.replace(':','').strip()
        secondary_text_nodes = secondary.css('::text').getall()
        tipo = secondary_text_nodes[0].replace('Tipo de verbo: ', '')
        tipos = [t.strip() for t in tipo.split(';')]
        if len(secondary_text_nodes) > 1:
            transitividade = secondary_text_nodes[1].replace('Transitividade:', '').strip()
        transitividades = [t.strip().lower() for t in transitividade.split(',')]
        tdi = 'transitivo direto e indireto'
        if len(transitividades) == 1:
            if tdi in transitividades[0]:
                t = transitividades[0].replace(tdi, '')
                t = t.replace(' e ', '')
                transitividades[0] = t.strip()
                transitividades.append(tdi)
        if tdi in transitividades[len(transitividades) - 1]:
            t2 = transitividades[len(transitividades) - 1].replace(tdi, '')
            t2 = t2.replace(' e ', '')
            transitividades[len(transitividades) - 1] = t2
            transitividades.append(tdi)
        else:
            t2 = transitividades[len(transitividades)-1]
            del(transitividades[len(transitividades)-1])
            transitividades += [t.strip() for t in t2.split(' e ')]
        separacao = None
        if len(secondary_text_nodes) > 2:
            separacao = secondary_text_nodes[2].replace('Separação silábica: ', '').strip()
            separacao += secondary_text_nodes[3].strip()
        conjugacoes = {}
        for tempo in response.css('.tempos'):
            modo = tempo.css('h3::text').get().strip()
            conjugacoes[modo] = {}
            for tempo_conjugacao in tempo.css('.tempo-conjugacao'):
                tempo = tempo_conjugacao.css('h4::text').get().strip()
                conjugacoes[modo][tempo] = []
                for conjugacao in tempo_conjugacao.css('p>span>span'):
                    first = conjugacao.css('span>span:first-child::text').get()
                    last = conjugacao.css('span>span:last-child::text').get()
                    flexao = conjugacao.css('.f::text').get()
                    if not first:
                        continue
                    if first == flexao:
                        conjugacoes[modo][tempo].append({
                            'pessoa': last,
                            'flexao': flexao
                        })
                    elif last == flexao:
                        conjugacoes[modo][tempo].append({
                            'pessoa': first,
                            'flexao': flexao
                        })
                    elif first != last and first != flexao:
                        conjugacoes[modo][tempo].append({
                            'preposicao': first,
                            'pessoa': last,
                            'flexao': flexao
                        })
                    else:
                        pass
        yield {
            'id': id,
            "verbo": verbo,
            "intro": intro,
            "gerundio": gerundio,
            "participio_passado": participio_passado,
            'infinitivo': infinitivo,
            'tipos': tipos,
            'transitividade': transitividades,
            'separacao': separacao,
            'conjugacoes': conjugacoes
        }
