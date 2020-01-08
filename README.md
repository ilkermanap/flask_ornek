
# Flask Şablonu

If you are looking for the english version of this guide, please  check the excellent guide at https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world  address. This document and the application template prepared from Miguel Grinberg's work.  

İçinde temel öğelerin bulunduğu basit flask uygulamasını hazırlayacağız. Temel öğeler aşağıda sıralanmıştır:

   * Jinja2 ile şablon(template) kullanımı.
   * Parolalı kullanıcı giriş desteği
   * Parola sıfırlama (email ile sıfırlama linki) 
   * Veritabanı olarak postgresql kullandık. İleride mysql, sqlite  gibi başka veritabanlarının nasıl kullanılacağını da anlatacağız.
   * SqlAlchemy ile ORM (Object relational mapping) kullanımı
   * Bootstrap kullanımı
   * Çoklu dil desteği. flask-babel ile i18n kullanımı ve yeni dillerin nasıl ekleneceği gösterilecek.
   
Buradaki işlemler, https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world  adresindeki adımlar izlenerek yazılmıştır. Çoklu dil desteğinde hazır bulunan dillerin gösterimi için de stackoverflow'dan yardım alınmıştır.

İşletim sistemi olarak Debian 10 kullandık. Windows üzerinde test edip adımları bu belgeye eklemek isteyenler pull request gönderebilirler.

Sisteminizde python3 sürümünün  kurulu olduğunu varsayıyoruz.


## Virtualenv Kurulumu


    $ sudo pip3 install virtualenv

## Github'dan Dosyaları İndir


    $ git clone https://github.com/ilkermanap/flask_ornek

## Virtualenv Hazırla

    $ virtualenv venv
    $ source venv/bin/activate

Bu işlemden sonra komut satırının başında (venv) yazıyorsa, virtualenv kurulumunuz başarılı olmuştur. Bundan sonra python ile ilgili yapılacak bütün işlemlerde komut satırının başında (venv) yazan terminalde işlem yapmalısınız.  Yeni açacağınız bir terminal penceresi, oluşturduğunuz virtualenv ortamının içinde olmayacaktır.


## Paketleri Kur


Bu uygulamada kullanılan python paketleri requirements.txt dosyası içinde verilmiştir. Veritabanı için postgresql kullandığım için psycopg2-binary paketi de kurulmaktadır.  İşlem adımlarını belgelendirirken, ileride farklı veritabanları için de nasıl kurulum yapılacağını ekleyeceğiz. Şu aşamada sadece postgresql için adımlar anlatılacaktır.

   (venv)... $  pip install -r requirements.txt

Bu adım sonunda flask, flask-wtf, flask-sqlalchemy, psycopg2-binary, flask-migrate,flask-login, flask-mail, pyjwt, flask-bootstrap, flask-babel paketleri ve bu paketlerin bağımlılıkları virtualenv ortamı içine kurulmuş olacaktır.


## Uygulama Yapısı

   babel.cfg
   config.py
   template.py
   LICENSE
   README.md
   requirements.txt
   template.py
   app
   ├── email.py
   ├── errors.py
   ├── forms.py
   ├── __init__.py
   ├── models.py
   ├── routes.py
   ├── templates
   │   ├── 404.html
   │   ├── 500.html
   │   ├── base.html
   │   ├── edit_profile.html
   │   ├── email
   │   │   ├── reset_password.html
   │   │   └── reset_password.txt
   │   ├── index.html
   │   ├── login.html
   │   ├── register.html
   │   ├── reset_password.html
   │   ├── reset_password_request.html
   │   └── user.html
   └── translations
        └── tr
       	    └── LC_MESSAGES
             	└── messages.po

## Veritabanı Yapılandırma

### Postgresql

Debian 10 kullandığımızı yukarıda belirtmiştik. Önce yetkili kullanıcı oluruz:

   $ su -

Ardından postgresql-11 paketini kurarız:

   # apt install postgresql-11

postgres kullanıcısı olup, veritabanı ve kullanıcı oluşturma işlemlerini yaparız:

   # su - postgres
   postgres:~$ 
   







