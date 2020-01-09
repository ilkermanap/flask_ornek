
# Flask Şablonu

If you are looking for the english version of this guide, 
please  check the excellent guide at  
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world  address. 
This document and the application template prepared from 
Miguel Grinberg's work.  

İçinde temel öğelerin bulunduğu basit 
flask uygulamasını hazırlayacağız. Temel öğeler aşağıda sıralanmıştır:

   * Jinja2 ile şablon(template) kullanımı.
   * Parolalı kullanıcı giriş desteği
   * Parola sıfırlama (email ile sıfırlama linki) 
   * Veritabanı olarak postgresql kullandık. İleride mysql, sqlite gibi 
   başka veritabanlarının nasıl kullanılacağını da anlatacağız.
   * SqlAlchemy ile ORM (Object relational mapping) kullanımı
   * Bootstrap kullanımı
   * Çoklu dil desteği. flask-babel ile i18n kullanımı ve yeni dillerin 
     nasıl ekleneceği gösterilecek.
   
Buradaki işlemler, https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world  
adresindeki adımlar izlenerek yazılmıştır. Çoklu dil desteğinde hazır 
bulunan dillerin gösterimi için de stackoverflow'dan yardım alınmıştır.

İşletim sistemi olarak Debian 10 kullandık. Windows üzerinde test edip 
adımları bu belgeye eklemek isteyenler pull request gönderebilirler.

Sisteminizde python3 sürümünün  kurulu olduğunu varsayıyoruz.


## Virtualenv Kurulumu


    $ sudo pip3 install virtualenv

## Github'dan Dosyaları İndir


    $ git clone https://github.com/ilkermanap/flask_ornek

## Virtualenv Hazırla

    $ virtualenv venv
    $ source venv/bin/activate

Bu işlemden sonra komut satırının başında (venv) yazıyorsa, virtualenv 
kurulumunuz başarılı olmuştur. Bundan sonra python ile ilgili yapılacak 
bütün işlemlerde komut satırının başında (venv) yazan terminalde işlem 
yapmalısınız.  Yeni açacağınız bir terminal penceresi, oluşturduğunuz 
virtualenv ortamının içinde olmayacaktır.


## Paketleri Kur


Bu uygulamada kullanılan python paketleri requirements.txt dosyası 
içinde verilmiştir. Veritabanı için postgresql kullandığım için 
psycopg2-binary paketi de kurulmaktadır.  İşlem adımlarını 
belgelendirirken, ileride farklı veritabanları için de nasıl kurulum 
yapılacağını ekleyeceğiz. Şu aşamada sadece postgresql için adımlar 
anlatılacaktır.

    (venv)... $  pip install -r requirements.txt

Bu adım sonunda flask, flask-wtf, flask-sqlalchemy, psycopg2-binary, 
flask-migrate, flask-login, flask-mail, pyjwt, flask-bootstrap, 
flask-babel paketleri ve bu paketlerin bağımlılıkları virtualenv 
ortamı içine kurulmuş olacaktır.


## Uygulama Yapısı

```
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
```


## Veritabanı Yapılandırma

Geliştirme aşamasında sqlite kullanılabilir. Gerçek çalışma ortamı için 
tercihim postgresql olur. Aşağıda farklı veritabanları için yapılması 
gereken ayarlar anlatılmıştır. Ayarlar, kullandığınız işletim sistemi ve 
sürümüne göre farklı olabilir. Flask ve SQLAlchemy açısından gerekli olan, 
SQLALCHEMY_DATABASE_URI satırında verilen bağlantı ile veritabanına bağlantı 
yapılabilmesidir.

### SQLite
Sqlite kullanmak için config.py dosyasında sqlite bağlantısı için verilmiş
olan SQLALCHEMY_DATABASE_URI satırı önündeki \# işaretini kaldırıp,
postgresql bağlantı satırının önüne koyun:
```
   SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
   #SQLALCHEMY_DATABASE_URI = 'postgresql://username:passwd@localhost:5432/dbname'
```

### Postgresql

Debian 10 kullandığımızı yukarıda belirtmiştik. Önce yetkili kullanıcı 
oluruz:

   $ su -

