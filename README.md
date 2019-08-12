# ![Universidade Digital](http://ntiufalara.github.io/universidade-digital/assets/img/logo.png)

Instalação e configuração do ambiente de desenvolvimento baseado no Odoo 12:

Usaremos como base o sistema Linux Ubuntu (Isso não impede a configuração em outros sistemas, porém não será explicado aqui).
Também estão disponíveis instruções para o **docker com docker-compose** 

Caso encontre problemas durante a configuração, busque mais informações no tutorial
de instalação oficial do Odoo <a href="https://www.odoo.com/documentation/master/setup/install.html">Setup instructions</a>

Para informações sobre o desenvolvimento dos módulos, consulte <a href="https://www.odoo.com/documentation/master/tutorials.html">os tutoriais para desenvolvedores do Odoo</a>

### Instalação a partir do código

Para realizar a instalação a partir do código, primeiro, instale as dependências do sistema operacional:

```shell script
sudo apt update && sudo apt install -y python3-pip python3-dev libxml2-dev libxslt1-dev libevent1-dev libsasl2-dev libldap2-dev wkhtmltopdf
```

Instale o servidor de banco de dados PostgreSQL (compatível com versão 10.x em diante):

```shell script
sudo apt install postgresql-10
```

Acesse o usuário de manutenção de bancos de sados:

```shell script
 sudo su postgres
```

Configure o usuário que executará o servidor Web para obter controle total no servidor: **(Por questões de segurança, você deve usar um superusuário apenas para desenvolvimento, em produção, configure um usuário com permissões de criar e alterar bancos de dados)**

```shell script
 createuser nomedousuario -P   # Subistitua "nomedousuario" pelo seu nome de usuário
```

Execute o script para levantar o servidor de desenvolvimento na porta 8069:

```shell script
# use -h para saber mais sobre esse script
./odoo-bin
```



