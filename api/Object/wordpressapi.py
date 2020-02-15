import os

class wordpress:
    def __init__(self, domain, name = None):
        self.domain = domain
        self.safedomain = self.domain.replace('.', '')
        self.name = name

    def save(self, name = None):
        name = name if name not None else self.name
        if name is None:
            return [False, "No name provided"]
        save = "/srv/src/" + name
        base = "/srv/www/"+ self.domain
        if os.path.isdir(save):
            return [False, "Save name already in use: '" + name + "'" , 400]
        if not os.path.isdir(base):
            return [False, "Domain does not exist: '" + name + "'" , 400]
        os.system("cp -r" + base + " " + save)
        return [True, {"name": name}, None]

    def deploy(self, login, email, name = None):
        name = name if name not None else self.name
        if name is None:
            return [False, "No name provided"]
        save = "/srv/src/" + name
        base = "/srv/www/"+ self.domain
        if not os.path.isdir(save):
            return [False, "Save name does not exist : '" + name + "'" , 400]
        if os.path.isdir(base):
            return [False, "Domain already in use : '" + name + "'" , 400]
        letters = string.ascii_lowercase
        password = ''.join(random.choice(letters) for i in range(10))
        os.system(` cp /srv/src/base_wp/ /wordpress/` + self.domain + ` -r ;\
                    cp /wordpress/` + self.domain + `/sample.env /wordpress/` + self.domain + `/.env;\
                    echo -e "VIRTUAL_HOST=` + self.domain + `\nDB_CONTAINER=db_` + self.safedomain + `\nWP_CONTAINER=wp_` + self.safedomain + `" >> /wordpress/` + self.domain + `/.env ;\
                    mkdir /srv/www/` + self.domain + ` ;\
                    cp -r /srv/src/` + name + `/* /srv/www/` + self.domain + `/ ;\
                    echo -e "define( 'DB_HOST', 'db_` + self.safedomain + `');" >> /srv/www/` + self.domain + `/html/wp-config.php ;\
                    cd /wordpress/` + self.domain + ` ;\
                    docker-compose up -d ;\
                    chown www-data /srv/www/` + self.domain + `/html -R ;\
                    sleep 10 ;\
                    docker exec wp_` + self.safedomain + ` curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar ;\
                    docker exec wp_` + self.safedomain + ` chmod +x wp-cli.phar ;\
                    docker exec wp_` + self.safedomain + ` mv wp-cli.phar /usr/local/bin/wp-cli ;\
                    docker exec wp_` + self.safedomain + ` wp-cli --allow-root user create ` + login +` `+ email +` --role=administrator --user_pass=` + password +`;\
                    docker exec wp_` + self.safedomain + ` wp-cli --allow-root option update home "http://` + self.domain + `";\
                    docker exec wp_` + self.safedomain + ` wp-cli --allow-root option update siteurl "http://` + self.domain + `";\
                    echo -e "php_value memory_limit 300M\nphp_value post_max_size 300M\nphp_value upload_max_filesize 300M" >> /srv/www/` + self.domain + `/html/.htaccess;\
                    cd -;`)
        return [True, {"url": "http://" + self.domain , "user": {"login": login, "password": password, "email": email}}, None]

    def new(self):
        base = "/srv/www/"+ self.domain
        if os.path.isdir(base):
            return [False, "Domain already in use : '" + name + "'" , 400]
        os.system(` cp /srv/src/base_wp/ /wordpress/` + self.domain + ` -r ;\
                    cp /wordpress/` + self.domain + `/sample.env /wordpress/` + self.domain + `/.env;\
                    echo -e "VIRTUAL_HOST=` + self.domain + `\nDB_CONTAINER=db_` + self.safedomain + `\nWP_CONTAINER=wp_` + self.safedomain + `" >> /wordpress/` + self.domain + `/.env ;\
                    cd /wordpress/` + self.domain + ` ;\
                    docker-compose up -d ;\
                    chown www-data /srv/www/` + self.domain + `/html -R ;\
                    docker exec wp_` + self.safedomain + ` curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar ;\
                    docker exec wp_` + self.safedomain + ` chmod +x wp-cli.phar ;\
                    docker exec wp` + self.safedomain + ` mv wp-cli.phar /usr/local/bin/wp-cli ;\
                    echo -e "php_value memory_limit 300M\nphp_value post_max_size 300M\nphp_value upload_max_filesize 300M" >> /srv/www/` + self.domain + `/html/.htaccess;\
                    cd -`)
        return [True, {"url": "http://" + self.domain}, None]


    def checkdomain(self):
        invalid = "-._~:/?#[]@!$&'()*+,;=\t\n\'\"\ "
        for i in invalid:
            if self.domain.find(i):
                return [False, "Your domain name is invalid: '" + i +"' char is forbidden", 400]
        return [True, {"domain": self.domain}]

    def checkname(self):
        if self.name not None:
            invalid = [',', '-', ';', '&', '#', '|', ' ']
            for i in invalid:
                if self.name.find(i):
                    return [False, "Your name is invalid: '" + i +"' char is forbidden", 400]
        return [True, {"name": self.name}]