Ardından postgresql-11 paketini kurarız:
```
   # apt install postgresql-11
```
postgres kullanıcısı olup, veritabanı ve kullanıcı oluşturma işlemlerini 
yaparız. Önce veritabanı:
```
   # su - postgres
   postgres:~$ createdb flask_ornek    
   local	flask_ornek	flask_ornek_kullanici			md5
   
```

Ardından kullanıcı oluşturma ve flask_ornek veritabanı için yetki verme:
```
   postgres:~$ psql
   psql (11.5 (Debian 11.5-1+deb10u1))
   Type "help" for help.
   postgres=# create user flask_ornek_kullanici with encrypted password '32319ae795b57d2e61b105dfd6f7b99061c04d93';
   CREATE ROLE
   postgres=# grant  all privileges on  database flask_ornek to flask_ornek_kullanici;
   GRANT
   postgres=#
```
Veritabanı bağlantı ayarlarının config.py içinde güncellenmesi gerekir. 
Githubda bulunan config.py dosyasında aşağıdaki satırı güncelleyeceğiz:
```
SQLALCHEMY_DATABASE_URI = 'postgresql://username:passwd@localhost:5432/dbname'
```

Yukarıda veritabanı ve kullanıcı oluşturma işlemlerinde kullandığımız 
isim ve parola ile satırı aşağıdaki gibi güncelleriz:
```
SQLALCHEMY_DATABASE_URI = 'postgresql://flask_ornek_kullanici:32319ae795b57d2e61b105dfd6f7b99061c04d93@localhost:5432/flask_ornek'
```

## Veritabanı Tablolarının Oluşturulması

Uygulamada kullanılacak olan tablolar, app/models.py dosyasının içinde sınıf şeklinde 
tanımlanmıştır. Örnek uygulamamızda sadece kullanıcı tablosu bulunmaktadır:  
```
   class User(UserMixin, db.Model):
       __tablename__ = "users" 
```
Yukarıdaki satırlar sınıfın tamamını göstermemektedir. Sadece sınıf adı ve o 
sınıfın karşılık geleceği veritabanı tablosu adını belirtmek için eklenmiştir.

Tabloları oluşturabilmek için tekrar (venv) yazan virtualenv'in aktif durumda 
olduğu terminale dönelim:

```
(venv) $ flask db init
 * Tip: There are .env or .flaskenv files present. Do "pip install python-dotenv" to use them.
  Creating directory /home/ilker/src/flask_ornek/migrations ...  done
  Creating directory /home/ilker/src/flask_ornek/migrations/versions ...  done
  Generating /home/ilker/src/flask_ornek/migrations/alembic.ini ...  done
  Generating /home/ilker/src/flask_ornek/migrations/script.py.mako ...  done
  Generating /home/ilker/src/flask_ornek/migrations/env.py ...  done
  Generating /home/ilker/src/flask_ornek/migrations/README ...  done
  Please edit configuration/connection/logging settings in '/home/ilker/src/flask_ornek/migrations/alembic.ini' before
  proceeding.
```

Yukarıdaki komut ile ilk veritabanı göç/migration işlemi için gerekli dizinleri 
ve ayar dosyalarını hazırlamış oluruz. Kullandığımız flask-migrate paketi sayesinde 
veritabanı tabloları güncelleme ya da değişiklikleri geri alma işlemleri kontrollü 
şekilde yapılabilecektir.  

İlk güncelleme işlemi için 
```
(venv) $ flask db migrate -m "users tablosu"
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'users'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_users_email' on '['email']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_users_username' on '['username']'
  Generating /home/ilker/src/flask_ornek/migrations/versions/c80d3ef420e1_users_tablosu.py ...  done
```

Komut çıktısındaki 'Detected added' içeren satırlara dikkat ederseniz, içi 
boş olan veritabanımıza uygulama içindeki app/models.py dosyasında 
tanımlanmış User sınıfı/users tablosunun ve ilgili indekslerin göç için 
eklendiğini görürüz.

Bu güncellemelerin veritabanına yansıtılması için:
```
(venv) $ flask db upgrade 
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> c80d3ef420e1, users tablosu
```

