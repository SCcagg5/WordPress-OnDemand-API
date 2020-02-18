import os

class wordpress:
    def __init__(self, domain, name = None):
        self.domain = domain
        self.safedomain = self.domain.replace('.', '')
        self.name = name

    def save(self, name = None):
        name = name if name is not None else self.name
        if name is None:
            return [False, "No name provided"]
        save = "/srv/src/" + name
        base = "/wordpress/"+ self.domain
        if os.path.isdir(save):
            return [False, "Save name already in use: '" + name + "'" , 400]
        if not os.path.isdir(base):
            return [False, "Domain does not exist: '" + name + "'" , 400]
        os.system("cp -r" + base + " " + save)
        return [True, {"name": name}, None]

    def deploy(self, login, email, name = None):
        name = name if name is not None else self.name
        if name is None:
            return [False, "No name provided"]
        save = "/srv/src/" + name
        base = "/wordpress/"+ self.domain
        if not os.path.isdir(save):
            return [False, "Save name does not exist : '" + name + "'" , 400]
        if os.path.isdir(base):
            return [False, "Domain already in use : '" + name + "'" , 400]
        letters = string.ascii_lowercase
        password = ''.join(random.choice(letters) for i in range(10))
        os.system(' mkdir /wordpress/' + self.domain + ' ;\
                    cp -r '+ save +'/* /wordpress/' + self.domain + ';\
                    cp /wordpress/' + self.domain + '/sample.env /wordpress/' + self.domain + '/.env;\
                    echo "V_VIRTUAL_HOST=' + self.domain + '\nV_DB_CONTAINER=db_' + self.safedomain + '\nV_WP_CONTAINER=wp_' + self.safedomain + '" >> /wordpress/' + self.domain + '/.env ;\
                    echo -e "define( \'DB_HOST\', \'db_' + self.safedomain + '\');" >> /wordpress/' + self.domain + '/html/wp-config.php ;\
                    cd /wordpress/' + self.domain + ' && docker-compose up -d;\
		            chown www-data /wordpress/' + self.domain + '/html -R ;\
                    docker exec wp_' + self.safedomain + ' curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar ;\
                    docker exec wp_' + self.safedomain + ' chmod +x wp-cli.phar ;\
                    docker exec wp_' + self.safedomain + ' mv wp-cli.phar /usr/local/bin/wp-cli ;\
                    docker exec wp_' + self.safedomain + ' wp-cli --allow-root user create ' + login + ' '+ email +' --role=administrator --user_pass=' + password + ' ;\
                    docker exec wp_' + self.safedomain + ' wp-cli --allow-root option update home "http://' + self.domain + '" ;\
                    docker exec wp_' + self.safedomain + ' wp-cli --allow-root option update siteurl "http://' + self.domain + '" ;\
                    echo -e "php_value memory_limit 300M\nphp_value post_max_size 300M\nphp_value upload_max_filesize 300M" >> /wordpress/' + self.domain + '/html/.htaccess;')
        return [True, {"url": "http://" + self.domain , "user": {"login": login, "password": password, "email": email}}, None]

    def new(self):
        base = "/wordpress/" + self.domain
        if os.path.isdir(base):
            return [False, "Domain already in use : '" + name + "'" , 400]
        os.system(' cp /srv/src/base_wp/ /wordpress/' + self.domain + ' -r ;\
                    cp /wordpress/' + self.domain + '/sample.env /wordpress/' + self.domain + '/.env;\
                    echo "V_VIRTUAL_HOST=' + self.domain + '\nV_DB_CONTAINER=db_' + self.safedomain + '\nV_WP_CONTAINER=wp_' + self.safedomain + '" >> /wordpress/' + self.domain + '/.env ;\
                    cd /wordpress/' + self.domain + ' && docker-compose up -d;\
		            chown www-data /wordpress/' + self.domain + '/html -R ;\
                    echo -e "php_value memory_limit 300M\nphp_value post_max_size 300M\nphp_value upload_max_filesize 300M" >> /wordpress/' + self.domain + '/html/.htaccess;')
        return [True, {"url": "http://" + self.domain}, None]


    def checkdomain(self):
        invalid = "-_~:/?#[]@!$&'()*+,;=\t\n\'\"\ "
        for i in invalid:
            if self.domain.find(i) > 0:
                return [False, "Your domain name is invalid: '" + i +"' char is forbidden", 400]
        return [True, {"domain": self.domain}]

    def checkname(self):
        if self.name is not None:
            invalid = [',', '-', ';', '&', '#', '|', ' ']
            for i in invalid:
                if self.name.find(i) > 0:
                    return [False, "Your name is invalid: '" + i +"' char is forbidden", 400]
        return [True, {"name": self.name}]
