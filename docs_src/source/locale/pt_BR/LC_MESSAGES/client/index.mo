��          �               ,  {   -     �     �     �     �     �  F   �  =   8     v  �   �     $     *     3  x   <     �  R   �  �    y   �          )     8     ?     H  @   f  E   �     �  �        �     �     �     �  
   D  m   O   API Client Factory is a python3 wrapper for REST APIs. That is, APIs that follow the pattern of using the methods as below: Client Methods Client Usage Create: Delete: Example to ``/user/users/`` For each endpoint the client Factory will create the follow structure: For more information on the available configurations, see at: Get/Retrieve/Detail: Import the api_client_factory module and create an instance using the name of the API you set in the ``DJANGO_API_CLIENT`` constant on settings.py file: List: Overview Settings To enable `django_api_client` in your project you need to add it to `INSTALLED_APPS` in your project `settings.py` file: Update: You need also to add your APIs settings using ``DJANGO_API_CLIENT`` constant. E.g: Project-Id-Version: Django API Client 0.3.0
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2020-07-27 19:26-0300
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: pt_BR
Language-Team: pt_BR <LL@li.org>
Plural-Forms: nplurals=2; plural=(n > 1)
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 O API Client Factory é um wrapper python3 para APIs REST. Ou seja, APIs que seguem o padrão de uso dos métodos abaixo: Métodos Cliente Uso do Cliente Criar: Deletar: Exemplo para ``/user/users/`` Para cada endpoint o API Client irá criar a seguinte estrutura: Para mais informações sobre as configurações diponiveis, veja em: Get/Recuperar/Detalhe: Importe o modulo api_client_factory e crie uma instância usando o nome da API que você definiu na constante ``DJANGO_API_CLIENT`` no arquivo settings.py Listar: Visão Geral Configurações Para habilitar o `django_api_client` você precisa adiciona-lo ao `INSTALLED_APPS` no seu arquivo `settings.py` do seu projeto: Atualizar: Você tambem precisa adicionar suas configurações das suas API usando a constante ``DJANGO_API_CLIENT``. Ex 