Böylece veritabanında kullanıcı bilgilerinin saklanacağı users tablosu 
yaratılmış olacaktır. Uygulamanın çalışması için gerekenlerin  bir kısmı 
(email ile parola sıfırlama, çoklu dil desteği gibi kısımlar hariç) 
tamamlanmıştır. Test edebilmek için 
```
(venv) $ flask run
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

komutunu çalıştırıp, web tarayıcınızda http://127.0.0.1:5000  adresine 
giderek uygulamayı kullanabilirsiniz. Bu aşamada kullanıcı oluşturma,  
oluşturulan kullanıcı adı ve parolası ile giriş yapma işlemleri çalışacaktır.

## Elektronik Posta Desteği
Uygulamamızın eposta ile parola sıfırlama isteği gönderebilme yeteneği vardır. 
Bu yeteneğin kullanılabilmesi için, config.py içindeki eposta servisi ayarlarının 
yapılması gerekmektedir.

```
ADMINS=["ilkermanap@gmail.com"]
MAIL_SERVER="smtp.gmail.com"
MAIL_PASSWORD='xxxxxxxxx'
MAIL_PORT=465
MAIL_USE_SSL=True
MAIL_USE_TLS=False
MAIL_USERNAME="ilkermanap@gmail.com"
```

ADMINS, MAIL_USERNAME ve MAIL_PASSWORD alanlarını güncelleyip uygulamayı
yeniden başlatırsanız, eposta ile parola sıfırlama isteği yapabileceksiniz.

 ## Çoklu Dil Desteği
 Çoklu dil desteği, flask-babel modülü ile gelmektedir.  Uygulama içinde farklı dillere 
 çevirilmesi gereken metinlerin işaretlenmesi gerekmektedir.  
 
Uygulama içinde:
```
class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))
```

Ya da jinja template dosyalarında: 
```
{% extends "base.html" %}
{% import "bootstrap/wtf.html"  as wtf %}

{% block app_content %}
    <h1>{{ _('Sign In') }}</h1>
    <div class="row">
      <div class="col-md-4">
	{{ wtf.quick_form(form) }}
      </div>
    </div>    

    <div class="row"> {{ _('New User?') }} <a href="{{ url_for('register') }}"> {{ _('Click to Register!') }}</a> </div> 
    <div class="row"> {{ _('Forgot Your Password?') }}
        <a href="{{ url_for('reset_password_request') }}">{{ _('Click to Reset It') }}</a>
    </div>
{% endblock %}
```
Farklı dillere çevirilmesi gereken metinleri uygulama ya da template dosyaları içinde
_() ya da _l() veririz. 

flask-babel ile kurulan yardımcı uygulamalar ile, tercüme edilmesi gereken metin 
kataloğu oluşturulur:

```
(venv) $ pybabel extract -F babel.cfg -k _l -o messages.pot .
extracting messages from app/__init__.py
extracting messages from app/email.py
extracting messages from app/errors.py
extracting messages from app/forms.py
extracting messages from app/models.py
extracting messages from app/routes.py
extracting messages from app/templates/404.html (extensions="jinja2.ext.autoescape, jinja2.ext.with_")
extracting messages from app/templates/500.html (extensions="jinja2.ext.autoescape, jinja2.ext.with_")
extracting messages from app/templates/base.html (extensions="jinja2.ext.autoescape, jinja2.ext.with_")
extracting messages from app/templates/edit_profile.html (extensions="jinja2.ext.autoescape, jinja2.ext.with_")
extracting messages from app/templates/index.html (extensions="jinja2.ext.autoescape, jinja2.ext.with_")
extracting messages from app/templates/login.html (extensions="jinja2.ext.autoescape, jinja2.ext.with_")
extracting messages from app/templates/register.html (extensions="jinja2.ext.autoescape, jinja2.ext.with_")
extracting messages from app/templates/reset_password.html (extensions="jinja2.ext.autoescape, jinja2.ext.with_")
extracting messages from app/templates/reset_password_request.html (extensions="jinja2.ext.autoescape, jinja2.ext.with_")
extracting messages from app/templates/user.html (extensions="jinja2.ext.autoescape, jinja2.ext.with_")
extracting messages from app/templates/email/reset_password.html (extensions="jinja2.ext.autoescape, jinja2.ext.with_")
writing PO template file to messages.pot
```

Şimdi türkçe tercümeler için gerekli dosyaları oluşturalım:  
```
(venv) $ pybabel init -i messages.pot -d app/translations -l tr
creating catalog app/translations/tr/LC_MESSAGES/messages.po based on messages.pot
``` 

Yukarıdaki komutla oluşturulan türkçe çeviri dosyasından birkaç satır aşağıdadır:
``` 
.
.
#: app/email.py:22
msgid "[Flask Template] Reset Your Password"
msgstr ""

