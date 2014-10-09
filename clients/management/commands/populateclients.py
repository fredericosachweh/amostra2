# -*- encoding: utf-8 -*-
import optparse
import os

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from splinter.browser import Browser
from splinter.exceptions import ElementDoesNotExist
from clients import models


class Command(BaseCommand):
    help = 'Webcrawler to populate base of clients.'

    option_list = BaseCommand.option_list + (
        optparse.make_option(
            '--driver', action='store', type='string',
            dest='driver', default='phantomjs'
        ),
        optparse.make_option(
            '--row', action='store', type='int', dest='row', default=0
        ),
        optparse.make_option(
            '--page', action='store', type='int', dest='page', default=1
        )
    )

    def data_from_ids(self, root, ids):
        data = {}
        for key, id in ids.items():
            try:
                elem = root.find_by_xpath("//span[@id='{0}']".format(id))
                data[key] = elem.first.text
            except ElementDoesNotExist:
                data[key] = ''
        return data

    def handle(self, driver, row, page, *args, **kwargs):
        browser = Browser(driver)
        browser.visit('http://www.dataescolabrasil.inep.gov.br/dataEscolaBrasil/')
        with browser.get_iframe(0) as iframe:
            iframe.check('situacaoEmAtividade')
            iframe.select('estadoDecorate:estadoSelect', '41')
            assert iframe.is_text_present('Abatia', wait_time=5)  # wait a known city
            iframe.find_by_id('pesquisar').first.click()
            assert iframe.is_text_present('Foram encontradas', wait_time=5)

            if page > 1:
                next_page = 1
                def click_pager():
                    scroller = iframe.find_by_id('resultadoDataScroller').first
                    pager = scroller.find_by_xpath('//td[text()="{0}"]'.format(next_page))
                    pager.first.click()
                while 1:
                    try:
                        click_pager()
                    except ElementDoesNotExist:
                        try:
                            print 'retry', next_page
                            os.system('sleep 1s')
                            click_pager()
                        except ElementDoesNotExist:
                            print 're-retry', next_page
                            os.system('sleep 2s')
                            click_pager()
                    os.system('sleep 2s')
                    if next_page == page:
                        break
                    next_page += 1

            while 1:
                # Reload the trs to avoid outdated references
                trs = iframe.find_by_css('#resultado tbody tr')

                # Go to the next page when done
                if (row + 1) > len(trs):
                    page += 1
                    row = 0
                    scroller = iframe.find_by_id('resultadoDataScroller').first
                    pager = scroller.find_by_xpath('//td[text()="{0}"]'.format(page))
                    pager.first.click()
                    continue

                # Click first td anchor and assert it is the detail tab
                tr = trs[row]
                tds = tr.find_by_css('td')
                tds[0].find_by_css('a').click()
                if not iframe.is_text_present('Dados gerais'):
                    browser.back()
                    row += 1
                    iframe.find_by_xpath('//td[text()="Resultado de busca"]').first.click()
                    continue

                # Get tab content
                content = iframe.find_by_css('.rich-tabpanel-content')
                data = self.data_from_ids(content, {
                    'external_code': 'dad_codEntidadeDecorate:dad_codEntidade',
                    'name': 'dad_noEntidadeDecorate:dad_noEntidade',
                    'city': 'dad_noMunicipioDecorate:dad_noMunicipio',
                    'address': 'dad_enderecoDecorate:dad_endereco',
                    'number': 'dad_numeroDecorate:dad_numero',
                    'complement': 'dad_complementoDecorate:dad_complemento',
                    'quarter': 'dad_bairroDecorate:dad_bairro',
                    'postal_code': 'dad_cepDecorate:dad_cep',
                    'phones': 'dad_numTelefoneDecorate:dad_numTelefone',
                    'email': 'dad_emailDecorate:dad_email',
                    'cnpj': 'cnpjEpDecorate:cnpjEp',
                    'adm_structure': 'dad_dependenciaAdmDecorate:dad_dependenciaAdm',
                    'private_school_category': 'descCategoriaEscPrivadaDecorate:descCategoriaEscPrivada',
                })
                try:
                    self.save_data(data, row=row, page=page)
                except IntegrityError:
                    pass  # could not save because cnpj already exists

                # Go back and move to next row
                iframe.find_by_xpath('//td[text()="Resultado de busca"]').first.click()
                row += 1

    def save_data(self, data, row, page):
        external_source = 'dataescolabrasil.inep.gov.br'
        try:
            client = models.Client.objects.get(
                external_source=external_source,
                external_code=data['external_code']
            )
            print '{0}.{1})'.format(page, row), client, 'already exist'
        except models.Client.DoesNotExist:
            data['external_source'] = external_source
            data['state'] = 'PR'
            data['city'] = data['city'].lower().title()
            if data['email']:
                data['email'] = data['email'].lower()
            if not data['cnpj']:
                data['cnpj'] = None  # force null to avoid unique constrain error
            client = models.Client.objects.create(**data)
            print '{0}.{1})'.format(page, row), client, 'just imported'
