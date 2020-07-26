��          T               �   �   �   �   U  �   �  X   }  q   �  b   H  �  �  �   9  �     |   �  ^   )  h   �  T   �   Create a clients.py file in the core folder of your project, if you haven't, created it within your project folder to be simple to be imported from anywhere in the project with the following content: In our case, we have 2 options,"production" and "localhost", the factory generates a `api client` according to the name used and the parameters identified in it It is recommended that the name comes from a constant in the settings.py file, and if possible it can even be an environment variable. Let's imagine which client has a project folder (folder containing the settings.py file) The client will generate a user-friendly structure for each endpoint. Example with the endpoint */order/orders/*: The name of this variable will be the name of the customer that you will import into every project Project-Id-Version: Django API Client 0.3.0
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2020-07-26 14:16-0300
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: pt_BR
Language-Team: pt_BR <LL@li.org>
Plural-Forms: nplurals=2; plural=(n > 1)
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 Crie um arquivo clients.py em alguma pasta nucleo do seu projeto, caso não tenha, crie dentro da sua pasta do projeto para ficar mais simples de ser importado de qualquer lugar do projeto com o seguinte conteúdo: No nosso caso, temos 2 opções, "produção" e "localhost", a fábrica gera um `api client` de acordo com o nome usado e os parâmetros identificados nele É recomendável que o nome venha de uma constante no arquivo settings.py, e se possível ser até uma variável de ambiente Vamos imaginar qual cliente tem uma pasta de projeto (pasta que contém o arquivo settings.py) O cliente irá gerar uma estrutura amigavel para cada endpoing. Exemplo com o endpoint */order/orders/*: O nome dessa variável será o nome do cliente que será importado para cada projeto 