#: app/forms.py:8 app/forms.py:15 app/forms.py:34
msgid "Username"
msgstr ""

#: app/forms.py:9 app/forms.py:17 app/forms.py:54
msgid "Password"
msgstr ""
.
.
``` 

Yukarıdaki birkaç satırı aşağıdaki şekilde güncelleyip kaydedelim:
``` 
.
.
#: app/email.py:22
msgid "[Flask Template] Reset Your Password"
msgstr "[Flask Örnek] Parolanızı Sıfırlayın"

#: app/forms.py:8 app/forms.py:15 app/forms.py:34
msgid "Username"
msgstr "Kullanıcı Adı"

#: app/forms.py:9 app/forms.py:17 app/forms.py:54
msgid "Password"
msgstr "Parola"
.
.
``` 

Şimdi de yapılan tercümeleri derleyelim:
``` 
(venv) $ pybabel compile -d app/translations
compiling catalog app/translations/tr/LC_MESSAGES/messages.po to app/translations/tr/LC_MESSAGES/messages.mo
``` 

Uygulamayı çalıştırıp tarayıcıda sağ üstte gelen dil linklerine tıkladığınızda, 
yaptığımız tercümelere göre ekrandaki mesajların değiştiğini göreceksiniz. 

Uygulama ile sadece ingilizce ve türkçe linkleri gelmektedir. Şimdi de ispanyolca 
ekleyelim. Bunun için ilk değişiklik config.py dosyasında yapılacaktır. Aşağıdaki 
satırı:
``` 
LANGUAGES = {"en": "English", "tr":"Turkish"}
``` 
şu şekilde değiştirelim:
``` 
LANGUAGES = {"en": "English", "tr":"Turkish", "es":"Spanish"}
``` 

Uygulamayı çalıştırdığımızda, sağ üstte görüntülenen diller arasına ispanyolcanın 
da geldiğini göreceğiz. Henüz tercümesi yapılmadığından, ispanyolca seçilirse mesajlar 
yine ingilizce görünecektir. Yukarıda türkçe için yaptığımız işlemleri ispanyolca 
için de yapalım:
```
(venv) $ pybabel init -i messages.pot -d app/translations -l es
creating catalog app/translations/tr/LC_MESSAGES/messages.po based on messages.pot
``` 

Tercümeleri yapalım, ispanyolcaları google translate ile buldum, 
doğruluğundan emin değilim: 
``` 
.
.
#: app/email.py:22
msgid "[Flask Template] Reset Your Password"
msgstr "[Flask Modelo] Restablecer su contraseña"

#: app/forms.py:8 app/forms.py:15 app/forms.py:34
msgid "Username"
msgstr "Nombre de usuario"

#: app/forms.py:9 app/forms.py:17 app/forms.py:54
msgid "Password"
msgstr "Contraseña"
.
.
``` 
Derleyelim:
``` 
(venv) $ pybabel compile -d app/translations
compiling catalog app/translations/tr/LC_MESSAGES/messages.po to app/translations/tr/LC_MESSAGES/messages.mo
compiling catalog app/translations/es/LC_MESSAGES/messages.po to app/translations/es/LC_MESSAGES/messages.mo
``` 

Uygulamayı çalıştırdığımızda, ispanyolca çevirisini yaptığımız kısımların 
ispanyolca seçildiği zaman görüntülendiğini görürüz.
 



